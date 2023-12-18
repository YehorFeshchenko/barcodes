from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base


class City(Base):
    """cities"""
    __tablename__ = 'cities'
    uid = Column(Integer,
                 Sequence('cities_uid_seq'),
                 primary_key=True,
                 server_default=Sequence('cities_uid_seq').next_value(),
                 autoincrement=True)
    name = Column(Text, nullable=False)
    addresses = relationship("Address", back_populates='city')

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
