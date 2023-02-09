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

from src.domain.entities.common_entity import BasicEntity
from src.domain.entities.user_entity import UserEntity, UserNewEntity, UsersPaginationEntity
from src.domain.entities.user_manage_entity import UserManageEntity


#
# This interface or port lets define the methods to implement by user_repository.
# @author David Córdoba
#
class IUserRepository(ABC):

    @abstractmethod
    def new_user(self, user_entity: UserNewEntity) -> UserEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_user_by_uuid(self, jwt: str, uuid: str) -> UserEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_users_count(self) -> int:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_all_users(self, limit: int, offset: int, jwt: str) -> UsersPaginationEntity:
        raise Exception('Not implemented method')

    def user_states(self) -> BasicEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def put_states_approval(self, user_manage: UserManageEntity) -> UserManageEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_whatsapp_link(self, jwt: str, uuid: str) -> str:
        raise Exception('Not implemented method')
