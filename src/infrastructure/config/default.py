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

from os import environ

from dotenv import load_dotenv

#
# This file contains basic default configuration
# @author David Córdoba
#

load_dotenv()


def _get_env_variable(name):
    try:
        return environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


# Environment flask-env
ENV = _get_env_variable("ENV").upper()
EMAIL_BAZAR_ADMIN = _get_env_variable("EMAIL_BAZAR_ADMIN")
URL_EMAIL_LAMBDA = _get_env_variable("URL_EMAIL_LAMBDA")
EMAIL_BAZAR_ADMIN = _get_env_variable("EMAIL_BAZAR_ADMIN")
URL_MS_BAZAR_AUTH = _get_env_variable("URL_MS_BAZAR_AUTH")

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
