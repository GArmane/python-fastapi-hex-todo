import uvicorn
from todolist.config.environment import get_initial_settings
from todolist.interfaces.fastapi import app as web_app


def main() -> None:
    conf = get_initial_settings()
    uvicorn.run(
        web_app,
        host=conf.WEB_SERVER_HOST,
        port=conf.WEB_SERVER_PORT,
        log_level=conf.LOG_LEVEL,
    )


if __name__ == "__main__":
    main()
