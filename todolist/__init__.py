import uvicorn

from todolist.config.environment import get_settings
from todolist.api import init_app


_SETTINGS = get_settings()


web_app = init_app(_SETTINGS)


def start_web_server() -> None:
    settings = get_settings()
    uvicorn.run(
        "todolist:web_app",
        host=settings.WEB_SERVER_HOST,
        port=settings.WEB_SERVER_PORT,
        reload=settings.WEB_SERVER_RELOAD,
        log_level=settings.LOG_LEVEL,
    )
