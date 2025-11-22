
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsAuthenticatedUser(IsAuthenticated):
    """ Allows access only to authenticated users
        Uses Django REST Framework's built-in IsAuthenticated permission

        Not overriding it, it still behaves exactly like IsAuthenticated
    """
    pass


class IsParticipantOfConversation(BasePermission):
    """Custom permission to only allow participants of a conversation to send, view, update and delete messages"""

    def has_permission(self, request, view):
        """Only authenticated users can access"""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """ Check if the user is a participant of the conversation
            obj can be a Conversation or Message:
                If Conversation: check if user is participant.
                If Message: check if user is participant of message.conversation
        """
        if hasattr(obj, "participants"):
            # It's a Conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, "conversation"):
            # It's a Message
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                # For updating or deleting a message, only the sender can do it
                return obj.sender == request.user and request.user in obj.conversation.participants.all()
            return request.user in obj.conversation.participants.all()
        return False
