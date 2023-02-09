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

from src.domain.entities.common_entity import BasicEntity
from src.domain.entities.user_entity import UserNewEntity, UsersPaginationEntity, UserEntity
from src.domain.entities.user_manage_entity import UserManageEntity
from src.domain.ports.user_interface import IUserRepository


#
# These classes lets define the user cases of user.
# @author David Córdoba
#


class CreateUser:
    @inject.autoparams('user_repository')
    def __init__(self, user_repository: IUserRepository):
        self.__user_repository = user_repository

    def execute(self, new_user: UserNewEntity) -> UserEntity:
        return self.__user_repository.new_user(new_user)


class GetUser:
    @inject.autoparams('user_repository')
    def __init__(self, user_repository: IUserRepository):
        self.__user_repository = user_repository

    def execute(self, jwt: str, uuid: str) -> UserEntity:
        return self.__user_repository.get_user_by_uuid(jwt, uuid)


class GetAllUsers:
    @inject.autoparams('user_repository')
    def __init__(self, user_repository: IUserRepository):
        self.__user_repository = user_repository

    def execute(self, limit: int, offset: int, jwt: str) -> UsersPaginationEntity:
        return self.__user_repository.get_all_users(limit, offset, jwt)


class GetUserStates:
    @inject.autoparams('user_repository')
    def __init__(self, user_repository: IUserRepository):
        self.__user_repository = user_repository

    def execute(self) -> BasicEntity:
        return self.__user_repository.user_states()


class PutStatesApproval:
    @inject.autoparams('user_repository')
    def __init__(self, user_repository: IUserRepository):
        self.__user_repository = user_repository

    def execute(self, user_manage: UserManageEntity) -> UserManageEntity:
        return self.__user_repository.put_states_approval(user_manage)


class GetWhatsappLink:
    @inject.autoparams('user_repository')
    def __init__(self, user_repository: IUserRepository):
        self.__user_repository = user_repository

    def execute(self, jwt: str, uuid: str) -> str:
        return self.__user_repository.get_whatsapp_link(jwt, uuid)
