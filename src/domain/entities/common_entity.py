from uuid import UUID

from pydantic import BaseModel


class UuidEntity(BaseModel):
    uuid: UUID


class PaginationEntity(BaseModel):
    limit: int
    offset: int
    total: int


class InputPaginationEntity(BaseModel):
    limit: int
    offset: int


class ErrorEntity(BaseModel):
    status_code: int
    message: str = None
    error: dict


class JwtEntity(BaseModel):
    iss: str
    sub: str
    aud: str
    iat: int
    exp: int
    azp: str
    scope: str
    gty: str