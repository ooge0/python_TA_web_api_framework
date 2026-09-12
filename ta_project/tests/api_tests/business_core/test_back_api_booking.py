"""
Back-end ``/booking`` CRUD on restful-booker.

Reads need no auth; ``PUT`` / ``PATCH`` / ``DELETE`` need a token. Every write
test creates and cleans up its own booking (via ``created_backend_booking``),
so nothing depends on ids another run left behind.
"""
import allure
import pytest
from assertpy2 import assert_that
from requests import HTTPError

from config.logger_config import get_logger


@allure.epic("Back-end API")
@allure.feature("Bookings")
class TestBackApiBooking:
    """Happy-path CRUD over ``/booking``."""

    logger = get_logger()

    # ---- reads ----

    @pytest.mark.tc("TC-BE-BOOK-001")
    @pytest.mark.req("REQ-BE-BOOKING-01")
    def test_booking_id_list_has_no_null_ids(self, back_booking_api):
        """TC-BE-BOOK-001: GET /booking returns ids, none null."""
        ids = back_booking_api.list_ids().get_booking_ids()
        assert_that(ids).is_not_empty()
        assert_that(all(i is not None for i in ids)).is_true()

    @pytest.mark.tc("TC-BE-BOOK-002")
    @pytest.mark.req("REQ-BE-BOOKING-01")
    def test_booking_ids_are_positive(self, back_booking_api):
        """TC-BE-BOOK-002."""
        ids = back_booking_api.list_ids().get_booking_ids()
        assert_that(all(i > 0 for i in ids)).is_true()

    @pytest.mark.tc("TC-BE-BOOK-019")
    @pytest.mark.req("REQ-BE-BOOKING-03")
    def test_get_booking_by_id(self, back_booking_api, created_backend_booking):
        """TC-BE-BOOK-008 area: GET /booking/{id} returns the object."""
        booking_id, _, payload = created_backend_booking
        assert_that(back_booking_api.get(booking_id).json().get("firstname")).is_equal_to(payload.firstname)

    @pytest.mark.tc("TC-BE-BOOK-018")
    @pytest.mark.req("REQ-BE-BOOKING-02")
    def test_name_filter_returns_the_matching_booking(self, back_booking_api, created_backend_booking):
        """TC-BE-BOOK-018 (REQ-BE-BOOKING-02): GET /booking?firstname=&lastname= filters the list."""
        booking_id, _, payload = created_backend_booking
        ids = back_booking_api.find(firstname=payload.firstname, lastname=payload.lastname).get_booking_ids()
        assert_that(ids).contains(booking_id)

    # ---- create ----

    @pytest.mark.tc("TC-BE-BOOK-003", "TC-BE-BOOK-004")
    @pytest.mark.req("REQ-BE-BOOKING-05")
    def test_create_booking_returns_ok(self, back_booking_api, backend_api_post_test_payload):
        """TC-BE-BOOK-003 / 004."""
        payload, _ = backend_api_post_test_payload
        assert_that(back_booking_api.create(payload).status_code).is_equal_to(200)

    @pytest.mark.tc("TC-BE-BOOK-005")
    @pytest.mark.req("REQ-BE-BOOKING-05")
    def test_create_booking_returns_a_booking_id(self, back_booking_api, backend_api_post_test_payload):
        """TC-BE-BOOK-005."""
        payload, _ = backend_api_post_test_payload
        assert_that(back_booking_api.create(payload).json().get("bookingid")).is_not_none()

    @pytest.mark.tc("TC-BE-BOOK-006")
    @pytest.mark.req("REQ-BE-BOOKING-05")
    def test_create_booking_needs_no_token(self, back_booking_api, backend_api_post_test_payload):
        """TC-BE-BOOK-006: POST works with no auth - documented behaviour."""
        payload, _ = backend_api_post_test_payload
        assert_that(back_booking_api.create(payload).status_code).is_equal_to(200)

    # ---- update ----

    @pytest.mark.tc("TC-BE-BOOK-009")
    @pytest.mark.req("REQ-BE-BOOKING-07")
    def test_put_replaces_the_booking(self, back_booking_api, created_backend_booking, get_back_end_token):
        """TC-BE-BOOK-007 / 009: PUT /booking/{id} with a token."""
        booking_id, _, payload = created_backend_booking
        payload.lastname = "_UpdatedUser"
        resp = back_booking_api.update(booking_id, payload, get_back_end_token)
        assert_that(resp.status_code).is_equal_to(200)
        assert_that(resp.json().get("lastname")).is_equal_to("_UpdatedUser")

    @pytest.mark.tc("TC-BE-BOOK-010")
    @pytest.mark.req("REQ-BE-BOOKING-09")
    def test_patch_updates_the_booking(self, back_booking_api, created_backend_booking, get_back_end_token):
        """TC-BE-BOOK-010: PATCH /booking/{id} with a token."""
        booking_id, _, _ = created_backend_booking
        resp = back_booking_api.patch(booking_id, {"lastname": "_PatchedUser"}, get_back_end_token)
        assert_that(resp.status_code).is_equal_to(200)
        assert_that(resp.json().get("lastname")).is_equal_to("_PatchedUser")

    # ---- delete ----

    @pytest.mark.tc("TC-BE-BOOK-011")
    @pytest.mark.req("REQ-BE-BOOKING-11")
    def test_delete_then_get_is_404(self, back_booking_api, backend_api_post_test_payload, get_back_end_token):
        """TC-BE-BOOK-011: create, delete with a token (201), then GET -> 404."""
        payload, _ = backend_api_post_test_payload
        booking_id = back_booking_api.create_and_get_id(payload)
        assert_that(back_booking_api.delete(booking_id, get_back_end_token).status_code).is_equal_to(201)
        with pytest.raises(HTTPError) as exc:
            back_booking_api.get(booking_id)
        assert_that(exc.value.response.status_code).is_equal_to(404)


