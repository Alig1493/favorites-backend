from rest_framework import serializers

from backend.favorites.models import Favorite


class FavoriteListSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()
    logs = serializers.JSONField(source="get_audit_log_change_list")

    class Meta:
        model = Favorite
        exclude = []
