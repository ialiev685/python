from fastapi import APIRouter, status, Body, HTTPException

from src.database import async_session_marker
from src.repositories.rooms import RoomRepository
from src.repositories.hotels import HotelsRepository

from src.schemas.rooms import RoomAddSchema, RoomPatchSchema, RoomAddRequestSchema, RoomPatchRequestSchema
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int, db: DBDep, ):
    rooms = await db.rooms.get_filtered(hotel_id=hotel_id)
    return {'status': status.HTTP_200_OK, 'data': rooms}


@router.post('/{hotel_id}/rooms', summary='Добавить номер отеля')
async def add_room(hotel_id: int, db: DBDep, data: RoomAddRequestSchema = Body(
    openapi_examples={
        "1": {
            "summary": "Номер люкс",
            "value": {"title": "Номер люкс", "description": "Двухместный номер с видом на море. Бесплатный бар.",
                      "price": 100000, "quantity": 1},
        },
        "2": {
            "summary": "Номер стандарт",
            "value": {"title": "Номер стандарт", "description": "Одноместный номер. Платный бар.", "price": 50000,
                      "quantity": 1},
        },
    }
)):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Отель не найден')
    _room = RoomAddSchema(**data.model_dump(), hotel_id=hotel_id)
    room = await db.rooms.add(data=_room)
    await db.commit()

    return {"status": status.HTTP_200_OK, 'data': room}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление")
async def update_room_patch(hotel_id: int, room_id: int, data: RoomPatchRequestSchema, db: DBDep, ):
    _room = RoomPatchSchema(**data.model_dump(exclude_unset=True), hotel_id=hotel_id)
    await db.rooms.edit(data=_room, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await  db.commit()
    return {"status": status.HTTP_200_OK}


@router.put("/{hotel_id}/rooms/{room_id}/", summary="Полное обновление")
async def update_room_put(hotel_id: int, room_id: int, data: RoomAddRequestSchema, db: DBDep, ):
    _room = RoomAddSchema(**data.model_dump(), hotel_id=hotel_id)
    await db.rooms.edit(data=data, id=room_id, hotel_id=hotel_id)
    await  db.commit()
    return {"status": status.HTTP_200_OK}


@router.delete("/{hotel_id}/rooms/{room_id}", summary='Удалить отели')
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep, ):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": status.HTTP_200_OK}
