from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from minerva.db.manager.session import Base

class AssignedTask(Base):
    __tablename__ = 'assigned_tasks'
    id = Column(Integer, primary_key=True)
    name = Column('name', String(254))
    code = Column('code', String(32), unique=True)
    description = Column('description', Text())
    skippable = Column('skippable', Boolean)
    status = Column('skippable', Boolean)
