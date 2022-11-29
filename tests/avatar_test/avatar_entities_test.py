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


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#


def validate_instance_avatars(avatars):
    for a in avatars:
        assert isinstance(a.image_name, str)
        assert isinstance(a.image_url, AnyHttpUrl)


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
                               'results': [data_avatar_entity_v1, data_avatar_entity_v2]}

    def validate_data_avatars(self, avatars):
        for a in avatars:
            assert a.image_name == self.data_base_avatar['image_name']
            assert a.image_url == self.data_base_avatar['image_url']

    def test_base_avatar_entity(self):
        avatar_1 = AvatarBaseEntity.parse_obj(self.data_base_avatar)
        self.validate_data_avatars([avatar_1])
        validate_instance_avatars([avatar_1])

    def test_new_avatar_entity(self):
        avatar_1 = AvatarNewEntity.parse_obj(self.data_new_avatar)
        self.validate_data_avatars([avatar_1])
        validate_instance_avatars([avatar_1])

    def test_avatar_entity(self):
        avatar_1 = AvatarEntity.parse_obj(self.data_avatar_entity_v1)
        avatar_2 = AvatarEntity.parse_obj(self.data_avatar_entity_v2)
        avatars = [avatar_1, avatar_2]
        assert avatar_1.uuid == self.generated_uuid
        assert avatar_2.uuid == self.generated_uuid
        assert isinstance(avatar_1.uuid, uuid.UUID)
        assert isinstance(avatar_2.uuid, uuid.UUID)
        self.validate_data_avatars(avatars)
        validate_instance_avatars(avatars)

    def test_product_pagination_entity(self):
        avatar_pagination = AvatarsPaginationEntity.parse_obj(self.data_avatar_pagination)
        assert avatar_pagination.limit == 10
        assert avatar_pagination.offset == 1
        self.validate_data_avatars(avatar_pagination.results)
        validate_instance_avatars(avatar_pagination.results)
