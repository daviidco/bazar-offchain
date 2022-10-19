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

from src.domain.entities.user_entity import UserEntity, UserNewEntity, UsersPaginationEntity


#
# This interface or port lets define the methods to implement by ruser_epository.
# @author David Córdoba
#
class IUserRepository(ABC):

    @abstractmethod
    def new_user(self, user_entity: UserNewEntity) -> UserEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_user_by_uuid(self, uuid: str) -> UserEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_users_count(self) -> int:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_all_users(self, limit: int, offset: int) -> UsersPaginationEntity:
        raise Exception('Not implemented method')
