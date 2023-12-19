# Server/models/store.py

from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base
from Server.models.address import Address


class Store(Base):
    """stores"""
    __tablename__ = 'stores'
    store_id = Column(Integer,
                      Sequence('stores_store_id_seq'),
                      primary_key=True,
                      server_default=Sequence('stores_store_id_seq').next_value(),
                      autoincrement=True)
    name = Column(Text, nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.address_id', onupdate='CASCADE'))
    phone = Column(Text)
    email = Column(Text)

    components = relationship("Component", back_populates='store')
    address = relationship("Address", back_populates='stores')

    def __init__(self, name, address_id, phone, email):
        self.name = name
        self.address_id = address_id
        self.phone = phone
        self.email = email

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
