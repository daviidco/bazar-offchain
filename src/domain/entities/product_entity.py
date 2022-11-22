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

from pydantic import BaseModel, AnyHttpUrl
from pydantic.types import date

from src.domain.entities.common_entity import UuidEntity, PaginationEntity
from src.domain.entities.incoterm_entity import IncotermEntity
from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationEntity


#
# These classes lets define the product type entities of domain.
# @author David Córdoba
#


class ProductBaseEntity(BaseModel):
    basic_product_uuid: UUID
    product_type_uuid: UUID
    variety_uuid: UUID
    capacity_per_year: float
    date_in_port: date
    guild_or_association: str
    available_for_sale: float
    minimum_order_uuid: UUID
    expected_price_per_kg: float
    assistance_logistic: bool
    additional_description: str

    class Config:
        orm_mode = True


class ProductNewEntity(ProductBaseEntity):
    uuid_user: UUID
    incoterms_uuid: List[UUID] = None
    sustainability_certifications_uuid: List[UUID] = None


class ProductEntity(ProductBaseEntity, UuidEntity):
    url_images: List[AnyHttpUrl] = None
    url_files: List[AnyHttpUrl] = None
    status: str
    incoterms: List[IncotermEntity] = None
    sustainability_certifications: List[SustainabilityCertificationEntity] = None


class ProductsListEntity(BaseModel):
    results: List[ProductEntity]


class ProductsPaginationEntity(PaginationEntity):
    results: List[ProductBaseEntity]