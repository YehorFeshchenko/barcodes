from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base


class User(Base):
    """users"""
    __tablename__ = 'users'
    uid = Column(Integer,
                 Sequence('users_uid_seq'),
                 primary_key=True,
                 server_default=Sequence('users_uid_seq').next_value(),
                 autoincrement=True)
    username = Column(VARCHAR, nullable=False, unique=True)
    password = Column(VARCHAR, nullable=False)
    fullname = Column(Text, nullable=False)
    admin = Column(Boolean, default=False, nullable=False)
    chain_id = Column(Integer, ForeignKey('chains.uid', onupdate='CASCADE', ondelete='CASCADE'))
    chain = relationship("Chain", back_populates='users')

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
