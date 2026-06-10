from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main_app.urls")),
    path("dashboard/", include("dashboard_24782087.urls")),
    path("about/", include("about.urls")),
    path("contacts/", include("contacts.urls")),
    path("accounts/", include("usermanagement_24782087.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/auth/", include("usermanagement_24782087.api_urls")),
    path("api/", include("main_app.api_urls")),
]
