from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base


class Component(Base):
    """components"""
    __tablename__ = 'components'
    component_id = Column(Integer,
                          Sequence('components_component_id_seq'),
                          primary_key=True,
                          server_default=Sequence('components_component_id_seq').next_value(),
                          autoincrement=True)
    name = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id', onupdate='CASCADE'))
    brand_id = Column(Integer, ForeignKey('brands.brand_id', onupdate='CASCADE'))
    store_id = Column(Integer, ForeignKey('stores.store_id', onupdate='CASCADE'))
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    stock_quantity = Column(Integer, nullable=False)
    barcode = Column(VARCHAR, nullable=False)

    category = relationship("Category", back_populates='components')
    brand = relationship("Brand", back_populates='components')
    store = relationship("Store", back_populates='components')

    def __init__(self, name, category_id, brand_id, store_id, price, description, stock_quantity, barcode):
        self.name = name
        self.category_id = category_id
        self.brand_id = brand_id
        self.store_id = store_id
        self.price = price
        self.description = description
        self.stock_quantity = stock_quantity
        self.barcode = barcode

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
