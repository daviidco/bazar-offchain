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

from src.domain.entities.basic_product_entity import ProductsBaseList


#
# This interface or port lets define the methods to implement by basic_product_repository.
# @author David Córdoba
#
class IBasicProductRepository(ABC):

    @abstractmethod
    def get_all_basic_products(self) -> ProductsBaseList:
        raise Exception('Not implemented method')
