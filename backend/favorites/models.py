from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import F

from backend.base.mixins.models import ModelDiffMixin
from backend.base.models import LogBase

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Favorite(ModelDiffMixin, LogBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    ranking = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    metadata = JSONField(blank=True, null=True)
    description = models.TextField(blank=True,
                                   validators=[
                                       MinLengthValidator(10, message="Must be at least 10 characters long.")
                                   ])

    class Meta:
        unique_together = ["ranking", "category"]

    def __str__(self):
        return f"{self.title}-{self.ranking}"

    def get_audit_log_change_list(self):
        log_entry = LogEntry.objects.filter(
            content_type_id=ContentType.objects.get_for_model(self).pk,
            object_id=self.id
        )

        return log_entry.values_list("change_message", flat=True)

    def adjust_category_ranking(self):
        self._meta.default_manager.filter(
            category=self.category,
            ranking__gte=self.ranking
        ).update(ranking=F("ranking") + 1)

    def save(self, *args, **kwargs):
        try:
            self.validate_unique()
        except ValidationError:
            self.adjust_category_ranking()

        super().save(*args, **kwargs)
