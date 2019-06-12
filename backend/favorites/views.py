from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Favorite
from .serializers import FavoriteSerializer


class BaseFavoriteView:
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class FavoriteListCreate(BaseFavoriteView, ListCreateAPIView):
    pass


class FavoriteRetrieveUpdate(BaseFavoriteView, RetrieveUpdateAPIView):
    pass
