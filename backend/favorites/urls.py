from django.urls import path

from backend.favorites.views import FavoriteListCreate, FavoriteRetrieveUpdate

app_name = "favorites"

urlpatterns = [
    path("", FavoriteListCreate.as_view(), name="list_create"),
    path("<int:pk>/", FavoriteRetrieveUpdate.as_view(), name="retrieve_update"),
]
