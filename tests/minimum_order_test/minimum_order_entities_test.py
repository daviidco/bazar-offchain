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

from src.domain.entities.minimum_order_entity import MinimumOrderBaseEntity, MinimumOrderEntity, MinimumOrderListEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

class TestMinimumOrderEntity:
    generated_uuid = uuid.uuid4()

    data_MinimumOrderBaseEntity = {'minimum_order': 'name order'}
    data_MinimumOrderEntity_v1 = {
        'uuid': generated_uuid,
        'minimum_order': 'name order'}

    data_MinimumOrderEntity_v2 = {
        'uuid': generated_uuid,
        'minimum_order': 'name two order'}

    data_MinimumOrderListEntity = {'results': [data_MinimumOrderEntity_v1, data_MinimumOrderEntity_v2]}

    def test_minimum_order_base_entity(self):
        minimum_order_1 = MinimumOrderBaseEntity.parse_obj(self.data_MinimumOrderBaseEntity)
        validate_data_entity([minimum_order_1], MinimumOrderBaseEntity, [self.data_MinimumOrderBaseEntity])
        validate_instance_properties_entity([minimum_order_1], MinimumOrderBaseEntity)

    def test_minimum_order_entity(self):
        minimum_order_1 = MinimumOrderEntity.parse_obj(self.data_MinimumOrderEntity_v1)
        minimum_order_2 = MinimumOrderEntity.parse_obj(self.data_MinimumOrderEntity_v2)
        base_products = [minimum_order_1, minimum_order_2]
        validate_data_entity(base_products, MinimumOrderEntity, [self.data_MinimumOrderEntity_v1,
                                                                 self.data_MinimumOrderEntity_v2])
        validate_instance_properties_entity(base_products, MinimumOrderEntity)

    def test_minimum_order_pagination_entity(self):
        minimum_order_pagination = MinimumOrderListEntity.parse_obj(self.data_MinimumOrderListEntity)
        validate_data_entity([minimum_order_pagination], MinimumOrderListEntity, [self.data_MinimumOrderListEntity])
        validate_instance_properties_entity([minimum_order_pagination], MinimumOrderListEntity)
