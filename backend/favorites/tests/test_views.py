import factory
import pytest
from django.contrib.admin.models import LogEntry, CHANGE
from django.urls import reverse

from backend.favorites.models import Favorite, Category
from backend.favorites.tests.factories import FavoriteFactory, CategoryFactory
from backend.users.tests.factories import UserFactory


class TestFavoriteListCreate:

    url = reverse("v1:favorites:list_create")
    metadata = {
        "integer": 1,
        "string": "c",
        "enum": [("a", 1), ("b", "c")]
    }

    def test_raise_unauthenticated_error(self, client):
        response = client.get(self.url)

        assert response.status_code == 401

    def test_get_favorites(self, favorite, auth_client):
        response = auth_client.get(self.url)

        assert response.status_code == 200

        data = response.data.pop()

        assert data.get("id") == favorite.id
        assert data.get("category") == favorite.category.title
        assert data.get("title") == favorite.title
        assert data.get("ranking") == favorite.ranking
        assert not data.get("metadata")
        assert data.get("logs") == [""]

    def test_post_favourites(self, user, auth_client):
        category = CategoryFactory()
        favorite_data = factory.build(dict, FACTORY_CLASS=FavoriteFactory,
                                      category=category.title,
                                      metadata=self.metadata)
        response = auth_client.post(self.url, data=favorite_data, format="json")

        assert response.status_code == 201
        assert Favorite.objects.filter(user_id=user.id,
                                       category_id=category.id,
                                       ranking__exact=favorite_data.get("ranking"),
                                       title=favorite_data.get("title"),
                                       metadata=self.metadata
                                       ).count() == 1

    def test_post_favorites_new_category(self, user, auth_client):
        category_title = "New category"
        favorite_data = factory.build(dict, FACTORY_CLASS=FavoriteFactory,
                                      category=category_title,
                                      metadata=self.metadata)
        response = auth_client.post(self.url, data=favorite_data, format="json")

        assert response.status_code == 201
        assert Category.objects.filter(title__iexact=category_title).count() == 1
        assert Favorite.objects.filter(user_id=user.id,
                                       category__title__iexact=category_title,
                                       ranking__exact=favorite_data.get("ranking"),
                                       title=favorite_data.get("title"),
                                       metadata=self.metadata
                                       ).count() == 1

    def test_post_duplicate_category_ranking(self, user, favorite, auth_client):
        category = favorite.category
        ranking = favorite.ranking

        favorite_data = factory.build(dict, FACTORY_CLASS=FavoriteFactory,
                                      category=category.title,
                                      ranking=ranking)

        response = auth_client.post(self.url, data=favorite_data, format="json")

        filter_dict = dict(
            user_id=user.id,
            category_id=category.id
        )

        assert response.status_code == 201

        favorite.refresh_from_db()

        assert favorite.ranking == ranking + 1
        assert Favorite.objects.filter(ranking__exact=favorite_data.get("ranking"),
                                       title=favorite_data.get("title"),
                                       **filter_dict).count() == 1
        assert Favorite.objects.filter(ranking__exact=favorite.ranking,
                                       title=favorite.title,
                                       **filter_dict).count() == 1

    def test_missing_required_field_value(self, user, auth_client):
        favorite_data = factory.build(dict, FACTORY_CLASS=FavoriteFactory,
                                      user=user.id, category=None,
                                      metadata=self.metadata)

        response = auth_client.post(self.url, data=favorite_data, format="json")

        assert response.status_code == 400


class TestFavoriteRetrieveUpdate:

    @pytest.fixture
    def url(self, favorite):
        return reverse("v1:favorites:retrieve_update", args=[favorite.id])

    def test_raise_unauthenticated_error(self, url, client):
        response = client.get(url)

        assert response.status_code == 401

    def test_raise_not_found_error(self, url, client):
        user = UserFactory()
        client.force_authenticate(user)
        response = client.get(url)

        assert response.status_code == 404

    def test_retrieve_favorite_object(self, favorite, auth_client, url):
        response = auth_client.get(url)

        assert response.status_code == 200
        assert response.data.get("id") == favorite.id

    def test_put_favorite(self, favorite, auth_client, url):
        description = "loren ipsum"

        favorite_data = {
            "ranking": favorite.ranking,
            "title": favorite.title,
            "description": description,
            "category": favorite.category.title
        }

        expected_change_message = {
            "description": ("", description)
        }

        response = auth_client.put(url, data=favorite_data, format="json")

        assert response.status_code == 200

        favorite.refresh_from_db()

        assert favorite.description == description
        assert LogEntry.objects.get(
            object_id=favorite.id,
            action_flag=CHANGE
        ).change_message == str(expected_change_message)

    def test_patch_favorite(self, favorite, auth_client, url):
        description = "loren ipsum"

        expected_change_message = {
            "description": ("", description)
        }

        response = auth_client.patch(url, data={"description": description}, format="json")

        assert response.status_code == 200

        favorite.refresh_from_db()

        assert favorite.description == description
        assert LogEntry.objects.get(
            object_id=favorite.id,
            action_flag=CHANGE
        ).change_message == str(expected_change_message)

    def test_patch_new_category(self, favorite, auth_client, url):
        category_title = "cat"
        response = auth_client.patch(url, data={"category": category_title}, format="json")

        assert response.status_code == 200
        assert Category.objects.filter(title__iexact=category_title).count() == 1

        favorite.refresh_from_db()

        assert favorite.category_id == Category.objects.get(title__iexact=category_title).id
