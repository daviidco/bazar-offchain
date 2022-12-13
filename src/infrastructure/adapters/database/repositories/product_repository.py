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
from src.domain.entities.common_entity import BasicEntity
from src.domain.entities.incoterm_entity import IncotermsListEntity, IncotermEntity
from src.domain.entities.minimum_order_entity import MinimumOrderEntity, MinimumOrderListEntity
from src.domain.entities.product_entity import ProductEntity, ProductsPaginationEntity, ProductNewEntity, \
    ProductsListEntity, AvailabilityEntity
from src.domain.entities.product_type_entity import ProductTypesListEntity, ProductTypeEntity
from src.domain.entities.sustainability_certifications_entity import SustainabilityCertificationsListEntity, \
    SustainabilityCertificationEntity
from src.domain.entities.variety_entity import VarietiesListEntity, VarietyEntity
from src.domain.ports.product_interface import IProductRepository
from src.infrastructure.adapters.database.models import User
from src.infrastructure.adapters.database.models.product import Product, BasicProduct, ProductType, Variety, \
    MinimumOrder, Incoterm, SustainabilityCertification, ProductFile, ProductSustainabilityCertification, \
    ProductImage,StatusProduct
from src.infrastructure.adapters.database.repositories.utils import send_email, get_user_names, build_url_storage, \
    build_url_bd
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error
from src.infrastructure.config.default import EMAIL_BAZAR_ADMIN
from src.infrastructure.config.default_infra import AWS_REGION, AWS_BUCKET_NAME
from src.infrastructure.templates_email import TemplateAdminProduct


#
# This repository contains logic main related with product.
# @author David Córdoba
#

