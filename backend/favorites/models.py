from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinLengthValidator
from django.db import models

from backend.base.mixins.models import ModelDiffMixin
from backend.base.models import LogBase

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=128)


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
        unique_together = ("ranking", "category")
