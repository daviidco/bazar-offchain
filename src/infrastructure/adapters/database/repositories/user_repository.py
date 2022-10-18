from flask_restx import abort
from sqlalchemy.orm import Session

from src.domain.ports.user_interface import IUserRepository
from src.domain.entities.user_entity import UserNewEntity, UserEntity, UsersPaginationEntity
from src.infrastructure.adapters.database.models.user import User
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


class UserRepository(IUserRepository):

    def __init__(self, adapter_db):
        self.engine = adapter_db.engine
        self.session = Session(adapter_db.engine)

    def new_user(self, user_entity: UserNewEntity) -> UserEntity:
        user_exist = self.get_user_by_uuid(user_entity.uuid)
        if user_exist is None:
            object_to_save = User(
                uuid=user_entity.uuid,
                rol=user_entity.rol,
            )

            self.session.add(object_to_save)
            self.session.commit()
            return UserEntity.from_orm(object_to_save)
        else:
            e = api_error('UserExistingError')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_user_by_uuid(self, uuid: str) -> UserEntity:
        found_object = self.session.query(User).filter_by(uuid=uuid).first()
        found_object = UserEntity.from_orm(found_object) if found_object is not None else None
        return found_object

    def get_users_count(self) -> int:
        count = self.session.query(User).count()
        count = count if count is not None else 0
        return count

    def get_all_users(self, limit: int, offset: int) -> UsersPaginationEntity:
        total = self.get_users_count()
        list_objects = self.session.query(User).offset(offset).limit(limit).all()
        return UsersPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects)

