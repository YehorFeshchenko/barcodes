from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base


class Address(Base):
    """addresses"""
    __tablename__ = 'addresses'
    uid = Column(Integer,
                 Sequence('addresses_uid_seq'), primary_key=True,
                 server_default=Sequence('addresses_uid_seq').next_value(),
                 autoincrement=True)
    street = Column(Text, nullable=False)
    building = Column(VARCHAR, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.uid', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    city = relationship("City", back_populates='addresses')
    stores = relationship("Store", back_populates='address')

    def __init__(self, street, building):
        self.street = street
        self.building = building

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
