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
from flask_restx import Resource, Namespace
from flask_restx.reqparse import request

from src.application.wishlist.wishlist_uc import CreateWishProduct, DeleteWishProduct, GetWishList, \
    GetWishListByUuidBuyerAndSearchBar, GetWishListByUuidBuyerAndBasicProduct, GetWishlistFilter
from src.domain.entities.common_entity import InputPaginationEntity
from src.domain.entities.product_entity import ProductsPaginationEntity, \
    ProductFilterBuyerBasicProductEntity, ProductFilterBuyerEntity
from src.domain.entities.wishlist_entity import WishProductNewEntity, WishProductEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth, requires_role
from src.infrastructure.adapters.flask.app.utils.ultils import get_schema, is_valid_uuid_input, compare_nums

#
# This file contains the wishlist endpoints Api-rest
# @author David Córdoba
#

api = Namespace("wishlist", description="Wishlist controller - Just works to Buyers", path='/api/v1/wishlist')


@api.route("/")
class ProductResource(Resource):

    @inject.autoparams('create_wish_product', 'delete_wish_product')
    def __init__(self, api: None, create_wish_product: CreateWishProduct, delete_wish_product: DeleteWishProduct):
        self.api = api
        self.create_wish_product = create_wish_product
        self.delete_wish_product = delete_wish_product

    @api.doc(params=get_schema(WishProductNewEntity), security='Private JWT')
    @requires_auth
    @requires_role(["buyer"])
    def post(self, *args, **kwargs):
        """Append product to user wishlist"""
        entity = WishProductNewEntity.parse_obj(request.args)
        result = self.create_wish_product.execute(entity)
        return json.loads(result.json()), 201

    @api.doc(params=get_schema(WishProductEntity), security='Private JWT')
    @requires_auth
    @requires_role(["buyer"])
    def delete(self, *args, **kwargs):
        """Remove product from user wishlist"""
        entity = WishProductNewEntity.parse_obj(request.args)
        result = self.delete_wish_product.execute(entity)
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
    @requires_role(["buyer"])
    def get(self, user_uuid, *args, **kwargs):
        """Get wishlist by buyer"""
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        is_valid_uuid_input(user_uuid)
        result = self.get_wishlist.execute(user_uuid, limit, offset)
        return json.loads(result.json()), self.success_code


@api.route("/basic-product")
class ProductFilterBuyerBasicProductResource(Resource):
    # Swagger
    response_schema = ProductsPaginationEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products_filter_buyer_basic_product')
    def __init__(self, app: current_app,
                 get_products_filter_buyer_basic_product: GetWishListByUuidBuyerAndBasicProduct,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products_filter_buyer_basic_product = get_products_filter_buyer_basic_product

    @api.doc(params=get_schema(ProductFilterBuyerBasicProductEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @requires_auth
    @requires_role(["buyer"])
    def get(self, *args, **kwargs):
        """Filter to wishlist products by name basic product to buyers"""
        user_uuid = request.args.get("user_uuid", 0)
        is_valid_uuid_input(user_uuid)
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        basic_product = request.args.get("basic_product", 0)
        entity = ProductFilterBuyerBasicProductEntity(limit=limit,
                                                      offset=offset,
                                                      user_uuid=user_uuid,
                                                      basic_product=basic_product)
        result = self.get_products_filter_buyer_basic_product.execute(entity)
        return json.loads(result.json()), self.success_code


@api.route("/search-bar")
class ProductFilterBuyerSearchBar(Resource):
    # Swagger
    response_schema = ProductsPaginationEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products_filter_buyer_search_bar')
    def __init__(self, app: current_app,
                 get_products_filter_buyer_search_bar: GetWishListByUuidBuyerAndSearchBar,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products_filter_buyer_search_bar = get_products_filter_buyer_search_bar

    @api.doc(params=get_schema(ProductFilterBuyerBasicProductEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @requires_auth
    @requires_role(["buyer"])
    def get(self, *args, **kwargs):
        """Filter to wishlist products by part of name basic product to buyers.
        It doesn't matter if part name is uppercase or lowercase."""
        user_uuid = request.args.get("user_uuid", 0)
        is_valid_uuid_input(user_uuid)
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        basic_product = request.args.get("basic_product", 0)
        entity = ProductFilterBuyerBasicProductEntity(limit=limit,
                                                      offset=offset,
                                                      user_uuid=user_uuid,
                                                      basic_product=basic_product)
        result = self.get_products_filter_buyer_search_bar.execute(entity)
        return json.loads(result.json()), self.success_code


@api.route("/filter-buyer")
class ProductFilterBuyerResource(Resource):
    # Swagger
    response_schema = ProductsPaginationEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products_filter_buyer')
    def __init__(self, app: current_app, get_products_filter_buyer: GetWishlistFilter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products_filter_buyer = get_products_filter_buyer

    @api.doc(params=get_schema(ProductFilterBuyerEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @requires_auth
    @requires_role(["buyer"])
    def get(self, *args, **kwargs):
        """Filter to products by buyer"""
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        price_per_kg_start = request.args.get("price_per_kg_start", 0)
        price_per_kg_end = request.args.get("price_per_kg_end", 0)
        compare_nums(price_per_kg_start, price_per_kg_end, '<')
        available_for_sale = request.args.get("available_for_sale", 0)
        user_uuid = request.args.get("user_uuid", 0)

        entity = ProductFilterBuyerEntity(limit=limit,
                                          offset=offset,
                                          price_per_kg_start=price_per_kg_start,
                                          price_per_kg_end=price_per_kg_end,
                                          available_for_sale=available_for_sale,
                                          user_uuid=user_uuid)
        result = self.get_products_filter_buyer.execute(entity)
        return json.loads(result.json()), self.success_code