class ProductRepository(IProductRepository):

    def __init__(self, logger, adapter_db, storage_repository, utils_db):
        self.logger = logger
        self.engine = adapter_db.engine
        self.session = Session(adapter_db.engine)
        self.utils_db = utils_db
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
            description = e.error.get('description', 'Not description')
            self.logger.error(f"{description}")
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_product_type_id_by_uuid(self, uuid: str) -> ProductTypeEntity:
        product_type = self.session.query(ProductType).filter_by(uuid=uuid).first()
        if product_type is not None:
            product_type_id = product_type.id
            return product_type_id
        else:
            e = api_error('ProductTypeNotExists')
            description = e.error.get('description', 'Not description')
            self.logger.error(f"{description}")
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_variety_id_by_uuid(self, uuid: str) -> VarietyEntity:
        variety = self.session.query(Variety).filter_by(uuid=uuid).first()
        if variety is not None:
            variety_id = variety.id
            return variety_id
        else:
            e = api_error('VarietyNotExists')
            description = e.error.get('description', 'Not description')
            self.logger.error(f"{description}")
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_minimum_order_id_by_uuid(self, uuid: str) -> MinimumOrderEntity:
        minimum_order = self.session.query(MinimumOrder).filter_by(uuid=uuid).first()
        if minimum_order is not None:
            minimum_order_id = minimum_order.id
            return minimum_order_id
        else:
            e = api_error('MinimumOrderNotExists')
            description = e.error.get('description', 'Not description')
            self.logger.error(f"{description}")
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_incoterm_id_by_uuid(self, uuid: str) -> IncotermEntity:
        incoterm = self.session.query(Incoterm).filter_by(uuid=uuid).first()
        if incoterm is not None:
            incoterm_id = incoterm.id
            return incoterm_id
        else:
            e = api_error('IncotermNotExists')
            description = e.error.get('description', 'Not description')
            self.logger.error(f"{description}")
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_sustainability_certifications_id_by_uuid(self, uuid: str) -> IncotermEntity:
        certification = self.session.query(SustainabilityCertification).filter_by(uuid=uuid).first()
        if certification is not None:
            certification_id = certification.id
            return certification_id
        else:
            e = api_error('IncotermNotExists')
            abort(code=e.status_code, message=e.message, error=e.error)

    def new_product(self, jwt: str, role: str, product_entity: ProductNewEntity,
                    objects_cloud: list, images: list) -> ProductEntity:
        self.logger.info(f"Creating new product of user: {product_entity.uuid_user}")
        global user
        global prefix
        prefix = None
        company = self.utils_db.get_company_by_uuid_user(product_entity.uuid_user)
        user = self.session.query(User).filter_by(uuid=product_entity.uuid_user).first()

        basic_product = self.get_basic_product_by_uuid(product_entity.basic_product_uuid)
        product_type_id = self.get_product_type_id_by_uuid(product_entity.product_type_uuid)
        variety_id = self.get_variety_id_by_uuid(product_entity.variety_uuid)
        minimum_order_id = self.get_minimum_order_id_by_uuid(product_entity.minimum_order_uuid)

        if product_entity.sustainability_certifications_uuid is None:
            product_entity.sustainability_certifications_uuid = []

        if len(product_entity.sustainability_certifications_uuid) != len(objects_cloud):
            e = api_error('NumCertificationsVSNumFilesError')
            description = e.error.get('description', 'Not description')
            self.logger.error(f"{description}")
            abort(code=e.status_code, message=e.message, error=e.error)

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

        with Session(self.engine) as session_trans:
            session_trans.begin()
            try:
                for i in product_entity.incoterms_uuid:
                    incoterm = session_trans.query(Incoterm).filter_by(uuid=i).first()
                    object_to_save.incoterms.append(incoterm)
                session_trans.add(object_to_save)
                session_trans.flush()
                # Save files in cloud and urls in database
                if objects_cloud:
                    self.logger.info(f"Uploading files to cloud")
                    path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))
                    prefix = f"{role}/{product_entity.uuid_user}/{object_to_save.uuid}" \
                             f"/documents_product/{path_datetime}"
                    for idx, o in enumerate(objects_cloud):
                        key_bd = build_url_bd(prefix, o.filename)
                        key_storage = build_url_storage(prefix, o.filename)

                        uuid_certification = str(product_entity.sustainability_certifications_uuid[idx])
                        certification = session_trans.query(SustainabilityCertification).filter_by(
                            uuid=uuid_certification
                        ).first()
                        if certification is None:
                            e = api_error('CompanySavingErrorByCertification')
                            abort(code=e.status_code, message=e.message, error=e.error)

                        file_to_save = ProductFile(name=o.filename, url=key_bd)
                        session_trans.add(file_to_save)
                        session_trans.flush()
                        product_sustainability_certification = ProductSustainabilityCertification(
                            product_id=object_to_save.id,
                            sustainability_certification_id=certification.id,
                            file_id=file_to_save.id
                        )
                        session_trans.add(product_sustainability_certification)
                        self.__storage_repository.put_object(body=o, key=key_storage, content_type=o.content_type)
                else:
                    # Product without certifications, status hidden because it's not necessary admin approve product,
                    # and its necessary seller publish the product to transfer data to blockchain.
                    status_product = session_trans.query(StatusProduct).filter_by(status_product='Hidden').first()
                    object_to_save.status_id = status_product.id
                # Save images in cloud and urls in database
                if images:
                    self.logger.info(f"Uploading images to cloud")
                    path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))
                    prefix_images = f"{role}/{product_entity.uuid_user}/" \
                                    f"{object_to_save.uuid}/product_images/{path_datetime}"
                    for i in images:
                        key_bd = build_url_bd(prefix_images, i.filename)
                        key_storage = build_url_storage(prefix_images, i.filename)
                        image_to_save = ProductImage(name=i.filename, product_id=object_to_save.id, url=key_bd)
                        object_to_save.product_images.append(image_to_save)
                        self.__storage_repository.put_object(body=i, key=key_storage, content_type=i.content_type)

            except AssertionError as e:
                if objects_cloud:
                    self.__storage_repository.delete_all_objects_path(key=prefix + "/")
                if images:
                    self.__storage_repository.delete_all_objects_path(key=prefix_images + "/")
                e = api_error('ProductSavingError')
                self.logger.error(f"{e.error['message']}")
                abort(code=e.status_code, message=e.message, error=e.error)
            except Exception as e:
                session_trans.rollback()
                session_trans.close()
                if objects_cloud:
                    self.__storage_repository.delete_all_objects_path(key=prefix + "/")
                if images:
                    self.__storage_repository.delete_all_objects_path(key=prefix_images + "/")
                error_detail = str(e)
                e = api_error('UndefendedError')
                e.error['message'] = error_detail
                self.logger.error(f"{e.error['message']}")
                abort(code=e.status_code, message=e.message, error=e.error)
            else:
                session_trans.commit()
                url_images = [x.url for x in object_to_save.product_images]
                url_files = [x.files.url for x in object_to_save.product_sustainability_certifications]
                res_product = ProductEntity.from_orm(object_to_save)
                res_product.url_images = url_images
                res_product.url_files = url_files
                self.logger.info(f"{object_to_save} saved")
                session_trans.close()

                if prefix is not None:
                    # Build html to send email
                    first_name, last_name = get_user_names(jwt, user.uuid)
                    user_name = f"{first_name.title()} {last_name.title()}"
                    url_s3 = f"https://s3.console.aws.amazon.com/s3/buckets/{AWS_BUCKET_NAME}?" \
                             f"region={AWS_REGION}&prefix={prefix}/&showversions=false"
                    data_email = TemplateAdminProduct.html.format(product_name=basic_product.basic_product,
                                                                  user_name=user_name,
                                                                  company_name=company.company_name,
                                                                  link=url_s3)

                    send_email(subject="Review Documents - Product",
                               data=data_email,
                               destination=[EMAIL_BAZAR_ADMIN],
                               is_html=True)

                return res_product

    def get_product_by_uuid(self, uuid: str) -> ProductEntity:
        product = self.session.query(Product).filter_by(uuid=uuid).first()
        return product

    def get_products_count(self) -> int:
        count = self.session.query(Product).count()
        count = count if count is not None else 0
        return count

    def get_all_products(self, limit: int, offset: int) -> ProductsPaginationEntity:
        total = self.get_products_count()
        list_objects = self.session.query(Product).offset(offset).limit(limit).all()
        return ProductsPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects)

    def get_products_by_user(self, uuid: str, role: str, limit: int, offset: int) -> ProductsListEntity:

        if role == 'buyer':
            total = self.get_products_count()
            list_objects = self.session.query(Product).offset(offset).limit(limit).all()
            for p in list_objects:
                p.check_use_like(uuid)
            return ProductsPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects)

        elif role == 'seller':
            company_id = self.utils_db.get_company_by_uuid_user(uuid).id
            list_objects = self.session.query(Product).filter_by(company_id=company_id).all()
            list_e_objects = []
            for p in list_objects:
                ep = ProductEntity.from_orm(p)
                ep.url_images = list(p.url_images_ap)
                ep.url_files = [x.url for x in p.url_files_ap]
                list_e_objects.append(ep)
            return ProductsListEntity(results=list_e_objects)

        else:
            e = api_error('RoleNotFound')
            e.error['description'] = e.error['description'] + f' <role: {role}>'
            self.logger.error(f"{e.error['description']}")
            abort(code=e.status_code, message=e.message, error=e.error)

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

    def product_states(self) -> BasicEntity:
        product_states = self.session.query(StatusProduct.uuid, StatusProduct.status_product.label('tag')).all()
        response = BasicEntity(results=product_states)
        return response

    def edit_product_availability(self, entity: AvailabilityEntity) -> AvailabilityEntity:
        product = self.utils_db.get_product_by_uuid_product(entity.uuid_product)
        product.available_for_sale = entity.available_for_sale
        self.session.merge(product)
        self.session.commit()
        self.logger.info(f"{product} availability edited")
        return entity

    def get_detail_product_by_uuid(self, uuid: str) -> ProductEntity:
        product = self.utils_db.get_product_by_uuid_product(uuid)
        return ProductEntity.from_orm(product)

    def edit_product_state(self, status: str, uuid: str) -> ProductEntity:
        product = self.utils_db.get_product_by_uuid_product(uuid)
        state = self.session.query(StatusProduct).filter_by(status_product=status).first()
        if state is None:
            e = api_error('ObjectNotFound')
            abort(code=e.status_code, message=e.message, error=e.error)
        product.status_id = state.id
        self.session.commit()
        self.logger.info(f"{product} state edited")
        return ProductEntity.from_orm(product)
