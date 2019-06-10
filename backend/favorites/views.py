from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from backend.favorites.models import Favorite
from backend.favorites.serializers import CategorySerializer, FavoriteSerializer


class CategoryCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer


class BaseFavoriteView:
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteListCreate(BaseFavoriteView, ListCreateAPIView):
    pass


class FavoriteRetrieveUpdate(BaseFavoriteView, RetrieveUpdateAPIView):
    pass
