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

import sqlalchemy.ext.declarative as dec
from sqlalchemy import MetaData

from src.infrastructure.config.default_infra import DB_SCHEMA

#
# This code is to let works with postgresql schemas or with public schema default. Check file .env of Alembic
# @author David Córdoba
#

base = dec.declarative_base()
if DB_SCHEMA != "public":
    base = dec.declarative_base(metadata=MetaData(schema=DB_SCHEMA))
