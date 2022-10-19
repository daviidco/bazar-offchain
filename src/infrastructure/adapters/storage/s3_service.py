import boto3
import inject
from botocore.exceptions import ClientError
from flask_restx import abort

from src.domain.ports.object_file_interface import IStorage
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error
from src.infrastructure.config.default_infra import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME


class S3Repository(IStorage):

    @inject.autoparams()
    def __init__(self, bucket_name=None, s3_client=None, session=None):
        self.bucket_name = bucket_name if bucket_name is not None else AWS_BUCKET_NAME
        self.s3_client = s3_client
        self.session = session

        if s3_client is None:
            self.s3_client = boto3.client("s3",
                                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        if session is None:
            self.session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        self.s3_resource = self.session.resource('s3')
        self.s3_bucket = self.s3_resource.Bucket(self.bucket_name)

    def copy_object(self, origin_key: str, destination_key: str, origin_bucket: str, destination_bucket: str):
        error = False
        try:
            origin_bucket = self.bucket_name if origin_bucket is None else origin_bucket
            destination_bucket = self.bucket_name if destination_bucket is None else destination_bucket
            self.s3_client.copy(CopySource={"Bucket": origin_bucket,
                                            "Key": origin_key},
                                Bucket=destination_bucket,
                                Key=destination_key)

        except ClientError as e:
            self.logger.info("Error copying object -> %s", str(e))
            error = e.response['Error']['Code']
        return error

    def get_object(self, key: str):
        error = False
        try:
            self.s3_client.get_object(Bucket=self.bucket_source, Key=key)
            # return response["Body"].read()
        except ClientError as e:
            self.logger.info("Error uploading object -> %s", str(e))
            error = e.response['Error']['Code']
        return error

    def key_existing_size__list(self, key):
        """return the key's size if it exists, else None"""
        error = False
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_source,
                Prefix=key,
            )
            for obj in response.get('Contents', []):
                if obj['Key'] == key:
                    return obj['Size']
        except ClientError as e:
            self.logger.info("Error uploading object -> %s", str(e))
            error = True
        return error

    def upload_file(self, filename: str, key: str):
        error = False
        try:
            self.s3_client.upload_file(filename, self.bucket_source, key)
        except ClientError as e:
            self.logger.info("Error uploading object -> %s", str(e))
            error = True
        return error

    def put_object(self, body: any, key: str, content_type: str, bucket: str = None):
        res = False
        try:
            self.s3_client.put_object(Body=body, Bucket=self.bucket_name, Key=key, ContentType=content_type)
            res = True
        except ClientError as e:
            msj = e.args[0]
            e = api_error('S3Error')
            e.error['description'] = msj
            abort(code=e.status_code, message=e.message, error=e.error)
        return res

    def file_exists(self, file_key: str):
        validation = False
        try:
            self.s3_resource.Object(self.bucket_source, file_key).load()
            validation = True
        except ClientError as e:
            self.logger.error(
                "Object '{}' doesn't exists in bucket '{}'. Error {}".format(
                    file_key, self.bucket_source, e.response["Error"]["Code"]
                )
            )
        return validation

    def update_file(self, actual_file_key: str, new_file_key: str):
        validation = False
        copy_source = f"{self.bucket_source}/{actual_file_key}"
        try:
            self.s3_resource.Object(self.bucket_source, new_file_key).copy_from(
                CopySource=copy_source
            )
            self.s3_resource.Object(self.bucket_source, actual_file_key).delete()
            validation = True

            self.logger.info(
                "Object '{}' updated in S3 correctly by '{}'.".format(
                    actual_file_key, new_file_key
                )
            )
        except ClientError as e:
            self.logger.error(
                "Could not update object '{}' by '{}'. {}".format(
                    actual_file_key, new_file_key, e.response
                )
            )
        return validation

    def delete_file(self, file_key: str):
        validation = False
        try:
            self.s3_resource.Object(self.bucket_source, file_key).delete()
            validation = True

            self.logger.info(
                "Object '{}' deleted from S3 successfully.".format(file_key)
            )
        except ClientError as e:
            self.logger.error(
                "Failed to delete object '{}' from S3. {}".format(file_key, e.response)
            )
        return validation

    def delete_all_objects_path(self, key: str):
        res = False
        try:
            self.s3_bucket.objects.filter(Prefix=key).delete()
            res = True
        except ClientError as e:
            msj = e.args[0]
            e = api_error('S3Error')
            e.error['description'] = msj
            abort(code=e.status_code, message=e.message, error=e.error)

        return res

    def upload_file_obj(self, buffer):
        error = False
        try:
            self.s3_client.upload_file_obj(buffer, self.bucket_source)
        except ClientError as e:
            self.logger.info("Error uploading object -> %s", str(e))
            error = True
        return error
