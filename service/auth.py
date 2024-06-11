from dataclasses import dataclass

from exceptions import UserNotFoundException, UserIncorrectPasswordException
from models import UserProfiles
from repository import UsersRepository
from schemas import UserLogin


@dataclass
class AuthService:
    user_repo: UsersRepository

    def login(self, username: str, password: str) -> UserLogin:
        user = self.user_repo.get_user_by_username(username)
        self._validate_auth_user(user, password)
        return UserLogin(id=user.id, access_token=user.access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfiles, password: str):
        if not user:
            raise UserNotFoundException()
        if user.password != password:
            raise UserIncorrectPasswordException()
