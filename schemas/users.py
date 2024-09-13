from pydantic import BaseModel


class UserLogin(BaseModel):
    id: int
    access_token: str


class UserCreate(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None
    name: str | None = None
    google_access_token: str | None = None
    yandex_access_token: str | None = None
