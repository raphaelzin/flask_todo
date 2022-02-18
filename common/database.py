import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PW')
DB_PORT = str(os.getenv('DB_PORT'))
DB_NAME = os.getenv('DB_NAME')

db_engine = create_engine("postgresql://{0}:{1}@{2}:{3}/{4}".format(DB_USER, DB_PWD, DB_HOST, DB_PORT, DB_NAME), 
                          echo=True, 
                          future=True,
                          isolation_level="READ UNCOMMITTED")

def get_session() -> Session:
    with Session(db_engine) as session:
        return session