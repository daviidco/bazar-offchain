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
from src.domain.entities.product_entity import ProductsPaginationEntity, ProductFilterBuyerBasicProductEntity, \
    ProductFilterBuyerEntity
from src.domain.entities.wishlist_entity import WishProductNewEntity, WishProductEntity
from src.domain.ports.wishlist_interface import IWishListRepository
from src.infrastructure.adapters.database.models import WishList, Product, BasicProduct
from src.infrastructure.adapters.database.repositories.utils import get_total_pages, get_urls_files_and_images, \
    get_field_is_like, get_user_by_uuid_user, get_product_by_uuid_product
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


#
# This repository contains logic main related with wishlist.
# @author David Córdoba
#

class WishListRepository(IWishListRepository):

    def __init__(self, adapter_db, utils_db):
        self.session_maker = sessionmaker(bind=adapter_db.engine)
        self.__utils_db = utils_db

    def new_product_on_wishlist(self, wish_product_entity: WishProductNewEntity) -> WishProductEntity:
        with self.session_maker() as session:
            user = get_user_by_uuid_user(session, wish_product_entity.user_uuid)
            product = get_product_by_uuid_product(session, wish_product_entity.product_uuid)
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

    def delete_product_from_wishlist(self, wish_product_entity: WishProductNewEntity):
        with self.session_maker() as session:
            user = get_user_by_uuid_user(session, wish_product_entity.user_uuid)
            product = get_product_by_uuid_product(session, wish_product_entity.product_uuid)
            object_to_delete = session.query(WishList).filter_by(user_id=user.id, product_id=product.id)
            object_to_delete.delete()
            session.commit()
            response = DeleteEntity(description=f'Wish product of user: {user.uuid}')
            current_app.logger.info(f"Wish product {object_to_delete} deleted")
            return response

    def get_wishlist_by_uuid_buyer(self, uuid: str, limit: int, offset: int) -> ProductsPaginationEntity:
        with self.session_maker() as session:
            user_id = self.__utils_db.get_user_by_uuid_user(uuid).id
            query = session.query(Product)\
                .join(WishList, Product.id == WishList.product_id)\
                .filter(WishList.user_id == user_id)

            total = query.from_self().count()
            list_objects = query.offset(offset).limit(limit).all()
            total_pages = get_total_pages(total, int(limit))
            for p in list_objects:
                p.check_use_like(uuid)

            list_e_objects = get_urls_files_and_images(list_objects)
            return ProductsPaginationEntity(limit=limit, offset=offset, total=total, results=list_e_objects,
                                            total_pages=total_pages)

    def get_wishlist_by_uuid_buyer_and_basic_product(self, filter_entity: ProductFilterBuyerBasicProductEntity) \
            -> ProductsPaginationEntity:
        with self.session_maker() as session:
            user = get_user_by_uuid_user(session, filter_entity.user_uuid)
            query = session.query(Product) \
                .join(WishList, WishList.product_id == Product.id) \
                .join(BasicProduct, Product.basic_product_id == BasicProduct.id) \
                .filter(WishList.user_id == user.id) \
                .filter(BasicProduct.basic_product == filter_entity.basic_product) \

            total = query.from_self().count()
            list_objects = query.offset(filter_entity.offset).limit(filter_entity.limit).all()
            total_pages = get_total_pages(total, int(filter_entity.limit))

            list_objects = get_field_is_like(list_objects, filter_entity.user_uuid)

            list_e_objects = get_urls_files_and_images(list_objects)
            return ProductsPaginationEntity(limit=filter_entity.limit, offset=filter_entity.offset, total=total,
                                            results=list_e_objects, total_pages=total_pages)

    def get_wishlist_by_uuid_buyer_and_search_bar(self, filter_entity: ProductFilterBuyerBasicProductEntity) \
            -> ProductsPaginationEntity:
        with self.session_maker() as session:
            user = get_user_by_uuid_user(session, filter_entity.user_uuid)
            query = session.query(Product) \
                .join(WishList, WishList.product_id == Product.id) \
                .join(BasicProduct, Product.basic_product_id == BasicProduct.id) \
                .filter(WishList.user_id == user.id) \
                .filter(BasicProduct.basic_product.ilike('%' + filter_entity.basic_product + '%')) \

            total = query.from_self().count()
            list_objects = query.offset(filter_entity.offset).limit(filter_entity.limit).all()
            total_pages = get_total_pages(total, int(filter_entity.limit))

            list_objects = get_field_is_like(list_objects, filter_entity.user_uuid)
            list_e_objects = get_urls_files_and_images(list_objects)

            return ProductsPaginationEntity(limit=filter_entity.limit, offset=filter_entity.offset, total=total,
                                            results=list_e_objects, total_pages=total_pages)

    def get_wishlist_filter(self, filter_entity: ProductFilterBuyerEntity) -> ProductsPaginationEntity:
        with self.session_maker() as session:
            user = get_user_by_uuid_user(session, filter_entity.user_uuid)
            query = session.query(Product) \
                .join(WishList, WishList.product_id == Product.id) \
                .filter(WishList.user_id == user.id) \
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
