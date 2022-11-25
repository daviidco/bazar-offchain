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
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Numeric, Date, Boolean, Text
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from src.infrastructure.adapters.database.models.model_base import base
from src.infrastructure.config.default_infra import UTC_TIME_ZONE


#
# These models are related with product model they are defined to create database table.
# @author David Córdoba
#

class BasicProduct(base):
    __tablename__ = 'basic_products'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    basic_product = Column(String(50), nullable=False, unique=True)

    def __init__(self, basic_product):
        self.basic_product = basic_product

    def __repr__(self):
        return f'<Basic Product {self.id}>'

    def __str__(self):
        return f'{self.id}: {self.basic_product}'


class ProductType(base):
    __tablename__ = 'products_type'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    product_type = Column(String(50), nullable=False)
    basic_product_id = Column(Integer, ForeignKey("basic_products.id"))

    # Relationship
    basic_product = relationship("BasicProduct", backref="products_type")

    def __init__(self, product_type):
        self.product_type = product_type

    def __repr__(self):
        return f'<Product Type {self.product_type}>'

    def __str__(self):
        return f'{self.id}: {self.product_type}'


class Variety(base):
    __tablename__ = 'varieties'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    variety = Column(String(50), nullable=False, unique=True)
    basic_product_id = Column(Integer, ForeignKey("basic_products.id"))

    # Relationship
    basic_product = relationship("BasicProduct", backref="varieties")

    def __init__(self, variety):
        self.variety = variety

    def __repr__(self):
        return f'<Variety {self.id}>'

    def __str__(self):
        return f'{self.id}: {self.variety}'


class MinimumOrder(base):
    __tablename__ = 'minimums_order'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    minimum_order = Column(String(50), nullable=False, unique=True)

    def __init__(self, minimum_order):
        self.minimum_order = minimum_order

    def __repr__(self):
        return f'<Minimum order {self.id}>'

    def __str__(self):
        return f'{self.id}: {self.minimum_order}'


class Incoterm(base):
    __tablename__ = 'incoterms'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    incoterm = Column(String(50), nullable=False, unique=True)

    def __init__(self, incoterm):
        self.incoterm = incoterm

    def __repr__(self):
        return f'<Incoterm {self.id}>'

    def __str__(self):
        return f'{self.id}: {self.incoterm}'


class StatusProduct(base):
    __tablename__ = 'status_product'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    status_product = Column(String(50), nullable=False, unique=True)
    description = Column(String(250))


class ProductImage(base):
    __tablename__ = "product_images"
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    name = Column(String(250))
    product_id = Column(ForeignKey("products.id"))
    url = Column(String(250))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(UTC_TIME_ZONE), nullable=False)


class ProductIncoterm(base):
    __tablename__ = "product_incoterms"
    product_id = Column(ForeignKey("products.id"), primary_key=True)
    incoterm_id = Column(ForeignKey("incoterms.id"), primary_key=True)

    # Relationship
    product = relationship("Product", viewonly=True)
    incoterm = relationship("Incoterm", viewonly=True)

    def __init__(self, product_id, incoterm_id):
        self.product_id = product_id
        self.incoterm_id = incoterm_id


# Relationship MANY TO MANY
# ProductCertification ->Association
# Product -> Parent
# SustainabilityCertification -> Child

