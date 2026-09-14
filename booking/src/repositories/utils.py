from sqlalchemy import select, func
from datetime import date
from src.models.bookings import BookingsModel
from src.models.rooms import RoomsModel


async def get_rooms_ids_for_booking(date_from: date, date_to: date, hotel_id: int | None = None):
    """
    with rooms_count as (
        select room_id, count(*) as room_booked from bookings
        where date_from <='2026-09-21' and date_to >='2026-09-13'
        group by room_id
    ),
    available_rooms as (
        select rooms.id, quantity - coalesce(room_booked, 0) as available_room from rooms
        left join rooms_count on rooms.id = rooms_count.room_id
    )
    select * from available_rooms
    where available_room > 0;
    """
    rooms_count = (
        select(BookingsModel.room_id, func.count('*').label('room_booked'))
        .select_from(BookingsModel)
        .filter(BookingsModel.date_from <= date_to, BookingsModel.date_to >= date_from)
        .group_by(BookingsModel.room_id)
        .cte(name='rooms_count')
    )

    rooms_available_table = (
        select(RoomsModel.id.label('room_id'), (
                RoomsModel.quantity - func.coalesce(rooms_count.c.room_booked, 0)).label('room_available'))
        .select_from(RoomsModel)
        .outerjoin(rooms_count, RoomsModel.id == rooms_count.c.room_id)
        .cte(name='rooms_available_table')
    )

    rooms_ids_for_hotels = (
        select(RoomsModel.id)
        .select_from(RoomsModel)
    )

    if hotel_id is not None:
        rooms_ids_for_hotels = rooms_ids_for_hotels.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotels = rooms_ids_for_hotels.subquery('rooms_ids_for_hotels')

    query = (
        select(rooms_available_table.c.room_id)
        .filter(rooms_available_table.c.room_available > 0,
                rooms_available_table.c.room_id.in_(rooms_ids_for_hotels))
    )
    return query
