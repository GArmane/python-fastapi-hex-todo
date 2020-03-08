import logging

import uvicorn
from todolist.config.environment import get_initial_settings
from todolist.interfaces.fastapi import app as web_app


def start_web_server() -> None:
    conf = get_initial_settings()
    logging.getLogger().info(f"Initializing {web_app.title}")
    uvicorn.run(
        "todolist:web_app",
        host=conf.WEB_SERVER_HOST,
        port=conf.WEB_SERVER_PORT,
        reload=conf.WEB_SERVER_RELOAD,
        log_level=conf.LOG_LEVEL,
    )
