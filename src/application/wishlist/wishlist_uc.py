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

from src.domain.entities.product_entity import ProductsPaginationEntity
from src.domain.entities.wishlist_entity import WishProductNewEntity, WishProductEntity
from src.domain.ports.wishlist_interface import IWishListRepository


#
# These classes lets define the wishlist user cases.
# @author David Córdoba
#


class CreateWishProduct:
    @inject.autoparams('wishlist_repository')
    def __init__(self, wishlist_repository: IWishListRepository):
        self.__wishlist_repository = wishlist_repository

    def execute(self, role: str, wish_product_entity: WishProductNewEntity) -> WishProductEntity:
        return self.__wishlist_repository.new_product_on_wishlist(role, wish_product_entity)


class DeleteWishProduct:
    @inject.autoparams('wishlist_repository')
    def __init__(self, wishlist_repository: IWishListRepository):
        self.__wishlist_repository = wishlist_repository

    def execute(self, role: str, wish_product_entity: WishProductNewEntity) -> WishProductEntity:
        return self.__wishlist_repository.delete_product_from_wishlist(role, wish_product_entity)


class GetWishList:
    @inject.autoparams('wishlist_repository')
    def __init__(self, wishlist_repository: IWishListRepository):
        self.__wishlist_repository = wishlist_repository

    def execute(self, uid: str, role: str, limit: int, offset: int) -> ProductsPaginationEntity:
        return self.__wishlist_repository.get_wishlist_by_uuid_buyer(uid, role, limit, offset)