@allure.epic("Back-end API")
@allure.feature("Bookings")
@allure.story("Negative")
class TestBackApiBookingNegative:
    """Negative cases - ``APIClient`` turns a 4xx/5xx into ``requests.HTTPError``."""

    logger = get_logger()

    @pytest.mark.tc("TC-BE-BOOK-012")
    @pytest.mark.req("REQ-BE-BOOKING-08")
    def test_put_without_token_forbidden(self, back_booking_api, created_backend_booking):
        """TC-BE-BOOK-012: PUT /booking/{id} without a token -> 403."""
        booking_id, _, payload = created_backend_booking
        with pytest.raises(HTTPError) as exc:
            back_booking_api.client.put(f"/booking/{booking_id}",
                                        headers={"Content-Type": "application/json"}, json=payload.to_dict())
        assert_that(exc.value.response.status_code).is_equal_to(403)

    @pytest.mark.tc("TC-BE-BOOK-013")
    @pytest.mark.req("REQ-BE-BOOKING-10")
    def test_patch_without_token_forbidden(self, back_booking_api, created_backend_booking):
        """TC-BE-BOOK-013."""
        booking_id, _, _ = created_backend_booking
        with pytest.raises(HTTPError) as exc:
            back_booking_api.client.patch(f"/booking/{booking_id}",
                                          headers={"Content-Type": "application/json"}, json={"firstname": "NoToken"})
        assert_that(exc.value.response.status_code).is_equal_to(403)

    @pytest.mark.tc("TC-BE-BOOK-014")
    @pytest.mark.req("REQ-BE-BOOKING-12")
    def test_delete_without_token_forbidden(self, back_booking_api, created_backend_booking):
        """TC-BE-BOOK-014."""
        booking_id, _, _ = created_backend_booking
        with pytest.raises(HTTPError) as exc:
            back_booking_api.delete(booking_id)
        assert_that(exc.value.response.status_code).is_equal_to(403)

    @pytest.mark.tc("TC-BE-BOOK-015")
    @pytest.mark.req("REQ-BE-BOOKING-04")
    def test_get_missing_id_is_404(self, back_booking_api):
        """TC-BE-BOOK-015."""
        with pytest.raises(HTTPError) as exc:
            back_booking_api.get(99999999)
        assert_that(exc.value.response.status_code).is_equal_to(404)

    @pytest.mark.tc("TC-BE-BOOK-016")
    @pytest.mark.req("REQ-BE-BOOKING-13")
    def test_create_with_empty_body_is_rejected(self, back_booking_api):
        """TC-BE-BOOK-016: POST /booking with an empty body -> 500."""
        with pytest.raises(HTTPError) as exc:
            back_booking_api.client.post("/booking", headers={"Content-Type": "application/json"}, json={})
        assert_that(exc.value.response.status_code).is_equal_to(500)

    @pytest.mark.tc("TC-BE-BOOK-017")
    @pytest.mark.req("REQ-BE-BOOKING-13")
    def test_create_without_dates_is_rejected(self, back_booking_api):
        """TC-BE-BOOK-017: POST /booking with no ``bookingdates`` -> 500."""
        body = {"firstname": "Jim", "lastname": "NoDates", "totalprice": 10, "depositpaid": True}
        with pytest.raises(HTTPError) as exc:
            back_booking_api.client.post("/booking", headers={"Content-Type": "application/json"}, json=body)
        assert_that(exc.value.response.status_code).is_equal_to(500)

