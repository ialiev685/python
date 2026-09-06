from fastapi import Query, APIRouter, Body, status

# import asyncio
# import time
from src.api.dependencies import PaginationParamsDep
from src.schemas.hotels import HotelAddSchema, HotelPatchSchema
from src.database import async_session_marker
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


# @router.get("/async/{id}")
# async def async_func(id: int):
#     print(f"Запущена асинхронная функция: {id}")
#     await asyncio.sleep(2)
#     print(f"Зафершена асинхронная функция: {id}")


# @router.get("/sync/{id}")
# def sync_func(id: int):
#     print(f"Запущена синхронная функция: {id}")
#     time.sleep(2)
#     print(f"Завершена синхронная функция: {id}")


@router.get("", summary="Получить все отели")
async def get_hotels(
        pagination: PaginationParamsDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Локация отеля"),
):
    per_page = pagination.per_page or 10
    async with async_session_marker() as session:
        return await HotelsRepository(session=session).get_all(
            title=title,
            location=location,
            offset=(pagination.page - 1) * per_page,
            limit=per_page,
        )


@router.get('/{hotel_id}', summary='Получить отель')
async def get_hotel(hotel_id: int):
    async with async_session_marker() as session:
        hotel = await  HotelsRepository(session).get_by_id(id=hotel_id)
        return {"status": status.HTTP_200_OK, 'data': hotel}


@router.post("", summary="Добавить отель")
async def create_hotel(
        hotel: HotelAddSchema = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {"title": "Сочи парк 5*", "location": "ул. Моря 1"},
                },
                "2": {
                    "summary": "Дубаи",
                    "value": {"title": "Дубай Марина", "location": "ул. Шейха 1"},
                },
            }
        )
):
    async with async_session_marker() as session:
        hotel = await HotelsRepository(session=session).add(data=hotel)
        await session.commit()

    return {"status": status.HTTP_200_OK, 'data': hotel}


@router.patch("/{hotel_id}", summary="Частичное обновление")
async def update_hotel_patch(hotel_id: int, data: HotelPatchSchema):
    async with async_session_marker() as session:
        await HotelsRepository(session=session).edit(data=data, exclude_unset=True, id=hotel_id)
        await  session.commit()
        return {"status": status.HTTP_200_OK}


@router.put("/{hotel_id}", summary="Полное обновление")
async def update_hotel_put(hotel_id: int, data: HotelAddSchema):
    async with async_session_marker() as session:
        await HotelsRepository(session=session).edit(data=data, id=hotel_id)
        await  session.commit()
        return {"status": status.HTTP_200_OK}


@router.delete("/{hotel_id}", summary='Удалить отели')
async def delete_hotel(hotel_id: int):
    async with async_session_marker() as session:
        await HotelsRepository(session=session).delete(id=hotel_id)
        await session.commit()
        return {"status": status.HTTP_200_OK}
