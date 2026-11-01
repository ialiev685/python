from src.schemas.bookings import BookingAddSchema

BOOKING_PAYLOAD = {
    "date_from": "2024-11-01",
    "date_to": "2024-11-11",
}


async def test_add_booking_success(authenticated_ac, db):
    room = (await  db.rooms.get_all())[0]
    for _ in range(room.quantity):
        response = await authenticated_ac.post(
            "/bookings",
            json={"room_id": room.id, **BOOKING_PAYLOAD},
        )
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["room_id"] == room.id

# async def test_add_booking_over_quantity_fails(authenticated_ac, db):
#     room = (await db.rooms.get_all())[0]
#
#     for _ in range(room.quantity):
#         response = await authenticated_ac.post(
#             "/bookings",
#             json={"room_id": room.id, **BOOKING_PAYLOAD},
#         )
#         assert response.status_code == 200, response.text
#
#     # Ещё одна бронь сверх лимита
#     response = await authenticated_ac.post(
#         "/bookings",
#         json={"room_id": room.id, **BOOKING_PAYLOAD},
#     )
#     assert response.status_code == 404
