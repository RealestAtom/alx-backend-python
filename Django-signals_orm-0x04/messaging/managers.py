#!/usr/bin/env python3
"""Custom managers for the Message model."""

from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to retrieve unread messages for a specific user.
    Required method name: unread_for_user
    """
    def unread_for_user(self, user):
        """
        Return only unread messages where the user is the receiver.
        Optimized with .only() to reduce payload.
        """
        return self.get_queryset().filter(
            receiver=user,
            is_read=False
        ).only(
            "id",
            "sender",
            "content",
            "timestamp",
            "parent_message_id",
        ).select_related("sender")
