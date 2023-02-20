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

from src.domain.entities.incoterm_entity import IncotermBaseEntity, IncotermEntity, IncotermsListEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

class TestIncotermEntity:
    generated_uuid = uuid.uuid4()

    data_IncotermBaseEntity = {'incoterm': 'name incoterm'}
    data_IncotermEntity_v1 = {
        'uuid': generated_uuid,
        'incoterm': 'name incoterm'}

    data_IncotermEntity_v2 = {
        'uuid': generated_uuid,
        'incoterm': 'name two incoterm'}

    data_IncotermsListEntity = {'results': [data_IncotermEntity_v1, data_IncotermEntity_v2]}

    def test_incoterm_base_entity(self):
        incoterm_1 = IncotermBaseEntity.parse_obj(self.data_IncotermBaseEntity)
        validate_data_entity([incoterm_1], IncotermBaseEntity, [self.data_IncotermBaseEntity])
        validate_instance_properties_entity([incoterm_1], IncotermBaseEntity)

    def test_incoterm_entity(self):
        incoterm_1 = IncotermEntity.parse_obj(self.data_IncotermEntity_v1)
        incoterm_2 = IncotermEntity.parse_obj(self.data_IncotermEntity_v2)
        base_products = [incoterm_1, incoterm_2]
        validate_data_entity(base_products, IncotermEntity, [self.data_IncotermEntity_v1,
                                                             self.data_IncotermEntity_v2])
        validate_instance_properties_entity(base_products, IncotermEntity)

    def test_incoterm_pagination_entity(self):
        incoterm_pagination = IncotermsListEntity.parse_obj(self.data_IncotermsListEntity)
        validate_data_entity([incoterm_pagination], IncotermsListEntity, [self.data_IncotermsListEntity])
        validate_instance_properties_entity([incoterm_pagination], IncotermsListEntity)
