from src.database import async_session_marker
from src.schemas.hotels import HotelAddSchema
from src.utils.db_manager import DBManager


async def test_add_hotel():
    async with DBManager(async_session_marker) as db:
        hotel = HotelAddSchema(title='Hilton 5 start', location='Moscow')
        added_hotel = await db.hotels.add(data=hotel)
        await db.commit()
        assert added_hotel.title == hotel.title
