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
from flask import current_app
from flask_restx import abort
from sqlalchemy.orm import sessionmaker
from werkzeug.exceptions import UnprocessableEntity

from src.domain.entities.common_entity import BasicEntity
from src.domain.entities.user_manage_entity import UserManageEntity
from src.domain.ports.user_interface import IUserRepository
from src.domain.entities.user_entity import UserNewEntity, UserEntity, UsersPaginationEntity
from src.infrastructure.adapters.database.models import Product, CommentApproval, StatusProduct, Company
from src.infrastructure.adapters.database.models.user import User, StatusUser
from src.infrastructure.adapters.database.repositories.utils import get_user_names, get_total_pages, \
    build_urls_from_url_image, send_email_with_template, get_whatsapp_phone
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


#
# This repository contains logic main related with user.
# @author David Córdoba
#
class UserRepository(IUserRepository):

    def __init__(self, adapter_db, utils_db):
        self.session_maker = sessionmaker(bind=adapter_db.engine)
        self.__utils_db = utils_db

    def new_user(self, user_entity: UserNewEntity) -> UserEntity:
        with self.session_maker() as session:
            user_exist = self.get_user_by_uuid(user_entity.uuid)
            if user_exist is None:
                object_to_save = User(
                    uuid_user=user_entity.uuid,
                    rol=user_entity.rol,
                )

                session.add(object_to_save)
                session.commit()
                return UserEntity.from_orm(object_to_save)
            else:
                e = api_error('UserExistingError')
                abort(code=e.status_code, message=e.message, error=e.error)

    def get_user_by_uuid(self, jwt: str, uuid: str) -> UserEntity:
        with self.session_maker() as session:
            found_object = session.query(User).filter_by(uuid=uuid).first()
            found_object = UserEntity.from_orm(found_object) if found_object is not None else None
            if found_object is None:
                e = api_error('ObjectNotFound')
                abort(code=e.status_code, message=e.message, error=e.error)
            for c in found_object.company:
                c.profile_images = build_urls_from_url_image(c.profile_image_url)
            found_object.first_name, found_object.last_name = get_user_names(uuid)
            return found_object

    def get_users_count(self) -> int:
        with self.session_maker() as session:
            count = session.query(User).count()
            count = count if count is not None else 0
            return count

    def get_all_users(self, limit: int, offset: int, jwt: str) -> UsersPaginationEntity:
        with self.session_maker() as session:
            total = self.get_users_count()
            total_pages = get_total_pages(total, int(limit))
            list_objects = session.query(User).join(User.company).order_by(Company.company_name).offset(offset) \
                .limit(limit).all()
            response = UsersPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects,
                                             total_pages=total_pages)

            for idx_r, x in enumerate(response.results):
                # Call endpoint to get user_name microservice auth
                first_name, last_name = get_user_names(response.results[idx_r].uuid)
                response.results[idx_r].first_name = first_name
                response.results[idx_r].last_name = last_name
                for idx_c, y in enumerate(x.company):
                    try:
                        # Exclude profile_images
                        response.results[idx_r].company[0] = y.dict(exclude={'profile_images'})
                    except Exception as e:
                        continue
            return response

    def user_states(self) -> BasicEntity:
        with self.session_maker() as session:
            user_states = session.query(StatusUser.uuid, StatusUser.status_user.label('tag')).all()
            response = BasicEntity(results=user_states)
            return response

    def put_states_approval(self, user_manage: UserManageEntity) -> UserManageEntity:
        with self.session_maker() as session_trans:
            session_trans.begin()
            try:
                current_app.logger.info(f"Editing with user-approval")
                company_id = self.__utils_db.get_company_by_uuid_user(user_manage.uuid_user).id

                # Add comment
                if len(user_manage.comment_approval):
                    comment = CommentApproval(comment=user_manage.comment_approval, company_id=company_id)
                    session_trans.add(comment)

                # Modify user state
                user = session_trans.query(User).filter_by(uuid=user_manage.uuid_user).first()
                if user is None:
                    e = api_error('ObjectNotFound')
                    e.error['description'] = e.error['description'] + f' <uuid> {user_manage.uuid_user}'
                    abort(code=e.status_code, message=e.message, error=e.error)

                old_user_status = user.status

                status = session_trans.query(StatusUser).filter_by(status_user=user_manage.user_status).first()
                if status is None:
                    e = api_error('ObjectNotFound')
                    e.error['description'] = e.error['description'] + f' <status_user> {user_manage.user_status}'
                    abort(code=e.status_code, message=e.message, error=e.error)

                user.status_id = status.id

                # Modify product state
                if user_manage.products is not None:
                    uuids_products = [p.uuid_product for p in user_manage.products]
                    products_from_db = session_trans.query(Product).filter(Product.uuid.in_(uuids_products)).all()

                    # Determinate uuid products not found
                    uuid_db = [p.uuid for p in products_from_db]
                    set1 = set(uuids_products)
                    set2 = set(uuid_db)
                    missing = list(sorted(set1 - set2))

                    if len(user_manage.products) == len(products_from_db):
                        for u_m_entity in user_manage.products:
                            for p in products_from_db:
                                if u_m_entity.uuid_product == p.uuid:
                                    status_product = session_trans.query(StatusProduct).filter_by(
                                        status_product=u_m_entity.product_status).first()
                                    if status_product is None:
                                        e = api_error('ObjectNotFound')
                                        e.error['description'] = e.error['description'] \
                                                                 + f' <status_product> {u_m_entity.product_status}'
                                        abort(code=e.status_code, message=e.message, error=e.error)

                                    p.status_id = status_product.id

                    else:
                        e = api_error('ObjectNotFound')
                        e.error['description'] = e.error['description'] + f' <uuid_product> {missing}'
                        abort(code=e.status_code, message=e.message, error=e.error)

            except Exception as e:
                session_trans.rollback()
                if isinstance(e, UnprocessableEntity):
                    abort(code=e.code, message=None, error=e.data['error'])
                else:
                    current_app.logger.error(f"Error undefended saving states approval: {str(e)}")

            else:
                session_trans.commit()

                # Send to email when user was approval or rejected by user-admin
                def send_approved_rejected_user():
                    data_to_render = {'comment': user_manage.comment_approval}
                    send_email_with_template(uuid_user=user_manage.uuid_user,
                                             type_email="TemplateAdminUser" + status.status_user,
                                             render_data=data_to_render)

                if status.status_user == 'Approved' and old_user_status != 'Approved':
                    send_approved_rejected_user()

                if status.status_user == 'Rejected' and old_user_status != 'Rejected':
                    send_approved_rejected_user()

                # Send to email each product if product was approved or rejected by user-admin
                if user_manage.products is not None:
                    for u_m_entity in user_manage.products:
                        if u_m_entity.product_status == 'Approved' or u_m_entity.product_status == 'Rejected':
                            render_data = {'comment': user_manage.comment_approval}
                            send_email_with_template(uuid_user=user_manage.uuid_user,
                                                     type_email="TemplateAdminProduct" + u_m_entity.product_status,
                                                     render_data=render_data)
                return user_manage

    def get_whatsapp_link(self, jwt, uuid) -> str:
        whatsapp_phone = get_whatsapp_phone(uuid)
        if whatsapp_phone is not None:
            link_whatsapp = f"https://wa.me/{whatsapp_phone}?text=I'm%20interested%20in%20your%20bazar%20product"
            dict_response = {"whatsapp_phone": link_whatsapp}
        else:
            dict_response = {"whatsapp_phone": None}
        return dict_response
