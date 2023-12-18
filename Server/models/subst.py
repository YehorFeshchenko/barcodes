from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base


class Substance(Base):
    """substances"""
    __tablename__ = 'substances'
    uid = Column(Integer,
                 Sequence('substances_uid_seq'),
                 primary_key=True,
                 server_default=Sequence('substances_uid_seq').next_value(),
                 autoincrement=True)
    name = Column(Text, nullable=False)
    drugs = relationship("Drug", back_populates='subs')

    def __init__(self, name):
        self.name = name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
