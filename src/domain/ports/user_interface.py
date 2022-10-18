from abc import ABC, abstractmethod

from src.domain.entities.user_entity import UserEntity, UserNewEntity, UsersPaginationEntity


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