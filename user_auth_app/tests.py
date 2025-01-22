from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from .models import UserProfile


class AuthTestCase(APITestCase):

    def setUp(self):
        """Erstelle einen Test-Benutzer"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            type="provider"  # Falls du User-Typen hast
        )

    def test_registration_success(self):
        """Testet eine erfolgreiche Registrierung"""
        url = reverse("registration")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "repeated_password": "newpassword123",
            "type": "customer"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "newuser")
        self.assertEqual(response.data["email"], "newuser@example.com")

    def test_registration_password_mismatch(self):
        """Testet Registrierung mit nicht übereinstimmenden Passwörtern"""
        url = reverse("registration")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "repeated_password": "wrongpassword",
            "type": "customer"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(response.data["password"], [
                         "Das Passwort ist nicht gleich mit dem wiederholten Passwort."])

    def test_registration_username_taken(self):
        """Testet Registrierung mit bereits vergebenem Benutzernamen"""
        url = reverse("registration")
        data = {
            "username": "testuser",  # Existierender Benutzername
            "email": "unique@example.com",
            "password": "newpassword123",
            "repeated_password": "newpassword123",
            "type": "customer"
        }
        response = self.client.post(url, data, format="json")
        expected_messages = [
            "Dieser Benutzername ist bereits vergeben.",
            "A user with that username already exists."
        ]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn(response.data["username"][0], expected_messages)

    def test_registration_email_taken(self):
        """Testet Registrierung mit bereits verwendeter E-Mail"""
        url = reverse("registration")
        data = {
            "username": "newuniqueuser",
            "email": "test@example.com",  # Existierende E-Mail
            "password": "newpassword123",
            "repeated_password": "newpassword123",
            "type": "customer"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], [
                         "Diese E-Mail-Adresse wird bereits verwendet."])

    def test_login_success(self):
        """Testet ein erfolgreiches Login"""
        url = reverse("login")
        data = {
            "username": "testuser",
            "password": "securepassword123"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "test@example.com")

    def test_login_invalid_password(self):
        """Testet Login mit falschem Passwort"""
        url = reverse("login")
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], ["Falsche Anmeldedaten."])

    def test_login_nonexistent_user(self):
        """Testet Login mit nicht existierendem Benutzer"""
        url = reverse("login")
        data = {
            "username": "doesnotexist",
            "password": "somepassword"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], ["Falsche Anmeldedaten."])
