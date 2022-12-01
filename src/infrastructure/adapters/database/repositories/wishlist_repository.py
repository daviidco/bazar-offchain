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
from flask_restx import abort
from sqlalchemy.orm import Session

from src.domain.entities.common_entity import DeleteEntity
from src.domain.entities.wishlist_entity import WishProductNewEntity, WishProductEntity
from src.domain.ports.wishlist_interface import IWishListRepository
from src.infrastructure.adapters.database.models import WishList
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


#
# This repository contains logic main related with wishlist.
# @author David Córdoba
#

class WishListRepository(IWishListRepository):

    def __init__(self, logger, adapter_db, utils_db):
        self.logger = logger
        self.engine = adapter_db.engine
        self.session = Session(adapter_db.engine)
        self.utils_db = utils_db

    def new_product_on_wishlist(self, role: str, wish_product_entity: WishProductNewEntity) -> WishProductEntity:
        if role == 'buyer':
            user = self.utils_db.get_user_by_uuid_user(wish_product_entity.user_uuid)
            product = self.utils_db.get_product_by_uuid_product(wish_product_entity.product_uuid)
            object_to_save = WishList(
                user_id=user.id,
                product_id=product.id,
            )
            self.session.add(object_to_save)
            try:
                self.session.commit()
            except Exception as e:
                self.session.close()
                self.logger.error(f"Error saving wishlist")
                e = api_error('IntegrityError')
                abort(code=e.status_code, message=e.message, error=e.error)

            response = WishProductEntity.from_orm(object_to_save)
            self.logger.info(f"Wish product {object_to_save} saved")
            return response
        else:
            self.logger.info(f"Can't do action because the role is not buyer")
            e = api_error('RoleWithoutPermission')
            abort(code=e.status_code, message=e.message, error=e.error)

    def delete_product_from_wishlist(self, role: str, wish_product_entity: WishProductNewEntity):
        if role == 'buyer':
            user = self.utils_db.get_user_by_uuid_user(wish_product_entity.user_uuid)
            product = self.utils_db.get_product_by_uuid_product(wish_product_entity.product_uuid)
            object_to_delete = self.session.query(WishList).filter_by(user_id=user.id, product_id=product.id)
            object_to_delete.delete()
            self.session.commit()
            response = DeleteEntity(description=f'Wish product of user: {user.uuid}')
            self.logger.info(f"Wish product {object_to_delete} deleted")
            return response
        else:
            self.logger.info(f"Can't do action because the role is not buyer")
            e = api_error('RoleWithoutPermission')
            abort(code=e.status_code, message=e.message, error=e.error)
