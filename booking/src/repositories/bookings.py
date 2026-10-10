from src.repositories.base import BaseRepository
from src.models.bookings import BookingsModel
from src.repositories.mapper.mappers import BookingDataMapper


class BookingRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingDataMapper
