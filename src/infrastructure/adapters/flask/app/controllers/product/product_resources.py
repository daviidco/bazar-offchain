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
    GetAllProducts, GetProductsByUser, GetProductStates, EditProductAvailability, GetDetailProduct, EditStateProduct, \
    EditProduct, GetProductsFilterSeller, GetProductsFilterBuyer, GetProductsFilterSellerAndBasicProduct, \
    GetProductsFilterBuyerAndBasicProduct, GetProductsFilterBuyerSearchBar, GetProductsFilterSellerSearchBar
from src.domain.entities.basic_product_entity import BasicProductsListEntity
from src.domain.entities.common_entity import InputPaginationEntity, BasicEntity
from src.domain.entities.incoterm_entity import IncotermsListEntity
from src.domain.entities.minimum_order_entity import MinimumOrderListEntity
from src.domain.entities.product_entity import ProductNewEntity, AvailabilityEntity, ProductEntity, \
    ProductsPaginationEntity, ProductEditEntity, ProductFilterSellerEntity, ProductFilterBuyerEntity, \
    ProductsListEntity, ProductFilterBuyerBasicProductEntity, ProductFilterSellerBasicProductEntity
from src.domain.entities.product_type_entity import ProductTypesListEntity
from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationsListEntity
from src.domain.entities.variety_entity import VarietiesListEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth
from src.infrastructure.adapters.flask.app.utils.ultils import get_help_schema, get_schema, is_valid_uuid_input, \
    compare_nums
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

    upload_parser.add_argument('images[]', location='files',
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
    @requires_auth
    def patch(self, uuid_product, *args, **kwargs):
        """Updates state product to delete"""
        state = 'Deleted'
        is_valid_uuid_input(uuid_product)
        result = self.edit_product_state.execute(state, uuid_product)
        return json.loads(result.json()), self.success_code


@api.route("/update-product/<string:uuid_product>")
class ProductEditResource(Resource):
    # Swagger
    response_schema_put = ProductEntity.schema()
    response_model_put = api.schema_model(response_schema_put['title'], response_schema_put)
    success_code_put = 200

    help_new_product = get_help_schema(ProductEditEntity)

    # Object to upload file and json body in form data
    upload_parser = reqparse.RequestParser()
    upload_parser.add_argument('files[]', location='files',
                               type=FileStorage, action='append', help='Product Files')

    upload_parser.add_argument('images[]', location='files',
                               type=FileStorage, action='append', help='Product Images')

    upload_parser.add_argument('body', location='form',
                               type=dict, required=False, help='Product Information \n' + help_new_product)

    @inject.autoparams('edit_product')
    def __init__(self, app: current_app, edit_product: EditProduct, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.edit_product = edit_product

    @api.expect(upload_parser)
    @api.doc(security='Private JWT', responses={403: 'Not Authorized'})
    @api.response(success_code_put, 'Success', response_model_put)
    @requires_auth
    def put(self, uuid_product, **kwargs):
        """Updates product. This endpoint has two important boolean keys (change_files, change_images)
        when one is true delete relationships and delete object from cloud repository respectively.

        It is not necessary upload old files when change_files is false
        It is not necessary upload old images when change_images is false

        When the request has a certification (file) will be sent email to bazar admin and product state will be
        (pending review)

        When the request has not a certification (file) product state will be (hidden)"""
        jwt = dict(request.headers).get('Authorization', None)
        role = kwargs.get('role', None)
        entity = ProductEditEntity.parse_obj(json.loads(request.form['body']))
        files = request.files.getlist('files[]')
        images = request.files.getlist('images[]')
        is_valid_uuid_input(uuid_product)
        result = self.edit_product.execute(jwt, role, uuid_product, entity, files, images)
        return json.loads(result.json()), self.success_code_put


@api.route("/filter-seller")
class ProductFilterSellerResource(Resource):
    # Swagger
    response_schema = ProductsListEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products_filter_seller')
    def __init__(self, app: current_app, get_products_filter_seller: GetProductsFilterSeller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products_filter_seller = get_products_filter_seller

    @api.doc(params=get_schema(ProductFilterSellerEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @requires_auth
    def get(self, *args, **kwargs):
        """Filter to products by seller"""
        user_uuid = request.args.get("user_uuid", 0)
        is_valid_uuid_input(user_uuid)
        price_per_kg_start = request.args.get("price_per_kg_start", 0)
        price_per_kg_end = request.args.get("price_per_kg_end", 0)
        compare_nums(price_per_kg_start, price_per_kg_end, '<')
        available_for_sale = request.args.get("available_for_sale", 0)

        entity = ProductFilterSellerEntity(price_per_kg_start=price_per_kg_start,
                                           price_per_kg_end=price_per_kg_end,
                                           available_for_sale=available_for_sale,
                                           user_uuid=user_uuid)

        result = self.get_products_filter_seller.execute(entity)
        return json.loads(result.json()), self.success_code


@api.route("/filter-buyer")
class ProductFilterBuyerResource(Resource):
    # Swagger
    response_schema = ProductsPaginationEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products_filter_buyer')
    def __init__(self, app: current_app, get_products_filter_buyer: GetProductsFilterBuyer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products_filter_buyer = get_products_filter_buyer

    @api.doc(params=get_schema(ProductFilterBuyerEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @requires_auth
    def get(self, *args, **kwargs):
        """Filter to products by buyer"""
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        price_per_kg_start = request.args.get("price_per_kg_start", 0)
        price_per_kg_end = request.args.get("price_per_kg_end", 0)
        available_for_sale = request.args.get("available_for_sale", 0)

        entity = ProductFilterBuyerEntity(limit=limit,
                                          offset=offset,
                                          price_per_kg_start=price_per_kg_start,
                                          price_per_kg_end=price_per_kg_end,
                                          available_for_sale=available_for_sale)
        result = self.get_products_filter_buyer.execute(entity)
        return json.loads(result.json()), self.success_code


@api.route("/filter-seller/basic-product")
class ProductFilterSellerBasicProductResource(Resource):
    # Swagger
    response_schema = ProductsListEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products_filter_seller_basic_product')
    def __init__(self, app: current_app,
                 get_products_filter_seller_basic_product: GetProductsFilterSellerAndBasicProduct,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products_filter_seller_basic_product = get_products_filter_seller_basic_product

    @api.doc(params=get_schema(ProductFilterSellerBasicProductEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @requires_auth
    def get(self, *args, **kwargs):
        """Filter to products by uuid seller and by name basic product"""
        user_uuid = request.args.get("user_uuid", 0)
        is_valid_uuid_input(user_uuid)
        basic_product = request.args.get("basic_product", 0)
        entity = ProductFilterSellerBasicProductEntity(user_uuid=user_uuid,
                                                       basic_product=basic_product,)
        result = self.get_products_filter_seller_basic_product.execute(entity)
        return json.loads(result.json()), self.success_code


@api.route("/filter-buyer/basic-product")
class ProductFilterBuyerBasicProductResource(Resource):
    # Swagger
    response_schema = ProductsPaginationEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products_filter_buyer_basic_product')
    def __init__(self, app: current_app,
                 get_products_filter_buyer_basic_product: GetProductsFilterBuyerAndBasicProduct,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products_filter_buyer_basic_product = get_products_filter_buyer_basic_product

    @api.doc(params=get_schema(ProductFilterBuyerBasicProductEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @requires_auth
    def get(self, *args, **kwargs):
        """Filter to products by name basic product to buyers"""
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


@api.route("/filter-seller/search-bar")
class ProductFilterSellerSearchBar(Resource):
    # Swagger
    response_schema = ProductsListEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products_filter_seller_search_bar')
    def __init__(self, app: current_app,
                 get_products_filter_seller_search_bar: GetProductsFilterSellerSearchBar,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products_filter_seller_search_bar = get_products_filter_seller_search_bar

    @api.doc(params=get_schema(ProductFilterSellerBasicProductEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @requires_auth
    def get(self, *args, **kwargs):
        """Filter to products by uuid seller and by part name basic product.
        It doesn't matter if part name is uppercase or lowercase."""
        user_uuid = request.args.get("user_uuid", 0)
        is_valid_uuid_input(user_uuid)
        basic_product = request.args.get("basic_product", 0)
        entity = ProductFilterSellerBasicProductEntity(user_uuid=user_uuid,
                                                       basic_product=basic_product,)
        result = self.get_products_filter_seller_search_bar.execute(entity)
        return json.loads(result.json()), self.success_code


@api.route("/filter-buyer/search-bar")
class ProductFilterBuyerSearchBar(Resource):
    # Swagger
    response_schema = ProductsPaginationEntity.schema()
    response_model = api.schema_model(response_schema['title'], response_schema)
    success_code = 200

    @inject.autoparams('get_products_filter_buyer_search_bar')
    def __init__(self, app: current_app,
                 get_products_filter_buyer_search_bar: GetProductsFilterBuyerSearchBar,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = app
        self.get_products_filter_buyer_search_bar = get_products_filter_buyer_search_bar

    @api.doc(params=get_schema(ProductFilterBuyerBasicProductEntity), security='Private JWT')
    @api.response(success_code, 'Success', response_model)
    @requires_auth
    def get(self, *args, **kwargs):
        """Filter to products by part of name basic product to buyers.
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
