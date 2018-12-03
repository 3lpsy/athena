
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from minerva.utils import minerva_path
from minerva.utils import logger

managersession = sessionmaker()
metadata = MetaData()
Base = declarative_base(metadata=metadata)

_engine = None

def get_engine():
    global _engine
    if _engine == None:
        _engine = create_engine('sqlite:///{}'.format(minerva_path('manager.sqlite')))
    return _engine

def load_database_engine():
    global managersession
    global metadata
    engine = get_engine()
    managersession.configure(bind=_engine)
    metadata.reflect(bind=_engine)


def load_database_tables():
    logger().debug("Creating all manager tables")
    Base.metadata.create_all(_engine)
