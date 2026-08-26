from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel
from src.config import settings


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_hotel_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        self.debug(request=add_hotel_stmt)
        hotel = await self.session.execute(add_hotel_stmt)
        return hotel.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_hotel_stmt = (update(self.model)
                             .filter_by(**filter_by)
                             .values(**data.model_dump(exclude_unset=exclude_unset)))
        self.debug(request=update_hotel_stmt)
        await self.session.execute(update_hotel_stmt)

    async def delete(self, **filter_by) -> None:
        delete_hotel_stmt = delete(self.model).filter_by(**filter_by)
        self.debug(request=delete_hotel_stmt)
        await self.session.execute(delete_hotel_stmt)

    def debug(self, request):
        if settings.DEBUG:
            print(request.compile(compile_kwargs={"literal_binds": True}))
