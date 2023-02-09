from unittest.mock import MagicMock

from application import application
from src.domain.ports.company_interface import ICompanyRepository
from src.infrastructure.adapters.database.repositories.company_repository import CompanyRepository


class TestCompanyRepository:

    def test_company_repository_implementation(self):
        """
        Function to check all methods are implemented
        :return: Error when doesn't pass the test
        """
        # Create an instance of the Repository class
        adapter_db = MagicMock()
        storage_repository = MagicMock()
        repository = CompanyRepository(adapter_db, storage_repository)
        # Check that the instance implements the InterfaceRepository interface
        assert isinstance(repository, ICompanyRepository)
        # Check that the instance has the required methods
        list_methods_repository = [func for func in dir(repository) if callable(getattr(repository, func))
                                   and not func.startswith("__")
                                   and not func.startswith("_")
                                   and not func == 'session_maker']
        list_methods_interface = [func for func in dir(ICompanyRepository) if callable(getattr(ICompanyRepository, func))
                                  and not func.startswith("__")]

        assert list_methods_repository == list_methods_interface
        for m in list_methods_interface:
            assert hasattr(repository, m)
            assert callable(getattr(repository, m))
