from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from main_app.models import Report


User = get_user_model()


class PrivacyDataTests(APITestCase):
    def setUp(self):
        self.warga_a = User.objects.create_user(
            username="warga_a",
            password="TestPass123!",
            is_admin=False,
        )
        self.warga_b = User.objects.create_user(
            username="warga_b",
            password="TestPass123!",
            is_admin=False,
        )
        self.draft_milik_b = Report.objects.create(
            title="Draf Rahasia Warga B",
            category="Infrastruktur",
            description="Ini adalah draf yang belum diajukan.",
            location="Lokasi Rahasia",
            status="DRAFT",
            reporter=self.warga_b,
        )
        self.laporan_publik_a = Report.objects.create(
            title="Jalan Berlubang di Depan Kampus",
            category="Infrastruktur",
            description="Ada lubang besar yang membahayakan pengendara.",
            location="Jl. Soekarno Hatta",
            status="REPORTED",
            reporter=self.warga_a,
        )
        self.laporan_publik_b = Report.objects.create(
            title="Sampah Menumpuk di Trotoar",
            category="Kebersihan",
            description="Sampah tidak diangkut selama seminggu.",
            location="Jl. Gatot Subroto",
            status="REPORTED",
            reporter=self.warga_b,
        )

    def test_PRIV_01_feed_kota_menyembunyikan_identitas_reporter(self):
        # Arrange
        self.client.force_authenticate(user=self.warga_a)

        # Act
        response = self.client.get("/api/report/?tab=feed")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", [])
        self.assertGreater(len(results), 0)
        for report in results:
            self.assertEqual(report["reporter"], "Warga Anonim")

    def test_PRIV_02_laporan_saya_menampilkan_nama_asli(self):
        # Arrange
        self.client.force_authenticate(user=self.warga_a)

        # Act
        response = self.client.get("/api/report/?tab=my_reports")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", [])
        self.assertGreater(len(results), 0)
        for report in results:
            self.assertEqual(report["reporter_name"], "warga_a")

    def test_PRIV_03_tidak_bisa_baca_draf_orang_lain(self):
        # Arrange
        self.client.force_authenticate(user=self.warga_a)

        # Act
        response = self.client.get(f"/api/report/{self.draft_milik_b.pk}/")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_PRIV_04_tidak_bisa_modifikasi_draf_orang_lain(self):
        # Arrange
        self.client.force_authenticate(user=self.warga_a)
        payload = {
            "title": "Judul Diubah Paksa",
            "category": self.draft_milik_b.category,
            "description": "Konten ini tidak boleh tersimpan.",
            "location": self.draft_milik_b.location,
            "status": self.draft_milik_b.status,
        }

        # Act
        response = self.client.put(
            f"/api/report/{self.draft_milik_b.pk}/",
            payload,
            format="json",
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.draft_milik_b.refresh_from_db()
        self.assertEqual(self.draft_milik_b.title, "Draf Rahasia Warga B")
        self.assertEqual(
            self.draft_milik_b.description,
            "Ini adalah draf yang belum diajukan.",
        )
