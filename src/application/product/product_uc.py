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

from src.domain.entities.basic_product_entity import ProductsBaseList
from src.domain.ports.basic_product_interface import IBasicProductRepository


#
# These classes lets define the product user cases.
# @author David Córdoba
#


class GetAllUsers:
    @inject.autoparams('product_base_repository')
    def __init__(self, product_base_repository: IBasicProductRepository):
        self.__product_base_repository = product_base_repository

    def execute(self) -> ProductsBaseList:
        return self.__product_base_repository.get_all_basic_products()



