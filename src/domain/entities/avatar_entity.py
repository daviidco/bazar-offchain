from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, AnyHttpUrl

from src.domain.entities.common_entity import UuidEntity, PaginationEntity


class AvatarBaseEntity(BaseModel):
    image_name: str
    image_url: AnyHttpUrl

    class Config:
        orm_mode = True


class AvatarNewEntity(AvatarBaseEntity):
    pass


class AvatarEntity(AvatarBaseEntity, UuidEntity):
    pass


class AvatarsPaginationEntity(PaginationEntity):
    results: List[AvatarEntity]


class AvatarsListEntity(BaseModel):
    results: List[AvatarEntity]

    class Config:
        orm_mode = True
