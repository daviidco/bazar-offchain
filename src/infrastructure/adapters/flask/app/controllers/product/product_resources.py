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
import typing

import inject
from flask import current_app
from flask_cors import cross_origin
from flask_restx import Resource, Namespace, reqparse
from flask_restx.reqparse import request
from werkzeug.datastructures import FileStorage

from src.application.product.product_uc import GetAllBasicProducts, GetProductTypes, GetVarieties, \
    GetSustainabilityCertifications, GetInconterms, GetMinimumOrders, CreateProduct, \
    GetAllProducts, GetProductsByUser, GetProductStates, EditProductAvailability, GetDetailProduct, EditStateProduct
from src.domain.entities.basic_product_entity import BasicProductsListEntity
from src.domain.entities.common_entity import InputPaginationEntity, BasicEntity
from src.domain.entities.incoterm_entity import IncotermsListEntity
from src.domain.entities.minimum_order_entity import MinimumOrderListEntity
from src.domain.entities.product_entity import ProductNewEntity, AvailabilityEntity, ProductEntity, \
    ProductsPaginationEntity, ProductEditEntity
from src.domain.entities.product_type_entity import ProductTypesListEntity
from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationsListEntity
from src.domain.entities.variety_entity import VarietiesListEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth
from src.infrastructure.adapters.flask.app.utils.ultils import get_help_schema, get_schema, is_valid_uuid_input
from tests.utils import generate_data_entity

#
# This file contains the products endpoints Api-rest
# @author David Córdoba
#

api = Namespace("products", description="Product controller", path='/api/v1/products')


