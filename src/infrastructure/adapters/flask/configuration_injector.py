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
from flask import Flask

from src.domain.ports.avatar_interface import IAvatarRepository
from src.domain.ports.company_interface import ICompanyRepository
from src.domain.ports.product_interface import IProductRepository
from src.domain.ports.user_interface import IUserRepository
from src.infrastructure.adapters.database.adapter_postgresql import PostgresAdapter
from src.infrastructure.adapters.database.repositories.avatar_repository import AvatarRepository
from src.infrastructure.adapters.database.repositories.company_repository import CompanyRepository
from src.infrastructure.adapters.database.repositories.product_repository import ProductRepository
from src.infrastructure.adapters.database.repositories.user_repository import UserRepository
from src.infrastructure.adapters.database.repositories.utils import UtilsDatabase
from src.infrastructure.adapters.storage.s3_service import S3Repository

#
# This file contains the injections
# @author David Córdoba
#


def configure_inject(logger) -> None:
    def config(binder: inject.Binder) -> None:
        psql_adapter = PostgresAdapter()
        utils_db = UtilsDatabase(logger, psql_adapter)
        binder.bind(IUserRepository, UserRepository(logger, psql_adapter, utils_db))
        binder.bind(ICompanyRepository, CompanyRepository(logger, psql_adapter, S3Repository(logger)))
        binder.bind(IAvatarRepository, AvatarRepository(logger, psql_adapter))
        binder.bind(IProductRepository, ProductRepository(logger, psql_adapter, S3Repository(logger), utils_db))

    inject.configure(config)