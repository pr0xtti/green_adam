from typing import Any

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import MetaData

from core.config import settings

metadata = MetaData(schema=settings.POSTGRES_SCHEMA_STAGING)


@as_declarative(metadata=metadata)
class Base:
    id: Any
    __name__: str

    # To generate tablename from class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
