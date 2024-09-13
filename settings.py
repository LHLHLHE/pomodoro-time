from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_NAME: str = 'pomodoro'

    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    JWT_SECRET_KEY: str ='secret'
    JWT_ENCODE_ALGORITHM: str = 'HS256'

    GOOGLE_CLIENT_ID: str = ''
    GOOGLE_CLIENT_SECRET: str = ''
    GOOGLE_REDIRECT_URI: str = ''
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'

    YANDEX_CLIENT_ID: str = ''
    YANDEX_CLIENT_SECRET: str = ''
    YANDEX_REDIRECT_URI: str = ''
    YANDEX_TOKEN_URL: str = 'https://oauth.yandex.ru/token'

    @property
    def db_url(self):
        return (
            f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )

    @property
    def google_redirect_url(self):
        return (
            'https://accounts.google.com/o/oauth2/auth?response_type=code'
            f'&client_id={self.GOOGLE_CLIENT_ID}'
            f'&redirect_uri={self.GOOGLE_REDIRECT_URI}'
            '&scope=openid%20email%20profile'
            '&access_type=offline'
        )

    @property
    def yandex_redirect_url(self):
        return (
            'https://oauth.yandex.ru/authorize?response_type=code'
            f'&client_id={self.YANDEX_CLIENT_ID}'
            f'&redirect_uri={self.YANDEX_REDIRECT_URI}'
        )
