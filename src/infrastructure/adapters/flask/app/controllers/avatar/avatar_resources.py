import json

import inject
from flask_cors import cross_origin
from flask_restx import Resource, Namespace
from flask_restx.reqparse import request

from src.application.company.avatar_uc import GetAllAvatars
from src.infrastructure.adapters.auth0.auth0_service import requires_auth

api = Namespace("/avatars", description="Avatar controller")


@api.route("/")
class AvatarsResource(Resource):
    @inject.autoparams('get_all_avatars')
    def __init__(self, api: None, get_all_avatars: GetAllAvatars):
        self.api = api
        self.get_all_avatars = get_all_avatars

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self):
        limit = request.json['limit'] if request.data else None
        offset = request.json['offset'] if request.data else None
        result = self.get_all_avatars.execute(limit, offset)
        return json.loads(result.json()), 200
