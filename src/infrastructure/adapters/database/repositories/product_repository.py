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

from flask_restx import abort
from sqlalchemy.orm import Session

from src.domain.entities.basic_product_entity import BasicProductsListEntity, BasicProductEntity
from src.domain.entities.company_entity import CompanyEntity, CompanyNewEntity, CompaniesPaginationEntity
from src.domain.entities.incoterm_entity import IncotermsListEntity, IncotermEntity
from src.domain.entities.minimum_order_entity import MinimumOrderEntity, MinimumOrderListEntity
from src.domain.entities.product_entity import ProductEntity, ProductsPaginationEntity, ProductNewEntity, \
    ProductsListEntity
from src.domain.entities.product_type_entity import ProductTypesListEntity, ProductTypeEntity
from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationsListEntity, \
    SustainabilityCertificationEntity
from src.domain.entities.variety_entity import VarietiesListEntity, VarietyEntity
from src.domain.ports.product_interface import IProductRepository
from src.infrastructure.adapters.database.models.product import Product, BasicProduct, ProductType, Variety, \
    MinimumOrder, Incoterm, SustainabilityCertification, ProductFile, ProductSustainabilityCertification
from src.infrastructure.adapters.database.models.company import Company, ProfileImage, FilesCompany, File
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


#
# This repository contains logic main related with product.
# @author David Córdoba
#

