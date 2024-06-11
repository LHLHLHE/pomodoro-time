from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declared_attr

from settings import Settings

settings = Settings()
engine = create_engine(settings.db_url)
Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session


class Base(DeclarativeBase):
    id: Any
    __name__: str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
