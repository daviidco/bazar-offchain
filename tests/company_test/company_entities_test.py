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

import uuid

from src.domain.entities.company_entity import CompanyEntity, CompanyBaseEntity, CompaniesPaginationEntity, \
    CompanyNewEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


class TestCompanyEntity:
    # Main Data
    generated_uuid = uuid.uuid4()

    data_base_company = {'company_name': 'test',
                         'address': 'cra - test',
                         'chamber_commerce': '123123',
                         'legal_representative': 'test',
                         'operative_years': 5,
                         'country': 'colombia',
                         'city': 'cali',
                         'profile_images': [
                             "https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-s.png",
                             "https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-m.png",
                             "https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-b.png"]}

    data_new_company_aux = {'uuid_user': generated_uuid,
                            'profile_image': "https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/"
                                             "astronaut-s.png"
                            }

    data_new_company = dict(data_base_company, **data_new_company_aux)

    data_company_entity_v1 = dict(data_base_company, **{'uuid': generated_uuid})

    data_company_entity_v2 = dict(data_base_company, **{'uuid': generated_uuid})

    data_companies_pagination = {'limit': 10,
                                 'offset': 1,
                                 'total': 100,
                                 'results': [data_company_entity_v1, data_company_entity_v2]}

    def test_base_company_entity(self):
        company_1 = CompanyBaseEntity.parse_obj(self.data_base_company)
        validate_data_entity([company_1], CompanyBaseEntity, [self.data_base_company])
        validate_instance_properties_entity([company_1], CompanyBaseEntity)

    def test_new_company_entity(self):
        company_1 = CompanyNewEntity.parse_obj(self.data_new_company)
        validate_data_entity([company_1], CompanyNewEntity, [self.data_new_company])
        validate_instance_properties_entity([company_1], CompanyNewEntity)

    def test_company_entity(self):
        company_1 = CompanyEntity.parse_obj(self.data_company_entity_v1)
        company_2 = CompanyEntity.parse_obj(self.data_company_entity_v2)
        validate_data_entity([company_1, company_2], CompanyEntity, [self.data_company_entity_v1,
                                                                     self.data_company_entity_v2])
        validate_instance_properties_entity([company_1, company_2], CompanyEntity)

    def test_company_pagination_entity(self):
        company_pagination = CompaniesPaginationEntity.parse_obj(self.data_companies_pagination)
        validate_data_entity([company_pagination], CompaniesPaginationEntity, [self.data_companies_pagination])
        validate_instance_properties_entity([company_pagination], CompaniesPaginationEntity)