class ProductRepository(IProductRepository):

    def __init__(self, adapter_db, storage_repository):
        self.engine = adapter_db.engine
        self.session = Session(adapter_db.engine)
        self.__storage_repository = storage_repository

    def get_basic_product_by_uuid(self, uuid: str) -> BasicProductEntity:
        basic_product = self.session.query(BasicProduct).filter_by(uuid=uuid).first()
        if basic_product is not None:
            return basic_product
        else:
            e = api_error('ObjectNotFound')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_product_type_by_uuid(self, uuid: str) -> ProductTypeEntity:
        product_type = self.session.query(ProductType).filter_by(uuid=uuid).first()
        if product_type is not None:
            return product_type
        else:
            e = api_error('ObjectNotFound')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_variety_by_uuid(self, uuid: str) -> VarietyEntity:
        variety = self.session.query(Variety).filter_by(uuid=uuid).first()
        if variety is not None:
            return variety
        else:
            e = api_error('ObjectNotFound')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_minimum_order_by_uuid(self, uuid: str) -> MinimumOrderEntity:
        minimum_order = self.session.query(MinimumOrder).filter_by(uuid=uuid).first()
        if minimum_order is not None:
            return minimum_order
        else:
            e = api_error('ObjectNotFound')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_incoterm_by_uuid(self, uuid: str) -> IncotermEntity:
        incoterm = self.session.query(Incoterm).filter_by(uuid=uuid).first()
        if incoterm is not None:
            return incoterm
        else:
            e = api_error('ObjectNotFound')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_sustainability_certifications_by_uuid(self, uuid: str) -> SustainabilityCertificationEntity:
        sustainability_certification = self.session.query(SustainabilityCertification).filter_by(uuid=uuid).first()
        if sustainability_certification is not None:
            return sustainability_certification
        else:
            e = api_error('ObjectNotFound')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_basic_product_id_by_uuid(self, uuid: str) -> BasicProductEntity:
        basic_product = self.session.query(BasicProduct).filter_by(uuid=uuid).first()
        if basic_product is not None:
            basic_product_id = basic_product.id
            return basic_product_id
        else:
            e = api_error('BasicProductNotExists')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_product_type_id_by_uuid(self, uuid: str) -> ProductTypeEntity:
        product_type = self.session.query(ProductType).filter_by(uuid=uuid).first()
        if product_type is not None:
            product_type_id = product_type.id
            return product_type_id
        else:
            e = api_error('ProductTypeNotExists')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_variety_id_by_uuid(self, uuid: str) -> VarietyEntity:
        variety = self.session.query(Variety).filter_by(uuid=uuid).first()
        if variety is not None:
            variety_id = variety.id
            return variety_id
        else:
            e = api_error('VarietyNotExists')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_minimum_order_id_by_uuid(self, uuid: str) -> MinimumOrderEntity:
        minimum_order = self.session.query(MinimumOrder).filter_by(uuid=uuid).first()
        if minimum_order is not None:
            minimum_order_id = minimum_order.id
            return minimum_order_id
        else:
            e = api_error('MinimumOrderNotExists')
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_incoterm_id_by_uuid(self, uuid: str) -> IncotermEntity:
        incoterm = self.session.query(Incoterm).filter_by(uuid=uuid).first()
        if incoterm is not None:
            incoterm_id = incoterm.id
            return incoterm_id
        else:
            e = api_error('IncotermNotExists')
            abort(code=e.status_code, message=e.message, error=e.error)
            
    def get_sustainability_certifications_id_by_uuid(self, uuid: str) -> IncotermEntity:
        certification = self.session.query(SustainabilityCertification).filter_by(uuid=uuid).first()
        if certification is not None:
            certification_id = certification.id
            return certification_id
        else:
            e = api_error('IncotermNotExists')
            abort(code=e.status_code, message=e.message, error=e.error)

    def new_product(self, role:str, product_entity: ProductNewEntity, objects_cloud: list, images: list) -> ProductEntity:
        basic_product_id = self.get_basic_product_id_by_uuid(product_entity.basic_product_uuid)
        product_type_id = self.get_product_type_id_by_uuid(product_entity.product_type_uuid)
        variety_id = self.get_variety_id_by_uuid(product_entity.variety_uuid)
        minimum_order_id = self.get_minimum_order_id_by_uuid(product_entity.minimum_order_uuid)
        incoterm_id = self.get_incoterm_id_by_uuid(product_entity.incoterm_uuid)

        if len(product_entity.sustainability_certifications_uuid) != len(objects_cloud):
            e = api_error('NumCertificationsVSNumFilesError')
            abort(code=e.status_code, message=e.message, error=e.error)
        object_to_save = Product(
            basic_product_id=basic_product_id,
            product_type_id=product_type_id,
            variety_id=variety_id,
            capacity_per_year=product_entity.capacity_per_year,
            date_in_port=product_entity.date_in_port,
            guild_or_association=product_entity.guild_or_association,
            available_for_sale=product_entity.available_for_sale,
            minimum_order_id=minimum_order_id,
            expected_price_per_kg=product_entity.expected_price_per_kg,
            incoterm_id=incoterm_id,
            assistance_logistic=product_entity.assistance_logistic,
            additional_description=product_entity.additional_description,
        )
        with Session(self.engine) as session_trans:
            session_trans.begin()
            try:
                session_trans.add(object_to_save)
                # Save files in cloud and urls in database
                if objects_cloud:
                    path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))
                    prefix = f"{role}/{product_entity.uuid_user}/documents_product/{path_datetime}"
                    for idx, o in enumerate(objects_cloud):
                        key = f"{prefix}/{o.filename}"

                        uuid_certification = str(product_entity.sustainability_certifications_uuid[idx])
                        certification = session_trans.query(SustainabilityCertification).filter_by(
                            uuid=uuid_certification
                        ).first()

                        file_to_save = ProductFile(name=o.filename, url=key)
                        session_trans.add(file_to_save)
                        session_trans.flush()
                        product_sustainability_certification = ProductSustainabilityCertification(
                            product_id=object_to_save.id,
                            sustainability_certification_id=certification.id,
                            file_id=file_to_save.id
                        )
                        session_trans.add(product_sustainability_certification)
                        self.__storage_repository.put_object(body=o, key=key, content_type=o.content_type)
                # Save images in cloud and urls in database
                if images:
                    path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))
                    prefix_images = f"{role}/{product_entity.uuid_user}/{object_to_save.uuid}" \
                                    f"/product_images/{path_datetime}"
                    for i in images:
                        key = f"{prefix_images}/{i.filename}"
                        file_to_save = File(name=o.filename,
                                            url=key)
                        object_to_save.f.append(file_to_save)
                        self.__storage_repository.put_object(body=o, key=key, content_type=o.content_type)

            except AssertionError as e:
                self.__storage_repository.delete_all_objects_path(key=prefix + "/")
                self.__storage_repository.delete_all_objects_path(key=prefix_images + "/")
                e = api_error('CompanySavingError')
                abort(code=e.status_code, message=e.message, error=e.error)
            except Exception as e:
                session_trans.rollback()
                self.__storage_repository.delete_all_objects_path(key=prefix + "/")
                self.__storage_repository.delete_all_objects_path(key=prefix_images + "/")
                abort(code=e.code, message=None, error=e.data['error'])
            else:
                session_trans.commit()
                res_product = ProductEntity.from_orm(object_to_save)
                session_trans.close()

                return res_product

    def get_product_by_uuid(self, uuid: str) -> ProductEntity:
        product = self.session.query(Product).filter_by(uuid=uuid).first()
        return product

    def get_products_count(self) -> int:
        count = self.session.query(Product).count()
        count = count if count is not None else 0
        return count

    def get_all_products(self, limit: int, offset: int) -> ProductsPaginationEntity:
        total = self.get_companies_count()
        list_objects = self.session.query(Product).offset(offset).limit(limit).all()
        return ProductsPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects)

    def get_all_basic_products(self) -> BasicProductsListEntity:
        list_objects = self.session.query(BasicProduct).all()
        return BasicProductsListEntity(results=list_objects)

    def get_products_type_by_uuid_basic_product(self, uuid: str) -> ProductTypesListEntity:
        basic_product = self.get_basic_product_by_uuid(uuid)
        list_objects = self.session.query(ProductType).filter_by(basic_product_id=basic_product.id).all()
        return ProductTypesListEntity(results=list_objects)

    def get_varieties_by_uuid_basic_product(self, uuid: str) -> VarietiesListEntity:
        basic_product = self.get_basic_product_by_uuid(uuid)
        list_objects = self.session.query(Variety).filter_by(basic_product_id=basic_product.id).all()
        return VarietiesListEntity(results=list_objects)

    def get_all_sustainability_certifications(self) -> SustainabilityCertificationsListEntity:
        list_objects = self.session.query(SustainabilityCertification).all()
        return SustainabilityCertificationsListEntity(results=list_objects)

    def get_all_incoterms(self) -> IncotermsListEntity:
        list_objects = self.session.query(Incoterm).all()
        return IncotermsListEntity(results=list_objects)

    def get_all_minimum_order(self) -> MinimumOrderListEntity:
        list_objects = self.session.query(MinimumOrder).all()
        return MinimumOrderListEntity(results=list_objects)