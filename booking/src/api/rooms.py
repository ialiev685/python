from fastapi import APIRouter, status, Body, HTTPException, Query

from src.database import async_session_marker
from src.repositories.rooms import RoomRepository
from src.repositories.hotels import HotelsRepository

from src.schemas.rooms import RoomAddSchema

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int, title: str | None = Query(None), description: str | None = Query(None)):
    async with async_session_marker() as session:
        rooms = await RoomRepository(session=session).get_all(hotel_id=hotel_id, title=title, description=description)
        return {'status': status.HTTP_200_OK, 'data': rooms}


@router.post('/add_room', summary='Добавить номер отеля')
async def add_room(room: RoomAddSchema = Body(
    openapi_examples={
        "1": {
            "summary": "Номер люкс",
            "value": {"title": "Номер люкс", "description": "Двухместный номер с видом на море. Бесплатный бар.",
                      "hotel_id": 1, "price": 100000},
        },
        "2": {
            "summary": "Номер стандарт",
            "value": {"title": "Номер стандарт", "description": "Одноместный номер. Платный бар.", "hotel_id": 1,
                      "price": 50000},
        },
    }
)):
    async with async_session_marker() as session:
        hotel = await HotelsRepository(session=session).get_one_or_none(id=room.hotel_id)
        if hotel is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Отель не найден')
        room = await RoomRepository(session=session).add(data=room)
        await session.commit()

    return {"status": status.HTTP_200_OK, 'data': room}
