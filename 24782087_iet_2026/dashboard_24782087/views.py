from django.db.models import Count
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from main_app.models import Report


class DashboardPageView(TemplateView):
    template_name = "dashboard_24782087/dashboard.html"


class DashboardDataAPIView(View):
    def get(self, request, *args, **kwargs):
        status_labels = dict(Report.STATUS_CHOICES)
        status_counts = {
            status: 0
            for status, _label in Report.STATUS_CHOICES
        }
        status_counts.update(
            {
                item["status"]: item["total"]
                for item in Report.objects.values("status").annotate(total=Count("id"))
            }
        )

        category_counts = list(
            Report.objects.values("category")
            .annotate(total=Count("id"))
            .order_by("-total", "category")
        )

        latest_reported = list(
            Report.objects.filter(status=Report.STATUS_REPORTED)
            .order_by("-created_at")[:5]
        )
        latest_resolved = list(
            Report.objects.filter(status=Report.STATUS_RESOLVED)
            .order_by("-created_at")[:5]
        )

        def serialize_report(report):
            return {
                "id": report.id,
                "title": report.title,
                "category": report.category,
                "reporter_name": report.reporter_name,
                "location": report.location,
                "status": report.status,
                "status_display": report.get_status_display(),
                "created_at": report.created_at.strftime("%d %b %Y %H:%M"),
            }

        return JsonResponse(
            {
                "status_distribution": {
                    "labels": [label for _status, label in Report.STATUS_CHOICES],
                    "values": [status_counts[status] for status, _label in Report.STATUS_CHOICES],
                },
                "category_distribution": {
                    "labels": [item["category"] for item in category_counts],
                    "values": [item["total"] for item in category_counts],
                },
                "latest_reported": [serialize_report(report) for report in latest_reported],
                "latest_resolved": [serialize_report(report) for report in latest_resolved],
            }
        )

