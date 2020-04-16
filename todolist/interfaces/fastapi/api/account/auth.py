from datetime import datetime, timedelta
from enum import Enum
from operator import attrgetter
from typing import Any, Dict

import jwt
from fastapi import Depends, HTTPException  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from fastapi.routing import APIRouter
from fastapi.security import (  # type: ignore
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from pydantic import BaseModel

from todolist.config.environment import get_initial_settings
from todolist.core.accounts.entities.user import Credentials, UserRegistry
from todolist.core.accounts.services import user_service
from todolist.infra.database.repositories import user_repository

_secret_key, _expire_minutes, _algorithm = attrgetter(
    "JWT_SECRET_KEY", "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "JWT_ALGORITHM"
)(get_initial_settings())
_credentials_exception = HTTPException(
    status_code=401, detail="invalid token", headers={"WWW-Authenticate": "Bearer"},
)


# View models
class TokenType(str, Enum):
    bearer = "bearer"


class Token(BaseModel):
    access_token: str
    expire: int
    token_type: TokenType = TokenType.bearer


# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/oauth2/token")

# Router
router = APIRouter(default_response_class=JSONResponse)


# Token handlers
def _decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, _secret_key, algorithms=[_algorithm])
        _, id_ = str(payload.get("sub")).split(":")
        return int(id_)
    except jwt.PyJWTError:
        raise _credentials_exception


def _encode_token(*, data: Dict[str, Any], expires_delta: timedelta) -> Token:
    expire = datetime.utcnow() + expires_delta
    access_token = jwt.encode(
        {**data.copy(), "exp": expire}, _secret_key, algorithm=_algorithm
    )
    return Token(access_token=access_token, expire=expire.timestamp())


# Authorizers
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserRegistry:
    id_ = _decode_token(token)
    user = await user_service.get_by_id_or_raise(user_repository.fetch_by_id, id_)
    return user


# Handlers
@router.post(
    "/token",
    response_model=Token,
    responses={
        200: {"description": "User authenticated"},
        401: {"description": "User unauthorized"},
    },
)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    username, password = attrgetter("username", "password")(form_data)
    credentials = Credentials(email=username, password=password)

    user = await user_service.get_by_credentials(
        user_repository.fetch_by_email, credentials
    )
    if not user:
        raise HTTPException(
            status_code=401, detail="invalid authentication credentials",
        )

    expire = timedelta(minutes=_expire_minutes)
    return _encode_token(data={"sub": f"userid:{user.id}"}, expires_delta=expire)


@router.get(
    "/instrospect",
    response_model=UserRegistry,
    responses={
        200: {"description": "User registry"},
        401: {"description": "User unauthorized"},
    },
)
def instrospect(user: UserRegistry = Depends(get_current_user)):
    return user
