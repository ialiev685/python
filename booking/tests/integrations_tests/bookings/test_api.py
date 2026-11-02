from src.schemas.bookings import BookingAddSchema
import pytest

from tests.conftest import get_db_with_null_pool


@pytest.mark.parametrize('room_id, date_from, date_to, status_code',
                         [
                             (1, "2024-11-01", "2024-11-11", 200),
                             (1, "2024-11-01", "2024-11-11", 200),
                             (1, "2024-11-01", "2024-11-11", 200),
                             (1, "2024-11-01", "2024-11-11", 200),
                             (1, "2024-11-01", "2024-11-11", 200),
                             (1, "2024-11-01", "2024-11-11", 404)
                         ])
async def test_add_bookings(authenticated_ac, db, room_id, date_from, date_to, status_code):
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    response_my_bookings = await authenticated_ac.post("/bookings/me")

    assert response.status_code == status_code
    if response.status_code == 200:
        data = response.json()["data"]
        assert data["room_id"] == room_id


@pytest.fixture(scope='module')
async def remove_all_bookings():
    async for _db in get_db_with_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize('room_id, date_from, date_to, status_code, my_bookings_count',
                         [
                             (1, "2024-11-01", "2024-11-11", 200, 1),
                             (1, "2024-11-01", "2024-11-11", 200, 2),
                             (1, "2024-11-01", "2024-11-11", 200, 3),
                             (1, "2024-11-01", "2024-11-11", 200, 4),
                             (1, "2024-11-01", "2024-11-11", 200, 5),

                         ])
async def test_add_and_get_bookings(
        authenticated_ac,
        db,
        room_id,
        date_from,
        date_to,
        status_code,
        my_bookings_count,
        remove_all_bookings
):
    response = await authenticated_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    response_my_bookings = await authenticated_ac.get("/bookings/me")
    assert len(response_my_bookings.json()) == my_bookings_count

    assert response.status_code == status_code
    data = response.json()["data"]
    assert data["room_id"] == room_id
