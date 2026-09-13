from fastapi import APIRouter, status, HTTPException

from src.schemas.bookings import BookingAddRequestSchema
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddSchema

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post('', summary='Создание брони')
async def create_order(data: BookingAddRequestSchema, user_id: UserIdDep, db: DBDep):
    room = await db.rooms.get_one_or_none(id=data.room_id)
    if not room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Номер отеля не найден')
    order = await db.bookings.add(data=BookingAddSchema(**data.model_dump(), user_id=user_id, price=room.price))
    return {"status": status.HTTP_200_OK, 'data': order}
