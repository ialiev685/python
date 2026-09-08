from pydantic import BaseModel
from fastapi import Query, Depends, Request, HTTPException
from typing import Annotated
from src.database import async_session_marker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Текущая страница")]
    per_page: Annotated[
        int | None,
        Query(None, ge=1, lt=30, description="Количество отелей на странице"),
    ]


PaginationParamsDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get('access_token', None)
    if not access_token:
        raise HTTPException(status_code=401, detail='Пользователь не авторизирован')
    return access_token


def get_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data['user_id']


UserIdDep = Annotated[int, Depends(get_user_id)]


async def get_db():
    async with DBManager(async_session_marker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
