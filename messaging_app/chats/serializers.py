from rest_framework import serializers
from .models import User, Conversation, Message


# -----------------------------------
# User Serializer
# -----------------------------------
class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "created_at",
        ]


# -----------------------------------
# Message Serializer
# -----------------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "sender_name",
            "conversation",
            "message_body",
            "sent_at",
        ]


# -----------------------------------
# Conversation Serializer (NESTED)
# -----------------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    def get_messages(self, obj):
        messages = obj.messages.all().order_by("sent_at")
        return MessageSerializer(messages, many=True).data


    def validate(self, data):
        if "participants" in data and len(data["participants"]) == 0:
            raise serializers.ValidationError("Conversation must have participants.")
        return data

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
        ]
