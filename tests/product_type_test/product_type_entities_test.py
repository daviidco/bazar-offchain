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

from src.domain.entities.product_type_entity import ProductTypeBaseEntity, ProductTypeEntity, ProductTypesListEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

class TestProductTypeEntity:
    generated_uuid = uuid.uuid4()

    data_ProductTypeBaseEntity = {'product_type': 'name product type'}
    data_ProductTypeEntity_v1 = {
        'uuid': generated_uuid,
        'product_type': 'name product type'}

    data_ProductTypeEntity_v2 = {
        'uuid': generated_uuid,
        'product_type': 'name two product type'}

    data_ProductTypesListEntity = {'results': [data_ProductTypeEntity_v1, data_ProductTypeEntity_v2]}

    def test_product_type_base_entity(self):
        product_type_1 = ProductTypeBaseEntity.parse_obj(self.data_ProductTypeBaseEntity)
        validate_data_entity([product_type_1], ProductTypeBaseEntity, [self.data_ProductTypeBaseEntity])
        validate_instance_properties_entity([product_type_1], ProductTypeBaseEntity)

    def test_product_type_entity(self):
        product_type_1 = ProductTypeEntity.parse_obj(self.data_ProductTypeEntity_v1)
        product_type_2 = ProductTypeEntity.parse_obj(self.data_ProductTypeEntity_v2)
        base_products = [product_type_1, product_type_2]
        validate_data_entity(base_products, ProductTypeEntity, [self.data_ProductTypeEntity_v1,
                                                                self.data_ProductTypeEntity_v2])
        validate_instance_properties_entity(base_products, ProductTypeEntity)

    def test_product_type_pagination_entity(self):
        product_type_pagination = ProductTypesListEntity.parse_obj(self.data_ProductTypesListEntity)
        validate_data_entity([product_type_pagination], ProductTypesListEntity, [self.data_ProductTypesListEntity])
        validate_instance_properties_entity([product_type_pagination], ProductTypesListEntity)
