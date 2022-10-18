from abc import ABC, abstractmethod

from src.domain.entities.avatar_entity import AvatarEntity, AvatarNewEntity, AvatarsListEntity


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