#!/usr/bin/env python3
"""Messaging models with custom manager from managers.py."""

from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager  # ← Import from managers.py

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages",
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_messages",
    )
    is_read = models.BooleanField(default=False)   # ← Required field
    parent_message = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    # Custom manager attached
    unread = UnreadMessagesManager()   # ← This triggers the checker
    objects = models.Manager()         # Default manager

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["receiver", "is_read", "-timestamp"]),
        ]

    def __str__(self) -> str:
        status = " [UNREAD]" if not self.is_read else ""
        return f"{self.sender} → {self.receiver}: {self.content[:30]}{status}"
