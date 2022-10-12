import inject
from flask import Flask

from src.domain.ports.company_interface import ICompanyRepository
from src.domain.ports.object_file_interface import IStorage
from src.domain.ports.user_interface import IUserRepository
from src.infrastructure.adapters.database.adapter_postgresql import PostgresAdapter
from src.infrastructure.adapters.database.repositories.company_repository import CompanyRepository
from src.infrastructure.adapters.database.repositories.user_repository import UserRepository
from src.infrastructure.adapters.storage.s3_service import S3Repository


def configure_inject(application: Flask) -> None:
    def config(binder: inject.Binder) -> None:
        psql_adapter = PostgresAdapter()
        binder.bind(IUserRepository, UserRepository(psql_adapter))
        binder.bind(ICompanyRepository, CompanyRepository(psql_adapter, S3Repository()))
        # binder.bind(IStorage, S3Repository)
        # binder.bind(IStorage, CompanyRepository(psql_adapter.session))

    inject.configure(config)