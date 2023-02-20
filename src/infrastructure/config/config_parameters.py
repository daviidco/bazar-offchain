import binascii
import os

import boto3


def _get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def __get_prefix_parameter():
    env = os.environ.get("ENV").lower()
    tag_env = '/backend/'
    if env == 'testing':
        tag_env += 'test/'
    elif env == 'development':
        tag_env += 'dev/'
    elif env == 'staging':
        tag_env += 'stag/'
    elif env == 'production':
        tag_env += 'prod/'
    else:
        tag_env += 'test/'

    return tag_env


def __get_ssm_client():
    aws_default_region = os.environ.get("AWS_DEFAULT_REGION")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    ssm_client = boto3.client('ssm',
                              region_name=aws_default_region,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

    return ssm_client


def get_parameter_value(parameter_name: str) -> str:
    ssm_client = __get_ssm_client()
    tag_env = __get_prefix_parameter()
    parameter_name = tag_env + parameter_name
    response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']


def get_database_connection_local():
    # DB credentials
    db_engine = _get_env_variable("DB_ENGINE")
    db_user = _get_env_variable(f"DB_USERNAME")
    db_password = _get_env_variable(f"DB_PASSWORD")
    db_host = _get_env_variable(f"DB_HOST")
    db_name = _get_env_variable(f"DB_NAME")
    db_schema = _get_env_variable(f"DB_SCHEMA")

    sqlalchemy_database_uri = fr"{db_engine}://{db_user}:{db_password}@{db_host}/{db_name}".replace('%', '%%')
    return sqlalchemy_database_uri, db_schema


def get_secret_database_connection():
    # DB credentials
    db_engine = get_parameter_value('DB_ENGINE')
    db_user = get_parameter_value('DB_USERNAME')
    db_password = get_parameter_value('DB_PASSWORD')
    db_host = get_parameter_value('DB_HOST')
    db_name = get_parameter_value('DB_NAME')
    db_schema = get_parameter_value('DB_SCHEMA')

    sqlalchemy_database_uri = fr"{db_engine}://{db_user}:{db_password}@{db_host}/{db_name}".replace('%', '%%')
    return sqlalchemy_database_uri, db_schema


def get_database_connection():
    env = os.environ.get("ENV")
    if env in ['testing', 'development', 'staging', 'production']:
        return get_secret_database_connection()
    elif env == 'local':
        return get_database_connection_local()
    else:
        raise Exception(f'ENVIRONMENT_NAME {env} is invalid')


def put_parameter_s_k():
    try:
        secret_key = binascii.hexlify(os.urandom(24)).decode('utf-8')
        ssm_client = __get_ssm_client()
        tag_env = __get_prefix_parameter()
        ssm_client.put_parameter(
            Name=f"{tag_env}SECRET_KEY",
            Description="Secret Key application flask",
            Value=secret_key,
            Type="SecureString",
            Overwrite=True
        )
        s_k = get_parameter_value(parameter_name='SECRET_KEY')
        return s_k
    except Exception as e:
        print(e)
