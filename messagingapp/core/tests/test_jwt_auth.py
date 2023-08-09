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
    assert response.status_code == 401
    error_details =  response.data.get("detail")
    assert error_details.code == "no_active_account"




@pytest.mark.django_db
def test_refresh_token(client: APIClient, sample_user:User):
    endpoint = '/auth/token/'
    payload = {
        "username" : TEST_USER_USERNAME,
        "password" : TEST_USER_PASSWORD
    }
    response = client.post(endpoint, format="json", data=payload)
    assert response.status_code == 200

    access_token = response.data.get("refresh", None)
    refresh_token = response.data.get("refresh", None)
    assert refresh_token is not None
    assert access_token is not None


    refresh_endpoint = '/auth/token/refresh/'
    refresh_payload = {
        "refresh" : refresh_token
    }
    refresh_response = client.post(refresh_endpoint, format="json", data=refresh_payload)
    assert refresh_response.status_code == 200
    assert "access" in refresh_response.data
    refreshed_raccess_token = refresh_response.data.get("access", None)
    assert refreshed_raccess_token is not None
    #print(refresh_response.data)



@pytest.mark.django_db
def test_verify_token(client: APIClient, sample_user:User):
    endpoint = '/auth/token/'
    payload = {
        "username" : TEST_USER_USERNAME,
        "password" : TEST_USER_PASSWORD
    }
    response = client.post(endpoint, format="json", data=payload)
    assert response.status_code == 200

    access_token = response.data.get("access", None)
    refresh_token = response.data.get("refresh", None)
    assert refresh_token is not None
    assert access_token is not None


    verify_endpoint = '/auth/token/verify/'
    verify_payload = {
        "token" : access_token
    }
    verify_response = client.post(verify_endpoint, format="json", data=verify_payload)
    assert verify_response.status_code == 200

    # assert "access" in refresh_response.data
    # refreshed_raccess_token = refresh_response.data.get("access", None)
    # assert refreshed_raccess_token is not None
    print(verify_response.data)

    refresh_endpoint = '/auth/token/refresh/'
    refresh_payload = {
        "refresh": refresh_token
    }
    refresh_response = client.post(refresh_endpoint, format="json", data=refresh_payload)
    assert refresh_response.status_code == 200

    # TODO: add blacklist token app
    verify_response = client.post(verify_endpoint, format="json", data=verify_payload)
    assert verify_response.status_code == 200







"""
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "rJX3NdpmQqn5D"}' \
  http://localhost:8028/auth/token/


curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxMzkxOTgyLCJpYXQiOjE2OTEzOTE2ODIsImp0aSI6ImNiMTRhNmQxNWE4MDQxNWU4ZjUzYWNmNDJlOTYzZjAxIiwidXNlcl9pZCI6ImZlYTk1OWU1LWQyMzUtNDRhNC1hZWIwLTc3MjcwYjk5ZWM2YSJ9.8LVxz-3GUVOaJxIFY70svSz-3Bt3x0iugPaPtb70JAk" \
  -d '{"to": "demo1", "subject": "Test Subj", "message": "Hello World"}' \
  http://localhost:8028/api/v1/messages/

"""