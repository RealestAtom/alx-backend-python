
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    """Pagination class for messages in a conversation: 20 messages per page"""
    page_size = 20  # Number of messages per page

    def get_paginated_response(self, data):
        """ Override this method to include page.paginator.count in the response"""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
