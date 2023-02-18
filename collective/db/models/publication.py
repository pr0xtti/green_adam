from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from db.mart.base_class import BaseMartModel


class Publication(BaseMartModel):
    id = Column(Integer, primary_key=True, index=True)
    entity = Column(String, unique=True, nullable=False)
    articles = Column(Integer)
    wikipedia = Column(Integer)

    def __str__(self):
        return f"Publication({self.entity}, {self.articles}, {self.wikipedia})"

    def __repr__(self):
        return f"Publication({self.entity}, {self.articles}, {self.wikipedia})"
