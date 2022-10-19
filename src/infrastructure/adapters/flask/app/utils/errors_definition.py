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


#
# This file contains a dictionary where are defined application errors
# @author David Córdoba
#

APIErrors = {
    # Errors Auth0 E2000 - E2100
    'AuthorizationHeaderMissing': {"error": {"code": "E2000",
                                             "message": "Authorization header missing",
                                             "description": "Authorization header is expected.",
                                             "status_code": 401}},

    'InvalidHeaderByBearer': {"error": {"code": "E2001",
                                        "message": "Invalid header by bearer",
                                        "description": "Authorization header must start with Bearer.",
                                        "status_code": 401}},

    'BearerTokenMissing': {"error": {"code": "E2002",
                                     "message": "Bearer token not found",
                                     "description": "Token not found.",
                                     "status_code": 401}},

    'InvalidHeaderByShapeToken': {"error": {"code": "E2003",
                                            "message": "Invalid header by token ",
                                            "description": "Authorization header must be bearer token.",
                                            "status_code": 401}},

    'TokenExpiredError': {"error": {"code": "E2004",
                                    "message": "token is expired",
                                    "description": "token is expired. Refresh your token.",
                                    "status_code": 401}},

    'InvalidClaimsError': {"error": {"code": "E2005",
                                     "message": "token is expired",
                                     "description": "token is expired. Refresh your token.",
                                     "status_code": 401}},

    'InvalidHeaderUnknownError': {"error": {"code": "E2006",
                                            "message": "Invalid header",
                                            "description": "Unable to parse authentication.",
                                            "status_code": 401}},

    'InvalidHeaderByKeyError': {"error": {"code": "E2007",
                                          "message": "Invalid header",
                                          "description": "Unable to find appropriate key.",
                                          "status_code": 401}},

    # Errors S3 E2100 - E2200

    # Company
    'CompanyExistingError': {"error": {"code": "E2200",
                                       "message": "Existing Company",
                                       "description": "Existing Company related with user.",
                                       "status_code": 401}},

    'CompanySavingError': {"error": {"code": "E2201",
                                           "message": "Error saving company",
                                           "description": "Please check the documents and json body.",
                                           "status_code": 401}},

    # User

    'UserExistingError': {"error": {"code": "E2202",
                                    "message": "Existing User",
                                    "description": "Existing user in system off-chain.",
                                    "status_code": 401}},
    # Errors Flask E2200 - E2300

    # Errors AWS E2300 - ...
    'S3Error': {"error": {"code": "E2300",
                          "message": "Error bucket s3",
                          "description": "Undefined.",
                          "status_code": 401}},

}
