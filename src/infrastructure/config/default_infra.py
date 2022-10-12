from os import environ

import pytz
from dotenv import load_dotenv

load_dotenv()


def _get_env_variable(name):
    try:
        return environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


ENV = _get_env_variable("ENV").upper()

UTC_TIME_ZONE = pytz.timezone(_get_env_variable("UTC_TIME_ZONE"))

# DB credentials
DB_ENGINE = _get_env_variable("DB_ENGINE")
DB_USER = _get_env_variable(f"{ENV}_DB_USERNAME")
DB_PASSWORD = _get_env_variable(f"{ENV}_DB_PASSWORD")
DB_HOST = _get_env_variable(f"{ENV}_DB_HOST")
DB_NAME = _get_env_variable(f"{ENV}_DB_NAME")

SQLALCHEMY_DATABASE_URI = fr"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".replace('%', '%%')

# AWS Credentials
AWS_ACCESS_KEY_ID = _get_env_variable(f"{ENV}_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = _get_env_variable(f"{ENV}_AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = _get_env_variable(f"{ENV}_AWS_BUCKET_NAME")

# Auth0
AUTH0_DOMAIN = _get_env_variable(f"AUTH0_DOMAIN")
AUTH0_API_AUDIENCE = _get_env_variable(f"AUTH0_API_AUDIENCE")
AUTH0_ALGORITHMS = ["RS256"]
