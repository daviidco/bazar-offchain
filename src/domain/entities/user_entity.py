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

from datetime import date
from typing import List

from src.domain.entities.common_entity import UuidEntity, PaginationEntity
from src.domain.entities.company_entity import CompanyEntity


#
# These classes lets define the user entities of domain.
# @author David Córdoba
#


class UserBaseEntity(UuidEntity):
    rol: str


class UserNewEntity(UserBaseEntity):
    pass


class UserEntity(UserBaseEntity):
    first_name: str = None
    last_name: str = None
    company: List[CompanyEntity]
    status: str
    created_at: date = None

    class Config:
        orm_mode = True


class UsersPaginationEntity(PaginationEntity):
    results: List[UserEntity]

