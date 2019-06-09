from django.urls import path

from backend.favorites.views import FavoriteListCreate

app_name = "favorites"

urlpatterns = [
    path("", FavoriteListCreate.as_view(), name="list")
]
