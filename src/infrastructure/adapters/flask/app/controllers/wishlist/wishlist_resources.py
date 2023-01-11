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

from src.application.product.product_uc import CreateProduct, \
    GetAllProducts
from src.application.wishlist.wishlist_uc import CreateWishProduct, DeleteWishProduct, GetWishList
from src.domain.entities.common_entity import InputPaginationEntity
from src.domain.entities.product_entity import ProductNewEntity, ProductsPaginationEntity
from src.domain.entities.wishlist_entity import WishProductNewEntity, WishProductEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth
from src.infrastructure.adapters.flask.app.utils.ultils import get_schema, is_valid_uuid_input

#
# This file contains the wishlist endpoints Api-rest
# @author David Córdoba
#

api = Namespace("wishlist", description="Wishlist controller", path='/api/v1/wishlist')


@api.route("/")
class ProductResource(Resource):

    @inject.autoparams('create_wish_product', 'delete_wish_product')
    def __init__(self, api: None, create_wish_product: CreateWishProduct, delete_wish_product: DeleteWishProduct):
        self.api = api
        self.create_wish_product = create_wish_product
        self.delete_wish_product = delete_wish_product

    @api.doc(params=get_schema(WishProductNewEntity), security='Private JWT')
    @requires_auth
    def post(self, *args, **kwargs):
        """Append product to user wishlist"""
        role = kwargs.get('role', None)
        entity = WishProductNewEntity.parse_obj(request.args)
        result = self.create_wish_product.execute(role, entity)
        return json.loads(result.json()), 201

    @api.doc(params=get_schema(WishProductEntity), security='Private JWT')
    @requires_auth
    def delete(self, *args, **kwargs):
        """Remove product from user wishlist"""
        role = kwargs.get('role', None)
        entity = WishProductNewEntity.parse_obj(request.args)
        result = self.delete_wish_product.execute(role, entity)
        return json.loads(result.json()), 200


@api.route("/<string:user_uuid>")
class ProductsByUserResource(Resource):
    # Swagger
    response_schema = ProductsPaginationEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_wishlist')
    def __init__(self, app: None, get_wishlist: GetWishList):
        self.api = api
        self.get_wishlist = get_wishlist

    @api.doc(params=get_schema(InputPaginationEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @requires_auth
    def get(self, user_uuid, *args, **kwargs):
        """Get wishlist by buyer"""
        role = kwargs.get('role', None)
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        is_valid_uuid_input(user_uuid)
        result = self.get_wishlist.execute(user_uuid, role, limit, offset)
        return json.loads(result.json()), self.success_code

