from django_filters import rest_framework as filters
from .models import Message


class MessageFilter(filters.FilterSet):
    """Filter messages by sender or date range"""
    # Filter messages from a specific user
    sender = filters.UUIDFilter(field_name="sender__user_id")
    # Messages in a conversation
    conversation = filters.UUIDFilter(field_name="conversation__conversation_id")
    # Sent after this data
    start_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    # Sent before this date
    end_date = filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')
    # Full text search in message body
    search = filters.CharFilter(field_name='message_body', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ["sender", "conversation", "start_date", "end_date", "search"]
