from datetime import date

from src.schemas.bookings import BookingAddSchema, BookingPatchSchema


async def test_bookings_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_create = BookingAddSchema(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=10, day=29),
        date_to=date(year=2026, month=11, day=4),
        price=53000
    )

    # create
    booking_new = await db.bookings.add(data=booking_create)
    booking = await db.bookings.get_one_or_none(id=booking_new.id)
    assert booking.user_id == user_id
    assert booking.room_id == room_id
    assert booking.price == 53000

    booking_update = BookingPatchSchema(
        user_id=user_id,
        room_id=room_id,
        price=49000,
    )

    # update
    await db.bookings.edit(data=booking_update, id=booking.id, exclude_unset=True)
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert booking.price == 49000
    assert booking.date_from == date(year=2026, month=10, day=29)
    assert booking.date_to == date(year=2026, month=11, day=4)

    # delete
    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert booking is None
