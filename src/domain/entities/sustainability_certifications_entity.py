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

from pydantic import BaseModel

from src.domain.entities.common_entity import UuidEntity


#
# These classes lets define the sustainability certifications of product entities of domain.
# @author David Córdoba
#


class SustainabilityCertificationBaseEntity(BaseModel):
    certification: str

    class Config:
        orm_mode = True


class SustainabilityCertificationEntity(SustainabilityCertificationBaseEntity, UuidEntity):
    pass


class SustainabilityCertificationsListEntity(BaseModel):
    results: List[SustainabilityCertificationEntity]

