import pytest
from rest_framework.test import APIClient

from backend.favorites.tests.factories import FavoriteFactory
from backend.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def auth_client(user, client):
    client.force_authenticate(user)
    return client


@pytest.fixture
def favorite(user):
    return FavoriteFactory(user=user)
