"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r"^blog/", include("blog.urls"))
"""
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from backend import settings
from rest_framework.documentation import include_docs_urls

api_v1_urlpatterns = ([
    path("auth/", include("backend.users.urls", namespace="users")),
    path("favorites/", include("backend.favorites.urls", namespace="favorites")),
], "backend_auth_urls")

urlpatterns = [
    path("", admin.site.urls),
    path("api/v1/", include(api_v1_urlpatterns, namespace="v1")),
    path("docs/", include_docs_urls(title="backend API")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
