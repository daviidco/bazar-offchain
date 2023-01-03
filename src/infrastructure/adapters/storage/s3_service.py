# -*- coding: utf-8 -*-
#
# This source code is the confidential, proprietary information of
# Bazar Network S.A.S., you may not disclose such Information,
# and may only use it in accordance with the terms of the license
# agreement you entered into with Bazar Network S.A.S.
#
# 2022: Bazar Network S.A.S.
# All Rights Reserved.
#

import boto3
import inject
from botocore.exceptions import ClientError
from flask import current_app
from flask_restx import abort

from src.domain.ports.object_file_interface import IStorage
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error
from src.infrastructure.config.config_parameters import get_parameter_value, _get_env_variable

# from src.infrastructure.config.default_infra import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME


#
# This file contains generic methods of bucket s3 aws
# @author David Córdoba
#

AWS_ACCESS_KEY_ID = _get_env_variable("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = _get_env_variable("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = get_parameter_value('AWS_BUCKET_NAME')


class S3Repository(IStorage):

    @inject.autoparams()
    def __init__(self,  bucket_name=None, s3_client=None, session=None):
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

    def error_s3_service(self, e):
        msj = e.args[0]
        current_app.logger.error(f"{msj}")
        e = api_error('S3Error')
        e.error['description'] = msj
        abort(code=e.status_code, message=None, error=e.error)

    def put_object(self, body: any, key: str, content_type: str, bucket: str = None):
        """
        Function to upload one object to s3-aws
        :param body: object to upload
        :param key: path s3
        :param content_type:
        :param bucket: name bucket s3 to upload file it's optional. for default use a bucket pre-defined
        :return: response boolean True if process was success, abort if process had some error
        """
        bucket_name = self.bucket_name if bucket is None else bucket
        try:
            self.s3_client.put_object(Body=body, Bucket=bucket_name, Key=key, ContentType=content_type)
            current_app.logger.info(f"Object uploaded successfully at  {key} - bucket {bucket_name}.")
            return True
        except ClientError as e:
            self.error_s3_service(e)
            return False

    def delete_objects(self, key: str, bucket: str = None):
        """
        Function to delete all objects of a specific path from s3
        :param key: path s3
        :param bucket: name bucket s3 to upload file it's optional. for default use a bucket pre-defined
        :return: boolean True if process was success, abort if process had some error
        """
        bucket_name = self.bucket_name if bucket is None else bucket

        try:
            objects = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=key)

            # If exists objects, these will be deleted
            if 'Contents' in objects:
                delete_keys = {'Objects': [{'Key': obj['Key']} for obj in objects['Contents']]}
                res = self.s3_client.delete_objects(Bucket=bucket_name, Delete=delete_keys)
                errors = res.get('Errors', None)
                if errors is None:
                    current_app.logger.info(f"All objects from  {key} were delete from bucket {bucket_name}.")
                    return True
                else:
                    raise Exception(f'Error trying delete objects s3 from {key} bucket {bucket_name}')
            else:
                current_app.logger.info(f"Not exists objects at {key} from bucket {bucket_name} to delete.")
            return True

        except ClientError as e:
            self.error_s3_service(e)
            return False

    def get_list_objects(self, key: str, bucket: str = None):
        """
        Function to get a list of objects from a specific path
        :param key: path s3
        :param bucket: name bucket s3 to upload file it's optional. for default use a bucket pre-defined
        :return: list of objects from specific path of bucket s3
        """
        bucket_name = self.bucket_name if bucket is None else bucket
        try:
            # Use the list_objects_v2() method to get the list of objects in the bucket
            objects = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=key)

            # If exists objects, these will be deleted
            if 'Contents' in objects:
                # Get the list of objects
                list_objects = objects['Contents']
                return list_objects
            return []
        except ClientError as e:
            self.error_s3_service(e)
            return []

    def validate_object_exists(self, body: any, key: str, bucket: str = None):
        """
        Function to validate if object was uploaded previously
        :param body: object to compare
        :param key: path s3
        :param bucket: name bucket s3 to upload file it's optional. for default use a bucket pre-defined
        :return: list of objects from specific path of bucket s3
        """
        bucket_name = self.bucket_name if bucket is None else bucket
        try:
            # Use the list_objects_v2() method to get the list of objects in the bucket
            objects = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=key)

            # If exists objects, these will be deleted
            if 'Contents' in objects:
                # Get the list of objects
                list_objects = objects['Contents']
                for obj in list_objects:
                    if obj['Key'] == body.filename and obj["Size"]:
                        return True
                    bucket.objects.filter(Prefix="path/to/dir").delete()

            return False

        except ClientError as e:
            self.error_s3_service(e)
            return False

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
            current_app.logger.info("Error copying object -> %s", str(e))
            error = e.response['Error']['Code']
        return error

    def get_object(self, key: str):
        error = False
        try:
            self.s3_client.get_object(Bucket=self.bucket_source, Key=key)
            # return response["Body"].read()
        except ClientError as e:
            current_app.logger.info("Error uploading object -> %s", str(e))
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
            current_app.logger.info("Error uploading object -> %s", str(e))
            error = True
        return error

    def upload_file(self, filename: str, key: str):
        error = False
        try:
            self.s3_client.upload_file(filename, self.bucket_source, key)
        except ClientError as e:
            current_app.logger.info("Error uploading object -> %s", str(e))
            error = True
        return error

    def put_list_object(self, files: list, prefix: str, bucket: str = None):
        res = False
        bucket_name = self.bucket_name if bucket is None else bucket
        try:
            for o in files:
                key = f"{prefix}/{o.filename}"
                self.s3_client.put_object(Body=o, Bucket=bucket_name, Key=key, ContentType=o.content_type)
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
            current_app.logger.error(
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

            current_app.logger.info(
                "Object '{}' updated in S3 correctly by '{}'.".format(
                    actual_file_key, new_file_key
                )
            )
        except ClientError as e:
            current_app.logger.error(
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

            current_app.logger.info(
                "Object '{}' deleted from S3 successfully.".format(file_key)
            )
        except ClientError as e:
            current_app.logger.error(
                "Failed to delete object '{}' from S3. {}".format(file_key, e.response)
            )
        return validation

    def upload_file_obj(self, buffer):
        error = False
        try:
            self.s3_client.upload_file_obj(buffer, self.bucket_source)
        except ClientError as e:
            current_app.logger.info("Error uploading object -> %s", str(e))
            error = True
        return error
