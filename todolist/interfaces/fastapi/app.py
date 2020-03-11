from fastapi.applications import FastAPI
from toolz import pipe

from todolist.config.environment import Settings
from todolist.interfaces.fastapi.api import root, todo


def _create_instance(settings: Settings) -> FastAPI:
    return FastAPI(
        debug=settings.WEB_APP_DEBUG,
        title=settings.WEB_APP_TITLE,
        description=settings.WEB_APP_DESCRIPTION,
        version=settings.WEB_APP_VERSION,
    )


def _register_applications(app: FastAPI) -> FastAPI:
    return app


def _register_middlewares(app: FastAPI) -> FastAPI:
    return app


def _register_routers(app: FastAPI) -> FastAPI:
    app.include_router(root.router)
    app.include_router(todo.router, prefix="/todo")
    return app


def init_app(settings: Settings) -> FastAPI:
    app: FastAPI = pipe(
        settings,
        _create_instance,
        _register_middlewares,
        _register_routers,
        _register_applications,
    )
    return app
