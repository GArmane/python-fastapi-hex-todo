import uvicorn
from todolist.config.environment import get_current_settings


def start_web_server() -> None:
    settings = get_current_settings()
    uvicorn.run(
        "todolist:web_app",
        host=settings.WEB_SERVER_HOST,
        port=settings.WEB_SERVER_PORT,
        reload=settings.WEB_SERVER_RELOAD,
        log_level=settings.LOG_LEVEL,
    )


start_web_server()
