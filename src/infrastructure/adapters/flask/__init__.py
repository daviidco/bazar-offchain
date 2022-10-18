from flask import Flask, jsonify
from flask_restx import Api

from src.infrastructure.adapters.flask import app
from src.infrastructure.adapters.flask.app.controllers.user.blueprints.user_blueprint_v1 import users_v1_01_bp
from src.infrastructure.adapters.flask.app.controllers.company.blueprints.company_bp_v1_0_1 import companies_v1_01_bp
from src.infrastructure.adapters.flask.app.controllers.avatar.blueprints.avatar_bp_v1_0_1 import avatars_v1_01_bp
from src.infrastructure.adapters.flask.app.utils.error_handling import ObjectNotFound, AppErrorBaseClass, \
    IntegrityErrorApp, AuthError
from src.infrastructure.adapters.flask.app.utils.logger import configure_logging
from src.infrastructure.adapters.flask.configuration_injector import configure_inject


def create_app(settings_module):
    app = Flask(__name__)

    app.config.from_object(settings_module)
    # Load the configuration depending of environment
    config_env = app.config.get('ENV', 'LOCAL').lower()
    path_config_file = f'../../config/{config_env}.py'
    app.config.from_pyfile(f'{path_config_file}')

    # Configure Logger
    configure_logging(app)
    app.logger.info(f'Environment: {config_env}')
    app.logger.info(f'Environment configuration file: {path_config_file}')

    configure_inject(app)

    # Initialize extensions
    # db.init_app(app)
    # ma.init_app(app)
    # migrate.init_app(app, db)
    # storage.init_app(app)
    # auth0.init_app(app)

    # Catch errors 404
    Api(app,  catch_all_404s=True)

    # Disable strict mode when URL ends with /
    app.url_map.strict_slashes = False

    prefix = '/api'
    # Blueprints register
    app.register_blueprint(users_v1_01_bp, url_prefix=f'{prefix}')
    app.register_blueprint(companies_v1_01_bp, url_prefix=f'{prefix}')
    app.register_blueprint(avatars_v1_01_bp, url_prefix=f'{prefix}')
    app.logger.info('Blueprints Registered')

    @app.route(f'{prefix}/help', methods=['GET'])
    def help():
        """Print available functions."""
        routes = {}
        rules = app.url_map.iter_rules()
        for r in rules:
            routes[r.rule] = {}
            routes[r.rule]["functionName"] = r.endpoint
            routes[r.rule]["methods"] = list(r.methods)

        routes.pop("/static/<path:filename>")

        return jsonify(routes)

    return app


