from django.urls import path

from .views import (
    ReportCreateView,
    ReportDeleteView,
    ReportDetailView,
    ReportListView,
    ReportUpdateStatusView,
    ReportUpdateView,
)

urlpatterns = [
    path("", ReportListView.as_view(), name="report_list"),
    path("reports/add/", ReportCreateView.as_view(), name="add_report"),
    path("reports/<int:pk>/", ReportDetailView.as_view(), name="report_detail"),
    path("reports/<int:pk>/edit/", ReportUpdateView.as_view(), name="update_report"),
    path("reports/<int:pk>/delete/", ReportDeleteView.as_view(), name="delete_report"),
    path("reports/<int:pk>/status/", ReportUpdateStatusView.as_view(), name="update_report_status"),
]
