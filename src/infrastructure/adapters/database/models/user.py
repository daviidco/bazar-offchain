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

from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from src.infrastructure.adapters.database.models.model_base import base
from src.infrastructure.config.default_infra import UTC_TIME_ZONE


#
# These models are related with user model they are defined to create database table.
# @author David Córdoba
#

class StatusUser(base):
    __tablename__ = 'status_user'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    status_user = Column(String(50), nullable=False, unique=True)
    description = Column(String(250))


class User(base):
    # Don't forget import model in __all_models.py
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    rol = Column(String(250))
    status_id = Column(Integer, ForeignKey("status_user.id"), default=1)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(UTC_TIME_ZONE), nullable=False)

    # Relationship
    status_user = relationship("StatusUser", backref="users")

    # Association Proxy
    status = association_proxy("status_user", "status_user")

    def __init__(self, uuid, rol):
        self.uuid = uuid
        self.rol = rol

    def __repr__(self):
        return f'<User uuid: {self.uuid}, id:{self.id}, rol:{self.rol}, state:{self.status_user}>'

    def __str__(self):
        return f'<User uuid: {self.uuid}, id:{self.id}, rol:{self.rol}, state:{self.status_user}>'
