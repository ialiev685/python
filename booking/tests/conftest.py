import pytest
import json

from schemas.hotels import HotelAddSchema
from schemas.rooms import RoomAddRequestSchema, RoomAddSchema
from src.database import engine_null_pool, async_session_marker_null_pool
from src.database import Base
from src.models import *
from src.config import settings
from httpx import ASGITransport, AsyncClient
from src.main import app
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(async_session_marker_null_pool) as _db:
        yield _db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding='utf-8') as hotels_file:
        hotels_raw = json.load(hotels_file)
    with open("tests/mock_rooms.json", encoding='utf-8') as rooms_file:
        rooms_raw = json.load(rooms_file)
    hotels = [HotelAddSchema.model_validate(hotel) for hotel in hotels_raw]
    rooms = [RoomAddSchema.model_validate(room) for room in rooms_raw]
    async with DBManager(async_session_marker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def create_user(setup_database, ac):
    response = await ac.post("/auth/register", json={'email': 'test@test.ru', 'password': '123456'})
    assert response.status_code == 200
