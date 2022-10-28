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

from abc import ABC, abstractmethod

from src.domain.entities.common_entity import JwtEntity
from src.domain.entities.company_entity import CompanyEntity, CompanyNewEntity, CompaniesPaginationEntity


#
# This interface or port lets define the methods to implement by company_repository.
# @author David Córdoba
#
class ICompanyRepository(ABC):

    @abstractmethod
    def new_company(self, role: str, company_entity: CompanyNewEntity,
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
