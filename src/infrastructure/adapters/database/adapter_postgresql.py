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

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from src.infrastructure.config.config_parameters import get_database_connection


#
# This class lets connect with postgresql
# @author David Córdoba
#
class PostgresAdapter:
    def __init__(self) -> None:
        SQLALCHEMY_DATABASE_URI, DB_SCHEMA = get_database_connection()
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI,
                                    connect_args={'options': '-csearch_path={}'.format(DB_SCHEMA)})

        @event.listens_for(self.engine, "connect", insert=True)
        def set_current_schema(dbapi_connection, connection_record):
            cursor_obj = dbapi_connection.cursor()
            cursor_obj.execute(f'SET SEARCH_PATH = "{DB_SCHEMA}"')
            cursor_obj.close()
