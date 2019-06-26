from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Favorite, Category
from .serializers import FavoriteSerializer, CategorySerializer, CategorizedFavoriteSerializer


class CategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BaseFavoriteView:
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by("ranking")


class FavoriteListCreate(BaseFavoriteView, ListCreateAPIView):

    def get_serializer_class(self):
        if getattr(self.request, "method", "GET"):
            return CategorizedFavoriteSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return Category.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavoriteRetrieveUpdate(BaseFavoriteView, RetrieveUpdateAPIView):

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
