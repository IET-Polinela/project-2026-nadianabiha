from django.urls import path

from .views import DashboardDataAPIView, DashboardPageView


urlpatterns = [
    path("", DashboardPageView.as_view(), name="dashboard"),
    path("data/", DashboardDataAPIView.as_view(), name="dashboard_data"),
]

