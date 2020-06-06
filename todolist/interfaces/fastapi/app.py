from fastapi.applications import FastAPI
from toolz import pipe

from todolist.config.environment import Settings
from todolist.infra.database.sqlalchemy import connect_database as connect_pgsql_db
from todolist.infra.database.sqlalchemy import (
    disconnect_database as disconnect_pgsql_db,
)
from todolist.infra.database.sqlalchemy import init_database as init_pgsql_db
from todolist.interfaces.fastapi import account, root, todo


def _create_instance(settings: Settings) -> FastAPI:
    return FastAPI(
        debug=settings.WEB_APP_DEBUG,
        title=settings.WEB_APP_TITLE,
        description=settings.WEB_APP_DESCRIPTION,
        version=settings.WEB_APP_VERSION,
    )


def _init_databases(app: FastAPI) -> FastAPI:
    init_pgsql_db()
    return app


def _register_applications(app: FastAPI) -> FastAPI:
    return app


def _register_events(app: FastAPI) -> FastAPI:
    app.on_event("startup")(connect_pgsql_db)
    app.on_event("shutdown")(disconnect_pgsql_db)

    return app


def _register_middlewares(app: FastAPI) -> FastAPI:
    return app


def _register_routers(app: FastAPI) -> FastAPI:
    app.include_router(root.router)
    app.include_router(account.router, prefix="/account")
    app.include_router(todo.router, prefix="/todo")
    return app


def init_app(settings: Settings) -> FastAPI:
    app: FastAPI = pipe(
        settings,
        _create_instance,
        _init_databases,
        _register_events,
        _register_middlewares,
        _register_routers,
        _register_applications,
    )
    return app
