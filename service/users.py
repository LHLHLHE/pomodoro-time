from dataclasses import dataclass

from repository import UsersRepository
from schemas import UserLogin
from service.auth import AuthService


@dataclass
class UserService:
    user_repo: UsersRepository
    auth_service: AuthService

    def create_user(self, username: str, password: str) -> UserLogin:
        user = self.user_repo.create_user(username, password)
        access_token = self.auth_service.generate_access_token(user.id)
        return UserLogin(id=user.id, access_token=access_token)
