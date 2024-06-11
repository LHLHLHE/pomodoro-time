from pydantic import BaseModel


class UserLogin(BaseModel):
    id: int
    access_token: str


class UserCreate(BaseModel):
    username: str
    password: str
