

# Add all your SQLAlchemy models here.
# This allows you to import just this file
# whenever you need to work with your models
# (like creating tables or for migrations)
# If alembic not generate the table please check env.py of alembic

from src.infrastructure.adapters.database.models.user import User
from src.infrastructure.adapters.database.models.company import Company
from src.infrastructure.adapters.database.models.producto import *