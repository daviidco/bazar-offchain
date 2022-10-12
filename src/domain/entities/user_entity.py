from datetime import date
from typing import List

from src.domain.entities.common_entity import UuidEntity, PaginationEntity


class UserBaseEntity(UuidEntity):
    rol: str


class UserNewEntity(UserBaseEntity):
    pass


class UserEntity(UserBaseEntity):
    status: str
    created_at: date = None

    class Config:
        orm_mode = True


class UsersPaginationEntity(PaginationEntity):
    results: List[UserEntity]

