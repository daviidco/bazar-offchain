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
from flask_restx import Resource, Namespace, reqparse
from flask_restx.reqparse import request
from werkzeug.datastructures import FileStorage

from src.application.product.product_uc import GetAllBasicProducts, GetProductTypes, GetVarieties, \
    GetSustainabilityCertifications, GetInconterms, GetMinimumOrders, CreateProduct, \
    GetAllProducts, GetProductsByUser, GetProductStates, EditProductAvailability, GetDetailProduct, EditStateProduct
from src.domain.entities.common_entity import InputPaginationEntity
from src.domain.entities.product_entity import ProductNewEntity, AvailabilityEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth
from src.infrastructure.adapters.flask.app.utils.ultils import get_help_schema, get_schema

#
# This file contains the products endpoints Api-rest
# @author David Córdoba
#

api = Namespace("products", description="Product controller", path='/api/v1/products')


@api.route("/")
class ProductResource(Resource):

    help_new_product = get_help_schema(ProductNewEntity)

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

    @api.doc(params=get_schema(InputPaginationEntity), security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets  all products with pagination"""
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        result = self.get_all_products.execute(limit, offset)
        return json.loads(result.json()), 200

    @api.expect(upload_parser)
    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def post(self, *args, **kwargs):
        """Creates a new product"""
        jwt = dict(request.headers).get('Authorization', None)
        role = kwargs.get('role', None)
        entity = ProductNewEntity.parse_obj(json.loads(request.form['body']))
        files = request.files.getlist('files[]')
        images = request.files.getlist('images[]')
        result = self.create_product.execute(jwt, role, entity, files, images)
        return json.loads(result.json()), 201


@api.route("/products-user/<string:user_uuid>")
@api.route("/feed/<string:user_uuid>")
class ProductsByUserResource(Resource):
    @inject.autoparams('get_products')
    def __init__(self, api: None, get_products: GetProductsByUser):
        self.api = api
        self.get_products = get_products

    @api.doc(params=get_schema(InputPaginationEntity), security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, user_uuid, *args, **kwargs):
        """Gets all user's products by the user uuid. if user is buyer will try to list all products"""
        role = kwargs.get('role', None)
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        result = self.get_products.execute(user_uuid, role, limit, offset)
        return json.loads(result.json()), 200


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
        """Gets all basic products"""
        result = self.get_all_basic_products.execute()
        return json.loads(result.json()), 200


@api.route("/product-types/<string:uuid_basic_product>")
class ProductTypesResource(Resource):
    @inject.autoparams('get_products_type_by_uuid_basic_product')
    def __init__(self, api: None, get_products_type_by_uuid_basic_product: GetProductTypes):
        self.api = api
        self.get_products_type_by_uuid_basic_product = get_products_type_by_uuid_basic_product

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, uuid_basic_product, *args, **kwargs):
        """Gets all product types"""
        result = self.get_products_type_by_uuid_basic_product.execute(uuid_basic_product)
        return json.loads(result.json()), 200


@api.route("/varieties/<string:uuid_basic_product>")
class VarietiesResource(Resource):
    @inject.autoparams('get_varieties_by_uuid_basic_product')
    def __init__(self, api: None, get_varieties_by_uuid_basic_product: GetVarieties):
        self.api = api
        self.get_varieties_by_uuid_basic_product = get_varieties_by_uuid_basic_product

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, uuid_basic_product, *args, **kwargs):
        """Gets all varieties"""
        result = self.get_varieties_by_uuid_basic_product.execute(uuid_basic_product)
        return json.loads(result.json()), 200


