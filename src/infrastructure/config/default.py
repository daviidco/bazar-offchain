from os import environ

from dotenv import load_dotenv

load_dotenv()


def _get_env_variable(name):
    try:
        return environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


# Environment flask-env
ENV = _get_env_variable("ENV").upper()

# Flask
SECRET_KEY = _get_env_variable('SECRET_KEY')
PROPAGATE_EXCEPTIONS = False

# Flask-Restx
BUNDLE_ERRORS = False
ERROR_404_HELP = True

# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''
