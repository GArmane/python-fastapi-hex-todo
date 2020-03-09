from typing import Callable

from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str
    PYTHONPATH: str
    LOG_LEVEL: str
    WEB_APP_DEBUG: bool
    WEB_APP_DESCRIPTION: str
    WEB_APP_TITLE: str
    WEB_APP_VERSION: str
    WEB_SERVER_HOST: str
    WEB_SERVER_PORT: int
    WEB_SERVER_RELOAD: bool


def _initial_settings_clojure() -> Callable[[], Settings]:
    load_dotenv()
    settings = Settings()

    def fn() -> Settings:
        return settings

    return fn


get_initial_settings = _initial_settings_clojure()


def get_current_settings() -> Settings:
    return Settings()
