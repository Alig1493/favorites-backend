from django.contrib.admin.models import LogEntry, CHANGE
from rest_framework import serializers

from .models import Category, Favorite


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["title"]


class FavoriteSerializer(serializers.ModelSerializer):

    logs = serializers.SerializerMethodField(read_only=True)
    category = serializers.CharField(max_length=128)

    class Meta:
        model = Favorite
        exclude = ["user"]

    def get_logs(self, instance):
        log_entry = LogEntry.objects.filter(
            action_flag=CHANGE,
            object_id=instance.id,
        )
        changes = log_entry.values_list("change_message", flat=True)

        return list(changes)

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


class CategorizedFavoriteSerializer(CategorySerializer):
    favorite_things = serializers.SerializerMethodField()

    class Meta(CategorySerializer.Meta):
        fields = ["id", "title", "favorite_things"]

    def get_favorite_things(self, instance):
        user = self.context.get("request").user
        queryset = Favorite.objects.filter(category=instance, user=user).order_by("ranking")
        serializer = FavoriteSerializer(instance=queryset, many=True)
        return serializer.data
