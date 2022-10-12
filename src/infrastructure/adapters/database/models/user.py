from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from src.infrastructure.adapters.database.models.model_base import base
from src.infrastructure.config.default_infra import UTC_TIME_ZONE


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
        return f'<User {self.id}>'

    def __str__(self):
        return f'{self.id}: {self.rol}'
