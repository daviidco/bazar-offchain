from unittest.mock import MagicMock

from application import application
from src.domain.ports.product_interface import IProductRepository
from src.infrastructure.adapters.database.repositories.product_repository import ProductRepository


class TestProductRepository:

    def test_product_repository_implementation(self):
        """
        Function to check all methods are implemented
        :return: Error when doesn't pass the test
        """
        # Create an instance of the Repository class
        adapter_db = MagicMock()
        storage_repository = MagicMock()
        utils_db = MagicMock()
        repository = ProductRepository(adapter_db, storage_repository, utils_db)
        # Check that the instance implements the InterfaceRepository interface
        assert isinstance(repository, IProductRepository)
        # Check that the instance has the required methods
        list_methods_repository = [func for func in dir(repository) if callable(getattr(repository, func))
                                   and not func.startswith("__")
                                   and not func.startswith("_")
                                   and not func == 'session_maker']
        list_methods_interface = [func for func in dir(IProductRepository) if callable(getattr(IProductRepository, func))
                                  and not func.startswith("__")]

        assert list_methods_repository == list_methods_interface
        for m in list_methods_interface:
            assert hasattr(repository, m)
            assert callable(getattr(repository, m))
