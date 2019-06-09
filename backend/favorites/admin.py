from django.contrib import admin

from backend.favorites.models import Category, Favorite

admin.site.register(Category)
admin.site.register(Favorite)
