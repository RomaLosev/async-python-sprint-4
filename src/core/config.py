import os

from pydantic import BaseSettings, PostgresDsn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class AppSettings(BaseSettings):
    app_title: str = "URLShortener"
    database_dsn: PostgresDsn

    class Config:
        env_file = '.env'


app_settings = AppSettings()
