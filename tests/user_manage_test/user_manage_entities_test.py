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
from datetime import date
from typing import List

from src.domain.entities.product_entity import ProductEntity, ProductBaseEntity, ProductsPaginationEntity, \
    ProductNewEntity
from src.domain.entities.user_manage_entity import UserManageEntity, ProductManageEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

class TestUserManageEntity:
    generated_uuid = uuid.uuid4()

    data_ProductManageEntity_v1 = {'uuid_product_status': generated_uuid,
                                   'uuid_product': generated_uuid}

    data_ProductManageEntity_v2 = {'uuid_product_status': generated_uuid,
                                   'uuid_product': generated_uuid}

    data_UserManageEntity_v1 = {'uuid_user': generated_uuid,
                                'uuid_user_status': generated_uuid,
                                'products': [],
                                'comment_approval': 'comment to approve'}

    data_UserManageEntity_v2 = {'uuid_user': generated_uuid,
                                'uuid_user_status': generated_uuid,
                                'products': [data_ProductManageEntity_v1, data_ProductManageEntity_v2],
                                'comment_approval': 'comment to approve'}

    def test_product_manage_entity(self):
        product_manage_v1 = ProductManageEntity.parse_obj(self.data_ProductManageEntity_v1)
        validate_data_entity([product_manage_v1], ProductManageEntity, [self.data_ProductManageEntity_v1])
        validate_instance_properties_entity([product_manage_v1], ProductManageEntity)

    def test_user_manage_entity(self):
        user_manage_v1 = UserManageEntity.parse_obj(self.data_UserManageEntity_v1)
        user_manage_v2 = UserManageEntity.parse_obj(self.data_UserManageEntity_v2)
        validate_data_entity([user_manage_v1, user_manage_v2], UserManageEntity, [self.data_UserManageEntity_v1,
                                                                                  self.data_UserManageEntity_v2])
        validate_instance_properties_entity([user_manage_v1, user_manage_v2], UserManageEntity)
