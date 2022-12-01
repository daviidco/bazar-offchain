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
    AvailabilityEntity
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

    def execute(self, jwt: str, role: str, product_entity: ProductNewEntity,
                objects_cloud: list, images: list) -> ProductEntity:
        return self.__product_repository.new_product(jwt, role, product_entity, objects_cloud, images)


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

    def execute(self, uuid: str, role: str, limit: int, offset: int) -> ProductsPaginationEntity:
        return self.__product_repository.get_products_by_user(uuid, role, limit, offset)


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
