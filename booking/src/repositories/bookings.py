from fastapi import status, HTTPException
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsModel
from src.repositories.mapper.mappers import BookingDataMapper
from src.repositories.utils import get_rooms_ids_for_booking
from src.schemas.bookings import BookingAddSchema


class BookingRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingDataMapper

    async def add_booking(self, data: BookingAddSchema, hotel_id: int) -> BookingAddSchema:
        rooms_ids_for_booking = await get_rooms_ids_for_booking(
            date_from=data.date_from, date_to=data.date_to,
            hotel_id=hotel_id
        )
        result = await self.session.execute(rooms_ids_for_booking)
        rooms_ids = result.scalars().all()
        if data.room_id in rooms_ids:
            return await self.add(data=data)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Номер отеля не доступен для бронирования в указанный период"
            )
