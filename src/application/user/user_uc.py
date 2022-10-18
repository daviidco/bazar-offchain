import inject


from src.domain.entities.user_entity import UserNewEntity, UsersPaginationEntity, UserEntity
from src.domain.ports.user_interface import IUserRepository


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

    def execute(self, uuid: str) -> UserEntity:
        return self.__user_repository.get_user_by_uuid(uuid)


class GetAllUsers:
    @inject.autoparams('user_repository')
    def __init__(self, user_repository: IUserRepository):
        self.__user_repository = user_repository

    def execute(self, limit: int, offset: int) -> UsersPaginationEntity:
        return self.__user_repository.get_all_users(limit, offset)