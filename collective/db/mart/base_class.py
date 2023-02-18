from typing import Any

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import MetaData

from core.config import settings
from core.tool import camel_to_snake

metadata = MetaData(schema=settings.POSTGRES_SCHEMA_MARTS)


@as_declarative(metadata=metadata)
class BaseMartModel:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """To generate tablename from class name"""
        return camel_to_snake(cls.__name__)

