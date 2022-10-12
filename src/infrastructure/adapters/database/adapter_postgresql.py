from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.infrastructure.config.default_infra import SQLALCHEMY_DATABASE_URI


class PostgresAdapter:
    def __init__(self) -> None:
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        self.session = Session(self.engine)
