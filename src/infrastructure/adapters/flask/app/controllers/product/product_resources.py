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
from flask import _request_ctx_stack
from flask_cors import cross_origin
from flask_restx import Resource, Namespace
from flask_restx.reqparse import request

from src.application.company.avatar_uc import GetAllAvatars
from src.application.company.product_uc import GetAllBasicProducts, GetProductTypes, GetVarieties, \
    GetSustainabilityCertifications, GetInconterms, GetMinimumOrders, CreateProduct, GetAllProducts
from src.domain.entities.common_entity import JwtEntity
from src.domain.entities.product_entity import ProductNewEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth

#
# This file contains the products endpoints Api-rest
# @author David Córdoba
#

api = Namespace("/products", description="Product controller")


@api.route("/")
class ProductResource(Resource):
    @inject.autoparams('get_all_products', 'create_product')
    def __init__(self, api:None, get_all_products: GetAllProducts, create_product: CreateProduct):
        self.api = api
        self.get_all_products = get_all_products
        self.create_product = create_product

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        limit = request.json['limit']
        offset = request.json['offset']
        result = self.get_all_products.execute(limit, offset)
        return json.loads(result.json()), 200

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def post(self, *args, **kwargs):
        role = kwargs['role']
        # role = 'undefinded'
        entity = ProductNewEntity.parse_obj(json.loads(request.form['body']))
        files = request.files.getlist('files[]')
        images = request.files.getlist('images[]')
        result = self.create_product.execute(role, entity, files, images)
        return json.loads(result.json()), 201


@api.route("/basic-products")
class BasicProductsResource(Resource):
    @inject.autoparams('get_all_basic_products')
    def __init__(self, api: None, get_all_basic_products: GetAllBasicProducts):
        self.api = api
        self.get_all_basic_products = get_all_basic_products

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        result = self.get_all_basic_products.execute()
        return json.loads(result.json()), 200


@api.route("/product-types/<string:uuid_basic_product>")
class BasicProductsResource(Resource):
    @inject.autoparams('get_products_type_by_uuid_basic_product')
    def __init__(self, api: None, get_products_type_by_uuid_basic_product: GetProductTypes):
        self.api = api
        self.get_products_type_by_uuid_basic_product = get_products_type_by_uuid_basic_product

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, uuid_basic_product, *args, **kwargs):
        result = self.get_products_type_by_uuid_basic_product.execute(uuid_basic_product)
        return json.loads(result.json()), 200


@api.route("/varieties/<string:uuid_basic_product>")
class BasicProductsResource(Resource):
    @inject.autoparams('get_varieties_by_uuid_basic_product')
    def __init__(self, api: None, get_varieties_by_uuid_basic_product: GetVarieties):
        self.api = api
        self.get_varieties_by_uuid_basic_product = get_varieties_by_uuid_basic_product

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, uuid_basic_product, *args, **kwargs):
        result = self.get_varieties_by_uuid_basic_product.execute(uuid_basic_product)
        return json.loads(result.json()), 200


@api.route("/sustainability-certifications")
class BasicProductsResource(Resource):
    @inject.autoparams('get_all_sustainability_certifications')
    def __init__(self, api: None, get_all_sustainability_certifications: GetSustainabilityCertifications, *args, **kwargs):
        self.api = api
        self.get_all_sustainability_certifications = get_all_sustainability_certifications

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        result = self.get_all_sustainability_certifications.execute()
        return json.loads(result.json()), 200


@api.route("/incoterms")
class BasicProductsResource(Resource):
    @inject.autoparams('get_all_incoterms')
    def __init__(self, api: None, get_all_incoterms: GetInconterms):
        self.api = api
        self.get_all_incoterms = get_all_incoterms

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        result = self.get_all_incoterms.execute()
        return json.loads(result.json()), 200


@api.route("/minimum-orders")
class BasicProductsResource(Resource):
    @inject.autoparams('get_all_minimum_orders')
    def __init__(self, api: None, get_all_minimum_orders: GetMinimumOrders):
        self.api = api
        self.get_all_minimum_orders = get_all_minimum_orders

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        result = self.get_all_minimum_orders.execute()
        return json.loads(result.json()), 200
