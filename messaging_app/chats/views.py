
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__first_name", "participants__last_name"]

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants")

        if not participants or len(participants) < 2:
            raise ValidationError("A conversation must include at least two participants.")

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body"]

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        sender = request.data.get("sender")
        message_body = request.data.get("message_body")

        if not conversation_id:
            raise ValidationError("conversation is required.")

        if not sender:
            raise ValidationError("sender is required.")

        if not message_body:
            raise ValidationError("message_body cannot be empty.")

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation does not exist.")

        message = Message.objects.create(
            conversation=conversation,
            sender_id=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
