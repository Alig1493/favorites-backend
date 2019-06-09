import pytest
from rest_framework.test import APIClient

from backend.users.tests.factories import UserFactory


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def auth_client(user, client):
    client.force_authenticate(user)
    return client


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass
