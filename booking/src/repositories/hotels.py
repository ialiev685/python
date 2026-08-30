from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from src.schemas.hotels import HotelSchema


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = HotelSchema

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
        self.debug(request=query)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
