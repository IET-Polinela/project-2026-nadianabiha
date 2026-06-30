from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main_app.models import Report


User = get_user_model()


class WorkflowStateTests(APITestCase):
    def setUp(self):
        self.warga = User.objects.create_user(
            username="warga_wf",
            password="TestPass123!",
            is_admin=False,
        )
        self.laporan_draft = Report.objects.create(
            title="Lampu Kampus Mati",
            category="Fasilitas Umum",
            description="Lampu di depan gedung rektorat tidak menyala.",
            location="Gedung Rektorat",
            status="DRAFT",
            reporter=self.warga,
        )
        self.laporan_reported = Report.objects.create(
            title="Saluran Air Tersumbat",
            category="Infrastruktur",
            description="Saluran air di samping kantin tersumbat.",
            location="Kantin Polinela",
            status="REPORTED",
            reporter=self.warga,
        )
        self.laporan_resolved = Report.objects.create(
            title="AC Rusak di Lab",
            category="Fasilitas Umum",
            description="AC di Lab CPS 1 sudah diperbaiki.",
            location="Lab CPS 1",
            status="RESOLVED",
            reporter=self.warga,
        )

    def test_WF_01_warga_mengajukan_draf_menjadi_reported(self):
        # Arrange
        self.client.force_authenticate(user=self.warga)
        payload = {
            "title": self.laporan_draft.title,
            "category": self.laporan_draft.category,
            "description": self.laporan_draft.description,
            "location": self.laporan_draft.location,
            "status": "REPORTED",
        }

        # Act
        response = self.client.put(
            f"/api/report/{self.laporan_draft.pk}/",
            payload,
            format="json",
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.laporan_draft.refresh_from_db()
        self.assertEqual(self.laporan_draft.status, "REPORTED")

    def test_WF_02_tidak_bisa_edit_laporan_yang_sudah_reported(self):
        # Arrange
        self.client.force_authenticate(user=self.warga)
        payload = {
            "title": "Judul Tidak Boleh Berubah",
            "category": self.laporan_reported.category,
            "description": "Deskripsi ini harus ditolak.",
            "location": self.laporan_reported.location,
            "status": self.laporan_reported.status,
        }

        # Act
        response = self.client.put(
            f"/api/report/{self.laporan_reported.pk}/",
            payload,
            format="json",
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.laporan_reported.refresh_from_db()
        self.assertEqual(self.laporan_reported.title, "Saluran Air Tersumbat")
        self.assertEqual(
            self.laporan_reported.description,
            "Saluran air di samping kantin tersumbat.",
        )

    def test_WF_05_laporan_resolved_tidak_bisa_diubah(self):
        # Arrange
        self.client.force_authenticate(user=self.warga)
        payload = {
            "title": "Judul Resolved Tidak Boleh Berubah",
            "category": self.laporan_resolved.category,
            "description": "Data final tidak boleh diedit.",
            "location": self.laporan_resolved.location,
            "status": self.laporan_resolved.status,
        }

        # Act
        response = self.client.put(
            f"/api/report/{self.laporan_resolved.pk}/",
            payload,
            format="json",
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.laporan_resolved.refresh_from_db()
        self.assertEqual(self.laporan_resolved.title, "AC Rusak di Lab")


class AdminWorkflowTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin_portal",
            password="AdminPass123!",
            is_admin=True,
            is_staff=True,
        )
        self.laporan_reported = Report.objects.create(
            title="Jalan Rusak di Blok C",
            category="Infrastruktur",
            description="Jalan berlubang parah di area parkir Blok C.",
            location="Blok C Polinela",
            status="REPORTED",
            reporter=self.admin,
        )

    def test_WF_03_admin_mengubah_status_reported_ke_verified(self):
        # Arrange
        self.client.force_login(self.admin)
        url = reverse("update_report_status", kwargs={"pk": self.laporan_reported.pk})

        # Act
        response = self.client.post(url, {"status": "VERIFIED"})

        # Assert
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_302_FOUND])
        self.laporan_reported.refresh_from_db()
        self.assertEqual(self.laporan_reported.status, "VERIFIED")

    def test_WF_04_tidak_ada_transisi_langsung_ke_resolved_dari_reported(self):
        # Arrange
        self.client.force_login(self.admin)
        url = reverse("report_detail", kwargs={"pk": self.laporan_reported.pk})

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "VERIFIED")
        self.assertNotContains(response, "RESOLVED")
        self.assertEqual(self.laporan_reported.next_status, "VERIFIED")
