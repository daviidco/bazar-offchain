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

from src.domain.entities.order_entity import OrderBaseEntity, SuccessfulOrderBuyerEntity, SuccessfulOrderSellerEntity
from tests.utils import validate_data_entity, validate_instance_properties_entity


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

class TestOrderEntity:
    generated_uuid = uuid.uuid4()

    data_base_order = {'uuid_product': generated_uuid,
                       'uuid_buyer': generated_uuid,
                       'amount': '1000 kg',
                       'value_x_kg': '1.40 kg',
                       'total_pay_bnb': '0.012312 BNB',
                       'total_pay_usd': '140.140 USD',
                       'date': '2 Oct, 2022'}

    data_successful_order_buyer_aux = {'payment_method': 'wallet',
                                       'order_code': 'x98R...235Ra',
                                       'exchange_rate': '1 BNB : 3.320 USD',
                                       'service_fee': '140.0'}

    data_successful_order_seller_aux = {'uuid_incoterm': generated_uuid}

    data_successful_order_buyer = dict(data_base_order, **data_successful_order_buyer_aux)
    data_successful_order_seller = dict(data_base_order, **data_successful_order_seller_aux)

    def test_order_base_entity(self):
        order_1 = OrderBaseEntity.parse_obj(self.data_base_order)
        validate_data_entity([order_1], OrderBaseEntity, [self.data_base_order])
        validate_instance_properties_entity([order_1], OrderBaseEntity)

    def test_successful_order_buyer_entity(self):
        order_1 = SuccessfulOrderBuyerEntity.parse_obj(self.data_successful_order_buyer)
        validate_data_entity([order_1], SuccessfulOrderBuyerEntity, [self.data_successful_order_buyer])
        validate_instance_properties_entity([order_1], SuccessfulOrderBuyerEntity)

    def test_successful_order_seller_entity(self):
        order_1 = SuccessfulOrderSellerEntity.parse_obj(self.data_successful_order_seller)
        validate_data_entity([order_1], SuccessfulOrderSellerEntity, [self.data_successful_order_seller])
        validate_instance_properties_entity([order_1], SuccessfulOrderSellerEntity)
