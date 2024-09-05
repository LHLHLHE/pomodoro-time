from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserProfiles(Base):
    __tablename__ = 'UserProfiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
