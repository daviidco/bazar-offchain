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

from src.domain.entities.user_entity import UserEntity, UserBaseEntity, UsersPaginationEntity, UserNewEntity

#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#


def validate_instance_users(users):
    for u in users:
        assert isinstance(u.uuid, uuid.UUID)
        assert isinstance(u.rol, str)
        assert isinstance(u.status, str)
        if u.created_at is not None:
            assert isinstance(u.created_at, date)


class TestUserEntity:
    generated_uuid = uuid.uuid4()

    data_base_user = {'uuid': generated_uuid,
                      'rol': 'seller'}

    data_new_user = {'uuid': generated_uuid,
                     'rol': 'buyer'}

    data_user_entity_v1 = {
        "company": [
            {
                "address": "Cali col",
                "chamber_commerce": "software",
                "city": "Cali",
                "company_name": "Cafeto105",
                "country": "Colombia",
                "legal_representative": "Luis",
                "operative_years": 7,
                "profile_image_url": "https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-b.png",
                "uuid": "dc26d103-848a-406f-b5ea-6af44aa7cd03"
            }
        ],
        'uuid': generated_uuid,
        'rol': 'seller',
        'status': 'active'}

    data_user_entity_v2 = {
        "company": [
            {
                "address": "Cali col",
                "chamber_commerce": "software",
                "city": "Cali",
                "company_name": "Cafeto105",
                "country": "Colombia",
                "legal_representative": "Luis",
                "operative_years": 7,
                "profile_image_url": "https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-b.png",
                "uuid": "dc26d103-848a-406f-b5ea-6af44aa7cd03"
            }
        ], 'uuid': generated_uuid,
        'rol': 'buyer',
        'status': 'inactive',
        'created_at': date(2017, 11, 17)}

    data_user_pagination = {'limit': 10,
                            'offset': 1,
                            'total': 100,
                            'results': [data_user_entity_v1, data_user_entity_v2]}

    def validate_data_users(self, users):
        for u in users:
            assert u.uuid == self.generated_uuid
            assert u.rol in ['seller', 'buyer']
            assert u.status in ['active', 'inactive']
            assert u.created_at in [None, date(2017, 11, 17)]

    def test_base_user_entity(self):
        user_1 = UserBaseEntity.parse_obj(self.data_base_user)
        assert user_1.uuid == self.generated_uuid
        assert user_1.rol in ['seller', 'buyer']

    def test_new_user_entity(self):
        user_1 = UserNewEntity.parse_obj(self.data_base_user)
        assert user_1.uuid == self.generated_uuid
        assert user_1.rol in ['seller', 'buyer']

    def test_user_entity(self):
        user_1 = UserEntity.parse_obj(self.data_user_entity_v1)
        user_2 = UserEntity.parse_obj(self.data_user_entity_v2)
        users = [user_1, user_2]
        self.validate_data_users(users)
        validate_instance_users(users)

    def test_user_pagination_entity(self):
        user_pagination = UsersPaginationEntity.parse_obj(self.data_user_pagination)
        assert user_pagination.limit == 10
        assert user_pagination.offset == 1
        self.validate_data_users(user_pagination.results)
        validate_instance_users(user_pagination.results)
