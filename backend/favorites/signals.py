from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Favorite


@receiver(post_save, sender=Favorite)
def audit_log_save(sender, instance, created, **kwargs):
    action_flag = ADDITION
    change_message = ""

    if not created:
        action_flag = CHANGE
        change_message = instance.diff

    LogEntry.objects.log_action(
        user_id=instance.user.id,
        content_type_id=ContentType.objects.get_for_model(instance).pk,
        object_id=instance.id,
        object_repr=instance.title,
        action_flag=action_flag,
        change_message=change_message
    )
