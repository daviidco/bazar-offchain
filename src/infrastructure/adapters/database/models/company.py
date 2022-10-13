from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from src.infrastructure.adapters.database.models.model_base import base
from src.infrastructure.config.default_infra import UTC_TIME_ZONE


class Company(base):
    # Don't forget import model in __all_models.py
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=str(uuid4()))
    company_name = Column(String(250))
    address = Column(String(250), nullable=False)
    chamber_commerce = Column(String(20))
    legal_representative = Column(String(250))
    operative_years = Column(Integer)
    country = Column(String(250))
    city = Column(String(250))
    path_photo_profile = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(UTC_TIME_ZONE), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(UTC_TIME_ZONE), nullable=False)

    # Relationship
    company = relationship("User", backref="companies")

    def __init__(self, company_name, address, chamber_commerce, legal_representative,
                 operative_years, country, city, user_id):

        self.company_name = company_name
        self.address = address
        self.chamber_commerce = chamber_commerce
        self.legal_representative = legal_representative
        self.operative_years = operative_years
        self.country = country
        self.city = city
        self.user_id = user_id

    def __repr__(self):
        return f'<Company {self.id}>'

    def __str__(self):
        return f'{self.company_name}: {self.chamber_commerce}'
