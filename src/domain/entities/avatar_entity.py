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

from pydantic import BaseModel, AnyHttpUrl

from src.domain.entities.common_entity import UuidEntity, PaginationEntity


#
# These classes lets define the avatar entities of domain.
# @author David Córdoba
#

class AvatarBaseEntity(BaseModel):
    image_name: str
    image_url: AnyHttpUrl

    class Config:
        orm_mode = True


class AvatarNewEntity(AvatarBaseEntity):
    pass


class AvatarEntity(AvatarBaseEntity, UuidEntity):
    pass


class AvatarsPaginationEntity(PaginationEntity):
    results: List[AvatarEntity]


class AvatarsListEntity(BaseModel):
    results: List[AvatarEntity]

    class Config:
        orm_mode = True
