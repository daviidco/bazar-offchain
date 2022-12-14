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

import uuid

from src.domain.entities.variety_entity import VarietyBaseEntity, VarietyEntity, VarietiesListEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

class TestVarietyEntity:
    generated_uuid = uuid.uuid4()

    data_VarietyBaseEntity = {'variety': 'name variety'}
    data_VarietyEntity_v1 = {
        'uuid': generated_uuid,
        'variety': 'name variety'}

    data_VarietyEntity_v2 = {
        'uuid': generated_uuid,
        'variety': 'name two variety'}

    data_VarietiesListEntity = {'results': [data_VarietyEntity_v1, data_VarietyEntity_v2]}

    def test_variety_base_entity(self):
        incoterm_1 = VarietyBaseEntity.parse_obj(self.data_VarietyBaseEntity)
        validate_data_entity([incoterm_1], VarietyBaseEntity, [self.data_VarietyBaseEntity])
        validate_instance_properties_entity([incoterm_1], VarietyBaseEntity)

    def test_variety_entity_(self):
        incoterm_1 = VarietyEntity.parse_obj(self.data_VarietyEntity_v1)
        incoterm_2 = VarietyEntity.parse_obj(self.data_VarietyEntity_v2)
        base_products = [incoterm_1, incoterm_2]
        validate_data_entity(base_products, VarietyEntity, [self.data_VarietyEntity_v1,
                                                            self.data_VarietyEntity_v2])
        validate_instance_properties_entity(base_products, VarietyEntity)

    def test_incoterm_pagination_entity(self):
        incoterm_pagination = VarietiesListEntity.parse_obj(self.data_VarietiesListEntity)
        validate_data_entity([incoterm_pagination], VarietiesListEntity, [self.data_VarietiesListEntity])
        validate_instance_properties_entity([incoterm_pagination], VarietiesListEntity)
