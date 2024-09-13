from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from models import UserProfiles
from schemas import UserCreate


@dataclass
class UsersRepository:
    db_session: Session

    def create_user(self, user: UserCreate) -> UserProfiles:
        query = insert(UserProfiles).values(**user.model_dump()).returning(UserProfiles.id)
        with self.db_session() as session:
            user_id: int = session.execute(query).scalar()
            session.commit()
            session.flush()
        return self.get_user(user_id)

    def get_user(self, user_id: int) -> UserProfiles | None:
        with self.db_session() as session:
            return session.execute(
                select(UserProfiles).where(UserProfiles.id == user_id)
            ).scalar_one_or_none()

    def get_user_by_username(self, username: str) -> UserProfiles | None:
        with self.db_session() as session:
            return session.execute(
                select(UserProfiles).where(UserProfiles.username == username)
            ).scalar_one_or_none()

    def get_user_by_email(self, email: str) -> UserProfiles | None:
        with self.db_session() as session:
            return session.execute(
                select(UserProfiles).where(UserProfiles.email == email)
            ).scalar_one_or_none()
