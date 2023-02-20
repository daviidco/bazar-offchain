from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
import sys

from src.infrastructure.config.config_parameters import get_database_connection

sys.path = ['', '..'] + sys.path[1:]

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
SQLALCHEMY_DATABASE_URI, DB_SCHEMA = get_database_connection()
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URI)
config.set_main_option("script_location", "myapp:migrations")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# Code to recognize all models
from src.infrastructure.adapters.database.models.model_base import base
import src.infrastructure.adapters.database.models

target_metadata = base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def include_name(name, type_, parent_names):
    if type_ == "schema":
        # note this will not include the default schema
        return name in [None]
    else:
        return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name
    )

    with context.begin_transaction():
        context.execute(f'create schema if not exists {target_metadata.schema};')
        context.execute(f'set search_path to {target_metadata.schema}')
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            # new
            version_table_schema=target_metadata.schema,
            include_schemas=True,
            include_name=include_name
        )

        with context.begin_transaction():
            """
            By default search_path is setted to "$user",public 
            that why alembic can't create foreign keys correctly
            """
            context.execute('SET search_path TO public')
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
