# -*- coding: utf-8 -*-
#
# This source code is the confidential, proprietary information of
# Bazar Network S.A.S., you may not disclose such Information,
# and may only use it in accordance with the terms of the license
# agreement you entered into with Bazar Network S.A.S.
#
# 2022: Bazar Network S.A.S.
# All Rights Reserved.
#

import inject

from src.domain.entities.common_entity import JwtEntity
from src.domain.entities.company_entity import CompanyEntity, CompaniesPaginationEntity, CompanyNewEntity
from src.domain.ports.company_interface import ICompanyRepository


#
# These classes lets define the company user cases.
# @author David Córdoba
#


class CreateCompany:
    @inject.autoparams('company_repository')
    def __init__(self, company_repository: ICompanyRepository):
        self.__company_repository = company_repository

    def execute(self, role: str, company_entity: CompanyNewEntity,
                objects_cloud: list) -> CompanyEntity:
        return self.__company_repository.new_company(role, company_entity, objects_cloud)


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