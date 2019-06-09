import ast

import pytest
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType

from backend.favorites.tests.factories import FavoriteFactory


class TestAuditLogs:

    @pytest.fixture
    def favorite(self):
        return FavoriteFactory()

    def test_audit_log_creation(self, favorite):
        log_entry = LogEntry.objects.filter(
            user_id=favorite.user.id,
            content_type_id=ContentType.objects.get_for_model(favorite).pk,
            object_id=favorite.id,
            object_repr=favorite.title,
            action_flag=ADDITION
        )

        assert log_entry.count() == 1

    def test_audit_log_change(self, favorite):
        title = "New title"
        old_title = favorite.title
        favorite.title = title
        favorite.save()

        log_entry = LogEntry.objects.filter(
            user_id=favorite.user.id,
            content_type_id=ContentType.objects.get_for_model(favorite).pk,
            object_id=favorite.id,
            object_repr=favorite.title,
            action_flag=CHANGE
        )

        assert log_entry.count() == 1

        change_message = ast.literal_eval(log_entry[0].change_message)

        for key, value in change_message.items():
            assert key == "title"
            assert value == (old_title, title)
