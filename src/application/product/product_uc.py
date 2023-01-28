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

import inject

from src.domain.entities.basic_product_entity import BasicProductsListEntity
from src.domain.entities.common_entity import BasicEntity
from src.domain.entities.incoterm_entity import IncotermsListEntity
from src.domain.entities.minimum_order_entity import MinimumOrderListEntity
from src.domain.entities.product_entity import ProductNewEntity, ProductEntity, ProductsPaginationEntity, \
    AvailabilityEntity, ProductFilterSellerEntity, ProductFilterBuyerEntity, ProductsListEntity, \
    ProductFilterSellerBasicProductEntity, ProductFilterBuyerBasicProductEntity
from src.domain.entities.product_type_entity import ProductTypesListEntity
from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationsListEntity
from src.domain.entities.variety_entity import VarietiesListEntity
from src.domain.ports.product_interface import IProductRepository


#
# These classes lets define the product user cases.
# @author David Córdoba
#


class CreateProduct:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, jwt: str, product_entity: ProductNewEntity,
                objects_cloud: list, images: list) -> ProductEntity:
        return self.__product_repository.new_product(jwt, product_entity, objects_cloud, images)


class GetProduct:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, uuid: str) -> ProductEntity:
        return self.__product_repository.get_product_by_uuid(uuid)
    

class GetAllProducts:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, limit: int, offset: int) -> ProductsPaginationEntity:
        return self.__product_repository.get_all_products(limit, offset)


class GetProductsByUser:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, uuid: str, roles: list, limit: int, offset: int) -> ProductsPaginationEntity:
        return self.__product_repository.get_products_by_user(uuid, roles, limit, offset)


class GetProductsBuyerByCategory:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, uuid: str, roles: list, basic_product:str, limit: int, offset: int) -> ProductsPaginationEntity:
        return self.__product_repository.get_products_user_by_category(uuid, roles, basic_product, limit, offset)


class GetAllBasicProducts:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self) -> BasicProductsListEntity:
        return self.__product_repository.get_all_basic_products()


class GetProductTypes:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, uuid: str) -> ProductTypesListEntity:
        return self.__product_repository.get_products_type_by_uuid_basic_product(uuid)


class GetVarieties:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, uuid: str) -> VarietiesListEntity:
        return self.__product_repository.get_varieties_by_uuid_basic_product(uuid)


class GetSustainabilityCertifications:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self) -> SustainabilityCertificationsListEntity:
        return self.__product_repository.get_all_sustainability_certifications()


class GetInconterms:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self) -> IncotermsListEntity:
        return self.__product_repository.get_all_incoterms()


class GetMinimumOrders:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self) -> MinimumOrderListEntity:
        return self.__product_repository.get_all_minimum_order()


class GetProductStates:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self) -> BasicEntity:
        return self.__product_repository.product_states()


class EditProductAvailability:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, entity: AvailabilityEntity) -> AvailabilityEntity:
        return self.__product_repository.edit_product_availability(entity)


class GetDetailProduct:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, uuid: str) -> ProductEntity:
        return self.__product_repository.get_detail_product_by_uuid(uuid)


class EditStateProduct:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, state: str, uuid: str, transaction_id: str = None) -> ProductEntity:
        return self.__product_repository.edit_product_state(state, uuid, transaction_id)


class EditProduct:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, jwt: str, uuid_product: str, product_entity: ProductNewEntity,
                objects_cloud: list, images: list) -> ProductEntity:
        return self.__product_repository.edit_product(jwt, uuid_product, product_entity, objects_cloud, images)


class GetProductsFilterSeller:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, product_filter_seller_entity: ProductFilterSellerEntity) -> ProductsListEntity:
        return self.__product_repository.get_products_filter_seller(product_filter_seller_entity)


class GetProductsFilterBuyer:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, product_filter_buyer_entity: ProductFilterBuyerEntity) -> ProductsPaginationEntity:
        return self.__product_repository.get_products_filter_buyer(product_filter_buyer_entity)


class GetProductsFilterSellerAndBasicProduct:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, product_filter_seller_basic_product_entity: ProductFilterSellerBasicProductEntity) \
            -> ProductsListEntity:
        return self.__product_repository.get_products_filter_seller_basic_product(
            product_filter_seller_basic_product_entity)


class GetProductsFilterBuyerAndBasicProduct:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, product_filter_buyer_basic_product_entity: ProductFilterBuyerBasicProductEntity) \
            -> ProductsPaginationEntity:
        return self.__product_repository.get_products_filter_buyer_basic_product(
            product_filter_buyer_basic_product_entity)


class GetProductsFilterSellerSearchBar:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, search_bar_filter: ProductFilterSellerBasicProductEntity) \
            -> ProductsListEntity:
        return self.__product_repository.get_products_filter_seller_search_bar(search_bar_filter)


class GetProductsFilterBuyerSearchBar:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, search_bar_filter: ProductFilterBuyerBasicProductEntity) \
            -> ProductsPaginationEntity:
        return self.__product_repository.get_products_filter_buyer_search_bar(search_bar_filter)
