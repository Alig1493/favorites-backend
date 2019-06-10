from django.urls import path

from backend.favorites.views import FavoriteListCreate, FavoriteRetrieveUpdate, CategoryCreate

app_name = "favorites"

urlpatterns = [
    path("", FavoriteListCreate.as_view(), name="list_create"),
    path("<int:pk>/", FavoriteRetrieveUpdate.as_view(), name="retrieve_update"),
    path("category", CategoryCreate.as_view(), name="category_create")
]
