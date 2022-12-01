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
from src.application.wishlist.wishlist_uc import CreateWishProduct, DeleteWishProduct
from src.domain.entities.product_entity import ProductNewEntity
from src.domain.entities.wishlist_entity import WishProductNewEntity, WishProductEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth
from src.infrastructure.adapters.flask.app.utils.ultils import get_schema

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
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def post(self, *args, **kwargs):
        role = kwargs.get('role', None)
        role = 'buyer'
        entity = WishProductNewEntity.parse_obj(request.args)
        result = self.create_wish_product.execute(role, entity)
        return json.loads(result.json()), 201

    @api.doc(params=get_schema(WishProductEntity), security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def delete(self, *args, **kwargs):
        role = kwargs.get('role', None)
        role = 'buyer'
        entity = WishProductNewEntity.parse_obj(request.args)
        result = self.delete_wish_product.execute(role, entity)
        return json.loads(result.json()), 200
