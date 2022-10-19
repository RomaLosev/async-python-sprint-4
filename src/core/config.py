import os

from pydantic import BaseSettings, PostgresDsn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET = os.getenv('SECRET')
BLOCKED_IPS = []


class AppSettings(BaseSettings):
    app_title: str = "URLShortener"
    database_dsn: PostgresDsn

    class Config:
        env_file = '.env'


app_settings = AppSettings()
