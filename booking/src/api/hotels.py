from fastapi import Query, HTTPException, APIRouter, Body
from sqlalchemy import insert, select, func

# import asyncio
# import time
from src.api.dependencies import PaginationParamsDep
from src.schemas.hotels import Hotel, HotelPUT
from src.database import async_session_marker, engine
from src.models.hotels import HotelsModel

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


@router.get("/hotels", summary="Получить все отели")
async def get_hotels(
    pagination: PaginationParamsDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Локация отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_marker() as session:
        query = select(HotelsModel)
        if title:
            query = query.where(HotelsModel.title.icontains(title))
        if location:
            query = query.where(HotelsModel.location.icontains(location))

        query = query.limit(per_page).offset((pagination.page - 1) * per_page)
        result = await session.execute(query)
        hotels = result.scalars().all()

        return hotels


@router.post("/add_hotel", summary="Добавить отель")
async def create_hotel(
    hotel: Hotel = Body(
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
        add_hotel_stmt = insert(HotelsModel).values(**hotel.model_dump())
        print(
            add_hotel_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True})
        )
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": 200}


@router.patch("/hotels/{hotel_id}", summary="Частичное обновление")
def update_hotel_patch(hotel_id: int, data: HotelPUT):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if not hotel:
        raise HTTPException(
            status_code=404, detail="Данные с задачанными параметрами не найдены"
        )
    if data.title:
        hotel["title"] = data.title
    if data.name:
        hotel["name"] = data.name

    return hotel


@router.put("/hotels/{hotel_id}", summary="Полное обновление")
def update_hotel_put(hotel_id: int, data: Hotel):
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if not hotel:
        raise HTTPException(
            status_code=404, detail="Данные с задачанными параметрами не найдены"
        )
    hotel["title"] = data.title
    hotel["name"] = data.name

    return hotel
