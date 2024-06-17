import os
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from .models import Base

engine: Engine | None = None
DBSession = sessionmaker()


def init_db(db_name: str):
    current_file_path = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file_path)

    db_file = os.path.join(current_directory, db_name)

    engine = create_engine(f'sqlite:///{db_file}')
    Base.metadata.bind = engine
    DBSession.configure(bind=engine)
