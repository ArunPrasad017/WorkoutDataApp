import pytest
from src import app


@pytest.fixture
def client():
    return app.test_client()


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert isinstance(resp.data, bytes)
