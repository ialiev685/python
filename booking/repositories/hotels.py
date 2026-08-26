from sqlalchemy import select
from repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from src.config import settings


class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all(
            self,
            title,
            location,
            offset,
            limit,
    ):
        query = select(HotelsModel)
        if title:
            query = query.where(HotelsModel.title.icontains(title))
        if location:
            query = query.where(HotelsModel.location.icontains(location))

        query = query.limit(limit).offset(offset)
        self.debug(query=query)
        result = await self.session.execute(query)
        return result.scalars().all()
