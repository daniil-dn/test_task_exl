import datetime
import random

from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey, BigInteger, Identity
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __repr__(self):
        return 'id: {}, role: {}'.format(self.id, self.name)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    role_id = Column(Integer, ForeignKey('role.id'), unique=False, )
    role = relationship(Role)
    birth = Column(DateTime,
                   default=datetime.datetime(year=random.randint(1930, 2000), month=random.randint(1, 12),
                                             day=random.randint(1, 28)))
    when = Column(DateTime, default=func.now())
    def __repr__(self):
        return 'name: {}, role: {}, birth: {}\n'.format(self.name, self.role_name, self.birth)