class Product(base):
    # Don't forget import model in __all_models.py
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    status_id = Column(Integer, ForeignKey("status_product.id"), default=1)

    basic_product_id = Column(Integer, ForeignKey("basic_products.id"))
    product_type_id = Column(Integer, ForeignKey("products_type.id"), default=1)
    variety_id = Column(Integer, ForeignKey("varieties.id"), default=1)

    capacity_per_year = Column(Integer, nullable=False)
    date_in_port = Column(Date, nullable=False)
    guild_or_association = Column(String(250), nullable=False)
    available_for_sale = Column(Numeric, nullable=False, comment='How much the company has available for sale (kg)')

    minimum_order_id = Column(Integer, ForeignKey("minimums_order.id"), default=1)
    expected_price_per_kg = Column(Numeric, nullable=False, comment='Expected price per kg (USD)')

    assistance_logistic = Column(Boolean, nullable=False)
    additional_description = Column(Text)

    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(UTC_TIME_ZONE), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Relationship
    company = relationship("Company", backref="products")
    status_product = relationship("StatusProduct", backref="products")
    basic_product_r = relationship("BasicProduct", backref="products")
    product_type_r = relationship("ProductType", backref="products")
    variety_r = relationship("Variety", backref="products")
    minimum_order_r = relationship("MinimumOrder", backref="products")
    incoterms = relationship("Incoterm", secondary="product_incoterms")
    sustainability_certifications = relationship("SustainabilityCertification",
                                                 secondary='product_sustainability_certifications')
    product_images = relationship("ProductImage", backref='products')

    # Association Proxy
    status = association_proxy("status_product", "status_product")
    basic_product = association_proxy("basic_product_r", "basic_product")
    basic_product_uuid = association_proxy("basic_product_r", "uuid")
    product_type = association_proxy("product_type_r", "product_type")
    product_type_uuid = association_proxy("product_type_r", "uuid")
    variety = association_proxy("variety_r", "variety")
    variety_uuid = association_proxy("variety_r", "uuid")
    minimum_order = association_proxy("minimum_order_r", "minimum_order")
    minimum_order_uuid = association_proxy("minimum_order_r", "uuid")
    url_avatar = association_proxy("company", "profile_image_url")

    def __init__(self, basic_product_id, product_type_id, variety_id, capacity_per_year, date_in_port,
                 guild_or_association, available_for_sale, minimum_order_id, expected_price_per_kg,
                 assistance_logistic, additional_description, company_id):

        self.basic_product_id = basic_product_id
        self.product_type_id = product_type_id
        self.variety_id = variety_id
        self.capacity_per_year = capacity_per_year
        self.date_in_port = date_in_port
        self.guild_or_association = guild_or_association
        self.available_for_sale = available_for_sale
        self.minimum_order_id = minimum_order_id
        self.expected_price_per_kg = expected_price_per_kg
        self.assistance_logistic = assistance_logistic
        self.additional_description = additional_description
        self.company_id = company_id

    def __repr__(self):
        return f'<Product {self.id}>'

    def __str__(self):
        return f'<Product id:{self.id} - uuid: {self.uuid}>'


class SustainabilityCertification(base):
    __tablename__ = 'sustainability_certifications'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    certification = Column(String(50), nullable=False, unique=True)

    def __init__(self, certification):
        self.certification = certification

    def __repr__(self):
        return f'<Sustainability Certification {self.id}>'

    def __str__(self):
        return f'{self.id}: {self.certification}'


class ProductSustainabilityCertification(base):
    __tablename__ = "product_sustainability_certifications"
    product_id = Column(ForeignKey("products.id"), primary_key=True)
    sustainability_certification_id = Column(ForeignKey("sustainability_certifications.id"), primary_key=True)
    file_id = Column(ForeignKey("product_files.id"), primary_key=True)

    # Relationship
    files = relationship('ProductFile', viewonly=True)
    products = relationship('Product', backref="product_sustainability_certifications", viewonly=True)

    def __init__(self, product_id, sustainability_certification_id, file_id):
        self.product_id = product_id
        self.sustainability_certification_id = sustainability_certification_id
        self.file_id = file_id

    def __repr__(self):
        return f'<File {self.file_id} - certification {self.sustainability_certification_id}>'

    def __str__(self):
        return f'File {self.file_id}: Certification {self.sustainability_certification_id}'


class ProductFile(base):
    # Don't forget import model in __all_models.py
    __tablename__ = 'product_files'
    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)
    name = Column(String(250))
    url = Column(String(250))
    status_file_id = Column(ForeignKey("status_file.id"), nullable=False, default=1)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.now(UTC_TIME_ZONE), nullable=False)

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f'<Product File {self.id}>'

    def __str__(self):
        return f'{self.name}: {self.url}'