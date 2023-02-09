from unittest.mock import MagicMock

from application import application
from src.domain.ports.wishlist_interface import IWishListRepository
from src.infrastructure.adapters.database.repositories.wishlist_repository import WishListRepository


class TestWishlistRepository:

    def test_wishlist_repository_implementation(self):
        """
        Function to check all methods are implemented
        :return: Error when doesn't pass the test
        """
        # Create an instance of the Repository class
        adapter_db = MagicMock()
        utils_db = MagicMock()
        repository = WishListRepository(adapter_db, utils_db)
        # Check that the instance implements the InterfaceRepository interface
        assert isinstance(repository, IWishListRepository)
        # Check that the instance has the required methods
        list_methods_repository = [func for func in dir(repository) if callable(getattr(repository, func))
                                   and not func.startswith("__")
                                   and not func.startswith("_")
                                   and not func == 'session_maker']
        list_methods_interface = [func for func in dir(IWishListRepository) if callable(getattr(IWishListRepository, func))
                                  and not func.startswith("__")]

        assert list_methods_repository == list_methods_interface
        for m in list_methods_interface:
            assert hasattr(repository, m)
            assert callable(getattr(repository, m))
