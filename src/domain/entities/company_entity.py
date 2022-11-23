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

from src.domain.entities.common_entity import UuidEntity, PaginationEntity


#
# These classes lets define the company entities of domain.
# @author David Córdoba
#


class CompanyBaseEntity(BaseModel):
    company_name: str
    address: str
    chamber_commerce: str
    legal_representative: str
    operative_years: int
    country: str
    city: str
    profile_images: List[AnyHttpUrl] = None

    class Config:
        orm_mode = True


class CompanyNewEntity(CompanyBaseEntity):
    uuid_user: UUID
    profile_image: AnyHttpUrl = None


class CompanyEntity(CompanyBaseEntity, UuidEntity):
    profile_image_url: AnyHttpUrl = None


class CompaniesPaginationEntity(PaginationEntity):
    results: List[CompanyEntity]