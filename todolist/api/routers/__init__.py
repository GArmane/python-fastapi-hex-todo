from fastapi.applications import FastAPI

from todolist.api.routers import account, root, todo


def register_routers(app: FastAPI) -> FastAPI:
    app.include_router(root.router)
    app.include_router(account.router, prefix="/account")
    app.include_router(todo.router, prefix="/todo")
    return app
