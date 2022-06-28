import pytest

from src import app, auth


@pytest.fixture
def client():
    return app.test_client()


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert isinstance(resp.data, bytes)


def test_sqlalchemy_model_mock(mock_my_model):
    my_model = mock_my_model
    assert my_model.user_id == 1


def test_login(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert isinstance(resp.data, bytes)


def test_authorize_url():
    CLIENT_ID = 100
    expected_url = "https://www.strava.com/oauth/authorize?client_id=100&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fstrava_auth_successful&response_type=code&scope=activity%3Aread_all"  # noqa
    assert expected_url == auth.authorize_url(CLIENT_ID)
