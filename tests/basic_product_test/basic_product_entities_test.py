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

from src.domain.entities.basic_product_entity import BasicProductEntity, BasicProductsListEntity, BasicProductBaseEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

class TestBasicProductEntity:
    generated_uuid = uuid.uuid4()

    data_BasicBasicProductBaseEntity = {'basic_product': 'name basic product'}
    data_BasicProductEntity_v1 = {
        'uuid': generated_uuid,
        'basic_product': 'name basic product'}

    data_BasicProductEntity_v2 = {
        'uuid': generated_uuid,
        'basic_product': 'name two basic product'}

    data_BasicProductsListEntity = {'results': [data_BasicProductEntity_v1, data_BasicProductEntity_v2]}

    def test_basic_product_base_entity(self):
        base_product_1 = BasicProductBaseEntity.parse_obj(self.data_BasicBasicProductBaseEntity)
        validate_data_entity([base_product_1], BasicProductBaseEntity, [self.data_BasicBasicProductBaseEntity])
        validate_instance_properties_entity([base_product_1], BasicProductBaseEntity)

    def test_basic_product_entity(self):
        base_product_1 = BasicProductEntity.parse_obj(self.data_BasicProductEntity_v1)
        base_product_2 = BasicProductEntity.parse_obj(self.data_BasicProductEntity_v2)
        base_products = [base_product_1, base_product_2]
        validate_data_entity(base_products, BasicProductEntity, [self.data_BasicProductEntity_v1,
                                                                 self.data_BasicProductEntity_v2])
        validate_instance_properties_entity(base_products, BasicProductEntity)

    def test_product_pagination_entity(self):
        product_pagination = BasicProductsListEntity.parse_obj(self.data_BasicProductsListEntity)
        validate_data_entity([product_pagination], BasicProductsListEntity, [self.data_BasicProductsListEntity])
        validate_instance_properties_entity([product_pagination], BasicProductsListEntity)
