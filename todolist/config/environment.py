from typing import Callable

from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str
    PYTHONPATH: str
    LOG_LEVEL: str
    WEB_SERVER_DEBUG: bool
    WEB_SERVER_DESCRIPTION: str
    WEB_SERVER_HOST: str
    WEB_SERVER_PORT: int
    WEB_SERVER_RELOAD: bool
    WEB_SERVER_TITLE: str
    WEB_SERVER_VERSION: str


def _initial_settings_clojure() -> Callable[[], Settings]:
    load_dotenv()
    settings = Settings()

    def func() -> Settings:
        return settings

    return func


get_initial_settings = _initial_settings_clojure()


def get_current_settings() -> Settings:
    return Settings()
