from src.schemas.hotels import HotelAddSchema


async def test_add_hotel(db):
    hotel = HotelAddSchema(title='Hilton 5 start', location='Moscow')
    added_hotel = await db.hotels.add(data=hotel)
    await db.commit()
    assert added_hotel.title == hotel.title
