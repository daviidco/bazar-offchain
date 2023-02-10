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

from typing import List
from uuid import UUID

from pydantic import BaseModel


#
# These classes lets define the successful order to buyer and seller entities of domain.
# @author David Córdoba
#

class OrderBaseEntity(BaseModel):
    uuid_product: UUID
    uuid_buyer: UUID
    amount: str
    value_x_kg: str
    total_pay_bnb: str
    total_pay_usd: str
    date: str


class SuccessfulOrderBuyerEntity(OrderBaseEntity):
    payment_method: str
    order_code: str
    exchange_rate: str
    service_fee: str


class SuccessfulOrderSellerEntity(OrderBaseEntity):
    uuid_incoterm: str
