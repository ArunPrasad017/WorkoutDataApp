from unittest.mock import MagicMock, patch

from src.auth import refresh_access_token, authorize_url


class MockPost(MagicMock):
    def json(self):
        return {"access_token": "FAKE_TOKEN"}


def test_refresh_access_token():
    with patch("requests.post", MockPost):
        access_token = refresh_access_token(None, None, None)
        assert access_token == "FAKE_TOKEN"


def test_authorize_url():
    CLIENT_ID = 100
    expected_url = "https://www.strava.com/oauth/authorize?client_id=100&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fstrava_auth_successful&response_type=code&scope=activity%3Aread_all"  # noqa
    assert expected_url == authorize_url(CLIENT_ID)
