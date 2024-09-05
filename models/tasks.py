from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Tasks(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('UserProfiles.id'), nullable=False)


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Optional[str]]
    name: Mapped[str]
