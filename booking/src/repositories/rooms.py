from datetime import date

from sqlalchemy import select

from src.repositories.utils import get_rooms_ids_for_booking
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import RoomSchema


class RoomRepository(BaseRepository):
    model = RoomsModel
    schema = RoomSchema

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_for_booking = await get_rooms_ids_for_booking(date_from=date_from, date_to=date_to, hotel_id=hotel_id)
        return await self.get_filtered(RoomsModel.id.in_(rooms_ids_for_booking))
