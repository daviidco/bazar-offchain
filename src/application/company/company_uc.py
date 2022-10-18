import inject

from src.domain.entities.common_entity import JwtEntity
from src.domain.entities.company_entity import CompanyEntity, CompaniesPaginationEntity, CompanyNewEntity
from src.domain.ports.company_interface import ICompanyRepository


class CreateCompany:
    @inject.autoparams('company_repository')
    def __init__(self, company_repository: ICompanyRepository):
        self.__company_repository = company_repository

    def execute(self, jwt_entity: JwtEntity, company_entity: CompanyNewEntity,
                objects_cloud: list) -> CompanyEntity:
        return self.__company_repository.new_company(jwt_entity, company_entity, objects_cloud)


class GetCompany:
    @inject.autoparams('company_repository')
    def __init__(self, company_repository: ICompanyRepository):
        self.__company_repository = company_repository

    def execute(self, uuid: str) -> CompanyEntity:
        return self.__company_repository.get_company_by_uuid(uuid)


class GetAllCompanies:
    @inject.autoparams('company_repository')
    def __init__(self, company_repository: ICompanyRepository):
        self.__company_repository = company_repository

    def execute(self, limit: int, offset: int) -> CompaniesPaginationEntity:
        return self.__company_repository.get_all_companies(limit, offset)