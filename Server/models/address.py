from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base


class Address(Base):
    """addresses"""
    __tablename__ = 'addresses'
    address_id = Column(Integer,
                        Sequence('addresses_address_id_seq'),
                        primary_key=True,
                        server_default=Sequence('addresses_address_id_seq').next_value(),
                        autoincrement=True)
    street = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    zip_code = Column(Text)
    country = Column(Text, nullable=False)

    stores = relationship("Store", back_populates='address')

    def __init__(self, street, city, state, zip_code, country):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
