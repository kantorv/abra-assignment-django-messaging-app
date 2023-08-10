import pytest
from core.models import User


@pytest.fixture
@pytest.mark.django_db
def sample_user() -> User:
    user = User.objects.create_user('testuser', 'asdasd123')
    return user


@pytest.mark.django_db
def test_db_accessible(sample_user:User):
    assert sample_user.username == "testuser"
    assert sample_user.is_superuser == False
    assert sample_user.is_staff == False
    assert sample_user.is_active == True

