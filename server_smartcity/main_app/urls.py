from django.urls import path

from .views import (
    HomePageView,
    ReportCreateView,
    ReportDeleteView,
    ReportDetailView,
    ReportDetailAPIView,
    ReportListView,
    ReportSearchAPIView,
    ReportUpdateStatusView,
    ReportUpdateView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("reports/", ReportListView.as_view(), name="report_list"),
    path("reports/search/", ReportSearchAPIView.as_view(), name="report_search"),
    path("reports/<int:pk>/json/", ReportDetailAPIView.as_view(), name="report_detail_json"),
    path("reports/add/", ReportCreateView.as_view(), name="add_report"),
    path("reports/<int:pk>/", ReportDetailView.as_view(), name="report_detail"),
    path("reports/<int:pk>/edit/", ReportUpdateView.as_view(), name="update_report"),
    path("reports/<int:pk>/delete/", ReportDeleteView.as_view(), name="delete_report"),
    path("reports/<int:pk>/status/", ReportUpdateStatusView.as_view(), name="update_report_status"),
]
