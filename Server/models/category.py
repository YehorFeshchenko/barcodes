from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base


class Category(Base):
    """categories"""
    __tablename__ = 'categories'
    category_id = Column(Integer,
                         Sequence('categories_category_id_seq'),
                         primary_key=True,
                         server_default=Sequence('categories_category_id_seq').next_value(),
                         autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text)

    components = relationship("Component", back_populates='category')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
