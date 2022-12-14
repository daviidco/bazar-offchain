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

from src.domain.entities.product_entity import ProductEntity, ProductBaseEntity, ProductsPaginationEntity, \
    ProductNewEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

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
                               'basic_product': 'Coffee',
                               'minimum_order': 'A Continer',
                               'product_type': 'Beans',
                               'variety': 'Criollo',
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
                                   {'certification': 'ISO 14001', 'uuid': 'b1e99725-6ff0-40a0-8b69-c7d8424d57ed'}],
                               'is_liked': True}

    data_product_entity_aux_2 = {'uuid': generated_uuid,
                                 'basic_product': 'Coffee',
                                 'minimum_order': 'A Continer',
                                 'product_type': 'Beans',
                                 'variety': 'Criollo',
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
                                     {'certification': 'ISO 14001', 'uuid': 'b1e99725-6ff0-40a0-8b69-c7d8424d57ed'}],
                                 'url_avatar': "https://s3-offchain-test.s3.us-east-2.amazonaws.com/"
                                               "profile_images/astronaut-s.png",
                                 'is_liked': False}

    data_product_entity_v1 = dict(data_base_product, **data_product_entity_aux)

    data_product_entity_v2 = dict(data_base_product, **data_product_entity_aux_2)

    data_product_pagination = {'limit': 10,
                               'offset': 1,
                               'total': 100,
                               'results': [data_product_entity_v1, data_product_entity_v2],
                               'total_pages': 10}

    def test_base_product_entity(self):
        product_1 = ProductBaseEntity.parse_obj(self.data_base_product)
        validate_data_entity([product_1], ProductBaseEntity, [self.data_base_product])
        validate_instance_properties_entity([product_1], ProductBaseEntity)

    def test_new_product_entity(self):
        product_1 = ProductNewEntity.parse_obj(self.data_new_product)
        validate_data_entity([product_1], ProductNewEntity, [self.data_new_product])
        validate_instance_properties_entity([product_1], ProductNewEntity)

    def test_product_entity(self):
        product_1 = ProductEntity.parse_obj(self.data_product_entity_v1)
        product_2 = ProductEntity.parse_obj(self.data_product_entity_v2)
        products = [product_1, product_2]
        validate_data_entity(products, ProductEntity, [self.data_product_entity_v1, self.data_product_entity_v2])
        validate_instance_properties_entity(products, ProductEntity)

    def test_product_pagination_entity(self):
        product_pagination = ProductsPaginationEntity.parse_obj(self.data_product_pagination)
        validate_data_entity([product_pagination], ProductsPaginationEntity, [self.data_product_pagination])
        validate_instance_properties_entity([product_pagination], ProductsPaginationEntity)
