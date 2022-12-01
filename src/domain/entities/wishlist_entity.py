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

from typing import List
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.common_entity import PaginationEntity


#
# These classes lets define the product type entities of domain.
# @author David Córdoba
#


class WishProductBaseEntity(BaseModel):
    user_uuid: UUID
    product_uuid: UUID

    class Config:
        orm_mode = True


class WishProductNewEntity(WishProductBaseEntity):
    pass


class WishProductEntity(WishProductBaseEntity):
    pass


class WishProductsListEntity(BaseModel):
    results: List[WishProductEntity]


class WishProductsEntityPaginationEntity(PaginationEntity):
    results: List[WishProductEntity]
