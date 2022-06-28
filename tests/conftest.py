import pytest
from src.app import User


@pytest.fixture
def mock_my_model():
    my_model = User(user_id=1, user_name="mock_name", refresh_token="mock_token")
    return my_model
