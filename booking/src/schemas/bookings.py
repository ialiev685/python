from pydantic import BaseModel
from datetime import date, datetime


class BookingAddRequestSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddSchema(BookingAddRequestSchema):
    user_id: int
    price: int


class BookingSchema(BookingAddSchema):
    id: int
    created_at: datetime


class BookingPatchSchema(BaseModel):
    user_id: int | None = None
    room_id: int | None = None
    price: int | None = None
    date_from: date | None = None
    date_to: date | None = None
