from django.apps import AppConfig


class FavoritesConfig(AppConfig):
    name = 'backend.favorites'

    def ready(self):
        from .signals import audit_log_save  # noqa
