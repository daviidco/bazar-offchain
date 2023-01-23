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

from src.domain.entities.product_entity import ProductsPaginationEntity, ProductFilterBuyerBasicProductEntity, \
    ProductFilterBuyerEntity
from src.domain.entities.wishlist_entity import WishProductNewEntity, WishProductEntity


#
# This interface or port lets define the methods to implement by wishlist_repository.
# @author David Córdoba
#
class IWishListRepository(ABC):

    @abstractmethod
    def new_product_on_wishlist(self, wish_product_entity: WishProductNewEntity) -> WishProductEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def delete_product_from_wishlist(self, wish_product_entity: WishProductNewEntity):
        raise Exception('Not implemented method')

    @abstractmethod
    def get_wishlist_by_uuid_buyer(self, uuid: str, limit: int, offset: int) -> ProductsPaginationEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_wishlist_by_uuid_buyer_and_basic_product(self, filter_entity: ProductFilterBuyerBasicProductEntity) \
            -> ProductsPaginationEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_wishlist_by_uuid_buyer_and_search_bar(self, filter_entity: ProductFilterBuyerBasicProductEntity) \
            -> ProductsPaginationEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_wishlist_filter(self, filter_entity: ProductFilterBuyerEntity) -> ProductsPaginationEntity:
        raise Exception('Not implemented method')
