import pytest
from rest_framework.test import APIClient
from core.models import User

@pytest.fixture
def client():
    return APIClient()

TEST_USER_USERNAME = 'testuser'
TEST_USER_PASSWORD = 'rJX3NdpmQqn5D'

@pytest.fixture
@pytest.mark.django_db
def sample_user() -> User:
    user = User(username=TEST_USER_USERNAME)
    user.set_password(TEST_USER_PASSWORD)
    user.save()
    return user


@pytest.mark.django_db
def test_token_endpoint_invalid_get_request(client: APIClient):
    endpoint = '/auth/token/'
    response = client.get(endpoint)
    assert response.status_code == 405

@pytest.mark.django_db
def test_token_endpoint_missing_params(client: APIClient):
    endpoint = '/auth/token/'
    response = client.post(endpoint)
    assert response.status_code == 400

@pytest.mark.django_db
def test_obtain_token(client: APIClient, sample_user:User):
    endpoint = '/auth/token/'
    payload = {
        "username" : TEST_USER_USERNAME,
        "password" : TEST_USER_PASSWORD
    }
    response = client.post(endpoint, format="json", data=payload)
    print(response.data)
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_obtain_token_invalid_credentials(client: APIClient):
    endpoint = '/auth/token/'
    payload = {
        "username" : "notexists",
        "password" : "asdasd123"
    }
    response = client.post(endpoint, format="json", data=payload)
    print(response.data)
    assert response.status_code == 401
    error_details =  response.data.get("detail")
    assert error_details.code == "no_active_account"





"""
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "rJX3NdpmQqn5D"}' \
  http://localhost:8028/auth/token/

"""