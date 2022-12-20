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

import json

import inject
from flask import current_app
from flask_cors import cross_origin
from flask_restx import Resource, Namespace
from flask_restx.reqparse import request

from src.application.user.user_uc import GetUser, GetAllUsers, CreateUser, PutStatesApproval, GetUserStates
from src.domain.entities.common_entity import InputPaginationEntity, JwtEntity
from src.domain.entities.user_entity import UserNewEntity
from src.domain.entities.user_manage_entity import UserManageEntity, ProductManageEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth
from src.infrastructure.adapters.flask.app.utils.ultils import get_schema, is_valid_uuid_input

#
# This file contains the user endpoints Api-rest
# @author David Córdoba
#

api = Namespace(name='users', description="User controller", path='/api/v1/users')


@api.route("/")
class UsersResource(Resource):

    @inject.autoparams('get_all_users', 'create_user')
    def __init__(self, api: None, get_all_users: GetAllUsers, create_user: CreateUser):
        self.api = api
        self.get_all_users = get_all_users
        self.create_user = create_user

    @api.doc(params=get_schema(InputPaginationEntity), security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all users with pagination"""
        current_app.logger.info(f"Starts {request.url} [{request.method}]")
        jwt = dict(request.headers).get('Authorization', None)
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        result = self.get_all_users.execute(limit, offset, jwt)
        current_app.logger.info(f"Ends {request.url} [{request.method}]")
        return json.loads(result.json()), 200

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def post(self, *args, **kwargs):
        """Creates a new user. Note: Just in bazar-offchain"""
        entity = UserNewEntity.parse_obj(request.json)
        result = self.create_user.execute(entity)
        return json.loads(result.json()), 201


@api.route("/<string:user_uuid>")
class UserByUuidResource(Resource):

    @inject.autoparams('get_user')
    def __init__(self, api: None, get_user: GetUser):
        self.api = api
        self.get_user = get_user

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, user_uuid, *args, **kwargs):
        """Gets a specific user by user uuid"""
        jwt = dict(request.headers).get('Authorization', None)
        is_valid_uuid_input(user_uuid)
        result = self.get_user.execute(jwt, user_uuid)
        return json.loads(result.json()), 200


@api.route("/user-states")
class UserResource(Resource):

    @inject.autoparams('get_user_states')
    def __init__(self, api: None, get_user_states: GetUserStates):
        self.api = api
        self.get_user_states = get_user_states

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all user states"""
        result = self.get_user_states.execute()
        return json.loads(result.json()), 200


@api.route("/user-approval")
class UserApprovalResource(Resource):

    # Swagger
    product_schema = ProductManageEntity.schema()
    product_model = api.schema_model("ProductManageEntity", product_schema)

    user_schema = UserManageEntity.schema()
    user_model = api.schema_model("UserManageEntity", user_schema)

    @inject.autoparams('put_states_approval')
    def __init__(self, api: None, put_states_approval: PutStatesApproval):
        self.api = api
        self.put_states_approval = put_states_approval

    @api.doc(security='Private JWT')
    @api.expect(product_model, user_model)
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def put(self, *args, **kwargs):
        """Approves user and product or only product or only user"""
        entity = UserManageEntity.parse_obj(request.json)
        result = self.put_states_approval.execute(entity)
        return json.loads(result.json()), 200
