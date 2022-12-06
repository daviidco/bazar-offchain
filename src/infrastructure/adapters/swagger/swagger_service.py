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
from flask import Blueprint
from flask_restx import Api
from importlib import import_module

# Instance Blueprint
service_swagger = Blueprint('api', __name__, url_prefix='/')

# Dictionary to manage Bearer token application
authorizations = {
    'Private JWT': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter JWT Bearer token. Example: \"Bearer {token}\"'

    },
}

# Instance Api swagger
api = Api(service_swagger, title="bazar-offchain Api - Documentation",
          authorizations=authorizations, version="0.1.0",
          description="This api documentation contains all endpoints developed by backend team with flask framework. \n"
                      "Remember you should first do login and set the Bearer token in option authorize.")

# Recursive import of controllers app as Namespaces
if os.getcwd().endswith('flask'):
    os.chdir('../../../../')
base_dir = os.getcwd()+"/src/infrastructure/adapters/flask/app/controllers"
module_managers_folders = os.listdir(base_dir)
list_name_spaces = []
for module in module_managers_folders:

    for root, dirs, files in os.walk(f"{base_dir}/{module}"):
        for file in files:
            if file.endswith("_resources.py"):
                route = os.path.join(root, file)
                base = ".".join(route.split('/')[3:-1])
                name = file.split('.')[0]
                imported_module = import_module(f"{base[base.find('.src.')+1:]}.{name}")
                for attribute_name in dir(imported_module):
                    if attribute_name == 'api':
                        attribute = getattr(imported_module, attribute_name)
                        list_name_spaces.append(attribute)


# Add namespaces from controllers app
order_list_name_spaces = sorted(list_name_spaces, key=lambda x: x.name)
for ns in order_list_name_spaces:
    api.add_namespace(ns)
