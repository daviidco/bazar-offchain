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

import os

from src.infrastructure.adapters.flask import create_app

#
# This file is the entrypoint of the application
# @author David Córdoba
#

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)

if __name__ == "__main__":
    app.run(port=8082)