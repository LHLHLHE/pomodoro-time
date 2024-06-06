from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLITE_DB_NAME: str = 'pomodoro.sqlite'
