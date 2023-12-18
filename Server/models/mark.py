from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base


class Mark(Base):
    """trademarks"""
    __tablename__ = 'trademarks'
    uid = Column(Integer,
                 Sequence('trademarks_uid_seq'),
                 primary_key=True,
                 server_default=Sequence('trademarks_uid_seq').next_value(),
                 autoincrement=True)
    name = Column(Text, nullable=False)
    drugs = relationship("Drug", back_populates='mark')

    def __init__(self, name):
        self.name = name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
