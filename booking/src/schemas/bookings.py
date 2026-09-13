from pydantic import BaseModel
from datetime import date


class BookingAddRequestSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddSchema(BookingAddRequestSchema):
    user_id: int
    price: int


class BookingSchema(BookingAddSchema):
    id: int