@api.route("/")
class ProductResource(Resource):
    # Swagger
    response_schema_get = ProductsPaginationEntity.schema()
    response_model_get = api.schema_model(response_schema_get['title'], response_schema_get)
    success_code_get = 200

    response_schema_post = ProductEntity.schema()
    response_model_post = api.schema_model(response_schema_post['title'], response_schema_post)
    success_code_post = 201

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
    def __init__(self, app: current_app, get_all_products: GetAllProducts, create_product: CreateProduct, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_all_products = get_all_products
        self.create_product = create_product

    @api.doc(params=get_schema(InputPaginationEntity), security='Private JWT')
    @api.response(success_code_get, 'Success', response_model_get)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets  all products with pagination"""
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        result = self.get_all_products.execute(limit, offset)
        return json.loads(result.json()), self.success_code_get

    @api.expect(upload_parser)
    @api.doc(security='Private JWT')
    @api.response(success_code_post, 'Success', response_model_post)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def post(self, *args, **kwargs):
        """Creates a new product"""
        jwt = dict(request.headers).get('Authorization', None)
        role = kwargs.get('role', None)
        entity = ProductNewEntity.parse_obj(json.loads(request.form['body']))
        files = request.files.getlist('files[]')
        images = request.files.getlist('images[]')
        result = self.create_product.execute(jwt, role, entity, files, images)
        return json.loads(result.json()), self.success_code_post


@api.route("/products-user/<string:user_uuid>")
@api.route("/feed/<string:user_uuid>")
class ProductsByUserResource(Resource):
    # Swagger
    response_schema = ProductsPaginationEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products')
    def __init__(self, app: current_app, get_products: GetProductsByUser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products = get_products

    @api.doc(params=get_schema(InputPaginationEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def get(self, user_uuid, *args, **kwargs):
        """Gets all user's products by the user uuid. if user is buyer will try to list all products"""
        role = kwargs.get('role', None)
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        is_valid_uuid_input(user_uuid)
        result = self.get_products.execute(user_uuid, role, limit, offset)
        return json.loads(result.json()), self.success_code


@api.route("/basic-products")
class BasicProductsResource(Resource):
    # Swagger
    response_schema = BasicProductsListEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_all_basic_products')
    def __init__(self, app: current_app, get_all_basic_products: GetAllBasicProducts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_all_basic_products = get_all_basic_products

    @api.doc(security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all basic products"""
        result = self.get_all_basic_products.execute()
        return json.loads(result.json()), self.success_code


@api.route("/product-types/<string:uuid_basic_product>")
class ProductTypesResource(Resource):
    # Swagger
    response_schema = ProductTypesListEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products_type_by_uuid_basic_product')
    def __init__(self, app: current_app, get_products_type_by_uuid_basic_product: GetProductTypes, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products_type_by_uuid_basic_product = get_products_type_by_uuid_basic_product

    @api.doc(security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def get(self, uuid_basic_product, *args, **kwargs):
        """Gets all product types"""
        is_valid_uuid_input(uuid_basic_product)
        result = self.get_products_type_by_uuid_basic_product.execute(uuid_basic_product)
        return json.loads(result.json()), self.success_code


@api.route("/varieties/<string:uuid_basic_product>")
class VarietiesResource(Resource):
    # Swagger
    response_schema = VarietiesListEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_varieties_by_uuid_basic_product')
    def __init__(self, app: current_app, get_varieties_by_uuid_basic_product: GetVarieties, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_varieties_by_uuid_basic_product = get_varieties_by_uuid_basic_product

    @api.doc(security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def get(self, uuid_basic_product, *args, **kwargs):
        """Gets all varieties"""
        is_valid_uuid_input(uuid_basic_product)
        result = self.get_varieties_by_uuid_basic_product.execute(uuid_basic_product)
        return json.loads(result.json()), self.success_code


@api.route("/sustainability-certifications")
class SustainabilityCertificationsResource(Resource):
    # Swagger
    response_schema = SustainabilityCertificationsListEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_all_sustainability_certifications')
    def __init__(self, app: current_app, get_all_sustainability_certifications: GetSustainabilityCertifications, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_all_sustainability_certifications = get_all_sustainability_certifications

    @api.doc(security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all sustainability certifications"""
        result = self.get_all_sustainability_certifications.execute()
        return json.loads(result.json()), self.success_code


@api.route("/incoterms")
class IncotermsResource(Resource):
    # Swagger
    response_schema = IncotermsListEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_all_incoterms')
    def __init__(self, app: current_app, get_all_incoterms: GetInconterms, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_all_incoterms = get_all_incoterms

    @api.doc(security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all incoterms"""
        result = self.get_all_incoterms.execute()
        return json.loads(result.json()), self.success_code


@api.route("/minimum-orders")
class MinimumOrdersResource(Resource):
    # Swagger
    response_schema = MinimumOrderListEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_all_minimum_orders')
    def __init__(self, app: current_app, get_all_minimum_orders: GetMinimumOrders, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_all_minimum_orders = get_all_minimum_orders

    @api.doc(security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all minimum orders"""
        result = self.get_all_minimum_orders.execute()
        return json.loads(result.json()), self.success_code


@api.route("/products-states")
class ProductStatesResource(Resource):
    # Swagger
    response_schema = BasicEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_product_states')
    def __init__(self, app: current_app, get_product_states: GetProductStates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_product_states = get_product_states

    @api.doc(security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        """Gets all product states"""
        result = self.get_product_states.execute()
        return json.loads(result.json()), self.success_code


@api.route("/availability")
class ProductAvailabilityEditResource(Resource):
    # Swagger
    response_schema = AvailabilityEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('edit_product_availability')
    def __init__(self, app: current_app, edit_product_availability: EditProductAvailability, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.edit_product_availability = edit_product_availability

    @api.doc(params=get_schema(AvailabilityEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def patch(self, *args, **kwargs):
        """Update product availability for sale"""
        entity = AvailabilityEntity.parse_obj(request.args)
        result = self.edit_product_availability.execute(entity)
        return json.loads(result.json()), self.success_code


@api.route("/detail/<string:uuid_product>")
class ProductDetailResource(Resource):
    # Swagger
    response_schema = ProductEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_detail_by_uuid_product')
    def __init__(self, app: current_app, get_detail_by_uuid_product: GetDetailProduct, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_detail_by_uuid_product = get_detail_by_uuid_product

    @api.doc(security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def get(self, uuid_product, *args, **kwargs):
        """Gets product detail of a specific product by product uuid"""
        is_valid_uuid_input(uuid_product)
        result = self.get_detail_by_uuid_product.execute(uuid_product)
        return json.loads(result.json()), self.success_code


@api.route("/update-hidden/<string:uuid_product>")
class ProductHiddenResource(Resource):
    # Swagger
    response_schema = ProductEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('edit_product_state')
    def __init__(self, app: current_app, edit_product_state: EditStateProduct, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.edit_product_state = edit_product_state

    @api.doc(security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def patch(self, uuid_product, *args, **kwargs):
        """Updates state product to hidden"""
        state = 'Hide'
        is_valid_uuid_input(uuid_product)
        result = self.edit_product_state.execute(state, uuid_product)
        return json.loads(result.json()), self.success_code


@api.route("/update-public/<string:uuid_product>")
@api.route("/update-approve/<string:uuid_product>")
class ProductPublicResource(Resource):
    # Swagger
    response_schema = ProductEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('edit_product_state')
    def __init__(self, app: current_app, edit_product_state: EditStateProduct, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.edit_product_state = edit_product_state

    @api.doc(security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def patch(self, uuid_product, *args, **kwargs):
        """Updates state product to public"""
        state = 'Approved'
        is_valid_uuid_input(uuid_product)
        result = self.edit_product_state.execute(state, uuid_product)
        return json.loads(result.json()), self.success_code


@api.route("/update-delete/<string:uuid_product>")
class ProductDeleteResource(Resource):
    # Swagger
    response_schema = typing.get_type_hints(EditStateProduct.execute)['return'].schema()
    example = generate_data_entity(ProductEntity)
    response_schema['example'] = example
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('edit_product_state')
    def __init__(self, app: current_app, edit_product_state: EditStateProduct, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.edit_product_state = edit_product_state

    @api.doc(security='Private JWT', responses={403: 'Not Authorized'})
    @api.response(success_code, 'Success', response_model)
    @cross_origin(["Content-Type", "Authorization"])
    @requires_auth
    def patch(self, uuid_product, *args, **kwargs):
        """Updates state product to delete"""
        state = 'Deleted'
        is_valid_uuid_input(uuid_product)
        result = self.edit_product_state.execute(state, uuid_product)
        return json.loads(result.json()), self.success_code
