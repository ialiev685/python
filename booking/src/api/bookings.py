from fastapi import APIRouter, status, HTTPException, Query
from typing import Annotated

from src.schemas.bookings import BookingAddRequestSchema
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddSchema
from src.schemas.bookings import BookingSchema
from datetime import date

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post('', summary='Создание брони')
async def create_order(data: BookingAddRequestSchema, user_id: UserIdDep, db: DBDep):
    room = await db.rooms.get_one_or_none(id=data.room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Номер отеля не найден')
    order = await db.bookings.add(data=BookingAddSchema(**data.model_dump(), user_id=user_id, price=room.price))
    await db.commit()
    return {"status": status.HTTP_200_OK, 'data': order}


@router.get('', summary='Получение броней')
async def get_bookings(db: DBDep, hotel_id: int,
                       date_from: date = Query(
                           description='Пример: 2024-09-13'),
                       date_to: date = Query(
                           description='Пример: 2024-09-21')):
    return await  db.bookings.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get('/me', summary='Получение броней пользователя', response_model=list[BookingSchema])
async def get_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)
