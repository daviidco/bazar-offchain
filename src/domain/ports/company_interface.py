from abc import ABC, abstractmethod

from src.domain.entities.common_entity import JwtEntity
from src.domain.entities.company_entity import CompanyEntity, CompanyNewEntity, CompaniesPaginationEntity


class ICompanyRepository(ABC):

    @abstractmethod
    def new_company(self, jwt_entity: JwtEntity, company_entity: CompanyNewEntity,
                    objects_cloud: list) -> CompanyEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_company_by_uuid(self, uuid: str) -> CompanyEntity:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_companies_count(self) -> int:
        raise Exception('Not implemented method')

    @abstractmethod
    def get_all_companies(self, limit: int, offset: int) -> CompaniesPaginationEntity:
        raise Exception('Not implemented method')