from sqlalchemy import *
from sqlalchemy.orm import relationship

from Server.models.base import Base


drug_store_association = Table(
    'stock', Base.metadata,
    Column('drug_id', Integer, ForeignKey('drugs.uid')),
    Column('store_id', Integer, ForeignKey('drugstores.uid')),
    Column('quantity', DOUBLE_PRECISION),
    Column('price', DOUBLE_PRECISION)
)


class Drug(Base):
    """drugs"""
    __tablename__ = 'drugs'
    uid = Column(Integer,
                 Sequence('drugs_uid_seq'),
                 primary_key=True,
                 server_default=Sequence('drugs_uid_seq').next_value(),
                 autoincrement=True)
    name = Column(Text, nullable=False)
    barcode = Column(VARCHAR, nullable=False)
    exp_date = Column(Date, nullable=False)
    serial_no = Column(Text, nullable=False)
    prescription = Column(Boolean, nullable=False, default=False)
    type_id = Column(Integer, ForeignKey('types.uid', onupdate='CASCADE'))
    type = relationship("Type", back_populates='drugs')
    main_subs_id = Column(Integer, ForeignKey('substances.uid', onupdate='CASCADE'))
    subs = relationship("Substance", back_populates='drugs')
    trademark_id = Column(Integer, ForeignKey('trademarks.uid', onupdate='CASCADE'))
    mark = relationship("Mark", back_populates='drugs')

    stores = relationship('Store', secondary=drug_store_association, back_populates='drugs')

    def __init__(self, name, barcode, exp_date, serial_no, prescription, type_id, main_subs_id, trademark_id):
        self.name = name
        self.barcode = barcode
        self.exp_date = exp_date
        self.serial_no = serial_no
        self.prescription = prescription
        self.type_id = type_id
        self.main_subs_id = main_subs_id
        self.trademark_id = trademark_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
