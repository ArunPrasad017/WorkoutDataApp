from unittest.mock import MagicMock, patch

from src.auth import refresh_access_token


class MockPost(MagicMock):
    def json(self):
        return {"access_token": "FAKE_TOKEN"}


def test_refresh_access_token():
    with patch("requests.post", MockPost):
        access_token = refresh_access_token(None, None, None)
        assert access_token == "FAKE_TOKEN"
