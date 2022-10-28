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
from typing import List, Union
from uuid import UUID

from pydantic import BaseModel


#
# These classes lets define the common entities of domain.
# @author David Córdoba
#


class UuidEntity(BaseModel):
    uuid: UUID


class PaginationEntity(BaseModel):
    limit: int
    offset: int
    total: int


class InputPaginationEntity(BaseModel):
    limit: int
    offset: int


class ErrorEntity(BaseModel):
    status_code: int
    message: str = None
    error: dict


class JwtEntity(BaseModel):
    iss: str
    sub: str
    aud: Union[str, List[str]]
    iat: int
    exp: int
    azp: str
    scope: str
    gty: str