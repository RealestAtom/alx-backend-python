#!/usr/bin/env python3
"""AppConfig for the messaging app."""

from django.apps import AppConfig


class MessagingConfig(AppConfig):
    """Configuration class for the messaging app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "messaging"

    def ready(self) -> None:
        """Import signals when the app is ready."""
        import messaging.signals  # noqa: F401


# Required final newline
