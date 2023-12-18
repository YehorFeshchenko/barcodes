from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base
from Server.models.drug import drug_store_association


class Store(Base):
    """stores"""
    __tablename__ = 'drugstores'
    uid = Column(Integer,
                 Sequence('drugstores_uid_seq'),
                 primary_key=True,
                 server_default=Sequence('drugstores_uid_seq').next_value(),
                 autoincrement=True)
    name = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.uid', onupdate='CASCADE'))
    address = relationship("Address", back_populates='stores')
    chain_id = Column(Integer, ForeignKey('chains.uid', onupdate='CASCADE', ondelete='CASCADE'))
    chain = relationship("Chain", back_populates='stores')

    drugs = relationship('Drug', secondary=drug_store_association, back_populates='stores')

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
