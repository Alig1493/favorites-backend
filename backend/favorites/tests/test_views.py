from django.urls import reverse


class TestFavorite:

    url = reverse("v1:favorites:list")

    def test_get_favorites(self, favorite, auth_client):
        response = auth_client.get(self.url)

        assert response.status_code == 200

        data = response.data.pop()

        assert data.get("id") == favorite.id
        assert data.get("category") == favorite.category.title
        assert data.get("ranking") == favorite.ranking
        assert data.get("user") == favorite.user_id
