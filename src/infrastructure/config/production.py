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

from src.infrastructure.config.default import *

#
# This file contains production configuration
# @author David Córdoba
#

APP_ENV = APP_ENV_PRODUCTION

# Secret key
SECRET_KEY = put_parameter_s_k()

# Basic parameters
TESTING = False
DEBUG = False
