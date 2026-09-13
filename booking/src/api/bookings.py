from fastapi import APIRouter, status, HTTPException

from src.schemas.bookings import BookingAddRequestSchema
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddSchema
from src.schemas.bookings import BookingSchema

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post('', summary='Создание брони')
async def create_order(data: BookingAddRequestSchema, user_id: UserIdDep, db: DBDep):
    room = await db.rooms.get_one_or_none(id=data.room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Номер отеля не найден')
    order = await db.bookings.add(data=BookingAddSchema(**data.model_dump(), user_id=user_id, price=room.price))
    await db.commit()
    return {"status": status.HTTP_200_OK, 'data': order}


@router.get('', summary='Получение броней', response_model=list[BookingSchema])
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get('/me', summary='Получение броней пользователя', response_model=list[BookingSchema])
async def get_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)
