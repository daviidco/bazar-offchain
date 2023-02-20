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
from inspect import signature
from unittest.mock import patch

from src.domain.ports.user_interface import IUserRepository
from src.domain.ports.avatar_interface import IAvatarRepository
from src.domain.ports.company_interface import ICompanyRepository
from src.domain.ports.product_interface import IProductRepository
from src.domain.ports.object_file_interface import IStorage


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#

def validate_not_implemented(list_methods, interface):
    for m in list_methods:
        try:
            sig = signature(getattr(interface, m))
            params = tuple(sig.parameters)
            getattr(interface, m)(*params)
            assert True, f"Method {m} from {interface} is ok"

        except Exception as e:
            if str(e) != 'Not implemented method':
                assert False, f"Interface {interface.__module__} has method {m} implemented"


class TestInterfaces:
    @patch("src.domain.ports.user_interface.IUserRepository.__abstractmethods__", set())
    @patch("src.domain.ports.avatar_interface.IAvatarRepository.__abstractmethods__", set())
    @patch("src.domain.ports.company_interface.ICompanyRepository.__abstractmethods__", set())
    @patch("src.domain.ports.product_interface.IProductRepository.__abstractmethods__", set())
    @patch("src.domain.ports.object_file_interface.IStorage.__abstractmethods__", set())
    def test_interfaces(self):
        i_user = IUserRepository()
        i_avatar = IAvatarRepository()
        i_company = ICompanyRepository()
        i_product = IProductRepository()
        i_storage = IStorage()

        list_methods_i_user = [method for method in dir(i_user) if method.startswith('_') is False]
        list_methods_i_avatar = [method for method in dir(i_avatar) if method.startswith('_') is False]
        list_methods_i_company = [method for method in dir(i_company) if method.startswith('_') is False]
        list_methods_i_product = [method for method in dir(i_product) if method.startswith('_') is False]
        list_methods_i_storage = [method for method in dir(i_storage) if method.startswith('_') is False]

        validate_not_implemented(list_methods_i_user, i_user)
        validate_not_implemented(list_methods_i_avatar, i_avatar)
        validate_not_implemented(list_methods_i_company, i_company)
        validate_not_implemented(list_methods_i_product, i_product)
        validate_not_implemented(list_methods_i_storage, i_storage)