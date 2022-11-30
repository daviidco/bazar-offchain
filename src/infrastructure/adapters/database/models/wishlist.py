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


from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from src.infrastructure.adapters.database.models.model_base import base


#
# These models are related with wishlist model they are defined to create database table.
# @author David Córdoba
#


class WishList(base):
    # Don't forget import model in __init__.py to alembic works
    __tablename__ = 'wish_lists'
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)

    product = relationship("Product", backref="user_wish_list")
    user = relationship("User", backref="product_wish_list")

    # Association Proxy
    user_uuid = association_proxy("product", "uuid")
    product_uuid = association_proxy("user", "uuid")

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    def __repr__(self):
        return f'<WishList user_uuid {self.user_id}, product_id {self.user_uuid}>'

    def __str__(self):
        return f'<WishList user_uuid {self.user_id}, product_id {self.product_uuid}>'
    