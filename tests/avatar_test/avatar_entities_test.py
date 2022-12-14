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

from pydantic import AnyHttpUrl

from src.domain.entities.avatar_entity import AvatarBaseEntity, AvatarNewEntity, AvatarEntity, AvatarsPaginationEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#


class TestAvatarEntity:
    generated_uuid = uuid.uuid4()

    data_base_avatar = {'image_name': 'astronaut-s',
                        'image_url': 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/'
                                     'astronaut-s.png'}

    data_new_avatar = {'image_name': 'astronaut-s',
                       'image_url': 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/'
                                    'astronaut-s.png'}

    data_avatar_entity_aux = {'uuid': generated_uuid}

    data_avatar_entity_v1 = dict(data_base_avatar, **data_avatar_entity_aux)

    data_avatar_entity_v2 = dict(data_base_avatar, **data_avatar_entity_aux)

    data_avatar_pagination = {'limit': 10,
                              'offset': 1,
                              'total': 100,
                              'results': [data_avatar_entity_v1, data_avatar_entity_v2],
                              'total_pages': 10}

    def test_base_avatar_entity(self):
        avatar_1 = AvatarBaseEntity.parse_obj(self.data_base_avatar)
        validate_data_entity([avatar_1], AvatarBaseEntity, [self.data_base_avatar])
        validate_instance_properties_entity([avatar_1], AvatarBaseEntity)

    def test_new_avatar_entity(self):
        avatar_1 = AvatarNewEntity.parse_obj(self.data_new_avatar)
        validate_data_entity([avatar_1], AvatarNewEntity, [self.data_new_avatar])
        validate_instance_properties_entity([avatar_1], AvatarNewEntity)

    def test_avatar_entity(self):
        avatar_1 = AvatarEntity.parse_obj(self.data_avatar_entity_v1)
        avatar_2 = AvatarEntity.parse_obj(self.data_avatar_entity_v2)
        avatars = [avatar_1, avatar_2]
        validate_data_entity(avatars, AvatarEntity, [self.data_avatar_entity_v1, self.data_avatar_entity_v2])
        validate_instance_properties_entity(avatars, AvatarEntity)

    def test_product_pagination_entity(self):
        avatar_pagination = AvatarsPaginationEntity.parse_obj(self.data_avatar_pagination)
        validate_data_entity([avatar_pagination], AvatarsPaginationEntity, [self.data_avatar_pagination])
        validate_instance_properties_entity([avatar_pagination], AvatarsPaginationEntity)
