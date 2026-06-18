from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_spectacular_scalar.views import SpectacularScalarView
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_scalar.views import scalar_viewer


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main_app.urls")),
    path("dashboard/", include("dashboard_24782087.urls")),
    path("about/", include("about.urls")),
    path("contacts/", include("contacts.urls")),
    path("accounts/", include("usermanagement_24782087.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/scalar/', scalar_viewer, name='scalar-ui'),
    path("api/auth/", include("usermanagement_24782087.api_urls")),
    path("api/", include("main_app.api_urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/scalar/', SpectacularScalarView.as_view(url_name='schema'), name='scalar'),
]
