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
from typing import Union
from uuid import UUID

from flask import current_app
from flask_restx import abort
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker

from src.domain.entities.basic_product_entity import BasicProductsListEntity, BasicProductEntity
from src.domain.entities.common_entity import BasicEntity
from src.domain.entities.incoterm_entity import IncotermsListEntity, IncotermEntity
from src.domain.entities.minimum_order_entity import MinimumOrderEntity, MinimumOrderListEntity
from src.domain.entities.product_entity import ProductEntity, ProductsPaginationEntity, ProductNewEntity, \
    ProductsListEntity, AvailabilityEntity, ProductEditEntity, ProductFilterBuyerEntity, ProductFilterSellerEntity, \
    ProductFilterSellerBasicProductEntity, ProductFilterBuyerBasicProductEntity
from src.domain.entities.product_type_entity import ProductTypesListEntity, ProductTypeEntity
from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationsListEntity, \
    SustainabilityCertificationEntity
from src.domain.entities.variety_entity import VarietiesListEntity, VarietyEntity
from src.domain.ports.product_interface import IProductRepository
from src.infrastructure.adapters.database.models import User
from src.infrastructure.adapters.database.models.product import Product, BasicProduct, ProductType, Variety, \
    MinimumOrder, Incoterm, SustainabilityCertification, ProductFile, ProductSustainabilityCertification, \
    ProductImage, StatusProduct, ProductIncoterm
from src.infrastructure.adapters.database.repositories.utils import build_url_storage, \
    build_url_bd, get_total_pages, validate_num_certifications_vs_num_files, send_email_to_admin, get_field_is_like, \
    get_urls_files_and_images
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error
from src.infrastructure.config.config_parameters import get_parameter_value

#
# This repository contains logic main related with product.
# @author David Córdoba
#

AWS_BUCKET_NAME = get_parameter_value('AWS_BUCKET_NAME')


