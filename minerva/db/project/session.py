
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from minerva.utils import minerva_path
from minerva.utils import logger

projectsession = sessionmaker()
metadata = MetaData()
Base = declarative_base(metadata=metadata)

_engine = None

def get_engine(db_path):
    global _engine
    if _engine == None:
        _engine = create_engine('sqlite:///{}'.format(db_path))
    return _engine

def load_database_engine(db_path):
    global projectsession
    global metadata
    engine = get_engine(db_path)
    projectsession.configure(bind=_engine)
    metadata.reflect(bind=_engine)


def load_database_tables(db_path):
    logger().debug("Creating all manager tables")
    Base.metadata.create_all(_engine)
