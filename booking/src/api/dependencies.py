from pydantic import BaseModel
from fastapi import Query, Depends
from typing import Annotated


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Текущая страница")]
    per_page: Annotated[
        int | None, Query(3, ge=1, lt=30, description="Количество отелей на странице")
    ]


PaginationParamsDep = Annotated[PaginationParams, Depends()]
