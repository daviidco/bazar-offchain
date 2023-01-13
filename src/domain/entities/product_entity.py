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

from pydantic import BaseModel, AnyHttpUrl, Field
from pydantic.types import date

from src.domain.entities.common_entity import UuidEntity, PaginationEntity, InputPaginationEntity
from src.domain.entities.incoterm_entity import IncotermEntity
from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationEntity


#
# These classes lets define the product type entities of domain.
# @author David Córdoba
#


class ProductOptionsEntity(BaseModel):
    basic_product_uuid: UUID
    product_type_uuid: UUID
    variety_uuid: UUID


class ProductBaseEntity(BaseModel):
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


class ProductNewEntity(ProductOptionsEntity, ProductBaseEntity):
    uuid_user: UUID
    incoterms_uuid: List[UUID] = []
    sustainability_certifications_uuid: List[UUID] = []


class ProductEditEntity(ProductBaseEntity):
    uuid_user: UUID
    incoterms_uuid: List[UUID] = []
    sustainability_certifications_uuid: List[UUID] = []
    change_files: bool = True
    change_images: bool = True


class ProductEntity(ProductOptionsEntity, ProductBaseEntity, UuidEntity):
    status: str
    basic_product: str
    minimum_order: str
    product_type: str
    variety: str
    url_images: List[AnyHttpUrl] = None
    url_files: List[AnyHttpUrl] = None
    incoterms: List[IncotermEntity] = None
    sustainability_certifications: List[SustainabilityCertificationEntity] = None
    url_avatar: AnyHttpUrl = None
    is_liked: bool = False


class ProductsListEntity(BaseModel):
    results: List[ProductEntity]


class ProductsPaginationEntity(PaginationEntity):
    results: List[ProductEntity]


class ProductFilterEntity(BaseModel):
    price_per_kg_start: float = Field(default=0, description="Initial price per kg")
    price_per_kg_end: float = Field(description="limit price per kg")
    available_for_sale: float = Field(description="Amount available for sale")
    user_uuid: UUID = Field(description="UUID of user")


class ProductFilterSellerEntity(ProductFilterEntity):
    pass


class ProductFilterBuyerEntity(ProductFilterEntity, InputPaginationEntity):
    pass


class ProductFilterBasicProductEntity(BaseModel):
    basic_product: str = Field(description="Name of basic Product example: (Cocoa, Avocado, Coffee)")
    user_uuid: UUID = Field(description="User UUID")


class ProductFilterSellerBasicProductEntity(ProductFilterBasicProductEntity):
    pass


class ProductFilterBuyerBasicProductEntity(ProductFilterBasicProductEntity, InputPaginationEntity):
    pass


# Availability
class AvailabilityEntity(BaseModel):
    uuid_product: UUID
    available_for_sale: float
