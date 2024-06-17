import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .models import Base



def create_db(db_name: str, script_file: str):
    current_file_path = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_file_path)

    db_file = os.path.join(current_directory, db_name)

    engine = create_engine(f'sqlite:///{db_file}')
    Base.metadata.create_all(engine)

    script_file = os.path.join(current_directory, script_file)

    with engine.connect() as connection:
        with open(script_file) as f:
            sql_script = f.read()
            statements = sql_script.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:
                    connection.execute(text(statement))
