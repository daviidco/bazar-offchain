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
from datetime import date
from typing import List

from src.domain.entities.incoterm_entity import IncotermEntity
from src.domain.entities.product_entity import ProductEntity, ProductBaseEntity, ProductsPaginationEntity, \
    ProductNewEntity
from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationEntity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#


def validate_instance_products(products):
    for p in products:
        assert isinstance(p.basic_product_uuid, uuid.UUID)
        assert isinstance(p.product_type_uuid, uuid.UUID)
        assert isinstance(p.variety_uuid, uuid.UUID)
        assert isinstance(p.capacity_per_year, float)
        assert isinstance(p.date_in_port, date)
        assert isinstance(p.guild_or_association, str)
        assert isinstance(p.available_for_sale, float)
        assert isinstance(p.minimum_order_uuid, uuid.UUID)
        assert isinstance(p.expected_price_per_kg, float)
        assert isinstance(p.assistance_logistic, bool)
        assert isinstance(p.additional_description, str)
        # assert isinstance(p.incoterms_uuid, List)
        # assert isinstance(p.sustainability_certifications_uuid, List)


class TestProductEntity:
    generated_uuid = uuid.uuid4()

    data_base_product = {'basic_product_uuid': generated_uuid,
                         'product_type_uuid': generated_uuid,
                         'variety_uuid': generated_uuid,
                         'capacity_per_year': 5,
                         'date_in_port': date(2017, 11, 17),
                         'guild_or_association': 'test',
                         'available_for_sale': 5.3,
                         'minimum_order_uuid': generated_uuid,
                         'expected_price_per_kg': 435.3,
                         'assistance_logistic': True,
                         'additional_description': 'Description test',
                         }

    data_new_product_aux = {
        'incoterms_uuid': [generated_uuid, generated_uuid],
        'sustainability_certifications_uuid': [generated_uuid, generated_uuid],
        'uuid_user': generated_uuid}

    data_new_product = dict(data_base_product, **data_new_product_aux)

    data_product_entity_aux = {'uuid': generated_uuid,
                               'url_images': [
                                   "https://s3-offchain-test.s3.us-east-2.amazonaws.com/buyer/"
                                   "6ebb797c-b204-46f0-8086-f3ca298f1b5a/product_images/"
                                   "2022/month-11/day-15/05-33-51/coffe.jpg",
                                   "https://s3-offchain-test.s3.us-east-2.amazonaws.com/buyer/"
                                   "6ebb797c-b204-46f0-8086-f3ca298f1b5a/product_images/"
                                   "2022/month-11/day-15/05-33-51/coffe2.jpg"],
                               'url_files': [
                                   "https://s3-offchain-test.s3.us-east-2.amazonaws.com/buyer/"
                                   "6ebb797c-b204-46f0-8086-f3ca298f1b5a/documents_product/"
                                   "2022/month-11/day-15/05-33-51/ISO-9001-IQ-NET-certificate.pdf",
                                   "https://s3-offchain-test.s3.us-east-2.amazonaws.com/buyer/"
                                   "6ebb797c-b204-46f0-8086-f3ca298f1b5a/documents_product/"
                                   "2022/month-11/day-15/05-33-51/ISO-9001-2008-Quality-Certificate-Melexis.pdf"],
                               'status': 'pending',
                               'incoterms': [
                                   {'incoterm': 'Delivery at place (DAP)',
                                    'uuid': 'd34b8d04-e1bd-497c-a657-388c9eea7151'}],

                               'sustainability_certifications': [
                                   {'certification': 'ISO 14001', 'uuid': 'b1e99725-6ff0-40a0-8b69-c7d8424d57ed'}]}

    data_product_entity_v1 = dict(data_base_product, **data_product_entity_aux)

    data_product_entity_v2 = dict(data_base_product, **data_product_entity_aux)

    data_product_pagination = {'limit': 10,
                               'offset': 1,
                               'total': 100,
                               'results': [data_product_entity_v1, data_product_entity_v2]}

    def validate_data_products(self, products):
        for p in products:
            assert p.basic_product_uuid == self.data_base_product['basic_product_uuid']
            assert p.product_type_uuid == self.data_base_product['product_type_uuid']
            assert p.variety_uuid == self.data_base_product['variety_uuid']
            assert p.capacity_per_year == self.data_base_product['capacity_per_year']
            assert p.date_in_port == self.data_base_product['date_in_port']
            assert p.guild_or_association == self.data_base_product['guild_or_association']
            assert p.available_for_sale == self.data_base_product['available_for_sale']
            assert p.minimum_order_uuid == self.data_base_product['minimum_order_uuid']
            assert p.expected_price_per_kg == self.data_base_product['expected_price_per_kg']
            assert p.assistance_logistic == self.data_base_product['assistance_logistic']
            assert p.additional_description == self.data_base_product['additional_description']
            # assert p.incoterms_uuid == self.data_base_product['incoterms_uuid']
            # assert p.sustainability_certifications_uuid == self.data_base_product['sustainability_certifications_uuid']

    def test_base_product_entity(self):
        product_1 = ProductBaseEntity.parse_obj(self.data_base_product)
        self.validate_data_products([product_1])
        validate_instance_products([product_1])

    def test_new_product_entity(self):
        product_1 = ProductNewEntity.parse_obj(self.data_new_product)
        assert product_1.uuid_user == self.generated_uuid
        assert product_1.incoterms_uuid == self.data_new_product['incoterms_uuid']
        assert product_1.sustainability_certifications_uuid == self.data_new_product['sustainability_' \
                                                                                     'certifications_uuid']
        assert isinstance(product_1.incoterms_uuid, List)
        assert isinstance(product_1.sustainability_certifications_uuid, List)
        self.validate_data_products([product_1])
        validate_instance_products([product_1])

    def test_product_entity(self):
        product_1 = ProductEntity.parse_obj(self.data_product_entity_v1)
        product_2 = ProductEntity.parse_obj(self.data_product_entity_v2)
        products = [product_1, product_2]
        assert product_1.url_images == self.data_product_entity_v1['url_images']
        assert product_1.url_files == self.data_product_entity_v1['url_files']
        assert product_2.url_images == self.data_product_entity_v1['url_images']
        assert product_2.url_files == self.data_product_entity_v1['url_files']

        assert product_1.incoterms == [IncotermEntity.parse_obj(self.data_product_entity_v1['incoterms'][0])]
        assert product_1.sustainability_certifications == [SustainabilityCertificationEntity.
                                                           parse_obj(self.data_product_entity_v1['sustainability_' \
                                                                                      'certifications'][0])]
        assert product_2.incoterms == [IncotermEntity.parse_obj(self.data_product_entity_v2['incoterms'][0])]
        assert product_2.sustainability_certifications == [SustainabilityCertificationEntity.
                                                           parse_obj(self.data_product_entity_v2['sustainability_' \
                                                                                                 'certifications'][0])]

        assert isinstance(product_1.incoterms, List)
        assert isinstance(product_1.sustainability_certifications, List)

        assert isinstance(product_2.incoterms, List)
        assert isinstance(product_2.sustainability_certifications, List)

        self.validate_data_products(products)
        validate_instance_products(products)

    def test_product_pagination_entity(self):
        product_pagination = ProductsPaginationEntity.parse_obj(self.data_product_pagination)
        assert product_pagination.limit == 10
        assert product_pagination.offset == 1
        self.validate_data_products(product_pagination.results)
        validate_instance_products(product_pagination.results)