from src.repositories.base import BaseRepository
from src.models.bookings import BookingsModel
from src.schemas.bookings import BookingSchema


class BookingRepository(BaseRepository):
    model = BookingsModel
    schema = BookingSchema
