from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV: str
    PYTHONPATH: str
    WEB_SERVER_DEBUG: bool
    WEB_SERVER_TITLE: str
    WEB_SERVER_DESCRIPTION: str
    WEB_SERVER_VERSION: str


load_dotenv()
