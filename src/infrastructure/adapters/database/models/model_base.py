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

from src.infrastructure.config.config_parameters import get_database_connection

#
# This code is to let works with postgresql schemas or with public schema default. Check file .env of Alembic
# @author David Córdoba
#

conn, db_schema = get_database_connection()
base = dec.declarative_base()
if db_schema != "public":
    base = dec.declarative_base(metadata=MetaData(schema=db_schema))
