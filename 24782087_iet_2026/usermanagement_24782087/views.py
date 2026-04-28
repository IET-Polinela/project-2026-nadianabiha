from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import BootstrapAuthenticationForm, CitizenRegistrationForm


class UserLoginView(LoginView):
    template_name = "usermanagement_24782087/login.html"
    authentication_form = BootstrapAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Berhasil login.")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Berhasil logout.")
        return super().dispatch(request, *args, **kwargs)


class CitizenRegisterView(CreateView):
    form_class = CitizenRegistrationForm
    template_name = "usermanagement_24782087/register.html"
    success_url = reverse_lazy("report_list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Anda sudah login.")
            return redirect("report_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Registrasi berhasil. Selamat datang.")
        return response
