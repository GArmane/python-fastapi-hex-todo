from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.routing import APIRouter
from pydantic import BaseModel

from todolist.core.accounts.entities.user import Credentials, UserRegistry
from todolist.core.accounts.services import user_service
from todolist.core.accounts.services.exceptions import EmailNotUniqueError
from todolist.infra.database.repositories import user_repository
from todolist.infra.database.sqlalchemy import database

# Router
router = APIRouter(default_response_class=JSONResponse)


# View Models
class EmailNotUniqueResponse(BaseModel):
    class Detail(BaseModel):
        msg: str
        email: str

    detail: Detail


# Handlers
@router.post(
    "",
    status_code=201,
    response_model=UserRegistry,
    responses={
        201: {"description": "User registered", "model": UserRegistry},
        409: {
            "description": "User already registered",
            "model": EmailNotUniqueResponse,
        },
    },
)
@database.transaction()
async def register_user(response: JSONResponse, credentials: Credentials):
    try:
        return await user_service.register(
            user_repository.fetch_by_email, user_repository.register, credentials,
        )
    except EmailNotUniqueError as err:
        raise HTTPException(409, detail=err.as_dict())
