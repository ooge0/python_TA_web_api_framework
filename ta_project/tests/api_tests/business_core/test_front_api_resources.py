"""
Front-end API (restful-booker-platform, ``/api``) resource reads / contact form.
M7 gap-fill - the front-end API had only auth coverage before this.
"""
import faker
from hamcrest import assert_that, is_, is_not, none, has_key

from config.logger_config import get_logger
from core.api.frontend_api_points import FrontEndPoints


class TestFrontApiResources:
    """Rooms, branding and the public contact-message endpoint."""

    logger = get_logger()

    def test_front_api_room_list(self, frontend_api_client):
        """TC-FE-ROOM-001: GET /api/room returns the room list."""
        response = frontend_api_client.get(FrontEndPoints.ROOM)
        assert_that(response.status_code, is_(200))
        body = response.json()
        assert_that(body, has_key("rooms"))
        assert_that(len(body["rooms"]), is_not(0))
        first = body["rooms"][0]
        for field in ("roomid", "roomName", "type", "roomPrice"):
            assert_that(first, has_key(field))

    def test_front_api_branding(self, frontend_api_client):
        """TC-FE-BRAND-001: GET /api/branding returns branding data."""
        response = frontend_api_client.get(FrontEndPoints.BRANDING)
        assert_that(response.status_code, is_(200))
        body = response.json()
        for field in ("name", "map", "logoUrl", "contact"):
            assert_that(body, has_key(field))
        assert_that(body["name"], is_not(none()))

    def test_front_api_create_message(self, frontend_api_client, api_valid_headers):
        """TC-FE-MSG-001: POST /api/message (contact form) is accepted."""
        fake = faker.Faker()
        payload = {
            "name": fake.name(),
            "email": fake.email(),
            "phone": "0" + fake.numerify("##########"),
            "subject": "Automated check " + fake.word(),
            "description": fake.sentence(nb_words=12),
        }
        response = frontend_api_client.post(FrontEndPoints.MESSAGE, headers=api_valid_headers, json=payload)
        assert_that(response.status_code, is_(200))
        assert_that(response.json().get("success"), is_(True))
