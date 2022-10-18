import sqlalchemy.ext.declarative as dec
from sqlalchemy import MetaData

from src.infrastructure.config.default_infra import DB_SCHEMA

base = dec.declarative_base()
if DB_SCHEMA != "public":
    base = dec.declarative_base(metadata=MetaData(schema=DB_SCHEMA))

