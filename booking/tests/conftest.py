import pytest
from src.database import test_engine
from src.database import Base
from src.models import *


@pytest.fixture(scope="session", autouse=True)
async def async_main() -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
