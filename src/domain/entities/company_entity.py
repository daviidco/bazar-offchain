from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, AnyHttpUrl

from src.domain.entities.common_entity import UuidEntity, PaginationEntity


class CompanyBaseEntity(BaseModel):
    company_name: str
    address: str
    chamber_commerce: str
    legal_representative: str
    operative_years: int
    country: str
    city: str
    profile_images: List[AnyHttpUrl] = None

    class Config:
        orm_mode = True


class CompanyNewEntity(CompanyBaseEntity):
    uuid_user: UUID
    profile_image: AnyHttpUrl = None


class CompanyEntity(CompanyBaseEntity, UuidEntity):
    pass


class CompaniesPaginationEntity(PaginationEntity):
    results: List[CompanyEntity]