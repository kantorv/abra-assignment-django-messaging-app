import pytest
from rest_framework.test import APIClient
from core.models import User
import uuid


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))

        return True
    except ValueError:
        return False


@pytest.fixture
def client():
    return APIClient()

TEST_USER_USERNAME1 = 'sender'
TEST_USER_PASSWORD1 = 'rJX3NdpmQqn5D'


TEST_USER_USERNAME2 = 'receiver'
TEST_USER_PASSWORD2 = '8vBUrp6dkCdMe'

@pytest.fixture
@pytest.mark.django_db
def sample_sender() -> User:
    user = User(username=TEST_USER_USERNAME1)
    user.set_password(TEST_USER_PASSWORD1)
    user.save()
    return user


@pytest.fixture
@pytest.mark.django_db
def sample_receiver() -> User:
    user = User(username=TEST_USER_USERNAME2)
    user.set_password(TEST_USER_PASSWORD2)
    user.save()
    return user


@pytest.mark.django_db
def test_create_message(client: APIClient, sample_sender:User, sample_receiver:User):
    # retreiving jwt
    auth_endpoint = '/auth/token/'
    auth_payload = {
        "username" : TEST_USER_USERNAME1,
        "password" : TEST_USER_PASSWORD1
    }
    response = client.post(auth_endpoint, format="json", data=auth_payload)
    assert response.status_code == 200

    access_token = response.data.get("access", None)
    refresh_token = response.data.get("refresh", None)
    assert refresh_token is not None
    assert access_token is not None

    print("access_token:" , access_token)
    #print(response.data)

    # creating message
    create_msg_endpoint = "/api/v1/messages/"
    payload = dict(
        subject = "Test Message",
        message = "Hello world",
        to = sample_receiver.username
    )

    # sending without jwt, excepting reject
    create_fail_msg_response = client.post(create_msg_endpoint, format="json", data=payload)
    assert create_fail_msg_response.status_code == 401 # jwt not provided
    assert create_fail_msg_response.data.get('detail').code == 'not_authenticated'

    #client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    # sending with jwt, excepting success
    create_msg_response = client.post(create_msg_endpoint, format="json", data=payload, HTTP_AUTHORIZATION='Bearer ' + access_token)
    print(create_msg_response.data,create_msg_response.status_code ,create_msg_response.headers )
    assert create_msg_response.status_code == 201
    msgid =  create_msg_response.data.get('id')
    assert is_valid_uuid(msgid) == True
    assert create_msg_response.data.get('from') == sample_sender.username
    assert create_msg_response.data.get('to') == sample_receiver.username











