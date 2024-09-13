import datetime as dt
from dataclasses import dataclass

from jose import jwt, JWTError

from client import GoogleClient, YandexClient
from exceptions import (
    UserNotFoundException,
    UserIncorrectPasswordException,
    TokenExpiredException,
    InvalidTokenException
)
from models import UserProfiles
from repository import UsersRepository
from schemas import UserLogin, UserCreate
from settings import Settings


@dataclass
class AuthService:
    user_repo: UsersRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    def login(self, username: str, password: str) -> UserLogin:
        user = self.user_repo.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user.id)
        return UserLogin(id=user.id, access_token=access_token)

    def get_google_redirect_url(self):
        return self.settings.google_redirect_url

    def auth_google(self, code: str):
        user_data = self.google_client.get_user_info(code)

        if user := self.user_repo.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user.id)
            return UserLogin(id=user.id, access_token=access_token)

        create_user_data = UserCreate(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name
        )
        created_user = self.user_repo.create_user(create_user_data)
        access_token = self.generate_access_token(created_user.id)
        return UserLogin(id=created_user.id, access_token=access_token)

    def get_yandex_redirect_url(self):
        return self.settings.yandex_redirect_url

    def auth_yandex(self, code: str):
        user_data = self.yandex_client.get_user_info(code)

        if user := self.user_repo.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user.id)
            return UserLogin(id=user.id, access_token=access_token)

        create_user_data = UserCreate(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name
        )
        created_user = self.user_repo.create_user(create_user_data)
        access_token = self.generate_access_token(created_user.id)
        return UserLogin(id=created_user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfiles, password: str):
        if not user:
            raise UserNotFoundException()
        if user.password != password:
            raise UserIncorrectPasswordException()

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (dt.datetime.utcnow() + dt.timedelta(days=7)).timestamp()
        return jwt.encode(
            {'user_id': user_id, 'expire': expires_date_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM
        )

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALGORITHM]
            )
        except JWTError:
            raise InvalidTokenException()

        if payload['expire'] < dt.datetime.utcnow().timestamp():
            raise TokenExpiredException()

        return payload['user_id']
