import ast

import pytest
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from factory.fuzzy import FuzzyText

from backend.favorites.models import Favorite
from backend.favorites.tests.factories import CategoryFactory, FavoriteFactory


class TestAuditLogs:

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


class TestRanking:

    def test_same_category_ranking(self, user):
        category = CategoryFactory()
        FavoriteFactory.create_batch(2, user=user, category=category, ranking=1)

        assert Favorite.objects.get(category=category, ranking__exact=1)
        assert Favorite.objects.get(category=category, ranking__exact=2)

    def test_different_category_ranking(self, user):
        FavoriteFactory.create_batch(2, user=user, ranking=1)
        assert Favorite.objects.filter(ranking__exact=1).count() == 2


class TestDescription:

    def test_description_minimum_length_success(self, user):
        fuzzy_text = FuzzyText(length=10).fuzz()
        assert FavoriteFactory(user=user, description=fuzzy_text)

    def test_description_minimum_length_failure(self, user):
        fuzzy_text = FuzzyText(length=9).fuzz()
        with pytest.raises(ValidationError) as validation_error:
            FavoriteFactory(user=user, description=fuzzy_text)
        assert validation_error.value.message_dict == {"description": ["Must be at least 10 characters long."]}
