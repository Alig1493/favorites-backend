from django.contrib import admin

from .models import Category, Favorite

admin.site.register(Category)
admin.site.register(Favorite)
