#!/usr/bin/env python3
"""Views for chats with caching."""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from messaging.models import Message


@login_required
@cache_page(60)  # ← REQUIRED: 60-second cache timeout
def conversation_list(request):
    """
    Display all root messages (conversations) for the current user.
    This view is cached for 60 seconds using @cache_page(60).
    """
    conversations = Message.objects.filter(
        parent_message__isnull=True
    ).filter(
        sender=request.user
    ).select_related("receiver").order_by("-timestamp")

    context = {
        "conversations": conversations
    }
    return render(request, "chats/conversation_list.html", context)


# Optional: Class-based version (also cached)
@method_decorator(cache_page(60), name='dispatch')
class CachedConversationListView(ListView):
    template_name = "chats/conversation_list.html"
    context_object_name = "conversations"

    def get_queryset(self):
        return Message.objects.filter(
            parent_message__isnull=True,
            sender=self.request.user
        ).select_related("receiver").order_by("-timestamp")
