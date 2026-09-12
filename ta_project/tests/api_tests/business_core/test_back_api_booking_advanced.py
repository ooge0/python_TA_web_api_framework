"""
Advanced back-end booking tests (restful-booker) — complex logic, round-trips,
boundary conditions and filter precision.

Each test in the write classes manages its own booking lifecycle with
``created_backend_booking`` so they are safe under ``pytest -n``.  Date-boundary
tests that need custom dates perform inline create/delete rather than relying on
the shared ``init_booking_date`` fixture.

Calls go through the service objects in :mod:`core.api.services`.
"""
import allure
import pytest
from assertpy2 import assert_that

from config.logger_config import get_logger
from core.data.data_models.front_api_booking_object_data_model import ApiBookingObjectPayload, BookingDates


@allure.epic("Back-end API")
@allure.feature("Bookings")
@allure.story("Round-trip consistency")
class TestBackApiBookingConsistency:
    """POST → GET → PUT → PATCH round-trip checks."""

    logger = get_logger()

    @pytest.mark.tc("TC-BE-BOOK-020")
    @pytest.mark.req("REQ-BE-BOOKING-14", "REQ-BE-BOOKING-03", "REQ-BE-BOOKING-05")
    def test_post_then_get_returns_same_data(self, back_booking_api, created_backend_booking):
        """POST a booking; GET it back; every field must match the submitted payload."""
        booking_id, _, payload = created_backend_booking
        response = back_booking_api.get(booking_id)
        assert_that(response.status_code).is_equal_to(200)
        body = response.json()

        assert_that(body["firstname"]).is_equal_to(payload.firstname)
        assert_that(body["lastname"]).is_equal_to(payload.lastname)
        assert_that(body["totalprice"]).is_equal_to(payload.totalprice)
        assert_that(body["bookingdates"]["checkin"]).is_equal_to(payload.bookingdates.checkin)
        assert_that(body["bookingdates"]["checkout"]).is_equal_to(payload.bookingdates.checkout)

    @pytest.mark.tc("TC-BE-BOOK-021")
    @pytest.mark.req("REQ-BE-BOOKING-14", "REQ-BE-BOOKING-08")
    def test_put_replaces_all_fields(self, back_booking_api, created_backend_booking):
        """PUT /booking/{id} replaces the booking; subsequent GET reflects the new data."""
        booking_id, auth_headers, original = created_backend_booking
        token = auth_headers.get("Cookie", "").replace("token=", "")

        replacement = ApiBookingObjectPayload(
            firstname="Replaced",
            lastname="Entirely",
            totalprice=999,
            depositpaid="false",
            bookingdates=BookingDates(checkin="2030-01-01", checkout="2030-01-10"),
            additionalneeds="none",
        )
        put_resp = back_booking_api.update(booking_id, replacement, token)
        assert_that(put_resp.status_code).is_equal_to(200)

        get_resp = back_booking_api.get(booking_id)
        body = get_resp.json()
        assert_that(body["firstname"]).is_equal_to("Replaced")
        assert_that(body["lastname"]).is_equal_to("Entirely")
        assert_that(body["totalprice"]).is_equal_to(999)
        assert_that(body["bookingdates"]["checkin"]).is_equal_to("2030-01-01")

    @pytest.mark.tc("TC-BE-BOOK-022")
    @pytest.mark.req("REQ-BE-BOOKING-18", "REQ-BE-BOOKING-10")
    def test_patch_does_not_alter_untouched_fields(self, back_booking_api, created_backend_booking):
        """PATCH updates only the named fields; all other fields remain unchanged."""
        booking_id, auth_headers, payload = created_backend_booking
        token = auth_headers.get("Cookie", "").replace("token=", "")

        patch_resp = back_booking_api.patch(booking_id, {"firstname": "Patched"}, token)
        assert_that(patch_resp.status_code).is_equal_to(200)

        get_resp = back_booking_api.get(booking_id)
        body = get_resp.json()
        assert_that(body["firstname"]).is_equal_to("Patched")
        assert_that(body["lastname"]).is_equal_to(payload.lastname)
        assert_that(body["totalprice"]).is_equal_to(payload.totalprice)
        assert_that(body["depositpaid"]).is_equal_to(True)

    @pytest.mark.tc("TC-BE-BOOK-023")
    @pytest.mark.req("REQ-BE-BOOKING-18", "REQ-BE-BOOKING-10")
    def test_successive_patches_accumulate(self, back_booking_api, created_backend_booking):
        """Two successive PATCH calls each leave their change in place."""
        booking_id, auth_headers, _ = created_backend_booking
        token = auth_headers.get("Cookie", "").replace("token=", "")

        back_booking_api.patch(booking_id, {"firstname": "First"}, token)
        back_booking_api.patch(booking_id, {"totalprice": 777}, token)

        body = back_booking_api.get(booking_id).json()
        assert_that(body["firstname"]).is_equal_to("First")
        assert_that(body["totalprice"]).is_equal_to(777)

    @pytest.mark.tc("TC-BE-BOOK-024")
    @pytest.mark.req("REQ-BE-BOOKING-15", "REQ-BE-AUTH-01")
    def test_token_reuse_across_consecutive_writes(self, back_booking_api, created_backend_booking, get_back_end_token):
        """A single auth token remains valid across two consecutive write operations."""
        booking_id, auth_headers, payload = created_backend_booking
        token = get_back_end_token

        put_resp = back_booking_api.update(booking_id, payload, token)
        assert_that(put_resp.status_code).described_as("first write (PUT)").is_equal_to(200)

        patch_resp = back_booking_api.patch(booking_id, {"lastname": "Reused"}, token)
        assert_that(patch_resp.status_code).described_as("second write (PATCH)").is_equal_to(200)

        body = back_booking_api.get(booking_id).json()
        assert_that(body["lastname"]).is_equal_to("Reused")


