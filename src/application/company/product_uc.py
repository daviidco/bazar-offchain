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

from src.domain.entities.product_entity import ProductNewEntity, ProductEntity, ProductsPaginationEntity
from src.domain.ports.product_interface import IProductRepository


#
# These classes lets define the product user cases.
# @author David Córdoba
#


class CreateProduct:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, role: str, product_entity: ProductNewEntity, objects_cloud: list, images: list) -> ProductEntity:
        return self.__product_repository.new_product(role, product_entity, objects_cloud, images)


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

    def execute(self, uuid: str) -> ProductsPaginationEntity:
        return self.__product_repository.get_products_by_user(uuid)


class GetAllBasicProducts:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self) -> ProductEntity:
        return self.__product_repository.get_all_basic_products()


class GetProductTypes:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, uuid: str) -> ProductEntity:
        return self.__product_repository.get_products_type_by_uuid_basic_product(uuid)

class GetVarieties:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self, uuid: str) -> ProductEntity:
        return self.__product_repository.get_varieties_by_uuid_basic_product(uuid)


class GetSustainabilityCertifications:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self) -> ProductEntity:
        return self.__product_repository.get_all_sustainability_certifications()


class GetInconterms:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self) -> ProductEntity:
        return self.__product_repository.get_all_incoterms()


class GetMinimumOrders:
    @inject.autoparams('product_repository')
    def __init__(self, product_repository: IProductRepository):
        self.__product_repository = product_repository

    def execute(self) -> ProductEntity:
        return self.__product_repository.get_all_minimum_order()


