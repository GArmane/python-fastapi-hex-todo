import uvicorn
from todolist.config.environment import get_current_settings
from todolist.interfaces.fastapi import create_app


_SETTINGS = get_current_settings()
WEB_APP = create_app(_SETTINGS)


def start_web_server() -> None:
    uvicorn.run(
        "todolist:WEB_APP",
        host=_SETTINGS.WEB_SERVER_HOST,
        port=_SETTINGS.WEB_SERVER_PORT,
        reload=_SETTINGS.WEB_SERVER_RELOAD,
        log_level=_SETTINGS.LOG_LEVEL,
    )