@allure.epic("Back-end API")
@allure.feature("Bookings")
@allure.story("Date boundaries")
class TestBackApiBookingDateBoundaries:
    """SUT behaviour with extreme or invalid date combinations."""

    logger = get_logger()

    @pytest.mark.tc("TC-BE-BOOK-025")
    @pytest.mark.req("REQ-BE-BOOKING-16")
    def test_inverted_dates_accepted_by_sut(self, back_booking_api, get_back_end_token):
        """
        POST /booking with checkout < checkin is accepted by restful-booker (SUT quirk).

        The service does not validate date order; this test documents and asserts
        the current (permissive) behaviour.  See KI-04 / KI-05 for related quirks.
        """
        payload = ApiBookingObjectPayload(
            firstname="InvertedDate",
            lastname="_TestUser",
            totalprice=50,
            depositpaid="false",
            bookingdates=BookingDates(checkin="2030-12-31", checkout="2030-01-01"),
        )
        resp = back_booking_api.create(payload)
        assert_that(resp.status_code).is_equal_to(200)
        booking_id = resp.json()["bookingid"]

        # cleanup
        try:
            back_booking_api.delete(booking_id, get_back_end_token)
        except Exception:  # noqa: BLE001
            pass

    @pytest.mark.tc("TC-BE-BOOK-026")
    @pytest.mark.req("REQ-BE-BOOKING-16")
    def test_far_future_dates_accepted(self, back_booking_api, get_back_end_token):
        """POST /booking with year-9999 dates is accepted without error."""
        payload = ApiBookingObjectPayload(
            firstname="FarFuture",
            lastname="_TestUser",
            totalprice=1,
            depositpaid="true",
            bookingdates=BookingDates(checkin="9999-01-01", checkout="9999-12-31"),
        )
        resp = back_booking_api.create(payload)
        assert_that(resp.status_code).is_equal_to(200)
        booking_id = resp.json()["bookingid"]

        get_resp = back_booking_api.get(booking_id)
        assert_that(get_resp.status_code).is_equal_to(200)

        try:
            back_booking_api.delete(booking_id, get_back_end_token)
        except Exception:  # noqa: BLE001
            pass


@allure.epic("Back-end API")
@allure.feature("Bookings")
@allure.story("Filter precision")
class TestBackApiFilterPrecision:
    """GET /booking filter behaviour."""

    logger = get_logger()

    @pytest.mark.tc("TC-BE-BOOK-027")
    @pytest.mark.req("REQ-BE-BOOKING-17")
    def test_name_filter_returns_empty_for_nonexistent_name(self, back_booking_api):
        """GET /booking?firstname=<uuid> returns an empty list when no match exists."""
        import uuid
        unique_name = f"NoSuchUser_{uuid.uuid4().hex}"
        response = back_booking_api.find(firstname=unique_name)
        assert_that(response.status_code).is_equal_to(200)
        body = response.json()
        assert_that(body).is_instance_of(list)
        assert_that(len(body)).is_equal_to(0)