@api.route("/sustainability-certifications")
class SustainabilityCertificationsResource(Resource):
    @inject.autoparams('get_all_sustainability_certifications')
    def __init__(self, api: None, get_all_sustainability_certifications: GetSustainabilityCertifications, *args, **kwargs):
        self.api = api
        self.get_all_sustainability_certifications = get_all_sustainability_certifications

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all sustainability certifications"""
        result = self.get_all_sustainability_certifications.execute()
        return json.loads(result.json()), 200


@api.route("/incoterms")
class IncotermsResource(Resource):
    @inject.autoparams('get_all_incoterms')
    def __init__(self, api: None, get_all_incoterms: GetInconterms):
        self.api = api
        self.get_all_incoterms = get_all_incoterms

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all incoterms"""
        result = self.get_all_incoterms.execute()
        return json.loads(result.json()), 200


@api.route("/minimum-orders")
class MinimumOrdersResource(Resource):
    @inject.autoparams('get_all_minimum_orders')
    def __init__(self, api: None, get_all_minimum_orders: GetMinimumOrders):
        self.api = api
        self.get_all_minimum_orders = get_all_minimum_orders

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all minimum orders"""
        result = self.get_all_minimum_orders.execute()
        return json.loads(result.json()), 200


@api.route("/products-states")
class ProductStatesResource(Resource):

    @inject.autoparams('get_product_states')
    def __init__(self, api: None, get_product_states: GetProductStates):
        self.api = api
        self.get_product_states = get_product_states

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all product states"""
        result = self.get_product_states.execute()
        return json.loads(result.json()), 200


@api.route("/availability")
class ProductsByUserResource(Resource):

    @inject.autoparams('edit_product_availability')
    def __init__(self, api: None, edit_product_availability: EditProductAvailability):
        self.api = api
        self.edit_product_availability = edit_product_availability

    @api.doc(params=get_schema(AvailabilityEntity), security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def patch(self, *args, **kwargs):
        """Update product availability for sale"""
        entity = AvailabilityEntity.parse_obj(request.args)
        result = self.edit_product_availability.execute(entity)
        return json.loads(result.json()), 200


@api.route("/detail/<string:uuid_product>")
class ProductDetailResource(Resource):
    @inject.autoparams('get_detail_by_uuid_product')
    def __init__(self, api: None, get_detail_by_uuid_product: GetDetailProduct):
        self.api = api
        self.get_detail_by_uuid_product = get_detail_by_uuid_product

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, uuid_product, *args, **kwargs):
        """Gets product detail of a specific product by product uuid"""
        result = self.get_detail_by_uuid_product.execute(uuid_product)
        return json.loads(result.json()), 200


@api.route("/update-hidden/<string:uuid_product>")
class ProductHiddenResource(Resource):
    @inject.autoparams('edit_product_state')
    def __init__(self, api: None, edit_product_state: EditStateProduct):
        self.api = api
        self.edit_product_state = edit_product_state

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def patch(self, uuid_product, *args, **kwargs):
        """Updates state product to hidden"""
        state = 'Hide'
        result = self.edit_product_state.execute(state, uuid_product)
        return json.loads(result.json()), 200


@api.route("/update-public/<string:uuid_product>")
@api.route("/update-approve/<string:uuid_product>")
class ProductPublicResource(Resource):
    @inject.autoparams('edit_product_state')
    def __init__(self, api: None, edit_product_state: EditStateProduct):
        self.api = api
        self.edit_product_state = edit_product_state

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def patch(self, uuid_product, *args, **kwargs):
        """Updates state product to public"""
        state = 'Approved'
        result = self.edit_product_state.execute(state, uuid_product)
        return json.loads(result.json()), 200


@api.route("/update-delete/<string:uuid_product>")
class ProductDeleteResource(Resource):
    @inject.autoparams('edit_product_state')
    def __init__(self, api: None, edit_product_state: EditStateProduct):
        self.api = api
        self.edit_product_state = edit_product_state

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def patch(self, uuid_product, *args, **kwargs):
        """Updates state product to delete"""
        state = 'Deleted'
        result = self.edit_product_state.execute(state, uuid_product)
        return json.loads(result.json()), 200
