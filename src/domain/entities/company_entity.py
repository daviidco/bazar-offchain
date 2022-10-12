from typing import List
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.common_entity import UuidEntity, PaginationEntity


class CompanyBaseEntity(BaseModel):
    company_name: str
    address: str
    chamber_commerce: str
    legal_representative: str
    operative_years: int
    country: str
    city: str

    class Config:
        orm_mode = True


class CompanyNewEntity(CompanyBaseEntity):
    uuid_user: UUID


class CompanyEntity(CompanyBaseEntity, UuidEntity):
    pass


class CompaniesPaginationEntity(PaginationEntity):
    results: List[CompanyEntity]