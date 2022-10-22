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

from src.domain.entities.common_entity import ErrorEntity
from src.infrastructure.adapters.flask.app.utils.errors_definition import APIErrors


#
# This file contains a method to build errors application
# @author David Córdoba
#
def api_error(error_name):
    """Internal API error handler"""

    error = APIErrors[f"{error_name}"]

    res_error = ErrorEntity(
        status_code=error['error']["status_code"],
        error=error['error']
    )
    return res_error
