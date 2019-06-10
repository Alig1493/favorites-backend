from rest_framework import serializers

from backend.favorites.models import Category, Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    logs = serializers.JSONField(source="get_audit_log_change_list", read_only=True)
    category = serializers.CharField(max_length=128)

    class Meta:
        model = Favorite
        exclude = []

    def create(self, validated_data):
        category_title = validated_data.pop("category")
        category, created = Category.objects.get_or_create(title=category_title)
        favorite = Favorite.objects.create(category=category, **validated_data)
        return favorite

    def update(self, instance, validated_data):
        if validated_data.get("category"):
            category_title = validated_data.pop("category")
            category, created = Category.objects.get_or_create(title=category_title)
            instance.category = category
        return super().update(instance, validated_data)
