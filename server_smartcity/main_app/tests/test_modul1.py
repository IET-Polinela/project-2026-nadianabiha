from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.warga = User.objects.create_user(
            username="warga_test",
            password="Password123!",
            is_admin=False,
        )
        self.admin = User.objects.create_user(
            username="admin_test",
            password="AdminPass123!",
            is_admin=True,
            is_staff=True,
        )

    def test_AUTH_01_login_warga_dengan_kredensial_valid(self):
        # Arrange
        payload = {"username": "warga_test", "password": "Password123!"}

        # Act
        response = self.client.post("/api/token/", payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_AUTH_02_login_warga_dengan_password_salah(self):
        # Arrange
        payload = {"username": "warga_test", "password": "passwordSALAH"}

        # Act
        response = self.client.post("/api/token/", payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)

    def test_AUTH_03_warga_tidak_bisa_akses_halaman_admin(self):
        # Arrange
        self.client.force_login(self.warga)

        # Act
        response = self.client.get("/dashboard/")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
