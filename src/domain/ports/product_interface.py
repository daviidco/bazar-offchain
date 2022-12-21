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

from abc import ABC, abstractmethod
from typing import Union

from src.domain.entities.basic_product_entity import BasicProductsListEntity, BasicProductEntity
from src.domain.entities.common_entity import BasicEntity
from src.domain.entities.incoterm_entity import IncotermsListEntity
from src.domain.entities.minimum_order_entity import MinimumOrderEntity, MinimumOrderListEntity
from src.domain.entities.product_entity import ProductNewEntity, ProductEntity, ProductsPaginationEntity, \
    AvailabilityEntity, ProductsListEntity, ProductFilterSellerEntity, ProductFilterBuyerEntity
from src.domain.entities.product_type_entity import ProductTypesListEntity, ProductTypeEntity
from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationsListEntity
from src.domain.entities.variety_entity import VarietiesListEntity, VarietyEntity


#
# This interface or port lets define the methods to implement by basic_product_repository.
# @author David Córdoba
#

class IProductRepository(ABC):

    @abstractmethod
    def new_product(self, jwt: str, role: str, product_entity: ProductNewEntity,
                    objects_cloud: list, images: list) -> ProductEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_product_by_uuid(self, uuid: str) -> ProductEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_products_count(self) -> int:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_all_products(self, limit: int, offset: int) -> ProductsPaginationEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_products_by_user(self, uuid: str, role: str, limit: int, offset: int) -> Union[ProductsPaginationEntity,
                                                                                           ProductsListEntity]:
        raise Exception('Not implemented method')

    # ComboBox
    @abstractmethod
    def get_all_basic_products(self) -> BasicProductsListEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_products_type_by_uuid_basic_product(self, uuid: str) -> ProductTypesListEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_varieties_by_uuid_basic_product(self, uuid: str) -> VarietiesListEntity:
        raise Exception('Not implemented method')

    # Dynamics checkbox

    @abstractmethod
    def get_all_sustainability_certifications(self) -> SustainabilityCertificationsListEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_all_incoterms(self) -> IncotermsListEntity:
        raise Exception('Not implemented method')

    def get_all_minimum_order(self) -> MinimumOrderListEntity:
        raise Exception('Not implemented method')

    # Get entities by id
    @abstractmethod
    def get_basic_product_by_uuid(self, uuid: str) -> BasicProductEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_product_type_by_uuid(self, uuid: str) -> ProductTypeEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_variety_by_uuid(self, uuid: str) -> VarietyEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_minimum_order_by_uuid(self, uuid: str) -> MinimumOrderEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def product_states(self) -> BasicEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def edit_product_availability(self, entity: AvailabilityEntity) -> AvailabilityEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_detail_product_by_uuid(self, uuid: str) -> ProductEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def edit_product_state(self, status: str, uuid: str) -> ProductEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def edit_product(self, jwt: str, role: str, uuid_product: str, product_entity: ProductNewEntity,
                     objects_cloud: list, images: list) -> ProductEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_products_filter_seller(self, filter_entity: ProductFilterSellerEntity):
        raise Exception('Not implemented method')

    @abstractmethod
    def get_products_filter_buyer(self, filter_entity: ProductFilterBuyerEntity):
        raise Exception('Not implemented method')

