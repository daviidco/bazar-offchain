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

from typing import Union

from sqlalchemy.orm import Session

from src.domain.entities.avatar_entity import AvatarsPaginationEntity, AvatarEntity, AvatarNewEntity, AvatarsListEntity
from src.domain.ports.avatar_interface import IAvatarRepository
from src.infrastructure.adapters.database.models.company import ProfileImage
from src.infrastructure.adapters.database.repositories.utils import get_total_pages


#
# This repository contains logic main related with avatar.
# @author David Córdoba
#

class AvatarRepository(IAvatarRepository):

    def __init__(self, logger, adapter_db):
        self.logger = logger
        self.engine = adapter_db.engine
        self.session = Session(adapter_db.engine)

    def new_avatar(self, avatar_entity: AvatarNewEntity) -> AvatarEntity:
        pass

    def get_avatar_by_uuid(self, uuid: str) -> AvatarEntity:
        pass

    def get_avatars_count(self) -> int:
        count = self.session.query(ProfileImage).count()
        count = count if count is not None else 0
        return count

    def get_all_avatars(self, limit: int = None, offset: int = None) -> \
            Union[AvatarsListEntity, AvatarsPaginationEntity]:
        total = self.get_avatars_count()
        list_objects = self.session.query(ProfileImage).offset(offset).limit(limit).all()
        if limit is not None and offset is not None:
            total_pages = get_total_pages(total, int(limit))
            return AvatarsPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects,
                                           total_pages=total_pages)
        else:
            return AvatarsListEntity(results=list_objects)
