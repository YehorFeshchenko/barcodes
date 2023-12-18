from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base


class Chain(Base):
    """chains"""
    __tablename__ = 'chains'
    uid = Column(Integer,
                 Sequence('chains_uid_seq'),
                 primary_key=True,
                 server_default=Sequence('chains_uid_seq').next_value(),
                 autoincrement=True)
    name = Column(Text, nullable=False)
    stores = relationship("Store", back_populates='chain')
    users = relationship("User", back_populates='chain')

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
