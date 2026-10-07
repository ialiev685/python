from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.utils import get_rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel

from src.schemas.rooms import RoomSchema, RoomSchemaWithConveniences


class RoomRepository(BaseRepository):
    model = RoomsModel
    schema = RoomSchema

    async def get_filtered_with_conveniences(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(RoomsModel.conveniences))
            .filter_by(**filter_by)
        )
        self.debug(request=query)
        result = await self.session.execute(query)
        room = result.scalars().one_or_none()
        if room is None:
            return None
        return RoomSchemaWithConveniences.model_validate(room, from_attributes=True)

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_for_booking = await get_rooms_ids_for_booking(date_from=date_from, date_to=date_to, hotel_id=hotel_id)

        query = select(self.model).options(selectinload(RoomsModel.conveniences)).filter(
            RoomsModel.id.in_(rooms_ids_for_booking))
        self.debug(request=query)
        result = await self.session.execute(query)
        return [RoomSchemaWithConveniences.model_validate(model, from_attributes=True) for model in
                result.scalars().all()]
