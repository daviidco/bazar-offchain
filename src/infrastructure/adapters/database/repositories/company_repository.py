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

from flask import current_app
from flask_restx import abort
from sqlalchemy.orm import Session

from src.domain.entities.company_entity import CompanyEntity, CompanyNewEntity, CompaniesPaginationEntity
from src.domain.ports.company_interface import ICompanyRepository
from src.infrastructure.adapters.database.models import User
from src.infrastructure.adapters.database.models.company import Company, ProfileImage, File
from src.infrastructure.adapters.database.repositories.utils import send_email, build_url_bd, build_url_storage, \
    get_total_pages, build_urls_from_profile_image
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error
from src.infrastructure.config.config_parameters import get_parameter_value
from src.infrastructure.templates_email import TemplateAdminReview


#
# This repository contains logic main related with company.
# @author David Córdoba
#

AWS_REGION = current_app.config['AWS_REGION']
EMAIL_BAZAR_ADMIN = get_parameter_value('EMAIL_BAZAR_ADMIN')
AWS_BUCKET_NAME = get_parameter_value('AWS_BUCKET_NAME')


class CompanyRepository(ICompanyRepository):

    def __init__(self, logger, adapter_db, storage_repository):
        self.logger = logger
        self.engine = adapter_db.engine
        self.session = Session(adapter_db.engine)
        self.__storage_repository = storage_repository

    def new_company(self, jwt: str, role: str, company_entity: CompanyNewEntity, objects_cloud: list) -> CompanyEntity:
        self.logger.info(f"Creating new company: {company_entity.company_name}")
        global user_rol
        global prefix
        prefix = None
        user = self.session.query(User).filter_by(uuid=company_entity.uuid_user).first()
        if user is None:
            user_to_save = User(
                uuid_user=company_entity.uuid_user,
                rol=role
            )
            self.session.add(user_to_save)
            self.session.commit()
            self.logger.info(f"User {user_to_save} saved")

        user_id = user.id if user is not None else user_to_save.id
        user_rol = user.rol if user is not None else user_to_save.rol
        company = self.session.query(Company).filter_by(user_id=user_id).first()

        if company is None:
            profile_image = self.session.query(ProfileImage).filter_by(image_url=company_entity.profile_image).first()
            profile_image_id = profile_image.id if profile_image is not None else None

            object_to_save = Company(
                company_name=company_entity.company_name,
                address=company_entity.address,
                chamber_commerce=company_entity.chamber_commerce,
                legal_representative=company_entity.legal_representative,
                operative_years=company_entity.operative_years,
                country=company_entity.country,
                city=company_entity.city,
                user_id=user_id,
                profile_image_id=profile_image_id
            )

            with Session(self.engine) as session_trans:
                session_trans.begin()
                try:

                    list_profile_images = build_urls_from_profile_image(profile_image)

                    # Save files in cloud and urls in database
                    if objects_cloud:
                        path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))
                        prefix = f"{role}/{company_entity.uuid_user}/documents_company/{path_datetime}"

                        for o in objects_cloud:
                            key_bd = build_url_bd(prefix, o.filename)
                            key_storage = build_url_storage(prefix, o.filename)

                            file_to_save = File(name=o.filename,
                                                url=key_bd)
                            object_to_save.files.append(file_to_save)
                            self.__storage_repository.put_object(body=o, key=key_storage, content_type=o.content_type)
                    session_trans.add(object_to_save)

                except AssertionError as e:
                    session_trans.close()
                    self.__storage_repository.delete_objects(key=prefix + "/")
                    e = api_error('CompanySavingError')
                    self.logger.error(f"{e.error['message']}")
                    abort(code=e.status_code, message=e.message, error=e.error)
                except Exception as e:
                    session_trans.rollback()
                    session_trans.close()
                    self.__storage_repository.delete_objects(key=prefix + "/")
                    error_detail = str(e)
                    e = api_error('UndefendedError')
                    e.error['message'] = error_detail
                    self.logger.error(f"{e.error['message']}")
                    abort(code=e.status_code, message=e.message, error=e.error)

                else:
                    session_trans.commit()
                    self.logger.info(f"Company {object_to_save} saved")
                    res_company = CompanyEntity.from_orm(object_to_save)
                    res_company.profile_images = list_profile_images
                    session_trans.close()

                    if prefix is not None:
                        # Build html to send email
                        url_s3 = f"https://s3.console.aws.amazon.com/s3/buckets/{AWS_BUCKET_NAME}?" \
                                 f"region={AWS_REGION}&prefix={prefix}/&showversions=false"
                        data_email = TemplateAdminReview.html.format(company_name=object_to_save.company_name,
                                                                     rol=user_rol.title(),
                                                                     link=url_s3)

                        send_email(subject="Review Documents",
                                   data=data_email,
                                   destination=[EMAIL_BAZAR_ADMIN],
                                   is_html=True)
                    return res_company

        else:
            e = api_error('CompanyExistingError')
            description = e.error.get('description', 'Not description')
            self.logger.error(f"{description}")
            abort(code=e.status_code, message=e.message, error=e.error)

    def get_company_by_uuid(self, uuid: str) -> CompanyEntity:
        try:
            self.logger.error(f"Get company by uuid: {uuid}")
            found_object = self.session.query(Company).filter_by(uuid=uuid).first()
            result_object = CompanyEntity.from_orm(found_object) if found_object is not None else None
            profile_image = self.session.query(ProfileImage).filter_by(id=found_object.profile_image_id).first()
            list_profile_images = build_urls_from_profile_image(profile_image)
            result_object.profile_images = list_profile_images
            return result_object

        except Exception as e:
            self.logger.error(f"Error undefended {str(e)}")
            raise Exception(f'Error: {str(e)}')

    def get_companies_count(self) -> int:
        count = self.session.query(Company).count()
        count = count if count is not None else 0
        self.logger.info(f"OK - Get total number companies")
        return count

    def get_all_companies(self, limit: int, offset: int) -> CompaniesPaginationEntity:
        total = self.get_companies_count()
        list_objects = self.session.query(Company).offset(offset).limit(limit).all()
        total_pages = get_total_pages(total, int(limit))
        response = CompaniesPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects,
                                             total_pages=total_pages)
        response.results = [x.dict(exclude={'profile_images'}) for x in response.results]
        self.logger.info(f"OK - Get all companies")
        return response
