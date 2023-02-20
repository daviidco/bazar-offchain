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

from pydantic import BaseModel, Field


#
# These classes lets define the common entities of domain.
# @author David Córdoba
#


class UuidEntity(BaseModel):
    uuid: UUID


class StatesEntity(UuidEntity):
    tag: str = None

    class Config:
        orm_mode = True


class BasicEntity(BaseModel):
    results: List[StatesEntity]


class PaginationEntity(BaseModel):
    limit: int
    offset: int
    total: int
    total_pages: int


class InputPaginationEntity(BaseModel):
    limit: int = Field(default=10, description="limit the number of rows returned from a query")
    offset: int = Field(default=0, description="Omit a specified number of rows before the beginning of the result set")


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


class DeleteEntity(BaseModel):
    status: str = 'Deleted'
    description: str