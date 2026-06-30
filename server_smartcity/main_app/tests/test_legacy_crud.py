from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from main_app.models import Report


class ReportCrudTests(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(
            username="admin_test",
            password="AdminPass123!",
            is_admin=True,
            is_staff=True,
        )

    def login_admin(self):
        self.client.login(username="admin_test", password="AdminPass123!")

    def test_report_list_page_shows_reports(self):
        report = Report.objects.create(
            reporter_name="Nabiha",
            title="Lampu jalan mati",
            category="Fasilitas umum",
            description="Lampu jalan di depan sekolah sudah mati selama dua hari.",
            location="Jl. Sudirman",
        )

        self.login_admin()
        response = self.client.get(reverse("report_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, report.title)

    def test_add_report_creates_record(self):
        self.login_admin()
        response = self.client.post(
            reverse("add_report"),
            {
                "reporter_name": "Nabiha",
                "title": "Jalan berlubang",
                "category": "Infrastruktur",
                "description": "Ada lubang besar yang membahayakan pengendara.",
                "location": "Jl. Pahlawan",
            },
        )

        self.assertRedirects(response, reverse("report_list"))
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(Report.objects.get().reporter_name, "Nabiha")

    def test_update_report_changes_fields(self):
        report = Report.objects.create(
            reporter_name="Anita",
            title="Selokan tersumbat",
            category="Lingkungan",
            description="Air meluap saat hujan deras.",
            location="Jl. Melati",
        )

        self.login_admin()
        response = self.client.post(
            reverse("update_report", args=[report.id]),
            {
                "reporter_name": "Nabiha",
                "title": "Selokan tersumbat parah",
                "category": "Lingkungan",
                "description": "Air meluap saat hujan deras dan menutup jalan.",
                "location": "Jl. Melati",
            },
        )

        report.refresh_from_db()

        self.assertRedirects(response, reverse("report_list"))
        self.assertEqual(report.reporter_name, "Nabiha")
        self.assertEqual(report.title, "Selokan tersumbat parah")
        self.assertEqual(report.status, Report.STATUS_REPORTED)

    def test_delete_report_removes_record(self):
        report = Report.objects.create(
            reporter_name="Budi",
            title="Pohon tumbang",
            category="Kedaruratan",
            description="Pohon menutupi sebagian badan jalan.",
            location="Jl. Diponegoro",
        )

        self.login_admin()
        response = self.client.post(reverse("delete_report", args=[report.id]))

        self.assertRedirects(response, reverse("report_list"))
        self.assertFalse(Report.objects.filter(id=report.id).exists())

    def test_update_status_advances_workflow(self):
        report = Report.objects.create(
            reporter_name="Sari",
            title="Lampu taman mati",
            category="Fasilitas umum",
            description="Lampu taman padam total.",
            location="Taman Kota",
        )

        self.login_admin()
        response = self.client.post(
            reverse("update_report_status", args=[report.id]),
            {"status": Report.STATUS_VERIFIED},
        )

        report.refresh_from_db()

        self.assertRedirects(response, reverse("report_list"))
        self.assertEqual(report.status, Report.STATUS_VERIFIED)
