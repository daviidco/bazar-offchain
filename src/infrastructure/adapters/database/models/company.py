from datetime import datetime
import uuid

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from src.infrastructure.adapters.database.models.model_base import base
from src.infrastructure.config.default_infra import UTC_TIME_ZONE


class StatusFile(base):
    __tablename__ = 'status_file'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    status_user = Column(String(50), nullable=False, unique=True)
    description = Column(String(250))


class ProfileImage(base):
    # Don't forget import model in __all_models.py
    __tablename__ = 'profile_images'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    image_name = Column(String(250))
    format = Column(String(250))
    image_url = Column(Text, nullable=False)

    def __repr__(self):
        return f'<Profile Image {self.id}>'

    def __str__(self):
        return f'{self.image_name}: {self.url}'


class FilesCompany(base):
    __tablename__ = "files_company"
    company_id = Column(ForeignKey("companies.id"), primary_key=True)
    file_id = Column(ForeignKey("files.id"), primary_key=True)
    status_file_id = Column(ForeignKey("status_file.id"), nullable=False, default=1)

    # Relationship
    files = relationship("File", backref="company_associations")
    company = relationship("Company", backref="file_associations")

    def __repr__(self):
        return f'<File {self.file_id} - Company {self.company_id}>'

    def __str__(self):
        return f'Company {self.company_id}: File {self.file_id}'


class Company(base):
    # Don't forget import model in __all_models.py
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    company_name = Column(String(250))
    address = Column(String(250), nullable=False)
    chamber_commerce = Column(String(20))
    legal_representative = Column(String(250))
    operative_years = Column(Integer)
    country = Column(String(250))
    city = Column(String(250))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    profile_image_id = Column(Integer, ForeignKey("profile_images.id"))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(UTC_TIME_ZONE), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.now(UTC_TIME_ZONE), nullable=False)

    # Relationship
    user_r = relationship("User", backref="companies")
    image_profile_r = relationship("ProfileImage", backref="companies")
    files = relationship("File", secondary='files_company')

    # Association Proxy
    profile_image_url = association_proxy("profile_images", "image_url")

    def __init__(self, company_name, address, chamber_commerce, legal_representative,
                 operative_years, country, city, user_id, profile_image_id):

        self.company_name = company_name
        self.address = address
        self.chamber_commerce = chamber_commerce
        self.legal_representative = legal_representative
        self.operative_years = operative_years
        self.country = country
        self.city = city
        self.user_id = user_id
        self.profile_image_id = profile_image_id

    def __repr__(self):
        return f'<Company {self.id}>'

    def __str__(self):
        return f'{self.company_name}: {self.chamber_commerce}'

class File(base):
    # Don't forget import model in __all_models.py
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    name = Column(String(250))
    url = Column(String(250))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(UTC_TIME_ZONE), nullable=False)

    def __repr__(self):
        return f'<File {self.id}>'

    def __str__(self):
        return f'{self.name}: {self.url}'
