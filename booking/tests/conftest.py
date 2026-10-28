import pytest
import json
from src.database import engine_null_pool
from src.database import Base
from src.models import *
from src.config import settings
from httpx import ASGITransport, AsyncClient
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def create_tables(check_test_mode) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def create_hotels(create_tables) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        with open("tests/integrations_tests/hotels/mock_hotels.json", "r") as f:
            pass
            hotels_raw = f.read()
            hotels_parsed = json.loads(hotels_raw)
            for hotel in hotels_parsed:
                response = await ac.post("/hotels", json=hotel)

                assert response.status_code == 200
                data = response.json()['data']
                assert data['title'] == hotel["title"]

    # assert response.status_code == 200


@pytest.fixture(scope="session", autouse=True)
async def create_user(create_tables):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={'email': 'test@test.ru', 'password': '123456'})
        assert response.status_code == 200
