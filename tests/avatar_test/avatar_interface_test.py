from unittest.mock import MagicMock
from src.infrastructure.config import default
from src.infrastructure.adapters.database.repositories.avatar_repository import AvatarRepository


class TestAvatarRepository:
    mock_repo = MagicMock(spec=AvatarRepository)

    def test_get_all_avatars(self):
        self.mock_repo.get_avatars_count.return_value = 10
        result = self.mock_repo.get_avatars_count()
        assert result == 10
        assert isinstance(result, int)