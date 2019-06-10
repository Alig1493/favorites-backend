import factory
from django.urls import reverse

from backend.favorites.models import Favorite
from backend.favorites.tests.factories import FavoriteFactory, CategoryFactory


class TestFavorite:

    url = reverse("v1:favorites:list_create")
    metadata = {
        "integer": 1,
        "string": "c",
        "enum": [("a", 1), ("b", "c")]
    }

    def test_get_favorites(self, favorite, auth_client):
        response = auth_client.get(self.url)

        assert response.status_code == 200

        data = response.data.pop()

        assert data.get("id") == favorite.id
        assert data.get("category") == favorite.category.title
        assert data.get("title") == favorite.title
        assert data.get("ranking") == favorite.ranking
        assert data.get("user") == favorite.user_id
        assert not data.get("metadata")
        assert data.get("logs") == [""]

    def test_post_favourites(self, user, auth_client):
        category = CategoryFactory()
        favorite_data = factory.build(dict, FACTORY_CLASS=FavoriteFactory,
                                      user=user.id, category=category.id,
                                      metadata=self.metadata)
        response = auth_client.post(self.url, data=favorite_data, format="json")

        assert response.status_code == 201
        assert Favorite.objects.filter(user_id=user.id,
                                       category_id=category.id,
                                       ranking__exact=favorite_data.get("ranking"),
                                       title=favorite_data.get("title"),
                                       metadata=self.metadata
                                       ).count() == 1

    def test_post_duplicate_category_ranking(self, user, favorite, auth_client):
        category = favorite.category
        ranking = favorite.ranking

        favorite_data = factory.build(dict, FACTORY_CLASS=FavoriteFactory,
                                      user=user.id, category=category.id,
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
