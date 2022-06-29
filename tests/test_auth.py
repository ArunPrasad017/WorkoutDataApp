from src.auth import refresh_access_token


def test_refresh_access_token():
    refresh_access_token(None, None, None)
    assert False
