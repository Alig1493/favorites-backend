from django.db import models


class LogBase(models.Model):

    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True
