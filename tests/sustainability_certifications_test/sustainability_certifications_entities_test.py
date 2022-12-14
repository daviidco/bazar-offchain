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

from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationBaseEntity, \
    SustainabilityCertificationEntity, SustainabilityCertificationsListEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

class TestSustainabilityCertificationEntity:
    generated_uuid = uuid.uuid4()

    data_SustainabilityCertificationBaseEntity = {'certification': 'name certification'}
    data_SustainabilityCertificationEntity_v1 = {
        'uuid': generated_uuid,
        'certification': 'name certification'}

    data_SustainabilityCertificationEntity_v2 = {
        'uuid': generated_uuid,
        'certification': 'name two certification'}

    data_SustainabilityCertificationsListEntity = {'results': [data_SustainabilityCertificationEntity_v1, 
                                                               data_SustainabilityCertificationEntity_v2]}

    def test_sustainability_certification_base_entity(self):
        sustainability_certification_1 = SustainabilityCertificationBaseEntity.parse_obj(
            self.data_SustainabilityCertificationBaseEntity)
        validate_data_entity([sustainability_certification_1], SustainabilityCertificationBaseEntity, 
                             [self.data_SustainabilityCertificationBaseEntity])
        validate_instance_properties_entity([sustainability_certification_1], SustainabilityCertificationBaseEntity)

    def test_sustainability_certification_entity(self):
        sustainability_certification_1 = SustainabilityCertificationEntity.parse_obj(
            self.data_SustainabilityCertificationEntity_v1)
        sustainability_certification_2 = SustainabilityCertificationEntity.parse_obj(
            self.data_SustainabilityCertificationEntity_v2)
        base_products = [sustainability_certification_1, sustainability_certification_2]
        validate_data_entity(base_products, SustainabilityCertificationEntity, 
                             [self.data_SustainabilityCertificationEntity_v1,
                              self.data_SustainabilityCertificationEntity_v2])
        validate_instance_properties_entity(base_products, SustainabilityCertificationEntity)

    def test_sustainability_certification_pagination_entity(self):
        sustainability_certification_pagination = SustainabilityCertificationsListEntity.parse_obj(
            self.data_SustainabilityCertificationsListEntity)
        validate_data_entity([sustainability_certification_pagination], SustainabilityCertificationsListEntity, 
                             [self.data_SustainabilityCertificationsListEntity])
        validate_instance_properties_entity([sustainability_certification_pagination],
                                            SustainabilityCertificationsListEntity)
