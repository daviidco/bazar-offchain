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

from src.domain.entities.common_entity import DeleteEntity
from src.domain.entities.product_entity import ProductsPaginationEntity
from src.domain.entities.wishlist_entity import WishProductNewEntity, WishProductEntity
from src.domain.ports.wishlist_interface import IWishListRepository
from src.infrastructure.adapters.database.models import WishList, Product
from src.infrastructure.adapters.database.repositories.utils import get_total_pages
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


#
# This repository contains logic main related with wishlist.
# @author David Córdoba
#

class WishListRepository(IWishListRepository):

    def __init__(self, adapter_db, utils_db):
        self.session_maker = sessionmaker(bind=adapter_db.engine)
        self.utils_db = utils_db

    def new_product_on_wishlist(self, role: str, wish_product_entity: WishProductNewEntity) -> WishProductEntity:
        with self.session_maker() as session:
            if role != 'buyer':
                current_app.logger.info(f"Can't do action because the role is not buyer")
                e = api_error('RoleWithoutPermission')
                abort(code=e.status_code, message=e.message, error=e.error)

            user = self.utils_db.get_user_by_uuid_user(wish_product_entity.user_uuid)
            product = self.utils_db.get_product_by_uuid_product(wish_product_entity.product_uuid)
            object_to_save = WishList(
                user_id=user.id,
                product_id=product.id,
            )
            session.add(object_to_save)
            try:
                session.commit()
            except Exception as e:
                session.close()
                current_app.logger.error(f"Error saving wishlist")
                e = api_error('IntegrityError')
                abort(code=e.status_code, message=e.message, error=e.error)

            response = WishProductEntity.from_orm(object_to_save)
            current_app.logger.info(f"Wish product {object_to_save} saved")
            return response

    def delete_product_from_wishlist(self, role: str, wish_product_entity: WishProductNewEntity):
        with self.session_maker() as session:
            if role != 'buyer':
                current_app.logger.info(f"Can't do action because the role is not buyer")
                e = api_error('RoleWithoutPermission')
                abort(code=e.status_code, message=e.message, error=e.error)
            user = self.utils_db.get_user_by_uuid_user(wish_product_entity.user_uuid)
            product = self.utils_db.get_product_by_uuid_product(wish_product_entity.product_uuid)
            object_to_delete = session.query(WishList).filter_by(user_id=user.id, product_id=product.id)
            object_to_delete.delete()
            session.commit()
            response = DeleteEntity(description=f'Wish product of user: {user.uuid}')
            current_app.logger.info(f"Wish product {object_to_delete} deleted")
            return response

    def get_wishlist_by_uuid_buyer(self, uuid: str, role: str, limit: int, offset: int) -> ProductsPaginationEntity:
        with self.session_maker() as session:
            if role != 'buyer':
                current_app.logger.error(f"Role {role} can't list wishlist")
                e = api_error('RoleWithoutPermission')
                abort(code=e.status_code, message=e.message, error=e.error)
            user_id = self.utils_db.get_user_by_uuid_user(uuid).id
            query = session.query(Product)\
                .join(WishList, Product.id == WishList.product_id)\
                .filter(WishList.user_id == user_id)

            total = query.from_self().count()
            list_objects = query.offset(offset).limit(limit).all()
            total_pages = get_total_pages(total, int(limit))
            for p in list_objects:
                p.check_use_like(uuid)
            return ProductsPaginationEntity(limit=limit, offset=offset, total=total, results=list_objects,
                                            total_pages=total_pages)
