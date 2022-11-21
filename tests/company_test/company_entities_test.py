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
from typing import List

from src.domain.entities.company_entity import CompanyEntity, CompanyBaseEntity, CompaniesPaginationEntity, \
    CompanyNewEntity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#


def validate_instance_company(companies):
    for c in companies:
        assert isinstance(c.company_name, str)
        assert isinstance(c.address, str)
        assert isinstance(c.chamber_commerce, str)
        assert isinstance(c.legal_representative, str)
        assert isinstance(c.operative_years, int)
        assert isinstance(c.country, str)
        assert isinstance(c.city, str)
        assert isinstance(c.profile_images, List)


def validate_data_companies(companies):
    for c in companies:
        assert c.company_name == 'test'
        assert c.address == 'cra - test'
        assert c.chamber_commerce == '123123'
        assert c.legal_representative == 'test'
        assert c.operative_years == 5
        assert c.country == 'colombia'
        assert c.city == 'cali'
        assert c.profile_images == [
            "https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-s.png",
            "https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-m.png",
            "https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-b.png"]


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
        validate_data_companies([company_1])
        validate_instance_company([company_1])

    def test_new_company_entity(self):
        company_1 = CompanyNewEntity.parse_obj(self.data_new_company)
        assert company_1.uuid_user == self.generated_uuid
        assert company_1.profile_image == self.data_new_company['profile_image']
        validate_data_companies([company_1])
        validate_instance_company([company_1])

    def test_company_entity(self):
        company_1 = CompanyEntity.parse_obj(self.data_company_entity_v1)
        company_2 = CompanyEntity.parse_obj(self.data_company_entity_v2)
        assert company_1.uuid == self.generated_uuid
        assert company_2.uuid == self.generated_uuid
        validate_data_companies([company_1, company_2])
        validate_instance_company([company_1])

    def test_company_pagination_entity(self):
        company_pagination = CompaniesPaginationEntity.parse_obj(self.data_companies_pagination)
        assert company_pagination.limit == 10
        assert company_pagination.offset == 1
        validate_data_companies(company_pagination.results)
        validate_instance_company(company_pagination.results)
