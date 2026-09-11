"""
Front-end API (restful-booker-platform, ``/api``) - rooms, branding, messages,
token validation. Uses the service objects from :mod:`core.api.services`.
"""
import allure
import faker
import pytest
from assertpy2 import assert_that, soft_assertions

from config.logger_config import get_logger


@allure.epic("Front-end API")
class TestFrontApiResources:
    """Rooms, branding, messages and token validation - one method per feature."""

    logger = get_logger()

    @allure.feature("Rooms")
    @pytest.mark.req("REQ-FE-ROOM-01")
    def test_front_api_room_list(self, front_room_api):
        """TC-FE-ROOM-001: GET /api/room returns the room list."""
        rooms = front_room_api.list()
        assert_that(rooms).is_not_empty()
        first = rooms[0]
        assert_that(first.roomid).is_not_none()
        assert_that(first.type).is_not_empty()

    @allure.feature("Rooms")
    @pytest.mark.req("REQ-FE-ROOM-02")
    def test_front_api_room_by_id(self, front_room_api):
        """TC-FE-ROOM-002: GET /api/room/{id} returns room details."""
        room = front_room_api.get(1)
        assert_that(room.roomid).is_equal_to(1)
        assert_that(room.features).is_not_none()

    @allure.feature("Branding")
    @pytest.mark.req("REQ-FE-BRANDING-01")
    def test_front_api_branding(self, front_branding_api):
        """TC-FE-BRAND-001: GET /api/branding returns the full branding block.

        Soft assertions: every missing field is reported, not just the first.
        """
        body = front_branding_api.get().json()
        with soft_assertions():
            for field in ("name", "map", "logoUrl", "contact"):
                assert_that(body).contains_key(field).described_as(
                    f"branding is missing '{field}'")
            assert_that(body.get("name")).is_not_empty().described_as("branding 'name' is empty")

    @allure.feature("Messages")
    @pytest.mark.req("REQ-FE-MESSAGE-01")
    def test_front_api_create_message(self, front_message_api):
        """TC-FE-MSG-001: POST /api/message (contact form) is accepted."""
        fake = faker.Faker()
        payload = {
            "name": fake.name(),
            "email": fake.email(),
            "phone": "0" + fake.numerify("##########"),
            "subject": "Automated check " + fake.word(),
            "description": fake.sentence(nb_words=12),
        }
        assert_that(front_message_api.send(payload).json().get("success")).is_true()

    @allure.feature("Messages")
    @pytest.mark.req("REQ-FE-MESSAGE-02")
    def test_front_api_message_inbox(self, front_message_api, front_token):
        """TC-FE-MSG-002: GET /api/message (token) lists messages, /count returns the unread badge."""
        messages = front_message_api.list(front_token).json().get("messages", [])
        count = front_message_api.count(front_token).json().get("count")
        assert_that(count).is_instance_of(int).is_greater_than_or_equal_to(0)
        if messages:
            with soft_assertions():
                for field in ("id", "name", "subject", "read"):
                    assert_that(messages[0]).contains_key(field).described_as(
                        f"message is missing '{field}'")

    @allure.feature("Authentication")
    @pytest.mark.req("REQ-FE-AUTH-03")
    def test_front_api_token_validation(self, front_auth_api, front_token):
        """TC-FE-AUTH-005: a valid token validates; a tampered one is rejected."""
        assert_that(front_auth_api.validate(front_token).json().get("valid")).is_true()
        try:
            front_auth_api.validate("not-a-real-token")
        except Exception as exc:  # APIClient raises HTTPError on 403
            assert_that(getattr(exc, "response", None)).is_not_none()
            assert_that(exc.response.status_code).is_equal_to(403)
        else:
            raise AssertionError("a bogus token should not validate")

    @allure.feature("Authentication")
    @pytest.mark.req("REQ-FE-AUTH-04")
    def test_front_api_logout(self, front_auth_api, front_api_valid_user_creds):
        """
        TC-FE-AUTH-006: POST /api/auth/logout with a token returns
        {"success": true}. (The SUT does not actually invalidate the token
        afterwards - a known platform quirk, not asserted here.)
        """
        token = front_auth_api.token_for(front_api_valid_user_creds)
        assert_that(front_auth_api.logout(token).json().get("success")).is_true()

