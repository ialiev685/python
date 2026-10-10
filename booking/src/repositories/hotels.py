from datetime import date

from sqlalchemy import select

from src.repositories.mapper.mappers import HotelsDataMapper
from src.repositories.utils import get_rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from src.schemas.hotels import HotelSchema
from src.models.rooms import RoomsModel


class HotelsRepository(BaseRepository):
    model = HotelsModel
    mapper = HotelsDataMapper

    async def get_filtered_by_time(self, date_from: date, date_to: date, offset: int, limit: int, title: str | None,
                                   location: str | None):
        rooms_ids_for_booking = await get_rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids = select(RoomsModel.hotel_id).filter(RoomsModel.id.in_(rooms_ids_for_booking))
        query = select(HotelsModel).filter(HotelsModel.id.in_(hotels_ids))

        if title:
            query = query.filter(HotelsModel.title.icontains(title))
        if location:
            query = query.filter(HotelsModel.location.icontains(location))

        query = query.limit(limit).offset(offset)
        self.debug(request=query)
        result = await self.session.execute(query)

        return [self.mapper.from_orm(model) for model in result.scalars().all()]
