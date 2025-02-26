from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User


class RegistrationTest(APITestCase):

    def test_registration(self):
        """Test successful registration"""
        url = reverse("rest_register")
        data = {
            "email": "testuser@example.com",
            "password1": "aStrongPassword",
            "password2": "aStrongPassword",
            "username": "test",
        }

        # Send registration request
        response = self.client.post(url, data)

        # Check if the registration response is successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTest(APITestCase):

    def test_login(self):
        """Test the user login via API"""
        # First, register the user
        register_url = reverse("rest_register")
        register_data = {
            "email": "testuser@example.com",
            "password1": "aStrongPassword",
            "password2": "aStrongPassword",
            "username": "test",
        }

        # Send registration request
        response = self.client.post(register_url, register_data)

        # Login User
        login_url = reverse("rest_login")
        login_data = {"email": "testuser@example.com", "password": "aStrongPassword"}
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("key", response.data)  # Ensure that access token is returned


class LogoutTest(APITestCase):

    def test_logout(self):
        """Test the user logout via API"""
        # First, register the user
        register_url = reverse("rest_register")
        register_data = {
            "email": "testuser@example.com",
            "password1": "aStrongPassword",
            "password2": "aStrongPassword",
            "username": "test",
        }

        # Send registration request
        response = self.client.post(register_url, register_data)

        # Login User
        login_url = reverse("rest_login")
        login_data = {"email": "testuser@example.com", "password": "aStrongPassword"}
        login_response = self.client.post(login_url, login_data)
        token = login_response.data["key"]

        # Log out the user
        logout_url = reverse("rest_logout")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        logout_response = self.client.post(logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", logout_response.data)
        self.assertEqual(logout_response.data["detail"], "Successfully logged out.")
