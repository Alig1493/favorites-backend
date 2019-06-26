from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import F

from backend.base.mixins.models import ModelDiffMixin
from backend.base.models import LogBase


User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

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

    def __str__(self):
        return f"{self.title}-{self.ranking}"

    def validate_unique_category_ranking(self):
        return self._meta.default_manager.filter(
            category=self.category,
            ranking=self.ranking
        ).exists()

    def adjust_category_ranking(self):
        self._meta.default_manager.filter(
            category=self.category,
            ranking__gte=self.ranking
        ).update(ranking=F("ranking") + 1)

    def save(self, *args, **kwargs):
        if self.validate_unique_category_ranking():
            self.adjust_category_ranking()
        self.full_clean()

        super().save(*args, **kwargs)
