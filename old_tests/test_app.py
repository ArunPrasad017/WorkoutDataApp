import pytest

from src_old import app, strava_api


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def rest_client():
    obj = strava_api.StravaApi
    obj.session = {"athlete_id": 1}
    return app.test_client(obj)


@pytest.fixture
def rest_client_with_id():
    obj = strava_api.StravaApi
    obj.session = {"athlete_id": 1, "refresh_token": "Token"}
    return app.test_client(obj)


# https://itnext.io/setting-up-transactional-tests-with-pytest-and-sqlalchemy-b2d726347629
# @pytest.fixture(scope="session")
# def db_engine():
#     conn = create_engine("sqlite://localhost/test_database").connect()
#     return conn


# @pytest.fixture
# def db_session(setup_database):
#     connection = db_engine()
#     transaction = connection.begin()
#     yield scoped_session(
#         sessionmaker(autocommit=False, autoflush=False, bind=connection)
#     )
#     transaction.rollback()


# def seed_database():
#     users = [
#         {"user_id": 1, "user_name": "John Doe", "refresh_token": "Fake_Token"},
#     ]

#     for user in users:
#         db_user = app.User(**user)
#         db_session.add(db_user)
#     db_session.commit()


# @pytest.fixture(scope="session")
# def setup_database():
#     seed_database()


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert isinstance(resp.data, bytes)


def test_root(rest_client):
    resp = rest_client.get("/")
    assert resp.status_code == 200
    assert isinstance(resp.data, bytes)


def test_sqlalchemy_model_mock(mock_my_model):
    my_model = mock_my_model
    assert my_model.user_id == 1


def test_login(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert isinstance(resp.data, bytes)


def test_login_post(client):
    resp = client.post(
        "/login", data=dict(username="test@gmail.com", password="test", login_form="")
    )
    assert resp.status_code == 200
    admin_resp = client.post(
        "/login", data=dict(username="admin", password="admin", login_form="")
    )  # noqa
    assert admin_resp.status_code != 200  # simulate error


def test_strava_authorize_fail(client):
    resp = client.get("/strava_authorize")
    assert resp.status_code == 302


def test_strava_authorize_pass(rest_client_with_id):
    resp = rest_client_with_id.get("/strava_authorize")
    assert resp.status_code == 200
