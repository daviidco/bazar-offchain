import inject

from src.domain.entities.avatar_entity import AvatarsListEntity
from src.domain.ports.avatar_interface import IAvatarRepository


class GetAllAvatars:
    @inject.autoparams('avatar_repository')
    def __init__(self, avatar_repository: IAvatarRepository):
        self.__avatar_repository = avatar_repository

    def execute(self, limit: int = None, offset: int = None) -> AvatarsListEntity:
        return self.__avatar_repository.get_all_avatars(limit, offset)