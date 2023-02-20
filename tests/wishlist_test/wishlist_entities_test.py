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

from src.domain.entities.wishlist_entity import WishProductEntity, WishProductNewEntity, WishProductBaseEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

class TestWishlistEntity:
    generated_uuid = uuid.uuid4()

    data_WishProductBaseEntity = {'user_uuid': generated_uuid,
                                  'product_uuid': generated_uuid}

    data_WishProductNewEntity = {'user_uuid': generated_uuid,
                                 'product_uuid': generated_uuid}

    data_WishProductEntity = {'user_uuid': generated_uuid,
                              'product_uuid': generated_uuid}

    def test_wish_product_base_entity(self):
        wish_1 = WishProductBaseEntity.parse_obj(self.data_WishProductBaseEntity)
        validate_data_entity([wish_1], WishProductBaseEntity, [self.data_WishProductBaseEntity])
        validate_instance_properties_entity([wish_1], WishProductBaseEntity)

    def test_wish_product_new_entity(self):
        wish_1 = WishProductNewEntity.parse_obj(self.data_WishProductNewEntity)
        validate_data_entity([wish_1], WishProductNewEntity, [self.data_WishProductNewEntity])
        validate_instance_properties_entity([wish_1], WishProductNewEntity)

    def test_wish_product_entity(self):
        wish_1 = WishProductEntity.parse_obj(self.data_WishProductEntity)
        validate_data_entity([wish_1], WishProductEntity, [self.data_WishProductEntity])
        validate_instance_properties_entity([wish_1], WishProductEntity)
