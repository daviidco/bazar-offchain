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
from flask_restx import Resource, Namespace, reqparse
from flask_restx.reqparse import request
from werkzeug.datastructures import FileStorage

from src.application.company.product_uc import GetAllBasicProducts, GetProductTypes, GetVarieties, \
    GetSustainabilityCertifications, GetInconterms, GetMinimumOrders, CreateProduct, GetAllProducts
from src.domain.entities.common_entity import JwtEntity, InputPaginationEntity
from src.domain.entities.product_entity import ProductNewEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth
from src.infrastructure.adapters.flask.app.utils.ultils import get_schema_and_type

#
# This file contains the products endpoints Api-rest
# @author David Córdoba
#

api = Namespace("products", description="Product controller", path='/api/v1/products')


@api.route("/")
class ProductResource(Resource):
    schema = InputPaginationEntity.schema()

    schema_product = ProductNewEntity.schema()
    model = api.schema_model("ProductNewEntity", schema_product)
    help_new_product = json.dumps(get_schema_and_type(schema_product), indent=2)

    # Object to upload file and json body in form data
    upload_parser = reqparse.RequestParser()
    upload_parser.add_argument('files[]', location='files',
                               type=FileStorage, action='append', help='Product Files')

    upload_parser.add_argument('images[]', location='images',
                               type=FileStorage, action='append', help='Product Images')

    upload_parser.add_argument('body', location='form',
                               type=dict, required=False, help='Product Information \n' + help_new_product)

    @inject.autoparams('get_all_products', 'create_product')
    def __init__(self, api:None, get_all_products: GetAllProducts, create_product: CreateProduct):
        self.api = api
        self.get_all_products = get_all_products
        self.create_product = create_product

    @api.doc(params=schema['properties'], security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 1)
        result = self.get_all_products.execute(limit, offset)
        return json.loads(result.json()), 200

    @api.expect(upload_parser)
    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def post(self, *args, **kwargs):
        role = kwargs['role']
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

    @api.doc(security='Private JWT')
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

    @api.doc(security='Private JWT')
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

    @api.doc(security='Private JWT')
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

    @api.doc(security='Private JWT')
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

    @api.doc(security='Private JWT')
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

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        result = self.get_all_minimum_orders.execute()
        return json.loads(result.json()), 200
