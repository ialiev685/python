from fastapi import Query, HTTPException, APIRouter, Body
from sqlalchemy import Insert

# import asyncio
# import time
from src.api.dependencies import PaginationParamsDep
from src.schemas.hotels import Hotel, HotelPUT
from src.database import async_session_marker
from src.models.hotels import HotelsModel

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels: list[dict] = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


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
def get_hotels(
    pagination: PaginationParamsDep,
    id: int = Query(None, description="id отеля"),
    title: str = Query(None, description="Название отеля"),
):

    def normalize(text: str) -> str:
        return text.lower().strip() if isinstance(text, str) else ""

    filtered = []
    for hotel in hotels:
        if id is not None and hotel["id"] != id:
            continue

        if title is not None:
            hotel_title = normalize(hotel["title"])
            search_title = normalize(title)
            if hotel_title != search_title:
                continue

        filtered.append(hotel)
    if pagination.page and pagination.per_page:
        start_index = (pagination.page - 1) * pagination.per_page
        return filtered[start_index:][: pagination.per_page]

    return filtered


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
        add_hotel_stmt = Insert(HotelsModel).values(**hotel.model_dump())
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
