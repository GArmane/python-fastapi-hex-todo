from fastapi.applications import FastAPI
from toolz import pipe

from todolist.config.environment import Settings
from todolist.interfaces.fastapi.api import root


def init_app(settings: Settings) -> FastAPI:
    return FastAPI(
        debug=settings.WEB_APP_DEBUG,
        title=settings.WEB_APP_TITLE,
        description=settings.WEB_APP_DESCRIPTION,
        version=settings.WEB_APP_VERSION,
    )


def register_applications(app: FastAPI) -> FastAPI:
    return app


def register_middlewares(app: FastAPI) -> FastAPI:
    return app


def register_routers(app: FastAPI) -> FastAPI:
    app.include_router(root.router)
    return app


def create_app(settings: Settings) -> FastAPI:
    app: FastAPI = pipe(
        settings,
        init_app,
        register_middlewares,
        register_routers,
        register_applications,
    )
    return app
