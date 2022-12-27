import os

import boto3

from src.infrastructure.config.default import _get_env_variable


def get_parameter_value(parameter_name: str) -> str:
    env = os.environ.get("ENV")
    aws_default_region = os.environ.get("AWS_DEFAULT_REGION")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    tag_env = '/backend/'
    if env == 'testing':
        tag_env += 'test'
    elif env == 'development':
        tag_env += 'dev'
    elif env == 'staging':
        tag_env += 'stag'
    elif env == 'production':
        tag_env += 'prod'
    else:
        tag_env += 'test'

    parameter_name = tag_env + parameter_name

    ssm_client = boto3.client('ssm',
                              region_name=aws_default_region,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

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
    db_user = get_parameter_value('DB_USER')
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

    
