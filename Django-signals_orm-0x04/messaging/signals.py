#!/usr/bin/env python3
"""Signal handlers for cleanup and history."""

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance: Message, **kwargs):
    if not instance.pk:
        return
    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old.content != instance.content:
        editor = getattr(instance, "_current_user", instance.sender)
        MessageHistory.objects.create(
            message=instance,
            old_content=old.content,
            edited_by=editor,
        )
        instance.edited_at = timezone.now()
        instance.edited_by = editor


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).delete()
