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

from flask import Blueprint
from flask_restx import Api

from src.infrastructure.adapters.flask.app.controllers.avatar.avatar_resources import api as avatar_ns

#
# This file lets instance a blueprint.
# @author David Córdoba
#
avatars_v1_01_bp = Blueprint('avatars_v1_01_bp', __name__)

api = Api(avatars_v1_01_bp, version="0.1.0", title="Avatar")
api.add_namespace(avatar_ns, path='/v1/avatars')
