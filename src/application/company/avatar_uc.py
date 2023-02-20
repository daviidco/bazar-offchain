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

import inject

from src.domain.entities.avatar_entity import AvatarsListEntity
from src.domain.ports.avatar_interface import IAvatarRepository


#
# These classes lets define the avatar user cases.
# @author David Córdoba
#


class GetAllAvatars:
    @inject.autoparams('avatar_repository')
    def __init__(self, avatar_repository: IAvatarRepository):
        self.__avatar_repository = avatar_repository

    def execute(self, limit: int = None, offset: int = None) -> AvatarsListEntity:
        return self.__avatar_repository.get_all_avatars(limit, offset)
