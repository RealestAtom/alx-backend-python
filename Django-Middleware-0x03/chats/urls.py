
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from .views import UserViewSet, ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'conversations', ConversationViewSet)

# Nested router for messages under conversations: /api/conversations/{conversation_id}/messages/
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]
