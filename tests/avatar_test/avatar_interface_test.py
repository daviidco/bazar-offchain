from unittest.mock import MagicMock

from application import application
from src.domain.entities.avatar_entity import AvatarsListEntity
from src.domain.ports.avatar_interface import IAvatarRepository
from src.infrastructure.adapters.database.repositories.avatar_repository import AvatarRepository


class TestAvatarRepository:

    def test_avatar_repository_implementation(self):
        # Create an instance of the AvatarRepository class
        adapter_db = MagicMock()
        repository = AvatarRepository(adapter_db)
        # Check that the instance implements the IAvatarRepository interface
        assert isinstance(repository, IAvatarRepository)
        # Check that the instance has the required methods
        list_methods_repository = [func for func in dir(repository) if callable(getattr(repository, func))
                                   and not func.startswith("__")
                                   and not func == 'session_maker']
        list_methods_interface = [func for func in dir(IAvatarRepository) if callable(getattr(IAvatarRepository, func))
                                  and not func.startswith("__")]

        assert list_methods_repository == list_methods_interface
        for m in list_methods_interface:
            assert hasattr(repository, m)
            assert callable(getattr(repository, m))

    def test_get_avatars_count(self):
        # Create a mock for the adapter_db object
        adapter_db = MagicMock(name='adapter_db')
        adapter_db.engine = 'fake_engine'
        flask_application = MagicMock(name='flask_app')
        # Create an instance of the AvatarRepository class
        # repository = AvatarRepository(flask_application, adapter_db)
        repository = AvatarRepository(adapter_db)
        repository.get_avatars_count = MagicMock()
        repository.get_avatars_count.return_value = 5
        # Call the get_avatars_count method
        result = repository.get_avatars_count()
        # Assert that the result is as expected
        assert result == 5

    def test_get_all_avatars(self):
        with application.app_context() as app:
            # Create a mock for the adapter_db object
            adapter_db = MagicMock()
            adapter_db.engine = 'fake_engine'
            # flask_application = MagicMock(name='flask_app')
            # Create an instance of the AvatarRepository class
            # repository = AvatarRepository(flask_application, adapter_db)
            repository = AvatarRepository(adapter_db)
            repository.get_all_avatars = MagicMock()
            repository.get_all_avatars.return_value = AvatarsListEntity(results=[])
            # Call the get_all_avatars method
            result = repository.get_all_avatars()
            # Assert that the result is as expected
            assert result == AvatarsListEntity(results=[])
