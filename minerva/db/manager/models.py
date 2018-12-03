from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from minerva.db.manager.session import Base

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(254))
    code = Column('code', String(32), unique=True)
    description = Column('description', Text())

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(254))
    code = Column('code', String(32), unique=True)
    description = Column('description', Text())
    skippable = Column('skippable', Boolean)
