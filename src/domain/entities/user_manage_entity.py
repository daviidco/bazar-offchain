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

from src.domain.entities.common_entity import UuidEntity


#
# These classes lets define the user entities of domain.
# @author David Córdoba
#

class ProductManageEntity(BaseModel):
    uuid_product_status: UUID
    uuid_product: UUID


class UserManageEntity(BaseModel):
    uuid_user: UUID
    uuid_user_status: UUID = None
    products: List[ProductManageEntity] = None
    comment_approval: str = None

    class Config:
        orm_mode = True

