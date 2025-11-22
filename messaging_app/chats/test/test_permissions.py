
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


User = get_user_model()


class TestPermissions(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="test@email.com", 
            password="pass", 
            username="test_user"
        )

        self.user2 = User.objects.create_user(
            email="test2@email.com",
            password="pass",
            username="test_user2"
        )

        self.user3 = User.objects.create_user(
            email="test3@email.com",
            password="pass",
            username="test_user3"
        )

        # Authenticate the user and get JWT tokens
        self.response = self.client.post("/api/token/", {"email": self.user.email, "password": "pass"})
        self.access_token = self.response.json()["access"]
        self.refresh_token = self.response.json()["refresh"]
        # Set the Authorization header for future requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
    

    def _create_conversation(self, participants):
        """Helper to create a conversation and return its ID"""
        data = {
            "participant_ids": [user.user_id for user in participants],
        }
        response = self.client.post("/api/conversations/", data, format='json')
        return response.json()["conversation_id"]

    def _authenticate(self, user):
        """Helper to authenticate a user and set the client credentials"""
        response = self.client.post("/api/token/", {"email": user.email, "password": "pass"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")

    # ===========================================================
    # Conversation Tests
    # ===========================================================

    # Get Conversation Tests

    def test_authenticated_user_can_list_conversations (self):
        """Test that an authenticated user can view conversations they're a participant of"""
        response = self.client.get("/api/conversations/")
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_cannot_list_conversations (self):
        """Test that an unauthenticated user cannot view conversations"""
        self.client.credentials()  # Remove authentication to simulate an unauthenticated user
        response = self.client.get("/api/conversations/")
        self.assertEqual(response.status_code, 401)

    # Create Conversation Tests

    def test_authenticated_user_can_create_conversation (self):
        """Test that an authenticated user can create a conversation"""
        data = {
            "participant_ids": [self.user.user_id, self.user2.user_id],
        }
        response = self.client.post("/api/conversations/", data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_unauthenticated_user_cannot_create_conversation (self):
        """Test that an unauthenticated user cannot create a conversation"""
        self.client.credentials()  # Remove authentication to simulate an unauthenticated user
        data = {
            "participant_ids": [self.user.user_id, self.user2.user_id],
        }
        response = self.client.post("/api/conversations/", data, format='json')
        self.assertEqual(response.status_code, 401)

    # ===========================================================
    # Message Tests
    # ===========================================================
    
    # Get Message Tests

    def test_authenticated_participant_can_list_messages (self):
        """Test that an authenticated participant can view messages in a conversation"""
        # First create a conversation with both users: user who is authenticated creates the conversation
        conversation_id = self._create_conversation([self.user, self.user2])

        # Now we can try to list messages in that conversation
        response = self.client.get(f"/api/conversations/{conversation_id}/messages/")
        self.assertEqual(response.status_code, 200)

    def test_authenticated_nonparticipant_cannot_list_messages (self):
        """Test that an authenticated non-participant cannot view messages in a conversation"""
        # First create a conversation with user and user2
        conversation_id = self._create_conversation([self.user, self.user2])

        # Authenticate as user3 who is not a participant
        self._authenticate(self.user3)

        # Now try to list messages in that conversation as user3
        response = self.client.get(f"/api/conversations/{conversation_id}/messages/")
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_user_cannot_list_messages (self):
        """Test that an unauthenticated user cannot view messages in a conversation"""
        # First create a conversation with user and user2
        conversation_id = self._create_conversation([self.user, self.user2])

        # Remove authentication to simulate an unauthenticated user
        self.client.credentials()

        # Now try to list messages in that conversation
        response = self.client.get(f"/api/conversations/{conversation_id}/messages/")
        self.assertEqual(response.status_code, 401)

    # Create Message Tests

    def test_authenticated_participant_can_create_message (self):
        """Test that an authenticated participant can create a message in a conversation"""
        # First create a conversation with both users: user who is authenticated creates the conversation
        conversation_id = self._create_conversation([self.user, self.user2])

        # Now try to create a message in that conversation
        message_data = {
            "message_body": "Hello, this is a test message."
        }
        response = self.client.post(f"/api/conversations/{conversation_id}/messages/", message_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_authenticated_nonparticipant_cannot_create_message (self):
        """Test that an authenticated non-participant cannot create a message in a conversation"""
        # First create a conversation with user and user2
        conversation_id = self._create_conversation([self.user, self.user2])

        # Authenticate as user3 who is not a participant
        self._authenticate(self.user3)

        # Now try to create a message in that conversation as user3
        message_data = {
            "message_body": "Hello, this is a test message from non-participant."
        }
        response = self.client.post(f"/api/conversations/{conversation_id}/messages/", message_data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_user_cannot_create_message (self):
        """Test that an unauthenticated user cannot create a message in a conversation"""
        # First create a conversation with user and user2
        conversation_id = self._create_conversation([self.user, self.user2])

        # Remove authentication to simulate an unauthenticated user
        self.client.credentials()

        # Now try to create a message in that conversation
        message_data = {
            "message_body": "Hello, this is a test message."
        }
        response = self.client.post(f"/api/conversations/{conversation_id}/messages/", message_data, format='json')
        self.assertEqual(response.status_code, 401)

    # Update Message Tests

    def test_message_sender_can_update_own_message (self):
        """Test that the sender of a message can update their own message"""
        # First create a conversation with both users: user who is authenticated creates the conversation
        conversation_id = self._create_conversation([self.user, self.user2])

        # Create a message in that conversation
        message_data = {
            "message_body": "Original message"
        }
        response = self.client.post(f"/api/conversations/{conversation_id}/messages/", message_data, format='json')
        message_id = response.json()["message_id"]

        # Now try to update the message
        updated_message_data = {
            "message_body": "Updated message"
        }
        response = self.client.put(f"/api/conversations/{conversation_id}/messages/{message_id}/", updated_message_data, format='json')
        self.assertEqual(response.status_code, 200)
    
    def test_non_sender_cannot_update_message (self):
        """Test that a participant who is not the sender cannot update someone else's message"""
        # First create a conversation with user and user2
        conversation_id = self._create_conversation([self.user, self.user2])

        # Create a message in that conversation as user
        message_data = {
            "message_body": "Original message"
        }
        response = self.client.post(f"/api/conversations/{conversation_id}/messages/", message_data, format='json')
        message_id = response.json()["message_id"]

        # Authenticate as user2 who is a participant but not the sender
        self._authenticate(self.user2)

        # Now try to update the message as user2
        updated_message_data = {
            "message_body": "Attempted update by non-sender"
        }
        response = self.client.put(f"/api/conversations/{conversation_id}/messages/{message_id}/", updated_message_data, format='json')
        self.assertEqual(response.status_code, 403)
