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

    'RoleAccessTokenError': {"error": {"code": "E2008",
                                       "message": "Role not found",
                                       "description": "Role not found in access token.",
                                       "status_code": 401}},

    # Errors S3 E2100 - E2200

    # Company
    'CompanyExistingError': {"error": {"code": "E2200",
                                       "message": "Existing Company",
                                       "description": "Existing Company related with user.",
                                       "status_code": 422}},

    'CompanySavingError': {"error": {"code": "E2201",
                                     "message": "Error saving company",
                                     "description": "Please check the documents and json body.",
                                     "status_code": 422}},

    'CompanySavingErrorByCertification': {"error": {"code": "E2202",
                                                    "message": "Error saving company",
                                                    "description": "Please check the uuid certification.",
                                                    "status_code": 422}},

    # User

    'UserExistingError': {"error": {"code": "E2202",
                                    "message": "Existing User",
                                    "description": "Existing user in system off-chain.",
                                    "status_code": 422}},

    'RoleNotFound': {"error": {"code": "E2203",
                               "message": "Role not found",
                               "description": "Role not defined.",
                               "status_code": 422}},

    'RoleWithoutPermission': {"error": {"code": "E2204",
                                        "message": "Role hasn't permission",
                                        "description": "Role hasn't permission.",
                                        "status_code": 422}},
    # Product
    'ProductSavingError': {"error": {"code": "E2209",
                                     "message": "Error saving product",
                                     "description": "Please check the documents and json body.",
                                     "status_code": 422}},

    'BasicProductNotExists': {"error": {"code": "E2210",
                                        "message": "Basic product not exists",
                                        "description": "Basic product type not exists please verify uuid.",
                                        "status_code": 422}},

    'ProductTypeNotExists': {"error": {"code": "E2211",
                                       "message": "Product type not exists",
                                       "description": "Product type not exists please verify uuid.",
                                       "status_code": 422}},

    'VarietyNotExists': {"error": {"code": "E2212",
                                   "message": "Variety type not exists",
                                   "description": "Variety not exists please verify uuid.",
                                   "status_code": 422}},

    'MinimumOrderNotExists': {"error": {"code": "E2213",
                                        "message": "Minimum Order not exists",
                                        "description": "Minimum Order not exists please verify uuid.",
                                        "status_code": 422}},

    'IncotermNotExists': {"error": {"code": "E2214",
                                    "message": "Minimum Order not exists",
                                    "description": "Minimum Order not exists please verify uuid.",
                                    "status_code": 422}},

    'NumCertificationsVSNumFilesError': {"error": {"code": "E2215",
                                                   "message": "Number certifications different number files",
                                                   "description": "Please verify the number files to upload",
                                                   "status_code": 400}},

    'ObjectNotFound': {"error": {"code": "E2216",
                                 "message": "Object not found",
                                 "description": "Object not found, please verify",
                                 "status_code": 422}},

    'EmailError': {"error": {"code": "E2217",
                             "message": "Email not sent",
                             "description": "Email not sent",
                             "status_code": 500}},

    'UndefendedError': {"error": {"code": "E2218",
                                  "message": "Error undefended",
                                  "description": "Undefined.",
                                  "status_code": 500}},

    'UuidError': {"error": {"code": "E2219",
                            "message": "Parameter is not UUID",
                            "description": "Convert to UUID is impossible",
                            "status_code": 406}},

    'CompareError': {"error": {"code": "E2220",
                               "message": "Values compared are not right",
                               "description": "Undefined.",
                               "status_code": 406}},

    'PublishProductError': {"error": {"code": "E2221",
                                      "message": "Previous state is not valid to publish product",
                                      "description": "Product must be previously Approved or Hidden to be published "
                                                     "but its ",
                                      "status_code": 400}},

    # Errors Flask E2200 - E2300

    # Errors AWS E2300 - ...
    'S3Error': {"error": {"code": "E2300",
                          "message": "Error bucket s3",
                          "description": "Undefined.",
                          "status_code": 500}},

    'IntegrityError': {"error": {"code": "E2301",
                                 "message": "Integrity error data",
                                 "description": "Duplicate key value violates unique constraint. row already exists.",
                                 "status_code": 500}},

}
