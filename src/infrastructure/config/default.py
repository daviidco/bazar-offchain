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

import pytz
from dotenv import load_dotenv

from src.infrastructure.config.config_parameters import put_parameter_s_k, _get_env_variable

#
# This file contains basic default configuration
# @author David Córdoba
#

load_dotenv()


# Environment flask-env
ENV = _get_env_variable("ENV").upper()
AWS_REGION = _get_env_variable("AWS_DEFAULT_REGION")

# Secret key
SECRET_KEY = put_parameter_s_k()

# Flask
PROPAGATE_EXCEPTIONS = False

# Flask-Restx
BUNDLE_ERRORS = False
ERROR_404_HELP = True
UTC_TIME_ZONE = pytz.timezone('America/Bogota')

# External services
EMAIL_BAZAR_ADMIN = 'pcordoba@cafetosoftware.com'
URL_EMAIL_LAMBDA = 'https://30mtgv2761.execute-api.us-east-2.amazonaws.com/dev/create'
URL_MS_BAZAR_AUTH = 'https://meerkat-auth.herokuapp.com/api/v1/user'
URL_MS_BAZAR_AUTH = 'https://auth.bazar.network/api/v1/user'
# AUTH0
AUTH0_DOMAIN = 'dev-bazarnetwork.us.auth0.com'
AUTH0_API_AUDIENCE = 'https://dev-bazarnetwork.us.auth0.com/api/v2/'


AUTH0_ALGORITHMS = ["RS256"]

# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''
