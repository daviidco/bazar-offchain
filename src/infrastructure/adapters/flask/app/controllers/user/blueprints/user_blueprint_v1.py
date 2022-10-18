from flask import Blueprint
from flask_restx import Api

from src.infrastructure.adapters.flask.app.controllers.user.user_resources import api as user_ns

users_v1_01_bp = Blueprint('users_v1_01_bp', __name__)

api = Api(users_v1_01_bp, version="0.1.0", title="User")
api.add_namespace(user_ns, path='/v1/users')
