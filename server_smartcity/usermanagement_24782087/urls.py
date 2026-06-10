from django.urls import path

from .views import CitizenRegisterView, UserLoginView, UserLogoutView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", CitizenRegisterView.as_view(), name="register"),
]
