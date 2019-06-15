from django.urls import path

from .views import FavoriteListCreate, FavoriteRetrieveUpdate, CategoryListView

app_name = "favorites"

urlpatterns = [
    path("", FavoriteListCreate.as_view(), name="list_create"),
    path("<int:pk>/", FavoriteRetrieveUpdate.as_view(), name="retrieve_update"),
    path("categories/", CategoryListView.as_view(), name="categories_list"),
]
