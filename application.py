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
import time

from flask import Flask, jsonify, request, g
from flask_restx import Api, Resource

import src.infrastructure.adapters.swagger.swagger_service
from src.infrastructure.adapters.flask.app.controllers.avatar.blueprints.avatar_bp_v1_0_1 import avatars_v1_01_bp
from src.infrastructure.adapters.flask.app.controllers.company.blueprints.company_bp_v1_0_1 import companies_v1_01_bp
from src.infrastructure.adapters.flask.app.controllers.product.blueprints.product_bp_v1_0_1 import products_v1_01_bp
from src.infrastructure.adapters.flask.app.controllers.user.blueprints.user_blueprint_v1 import users_v1_01_bp
from src.infrastructure.adapters.flask.app.controllers.wishlist.blueprints.wishlist_bp_v1_0_1 import wish_lists_v1_01_bp
from src.infrastructure.adapters.flask.app.utils.logger import configure_logging
from src.infrastructure.adapters.flask.configuration_injector import configure_inject
from src.infrastructure.config.config_parameters import get_parameter_value

application = Flask(__name__)
settings_module = get_parameter_value('APP_SETTINGS_MODULE')
application.config.from_object(settings_module)
# Load the configuration depending of environment
config_env = application.config.get('ENV', 'LOCAL').lower()
path_config_file = f'src/infrastructure/config/{config_env}.py'
application.config.from_pyfile(f'{path_config_file}')

# Configure Logger
configure_logging(application)
application.logger.info(f'Environment: {config_env}')
application.logger.info(f'Environment configuration file: {path_config_file}')
configure_inject(application.logger)

# Disable strict mode when URL ends with /
application.url_map.strict_slashes = False


@application.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@application.before_request
def log_request_start():
    g.start_time = time.time()
    application.logger.debug(f"Request {request.url} started")


@application.after_request
def log_request_end(response):
    elapsed_time = time.time() - g.start_time
    minutes, seconds = divmod(elapsed_time, 60)
    seconds = round(seconds, 2)
    application.logger.debug(f"Request {request.url} processed in {minutes} minutes and {seconds} seconds")
    return response


prefix = '/api/v1/'
# Blueprints register
application.register_blueprint(users_v1_01_bp, url_prefix=f'{prefix}')
application.register_blueprint(companies_v1_01_bp, url_prefix=f'{prefix}')
application.register_blueprint(avatars_v1_01_bp, url_prefix=f'{prefix}')
application.register_blueprint(products_v1_01_bp, url_prefix=f'{prefix}')
application.register_blueprint(wish_lists_v1_01_bp, url_prefix=f'{prefix}')
application.logger.info('Blueprints Registered')

# Initialize swagger
application.register_blueprint(src.infrastructure.adapters.swagger.swagger_service.service_swagger)

# Catch errors 404
api = Api(application, catch_all_404s=True)


@api.route(f'{prefix}/help', methods=['GET'])
class Help(Resource):
    def get(self):
        """Print available functions."""
        routes = {}
        rules = application.url_map.iter_rules()
        for r in rules:
            routes[r.rule] = {}
            routes[r.rule]["functionName"] = r.endpoint
            routes[r.rule]["methods"] = list(r.methods)

        routes.pop("/static/<path:filename>")

        return jsonify(routes)


if __name__ == '__main__':
    application.run(host='0.0.0.0')
