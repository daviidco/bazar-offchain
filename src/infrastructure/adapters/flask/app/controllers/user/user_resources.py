import json

import inject
from flask_cors import cross_origin
from flask_restx import Resource, Namespace
from flask_restx.reqparse import request

from src.application.user.user_uc import GetUser, GetAllUsers, CreateUser
from src.domain.entities.user_entity import UserNewEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth

api = Namespace(name='users', description="User controller")


@api.route("/")
class UsersResource(Resource):
    @inject.autoparams('get_all_users', 'create_user')
    def __init__(self, api: None, get_all_users: GetAllUsers, create_user: CreateUser):
        self.api = api
        self.get_all_users = get_all_users
        self.create_user = create_user

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self):
        limit = request.json['limit']
        offset = request.json['offset']
        result = self.get_all_users.execute(limit, offset)
        return json.loads(result.json()), 201

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def post(self):
        entity = UserNewEntity.parse_obj(request.json)
        result = self.create_user.execute(entity)
        return json.loads(result.json()), 201


@api.route("/<string:user_uuid>")
class UserResource(Resource):

    @inject.autoparams('get_user')
    def __init__(self, api: None, get_user: GetUser):
        self.api = api
        self.get_user = get_user

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, user_uuid):
        result = self.get_user.execute(user_uuid)
        return json.loads(result.json()), 200
