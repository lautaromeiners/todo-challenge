from django.test import TestCase
from authentication.models import User


class TestUser(TestCase):

    def test_create_user(self):
        """Test creating a user with an email and password"""
        user = User.objects.create_user(
            email="testuser@example.com", username="Test", password="password123"
        )
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(
            user.check_password("password123")
        )  # Verifies the password is hashed and works
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = User.objects.create_superuser(
            email="admin@example.com", username="Admin", password="adminpass"
        )
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertTrue(superuser.check_password("adminpass"))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_email(self):
        """Test creating a user without an email should raise an error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", username="Test", password="password123")
