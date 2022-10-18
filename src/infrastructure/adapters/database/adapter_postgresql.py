from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from src.infrastructure.config.default_infra import SQLALCHEMY_DATABASE_URI, DB_SCHEMA


class PostgresAdapter:
    def __init__(self) -> None:
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI,
                                    connect_args={'options': '-csearch_path={}'.format(DB_SCHEMA)})
        self.session = Session(self.engine)
        self.session_marker = sessionmaker(self.engine)

        @event.listens_for(self.engine, "connect", insert=True)
        def set_current_schema(dbapi_connection, connection_record):
            cursor_obj = dbapi_connection.cursor()
            cursor_obj.execute(f'SET SEARCH_PATH = "{DB_SCHEMA}"')
            cursor_obj.close()
