from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Favorite, Category
from .serializers import FavoriteSerializer, CategorySerializer


class CategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BaseFavoriteView:
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteListCreate(BaseFavoriteView, ListCreateAPIView):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteRetrieveUpdate(BaseFavoriteView, RetrieveUpdateAPIView):

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
