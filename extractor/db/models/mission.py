from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from db.base_class import Base


class Mission(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    external_object_id = Column(String, unique=True, nullable=False)
    launches = relationship('Launch', back_populates='mission')
