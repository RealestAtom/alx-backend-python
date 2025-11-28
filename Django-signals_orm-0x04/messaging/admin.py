#!/usr/bin/env python3
"""Admin configuration for messaging app — edit history version."""

from django.contrib import admin
from messaging.models import Message, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message with edit history."""
    list_display = ("id", "sender", "receiver", "short_content", "timestamp", "edited_at", "is_read")
    list_filter = ("is_read", "edited_at", "timestamp")
    search_fields = ("sender__username", "receiver__username", "content")
    readonly_fields = ("timestamp", "edited_at")
    date_hierarchy = "timestamp"

    def short_content(self, obj):
        return obj.content[:50] + ("..." if len(obj.content) > 50 else "")
    short_content.short_description = "Content"


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    """Admin view for message edit history."""
    list_display = ("message", "edited_at", "short_old_content")
    list_filter = ("edited_at",)
    search_fields = ("message__id", "message__sender__username", "old_content")
    readonly_fields = ("message", "old_content", "edited_at")
    date_hierarchy = "edited_at"

    def short_old_content(self, obj):
        return obj.old_content[:60] + ("..." if len(obj.old_content) > 60 else "")
    short_old_content.short_description = "Previous Content"

    def has_add_permission(self, request):
        return False  # History is auto-generated only
