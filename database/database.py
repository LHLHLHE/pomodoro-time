from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import Settings

settings = Settings()
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/pomodoro')
Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session
