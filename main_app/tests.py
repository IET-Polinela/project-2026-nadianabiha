from django.test import TestCase
from django.urls import reverse

from .models import Report


class ReportCrudTests(TestCase):
    def test_home_page_shows_reports(self):
        report = Report.objects.create(
            reporter_name="Nabiha",
            title="Lampu jalan mati",
            category="Fasilitas umum",
            description="Lampu jalan di depan sekolah sudah mati selama dua hari.",
            location="Jl. Sudirman",
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, report.title)

    def test_add_report_creates_record(self):
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

        self.assertRedirects(response, reverse("home"))
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

        response = self.client.post(
            reverse("update_report", args=[report.id]),
            {
                "reporter_name": "Nabiha",
                "title": "Selokan tersumbat parah",
                "category": "Lingkungan",
                "description": "Air meluap saat hujan deras dan menutup jalan.",
                "location": "Jl. Melati",
                "status": Report.STATUS_IN_PROGRESS,
            },
        )

        report.refresh_from_db()

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(report.reporter_name, "Nabiha")
        self.assertEqual(report.title, "Selokan tersumbat parah")
        self.assertEqual(report.status, Report.STATUS_IN_PROGRESS)

    def test_delete_report_removes_record(self):
        report = Report.objects.create(
            reporter_name="Budi",
            title="Pohon tumbang",
            category="Kedaruratan",
            description="Pohon menutupi sebagian badan jalan.",
            location="Jl. Diponegoro",
        )

        response = self.client.post(reverse("delete_report", args=[report.id]))

        self.assertRedirects(response, reverse("home"))
        self.assertFalse(Report.objects.filter(id=report.id).exists())
