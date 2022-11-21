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

from flask_restx import abort
from sqlalchemy.orm import Session

from src.domain.ports.user_interface import IUserRepository
from src.domain.entities.user_entity import UserNewEntity, UserEntity, UsersPaginationEntity
from src.infrastructure.adapters.database.models.user import User
from src.infrastructure.adapters.database.repositories.utils import get_user_names
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


#
# This repository contains logic main related with user.
# @author David Córdoba
#
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
        if found_object is None:
            e = api_error('ObjectNotFound')
            abort(code=e.status_code, message=e.message, error=e.error)
        return found_object

    def get_users_count(self) -> int:
        count = self.session.query(User).count()
        count = count if count is not None else 0
        return count

    def get_all_users(self, limit: int, offset: int, jwt: str) -> UsersPaginationEntity:
        total = self.get_users_count()
        list_objects = self.session.query(User).offset(offset).limit(limit).all()
        response = UsersPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects)

        # Exclude profile_images

        for idx_r, x in enumerate(response.results):
            # Call endpoint to get user_name microservice auth
            first_name, last_name = get_user_names(jwt, response.results[idx_r].uuid)
            response.results[idx_r].first_name = first_name
            response.results[idx_r].last_name = last_name
            for idx_c, y in enumerate(x.company):
                try:
                    response.results[idx_r].company[0] = y.dict(exclude={'profile_images'})

                except Exception as e:
                    continue


        return response
