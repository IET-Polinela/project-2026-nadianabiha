from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main_app.models import Report


User = get_user_model()


class CRUDValidationTests(APITestCase):
    def setUp(self):
        self.warga = User.objects.create_user(
            username="warga_crud",
            password="TestPass123!",
            is_admin=False,
        )
        self.client.force_authenticate(user=self.warga)

    def test_FT_01_buat_laporan_dengan_data_lengkap(self):
        # Arrange
        payload = {
            "title": "Lampu Jalan Mati",
            "category": "Fasilitas Umum",
            "description": "Lampu jalan mati sejak tiga hari lalu.",
            "location": "Jl. Merdeka",
            "status": "DRAFT",
        }

        # Act
        response = self.client.post(reverse("report-list"), payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        report = Report.objects.get(title="Lampu Jalan Mati")
        self.assertEqual(report.reporter, self.warga)
        self.assertEqual(response.data["title"], payload["title"])

    def test_FT_02_ditolak_jika_judul_kosong(self):
        # Arrange
        payload = {
            "category": "Infrastruktur",
            "description": "Deskripsi lengkap tanpa judul.",
            "location": "Jl. Mawar",
        }

        # Act
        response = self.client.post(reverse("report-list"), payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_FT_03_ditolak_jika_deskripsi_kosong(self):
        # Arrange
        payload = {
            "title": "Laporan Tanpa Deskripsi",
            "category": "Kebersihan",
            "location": "Pasar Kota",
        }

        # Act
        response = self.client.post(reverse("report-list"), payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("description", response.data)

    def test_FT_04_xss_script_disimpan_sebagai_string_literal(self):
        # Arrange
        kode_xss = '<script>alert("xss")</script>'
        payload = {
            "title": "Laporan XSS Test",
            "category": "Keamanan",
            "description": kode_xss,
            "location": "Lab Keamanan Siber",
        }

        # Act
        response = self.client.post(reverse("report-list"), payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        report = Report.objects.get(title="Laporan XSS Test")
        self.assertEqual(report.description, kode_xss)
