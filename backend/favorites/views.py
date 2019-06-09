from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from backend.favorites.models import Favorite
from backend.favorites.serializers import FavoriteListSerializer


class FavoriteListCreate(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteListSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
