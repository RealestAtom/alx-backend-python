#!/usr/bin/env python3
"""Tests for message notification signal behavior."""

from django.test import TestCase
from django.contrib.auth import get_user_model

from messaging.models import Message, Notification

User = get_user_model()


class MessageNotificationSignalTest(TestCase):
    """Test cases for the notification creation signal."""

    def setUp(self) -> None:
        self.alice = User.objects.create_user(username="alice", password="pass")
        self.bob = User.objects.create_user(username="bob", password="pass")

    def test_notification_created_on_new_message(self) -> None:
        """Ensure notification is created when a user receives a message."""
        Message.objects.create(
            sender=self.alice,
            receiver=self.bob,
            content="Hello Bob!",
        )
        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        self.assertEqual(notif.user, self.bob)
        self.assertFalse(notif.is_seen)

    def test_no_notification_on_self_message(self) -> None:
        """No notification should be created for self-sent messages."""
        Message.objects.create(
            sender=self.alice,
            receiver=self.alice,
            content="Note to self",
        )
        self.assertEqual(Notification.objects.count(), 0)

    def test_no_notification_on_message_update(self) -> None:
        """Updating a message should not create a new notification."""
        msg = Message.objects.create(
            sender=self.alice,
            receiver=self.bob,
            content="Initial",
        )
        Notification.objects.all().delete()
        msg.content = "Updated"
        msg.save()
        self.assertEqual(Notification.objects.count(), 0)


# Required final newline
