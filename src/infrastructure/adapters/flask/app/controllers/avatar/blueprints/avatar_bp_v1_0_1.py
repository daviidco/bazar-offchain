from flask import Blueprint
from flask_restx import Api

from src.infrastructure.adapters.flask.app.controllers.avatar.avatar_resources import api as avatar_ns

avatars_v1_01_bp = Blueprint('avatars_v1_01_bp', __name__)

api = Api(avatars_v1_01_bp, version="0.1.0", title="Avatar")
api.add_namespace(avatar_ns, path='/v1/avatars')
