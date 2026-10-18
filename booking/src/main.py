from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.api.users import router as users_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.conveniences import router as conveniences_router
from src.init import redis_manager
from src.api.images import router as images_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.client), prefix="fastapi-cache")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router=users_router)
app.include_router(router=hotels_router)
app.include_router(router=rooms_router)
app.include_router(router=bookings_router)
app.include_router(router=conveniences_router)
app.include_router(router=images_router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
