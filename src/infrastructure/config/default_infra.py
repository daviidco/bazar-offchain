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

import pytz
from dotenv import load_dotenv

load_dotenv()


#
# This file contains basic default configuration to infrastructure adapters
# @author David Córdoba
#


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
DB_SCHEMA = _get_env_variable(f"{ENV}_DB_SCHEMA")

SQLALCHEMY_DATABASE_URI = fr"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".replace('%', '%%')


# AWS Credentials
AWS_ACCESS_KEY_ID = _get_env_variable(f"{ENV}_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = _get_env_variable(f"{ENV}_AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = _get_env_variable(f"{ENV}_AWS_BUCKET_NAME")
AWS_REGION = _get_env_variable(f"AWS_DEFAULT_REGION")

# Auth0
AUTH0_DOMAIN = _get_env_variable(f"AUTH0_DOMAIN")
AUTH0_API_AUDIENCE = _get_env_variable(f"AUTH0_API_AUDIENCE")
AUTH0_ALGORITHMS = ["RS256"]
