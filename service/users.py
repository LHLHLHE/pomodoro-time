import random
import string
from dataclasses import dataclass

from repository import UsersRepository
from schemas import UserLogin


@dataclass
class UserService:
    user_repo: UsersRepository

    def create_user(self, username: str, password: str) -> UserLogin:
        access_token: str = self._generate_access_token()
        user = self.user_repo.create_user(username, password, access_token)
        return UserLogin(id=user.id, access_token=user.access_token)

    @staticmethod
    def _generate_access_token() -> str:
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
