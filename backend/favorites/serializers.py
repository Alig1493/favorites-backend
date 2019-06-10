from rest_framework import serializers

from backend.favorites.models import Category, Favorite


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = []


class FavoriteSerializer(serializers.ModelSerializer):

    logs = serializers.JSONField(source="get_audit_log_change_list", read_only=True)

    class Meta:
        model = Favorite
        exclude = []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.title
        return representation
