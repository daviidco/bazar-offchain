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

from abc import ABC, abstractmethod

from src.domain.entities.avatar_entity import AvatarEntity, AvatarNewEntity, AvatarsListEntity


#
# This interface or port lets define the methods to implement by avatar_repository.
# @author David Córdoba
#
class IAvatarRepository(ABC):

    @abstractmethod
    def new_avatar(self, avatar_entity: AvatarNewEntity) -> AvatarEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_avatar_by_uuid(self, uuid: str) -> AvatarEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_avatars_count(self) -> int:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_all_avatars(self, limit: int = None, offset: int = None) -> AvatarsListEntity:
        raise Exception('Not implemented method')