class ProductRepository(IProductRepository):

    def __init__(self, adapter_db, storage_repository, utils_db):
        self.session_maker = sessionmaker(bind=adapter_db.engine)
        self.utils_db = utils_db
        self.__storage_repository = storage_repository

    def get_basic_product_by_uuid(self, uuid: UUID) -> BasicProduct:
        with self.session_maker() as session:
            basic_product = session.query(BasicProduct).filter_by(uuid=uuid).first()
            if basic_product is not None:
                return basic_product
            else:
                e = api_error('ObjectNotFound')
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_product_type_by_uuid(self, uuid: str) -> ProductTypeEntity:
        with self.session_maker() as session:
            product_type = session.query(ProductType).filter_by(uuid=uuid).first()
            if product_type is not None:
                return product_type
            else:
                e = api_error('ObjectNotFound')
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_variety_by_uuid(self, uuid: str) -> VarietyEntity:
        with self.session_maker() as session:
            variety = session.query(Variety).filter_by(uuid=uuid).first()
            if variety is not None:
                return variety
            else:
                e = api_error('ObjectNotFound')
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_minimum_order_by_uuid(self, uuid: str) -> MinimumOrderEntity:
        with self.session_maker() as session:
            minimum_order = session.query(MinimumOrder).filter_by(uuid=uuid).first()
            if minimum_order is not None:
                return minimum_order
            else:
                e = api_error('ObjectNotFound')
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_incoterm_by_uuid(self, uuid: str) -> IncotermEntity:
        with self.session_maker() as session:
            incoterm = session.query(Incoterm).filter_by(uuid=uuid).first()
            if incoterm is not None:
                return incoterm
            else:
                e = api_error('ObjectNotFound')
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_sustainability_certifications_by_uuid(self, uuid: str) -> SustainabilityCertificationEntity:
        with self.session_maker() as session:
            sustainability_certification = session.query(SustainabilityCertification).filter_by(uuid=uuid).first()
            if sustainability_certification is not None:
                return sustainability_certification
            else:
                e = api_error('ObjectNotFound')
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_basic_product_id_by_uuid(self, uuid: str) -> BasicProductEntity:
        with self.session_maker() as session:
            basic_product = session.query(BasicProduct).filter_by(uuid=uuid).first()
            if basic_product is not None:
                basic_product_id = basic_product.id
                return basic_product_id
            else:
                e = api_error('BasicProductNotExists')
                description = e.error.get('description', 'Not description')
                current_app.logger.error(f"{description}")
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_product_type_id_by_uuid(self, uuid: UUID) -> ProductTypeEntity:
        with self.session_maker() as session:
            product_type = session.query(ProductType).filter_by(uuid=uuid).first()
            if product_type is not None:
                product_type_id = product_type.id
                return product_type_id
            else:
                e = api_error('ProductTypeNotExists')
                description = e.error.get('description', 'Not description')
                current_app.logger.error(f"{description}")
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_variety_id_by_uuid(self, uuid: UUID) -> VarietyEntity:
        with self.session_maker() as session:
            variety = session.query(Variety).filter_by(uuid=uuid).first()
            if variety is not None:
                variety_id = variety.id
                return variety_id
            else:
                e = api_error('VarietyNotExists')
                description = e.error.get('description', 'Not description')
                current_app.logger.error(f"{description}")
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_minimum_order_id_by_uuid(self, uuid: UUID) -> MinimumOrderEntity:
        with self.session_maker() as session:
            minimum_order = session.query(MinimumOrder).filter_by(uuid=uuid).first()
            if minimum_order is not None:
                minimum_order_id = minimum_order.id
                return minimum_order_id
            else:
                e = api_error('MinimumOrderNotExists')
                description = e.error.get('description', 'Not description')
                current_app.logger.error(f"{description}")
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_incoterm_id_by_uuid(self, uuid: str) -> IncotermEntity:
        with self.session_maker() as session:
            incoterm = session.query(Incoterm).filter_by(uuid=uuid).first()
            if incoterm is not None:
                incoterm_id = incoterm.id
                return incoterm_id
            else:
                e = api_error('IncotermNotExists')
                description = e.error.get('description', 'Not description')
                current_app.logger.error(f"{description}")
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_sustainability_certifications_id_by_uuid(self, uuid: str) -> IncotermEntity:
        with self.session_maker() as session:
            certification = session.query(SustainabilityCertification).filter_by(uuid=uuid).first()
            if certification is not None:
                certification_id = certification.id
                return certification_id
            else:
                e = api_error('IncotermNotExists')
                abort(code=e.status_code, message=e.message, error=e.error)

    def validate_exists_certifications(self, certifications):
        with self.session_maker() as session:
            for c in certifications:
                certification = session.query(SustainabilityCertification).filter_by(uuid=c).first()
                if certification is None:
                    e = api_error('ObjectNotFound')
                    e.error['description'] = e.error['description'] + f' <uuid_certification> {c}'
                    abort(code=e.status_code, message=e.message, error=e.error)

    def new_product(self, jwt: str, role: str, product_entity: ProductNewEntity,
                    objects_cloud: list, images: list) -> ProductEntity:
        with self.session_maker() as session:
            current_app.logger.info(f"Creating new product of user: {product_entity.uuid_user}")
            validate_num_certifications_vs_num_files(len(product_entity.sustainability_certifications_uuid),
                                                     len(objects_cloud))

            if len(product_entity.sustainability_certifications_uuid):
                self.validate_exists_certifications(product_entity.sustainability_certifications_uuid)

            company = self.utils_db.get_company_by_uuid_user(product_entity.uuid_user)
            session.query(User).filter_by(uuid=product_entity.uuid_user).first()

            basic_product = self.get_basic_product_by_uuid(product_entity.basic_product_uuid)
            product_type_id = self.get_product_type_id_by_uuid(product_entity.product_type_uuid)
            variety_id = self.get_variety_id_by_uuid(product_entity.variety_uuid)
            minimum_order_id = self.get_minimum_order_id_by_uuid(product_entity.minimum_order_uuid)

            object_to_save = Product(
                basic_product_id=basic_product.id,
                product_type_id=product_type_id,
                variety_id=variety_id,
                capacity_per_year=product_entity.capacity_per_year,
                date_in_port=product_entity.date_in_port,
                guild_or_association=product_entity.guild_or_association,
                available_for_sale=product_entity.available_for_sale,
                minimum_order_id=minimum_order_id,
                expected_price_per_kg=product_entity.expected_price_per_kg,
                assistance_logistic=product_entity.assistance_logistic,
                additional_description=product_entity.additional_description,
                company_id=company.id
            )

            global prefix_files
            prefix_files = None

            with self.session_maker() as session_trans:
                session_trans.begin()
                try:
                    # Save incoterms
                    for i in product_entity.incoterms_uuid:
                        incoterm = session_trans.query(Incoterm).filter_by(uuid=i).first()
                        object_to_save.incoterms.append(incoterm)
                    session_trans.add(object_to_save)
                    session_trans.flush()

                    path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))
                    prefix_base = f"{role}/{product_entity.uuid_user}/{object_to_save.uuid}"

                    # Save files in cloud and urls in database
                    if objects_cloud:
                        current_app.logger.info(f"Uploading files to cloud")
                        prefix_files = f"{prefix_base}/documents_product/{path_datetime}"
                        for idx, o in enumerate(objects_cloud):
                            key_bd = build_url_bd(prefix_files, o.filename)
                            key_storage = build_url_storage(prefix_files, o.filename)

                            file_to_save = ProductFile(name=o.filename, url=key_bd)
                            session_trans.add(file_to_save)
                            session_trans.flush()

                            uuid_certification = str(product_entity.sustainability_certifications_uuid[idx])
                            certification = session_trans.query(SustainabilityCertification).filter_by(
                                uuid=uuid_certification).first()
                            product_sustainability_certification = ProductSustainabilityCertification(
                                product_id=object_to_save.id,
                                sustainability_certification_id=certification.id,
                                file_id=file_to_save.id)
                            session_trans.add(product_sustainability_certification)

                            self.__storage_repository.put_object(body=o, key=key_storage, content_type=o.content_type)
                    else:
                        # Product without certifications, status hidden because it's not necessary admin
                        # approve product and its necessary seller publish the product to transfer data to blockchain.
                        status_product = session_trans.query(StatusProduct).filter_by(status_product='Hidden').first()
                        object_to_save.status_id = status_product.id

                    # Save images in cloud and urls in database
                    if images:
                        current_app.logger.info(f"Uploading images to cloud")
                        prefix_images = f"{prefix_base}/product_images/{path_datetime}"
                        for i in images:
                            key_bd = build_url_bd(prefix_images, i.filename)
                            key_storage = build_url_storage(prefix_images, i.filename)
                            image_to_save = ProductImage(name=i.filename, product_id=object_to_save.id, url=key_bd)
                            object_to_save.product_images.append(image_to_save)
                            self.__storage_repository.put_object(body=i, key=key_storage, content_type=i.content_type)
                    session_trans.flush()

                except AssertionError as e:
                    session_trans.close()
                    if objects_cloud:
                        self.__storage_repository.delete_objects(key=prefix_files + "/")
                    if images:
                        self.__storage_repository.delete_objects(key=prefix_images + "/")
                    e = api_error('ProductSavingError')
                    current_app.logger.error(f"{e.error['description']}")
                    abort(code=e.status_code, message=e.message, error=e.error)
                except Exception as e:
                    session_trans.rollback()
                    session_trans.close()
                    if objects_cloud:
                        self.__storage_repository.delete_objects(key=prefix_files + "/")
                    if images:
                        self.__storage_repository.delete_objects(key=prefix_images + "/")
                    error_detail = str(e)
                    e = api_error('UndefendedError')
                    e.error['description'] = error_detail
                    current_app.logger.error(f"{e.error['description']}")
                    abort(code=e.status_code, message=e.message, error=e.error)
                else:
                    session_trans.commit()
                    url_images = [x.url for x in object_to_save.product_images]
                    url_files = [x.files.url for x in object_to_save.product_sustainability_certifications]
                    res_product = ProductEntity.from_orm(object_to_save)
                    res_product.url_images = url_images
                    res_product.url_files = url_files
                    current_app.logger.info(f"{object_to_save} saved")
                    session_trans.close()

                    if prefix_files is not None:
                        current_app.logger.info(f"Sending email to bazar admin")
                        send_email_to_admin(jwt, product_entity.uuid_user, object_to_save, prefix_files)
                        current_app.logger.info(f"Email sent")
                    return res_product
                finally:
                    session_trans.close()

    def get_product_by_uuid(self, uuid: str) -> ProductEntity:
        with self.session_maker() as session:
            product = session.query(Product).filter_by(uuid=uuid).first()
            return product

    def get_products_count(self) -> int:
        with self.session_maker() as session:
            count = session.query(Product).count()
            count = count if count is not None else 0
            return count

    def get_all_products(self, limit: int, offset: int) -> ProductsPaginationEntity:
        with self.session_maker() as session:
            total = self.get_products_count()
            total_pages = get_total_pages(total, int(limit))
            list_objects = session.query(Product).offset(offset).limit(limit).all()
            return ProductsPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects,
                                            total_pages=total_pages)

    def get_products_by_user(self, uuid: str, role: str, limit: int, offset: int) -> Union[ProductsPaginationEntity,
                                                                                           ProductsListEntity]:

        with self.session_maker() as session:
            if role == 'buyer':
                total = self.get_products_count()
                total_pages = get_total_pages(total, int(limit))
                list_objects = session.query(Product).offset(offset).limit(limit).all()
                list_objects = get_field_is_like(list_objects, uuid)
                return ProductsPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects,
                                                total_pages=total_pages)

            elif role == 'seller':
                company_id = self.utils_db.get_company_by_uuid_user(uuid).id
                list_objects = session.query(Product).filter_by(company_id=company_id).all()
                list_e_objects = get_urls_files_and_images(list_objects)
                return ProductsListEntity(results=list_e_objects)

            else:
                e = api_error('RoleNotFound')
                e.error['description'] = e.error['description'] + f' <role: {role}>'
                current_app.logger.error(f"{e.error['description']}")
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_all_basic_products(self) -> BasicProductsListEntity:
        with self.session_maker() as session:
            list_objects = session.query(BasicProduct).all()
            return BasicProductsListEntity(results=list_objects)

    def get_products_type_by_uuid_basic_product(self, uuid: str) -> ProductTypesListEntity:
        with self.session_maker() as session:
            basic_product = self.get_basic_product_by_uuid(uuid)
            list_objects = session.query(ProductType).filter_by(basic_product_id=basic_product.id).all()
            return ProductTypesListEntity(results=list_objects)

    def get_varieties_by_uuid_basic_product(self, uuid: str) -> VarietiesListEntity:
        with self.session_maker() as session:
            basic_product = self.get_basic_product_by_uuid(uuid)
            list_objects = session.query(Variety).filter_by(basic_product_id=basic_product.id).all()
            return VarietiesListEntity(results=list_objects)

    def get_all_sustainability_certifications(self) -> SustainabilityCertificationsListEntity:
        with self.session_maker() as session:
            list_objects = session.query(SustainabilityCertification).all()
            return SustainabilityCertificationsListEntity(results=list_objects)

    def get_all_incoterms(self) -> IncotermsListEntity:
        with self.session_maker() as session:
            list_objects = session.query(Incoterm).all()
            return IncotermsListEntity(results=list_objects)

    def get_all_minimum_order(self) -> MinimumOrderListEntity:
        with self.session_maker() as session:
            list_objects = session.query(MinimumOrder).all()
            return MinimumOrderListEntity(results=list_objects)

    def product_states(self) -> BasicEntity:
        with self.session_maker() as session:
            product_states = session.query(StatusProduct.uuid, StatusProduct.status_product.label('tag')).all()
            response = BasicEntity(results=product_states)
            return response

    def edit_product_availability(self, entity: AvailabilityEntity) -> AvailabilityEntity:
        with self.session_maker() as session:
            product = session.query(Product).filter_by(uuid=entity.uuid_product).first()
            if product is None:
                e = api_error('ObjectNotFound')
                e.error['description'] = e.error['description'] + f' <product uuid_product: {entity.uuid_product}>'
                current_app.logger.error(e.error['description'])
                abort(code=e.status_code, message=e.message, error=e.error)
            product.available_for_sale = entity.available_for_sale
            session.commit()
            current_app.logger.info(f"{product} availability edited")
            return entity

    def get_detail_product_by_uuid(self, uuid: str) -> ProductEntity:
        product = self.utils_db.get_product_by_uuid_product(uuid)
        url_images = [x.url for x in product.product_images]
        url_files = [x.files.url for x in product.product_sustainability_certifications]
        res_product = ProductEntity.from_orm(product)
        res_product.url_images = url_images
        res_product.url_files = url_files
        self.utils_db.close_session()
        return res_product

    def edit_product_state(self, status: str, uuid: str) -> ProductEntity:
        with self.session_maker() as session:
            product = self.utils_db.get_product_by_uuid_product(uuid)
            state = session.query(StatusProduct).filter_by(status_product=status).first()
            if state is None:
                e = api_error('ObjectNotFound')
                abort(code=e.status_code, message=e.message, error=e.error)
            product.status_id = state.id
            session.commit()
            current_app.logger.info(f"{product} state edited")
            return ProductEntity.from_orm(product)

    def edit_product(self, jwt: str, role: str, uuid_product: str, product_entity: ProductEditEntity,
                     objects_cloud: list, images: list) -> ProductEntity:

        with self.session_maker() as session:
            current_app.logger.info(f"Editing product: {uuid_product}")

            if product_entity.change_files:
                validate_num_certifications_vs_num_files(len(product_entity.sustainability_certifications_uuid),
                                                         len(objects_cloud))

            if len(product_entity.sustainability_certifications_uuid):
                self.validate_exists_certifications(product_entity.sustainability_certifications_uuid)

            product_to_edit = self.utils_db.get_product_by_uuid_product(uuid_product)
            product_to_edit.capacity_per_year = product_entity.capacity_per_year
            product_to_edit.date_in_port = product_entity.date_in_port
            product_to_edit.guild_or_association = product_entity.guild_or_association
            product_to_edit.available_for_sale = product_entity.available_for_sale
            product_to_edit.minimum_order_uuid = product_entity.minimum_order_uuid
            product_to_edit.expected_price_per_kg = product_entity.expected_price_per_kg
            product_to_edit.assistance_logistic = product_entity.assistance_logistic
            product_to_edit.additional_description = product_entity.additional_description

            global prefix_files
            prefix_files = None

            with self.session_maker() as session_trans:
                session_trans.begin()
                try:
                    incoterms_uuid_saved = [x.uuid for x in product_to_edit.incoterms]
                    if set(incoterms_uuid_saved) != set(product_entity.incoterms_uuid):
                        # Remove old incoterms
                        session.query(ProductIncoterm).filter(
                            ProductIncoterm.product_id == product_to_edit.id).delete()

                        # Save new incoterms
                        for i in product_entity.incoterms_uuid:
                            incoterm = session_trans.query(Incoterm).filter_by(uuid=i).first()
                            product_to_edit.incoterms.append(incoterm)
                        session_trans.add(product_to_edit)

                    session_trans.flush()

                    path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))
                    prefix_base = f"{role}/{product_entity.uuid_user}/{product_to_edit.uuid}"

                    # Save new files in cloud and urls in database
                    if product_entity.change_files:
                        current_app.logger.info(f"Removing old file relationships product")
                        # Remove old product files (certifications)
                        subquery_certifications = session_trans.query(ProductSustainabilityCertification).filter(
                            ProductSustainabilityCertification.product_id == product_to_edit.id).subquery()

                        # Remove old certifications
                        session_trans.query(ProductSustainabilityCertification).filter(exists().where(
                            subquery_certifications.c.product_id == product_to_edit.id)).delete(
                            synchronize_session=False)

                        session_trans.query(ProductFile).filter(exists().where(
                            subquery_certifications.c.file_id == ProductFile.id)).delete(synchronize_session=False)

                        # Remove old objects from cloud
                        current_app.logger.info(f"Remove old files from cloud")
                        self.__storage_repository.delete_objects(key=f'{prefix_base}/documents_product/')

                    if objects_cloud:
                        if product_entity.change_files:
                            current_app.logger.info(f"Uploading files to cloud")
                            prefix_files = f"{prefix_base}/documents_product/{path_datetime}"
                            for idx, o in enumerate(objects_cloud):
                                key_bd = build_url_bd(prefix_files, o.filename)
                                key_storage = build_url_storage(prefix_files, o.filename)

                                file_to_save = ProductFile(name=o.filename, url=key_bd)
                                session_trans.add(file_to_save)
                                session_trans.flush()

                                uuid_certification = str(product_entity.sustainability_certifications_uuid[idx])
                                certification = session_trans.query(SustainabilityCertification).filter_by(
                                    uuid=uuid_certification).first()
                                product_sustainability_certification = ProductSustainabilityCertification(
                                    product_id=product_to_edit.id,
                                    sustainability_certification_id=certification.id,
                                    file_id=file_to_save.id)
                                session_trans.add(product_sustainability_certification)

                                self.__storage_repository.put_object(body=o, key=key_storage,
                                                                     content_type=o.content_type)
                    else:
                        # Product without certifications, status hidden because it's not necessary admin
                        # approve product and its necessary seller publish the product to transfer data to blockchain.
                        status_product = session_trans.query(StatusProduct).filter_by(status_product='Hidden').first()
                        product_to_edit.status_id = status_product.id

                    if product_entity.change_images:
                        # Remove old images
                        session_trans.query(ProductImage).filter(
                            ProductImage.product_id == product_to_edit.id).delete(synchronize_session=False)

                        # Remove old objects from cloud
                        current_app.logger.info(f"Remove old images from cloud")
                        self.__storage_repository.delete_objects(key=f'{prefix_base}/product_images/')

                    # Save images in cloud and urls in database
                    if images:
                        if product_entity.change_images:
                            current_app.logger.info(f"Uploading images to cloud")
                            prefix_images = f"{prefix_base}/product_images/{path_datetime}"
                            for i in images:
                                key_bd = build_url_bd(prefix_images, i.filename)
                                key_storage = build_url_storage(prefix_images, i.filename)
                                image_to_save = ProductImage(name=i.filename, product_id=product_to_edit.id, url=key_bd)
                                product_to_edit.product_images.append(image_to_save)
                                self.__storage_repository.put_object(body=i, key=key_storage,
                                                                     content_type=i.content_type)

                except AssertionError as e:
                    session_trans.close()
                    if objects_cloud:
                        self.__storage_repository.delete_objects(key=prefix_files + "/")
                    if images:
                        self.__storage_repository.delete_objects(key=prefix_images + "/")
                    e = api_error('ProductSavingError')
                    current_app.logger.error(f"{e.error['description']}")
                    abort(code=e.status_code, message=e.message, error=e.error)
                except Exception as e:
                    session_trans.rollback()
                    session_trans.close()
                    if objects_cloud:
                        self.__storage_repository.delete_objects(key=prefix_files + "/")
                    if images:
                        self.__storage_repository.delete_objects(key=prefix_images + "/")
                    error_detail = str(e)
                    e = api_error('UndefendedError')
                    e.error['description'] = error_detail
                    current_app.logger.error(f"{e.error['description']}")
                    abort(code=e.status_code, message=e.message, error=e.error)
                else:
                    session_trans.commit()
                    url_images = [x.url for x in product_to_edit.product_images]
                    url_files = [x.files.url for x in product_to_edit.product_sustainability_certifications]
                    res_product = ProductEntity.from_orm(product_to_edit)
                    res_product.url_images = url_images
                    res_product.url_files = url_files
                    current_app.logger.info(f"{product_to_edit} saved")
                    session_trans.close()

                    if prefix_files is not None:
                        send_email_to_admin(jwt, product_entity.uuid_user, product_to_edit, prefix_files)

                    return res_product
                finally:
                    session_trans.close()

    def get_products_filter_seller(self, filter_entity: ProductFilterSellerEntity) -> ProductsListEntity:
        with self.session_maker() as session:
            company_id = self.utils_db.get_company_by_uuid_user(filter_entity.user_uuid).id
            list_objects = session.query(Product) \
                .filter(Product.company_id == company_id,
                        Product.expected_price_per_kg >= filter_entity.price_per_kg_start,
                        Product.expected_price_per_kg <= filter_entity.price_per_kg_end,
                        Product.available_for_sale >= filter_entity.available_for_sale).all()

            list_e_objects = get_urls_files_and_images(list_objects)
            return ProductsListEntity(results=list_e_objects)

    def get_products_filter_buyer(self, filter_entity: ProductFilterBuyerEntity) -> ProductsPaginationEntity:
        with self.session_maker() as session:
            query = session.query(Product) \
                .filter(Product.expected_price_per_kg >= filter_entity.price_per_kg_start,
                        Product.expected_price_per_kg <= filter_entity.price_per_kg_end,
                        Product.available_for_sale >= filter_entity.available_for_sale)

            total = query.from_self().count()
            list_objects = query.offset(filter_entity.offset).limit(filter_entity.limit).all()
            total_pages = get_total_pages(total, int(filter_entity.limit))

            list_objects = get_field_is_like(list_objects, filter_entity.user_uuid)
            list_e_objects = get_urls_files_and_images(list_objects)
            return ProductsPaginationEntity(limit=filter_entity.limit, offset=filter_entity.offset, total=total,
                                            results=list_e_objects, total_pages=total_pages)

    def get_products_filter_seller_basic_product(self, filter_entity: ProductFilterSellerBasicProductEntity) \
            -> ProductsListEntity:
        with self.session_maker() as session:
            company_id = self.utils_db.get_company_by_uuid_user(filter_entity.user_uuid).id
            list_objects = session.query(Product) \
                .join(BasicProduct, Product.basic_product_id == BasicProduct.id) \
                .filter(Product.company_id == company_id,
                        Product.basic_product == filter_entity.basic_product).all()
            list_e_objects = get_urls_files_and_images(list_objects)
            return ProductsListEntity(results=list_e_objects)

    def get_products_filter_buyer_basic_product(self, filter_entity: ProductFilterBuyerBasicProductEntity) \
            -> ProductsPaginationEntity:
        with self.session_maker() as session:
            query = session.query(Product) \
                .join(BasicProduct, Product.basic_product_id == BasicProduct.id) \
                .filter(BasicProduct.basic_product == filter_entity.basic_product)

            total = query.from_self().count()
            list_objects = query.offset(filter_entity.offset).limit(filter_entity.limit).all()
            total_pages = get_total_pages(total, int(filter_entity.limit))

            list_objects = get_field_is_like(list_objects, filter_entity.user_uuid)

            list_e_objects = get_urls_files_and_images(list_objects)
            return ProductsPaginationEntity(limit=filter_entity.limit, offset=filter_entity.offset, total=total,
                                            results=list_e_objects, total_pages=total_pages)

    def get_products_filter_seller_search_bar(self, filter_entity: ProductFilterSellerBasicProductEntity) \
            -> ProductsListEntity:
        with self.session_maker() as session:
            company_id = self.utils_db.get_company_by_uuid_user(filter_entity.user_uuid).id
            list_objects = session.query(Product) \
                .join(BasicProduct, Product.basic_product_id == BasicProduct.id) \
                .filter(Product.company_id == company_id,
                        Product.basic_product.ilike('%' + filter_entity.basic_product + '%')).all()

            list_e_objects = get_urls_files_and_images(list_objects)
            return ProductsListEntity(results=list_e_objects)

    def get_products_filter_buyer_search_bar(self, filter_entity: ProductFilterBuyerBasicProductEntity) \
            -> ProductsPaginationEntity:
        with self.session_maker() as session:
            query = session.query(Product) \
                .join(BasicProduct, Product.basic_product_id == BasicProduct.id) \
                .filter(BasicProduct.basic_product.ilike('%' + filter_entity.basic_product + '%'))

            total = query.from_self().count()
            list_objects = query.offset(filter_entity.offset).limit(filter_entity.limit).all()
            total_pages = get_total_pages(total, int(filter_entity.limit))

            list_objects = get_field_is_like(list_objects, filter_entity.user_uuid)
            list_e_objects = get_urls_files_and_images(list_objects)

            return ProductsPaginationEntity(limit=filter_entity.limit, offset=filter_entity.offset, total=total,
                                            results=list_e_objects, total_pages=total_pages)
