
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


User = get_user_model()


class TestJWT(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@email.com", 
            password="pass", 
            username="jwt_test"
        )

    def test_jwt_token_and_api_access(self):
        """ Integration test for testing JWT authentication including:
                1. Obtaining JWT token
                2. Accessing protected API
                3. Refreshing token
        """
        # 1. Get JWT token
        response = self.client.post("/api/token/", {"email": self.user.email, "password": "pass"})
        self.assertEqual(response.status_code, 200)
        tokens = response.json()
        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)

        access_token = tokens["access"]
        refresh_token = tokens["refresh"]

        # 2. Access protected API
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response2 = self.client.get("/api/conversations/")
        self.assertEqual(response2.status_code, 200)

        # 3. Refresh token
        response3 = self.client.post("/api/token/refresh/", {"refresh": refresh_token})
        self.assertEqual(response3.status_code, 200)
        self.assertIn("access", response3.json())
