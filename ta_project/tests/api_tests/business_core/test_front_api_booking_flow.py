"""
Front-end API (restful-booker-platform, ``/api``) - the public reservation flow
and room administration. Uses the service objects from
:mod:`core.api.services`.
"""
import random
from datetime import date, timedelta

import allure
import faker
import pytest
from hamcrest import assert_that, is_, is_not, none, greater_than_or_equal_to
from requests import HTTPError

from config.logger_config import get_logger


def _reservation(room_id: int, checkin: str, checkout: str) -> dict:
    fake = faker.Faker()
    return {
        "bookingdates": {"checkin": checkin, "checkout": checkout},
        "roomid": room_id,
        "firstname": fake.first_name()[:18].ljust(3, "x"),
        "lastname": fake.last_name()[:30].ljust(3, "x"),
        "depositpaid": True,
        "email": fake.email(),
        "phone": "0" + fake.numerify("##########"),
    }


def _far_future_window(nights: int = 2):
    """A random 2-night window years out, so parallel tests do not collide."""
    start = date(2029, 1, 1) + timedelta(days=random.randint(0, 3000))
    return start.isoformat(), (start + timedelta(days=nights)).isoformat()


@allure.epic("Front-end API")
@allure.feature("Bookings")
class TestFrontApiReservation:
    """``POST /api/booking`` - the public 'Book now' flow."""

    logger = get_logger()

    @pytest.fixture
    def created_reservation(self, front_booking_api, front_token):
        """Reserve room 2 for a random far-future window; delete it on teardown."""
        checkin, checkout = _far_future_window()
        payload = _reservation(2, checkin, checkout)
        resp = front_booking_api.reserve(payload)
        assert_that(resp.status_code, is_(201), "precondition: reservation failed")
        booking_id = resp.json()["bookingid"]
        yield booking_id, payload
        try:
            front_booking_api.delete(booking_id, front_token)
        except Exception:  # noqa: BLE001 - best-effort cleanup
            pass

    @pytest.mark.req("REQ-FE-BOOKING-02")
    def test_public_reservation_is_created(self, created_reservation):
        """TC-FE-BOOK-001: a valid reservation returns 201 with a bookingid."""
        booking_id, _ = created_reservation
        assert_that(booking_id, is_not(none()))
        assert_that(isinstance(booking_id, int), is_(True))

    @pytest.mark.req("REQ-FE-BOOKING-03")
    def test_overlapping_reservation_is_rejected(self, front_booking_api, created_reservation):
        """TC-FE-BOOK-002: a reservation overlapping an existing one -> 409."""
        _, existing = created_reservation
        dates = existing["bookingdates"]
        overlap_start = date.fromisoformat(dates["checkin"]) + timedelta(days=1)
        overlap = _reservation(2, overlap_start.isoformat(),
                               (overlap_start + timedelta(days=2)).isoformat())
        with pytest.raises(HTTPError) as exc:
            front_booking_api.reserve(overlap)
        assert_that(exc.value.response.status_code, is_(409))

    @pytest.mark.req("REQ-FE-BOOKING-01")
    def test_bookings_for_room(self, front_booking_api, front_token, created_reservation):
        """TC-FE-BOOK-003: GET /api/booking?roomid= (token) returns room bookings."""
        booking_id, _ = created_reservation
        bookings = front_booking_api.for_room(2, front_token).json().get("bookings", [])
        assert_that(any(b.get("bookingid") == booking_id for b in bookings), is_(True))


@allure.epic("Front-end API")
class TestFrontApiRoomAdmin:
    """``POST`` / ``DELETE /api/room`` and the room report - need a token."""

    logger = get_logger()

    @allure.feature("Rooms")
    @pytest.mark.req("REQ-FE-ROOM-03", "REQ-FE-ROOM-04")
    def test_create_and_delete_room(self, front_room_api, front_token):
        """TC-FE-ROOM-003 / 004: create a room, see it in the list, delete it."""
        fake = faker.Faker()
        name = f"9{fake.numerify('##')}"
        room = {
            "roomName": name,
            "type": "Single",
            "accessible": True,
            "description": "created by an automated test",
            "image": "/images/room2.jpg",
            "roomPrice": 111,
            "features": ["WiFi"],
        }
        assert_that(front_room_api.create(room, front_token).json().get("success"), is_(True))

        created = [r for r in front_room_api.list() if r.roomName == name]
        assert_that(len(created), greater_than_or_equal_to(1), "new room not found in the list")

        resp = front_room_api.delete(created[0].roomid, front_token)
        assert_that(resp.status_code, is_(202))
        assert_that([r for r in front_room_api.list() if r.roomName == name], is_([]))

    @allure.feature("Report")
    @pytest.mark.req("REQ-FE-REPORT-01")
    def test_report_is_reachable(self, front_report_api, front_token):
        """TC-FE-REPORT-001: GET /api/report (token) -> 200."""
        assert_that(front_report_api.get(front_token).status_code, is_(200))
