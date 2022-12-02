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
from flask_cors import cross_origin
from flask_restx import Resource, Namespace
from flask_restx.reqparse import request

from src.application.company.avatar_uc import GetAllAvatars
from src.domain.entities.common_entity import InputPaginationEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth
from src.infrastructure.adapters.flask.app.utils.ultils import get_schema

#
# This file contains the avatar endpoints Api-rest
# @author David Córdoba
#

api = Namespace("avatars", description="Avatar controller", path='/api/v1/avatars')


@api.route("/")
class AvatarsResource(Resource):

    @inject.autoparams('get_all_avatars')
    def __init__(self, api: None, get_all_avatars: GetAllAvatars):
        self.api = api
        self.get_all_avatars = get_all_avatars

    @api.doc(params=get_schema(InputPaginationEntity), security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets  all avatars with pagination or without pagination"""
        limit = request.args.get('limit', None)
        offset = request.args.get('offset', None)
        result = self.get_all_avatars.execute(limit, offset)
        return json.loads(result.json()), 200
