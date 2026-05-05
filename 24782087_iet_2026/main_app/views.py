from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ReportForm, ReportUpdateForm
from .models import Report


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, "is_admin", False):
            messages.error(request, "Akses Ditolak. Fitur ini hanya untuk admin.")
            return redirect("report_list")
        return super().dispatch(request, *args, **kwargs)


class HomePageView(TemplateView):
    template_name = "main_app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reports = Report.objects.all()
        context["total_reports"] = reports.count()
        context["reported_count"] = reports.filter(status=Report.STATUS_REPORTED).count()
        context["resolved_count"] = reports.filter(status=Report.STATUS_RESOLVED).count()
        context["latest_reports"] = reports[:3]
        return context


class ReportListView(ListView):
    model = Report
    template_name = "main_app/report_page.html"
    context_object_name = "reports"


class ReportSearchAPIView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip()
        reports = Report.objects.all()

        if query:
            reports = reports.filter(
                Q(title__icontains=query)
                | Q(category__icontains=query)
                | Q(location__icontains=query)
                | Q(reporter_name__icontains=query)
                | Q(description__icontains=query)
            )

        reports = reports[:50]
        is_admin = request.user.is_authenticated and getattr(request.user, "is_admin", False)

        return JsonResponse(
            {
                "query": query,
                "is_admin": is_admin,
                "reports": [
                    {
                        "id": report.id,
                        "title": report.title,
                        "category": report.category,
                        "reporter_name": report.reporter_name,
                        "location": report.location,
                        "description": report.description,
                        "status": report.status,
                        "status_display": report.get_status_display(),
                        "status_badge_class": report.status_badge_class,
                        "next_status": report.next_status,
                        "next_status_label": report.next_status_label,
                        "next_status_button_class": report.next_status_button_class,
                        "detail_url": reverse("report_detail", kwargs={"pk": report.pk}),
                        "edit_url": reverse("update_report", kwargs={"pk": report.pk}),
                        "delete_url": reverse("delete_report", kwargs={"pk": report.pk}),
                        "status_url": reverse("update_report_status", kwargs={"pk": report.pk}),
                    }
                    for report in reports
                ],
            }
        )


class ReportDetailAPIView(View):
    def get(self, request, pk, *args, **kwargs):
        report = get_object_or_404(Report, pk=pk)
        return JsonResponse(
            {
                "id": report.id,
                "title": report.title,
                "category": report.category,
                "reporter_name": report.reporter_name,
                "location": report.location,
                "description": report.description,
                "status": report.status,
                "status_display": report.get_status_display(),
                "status_badge_class": report.status_badge_class,
                "created_at": report.created_at.strftime("%d %B %Y %H:%M"),
            }
        )


class ReportDetailView(DetailView):
    model = Report
    template_name = "main_app/report_detail.html"
    context_object_name = "report"
    pk_url_kwarg = "pk"


class ReportCreateView(AdminRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = "main_app/add_report.html"
    success_url = reverse_lazy("report_list")
    extra_context = {
        "page_title": "Tambah Laporan",
        "heading": "Tambah Laporan",
        "submit_label": "Submit",
    }

    def form_valid(self, form):
        messages.success(self.request, "Laporan baru berhasil ditambahkan.")
        return super().form_valid(form)


class ReportUpdateView(AdminRequiredMixin, UpdateView):
    model = Report
    form_class = ReportUpdateForm
    template_name = "main_app/add_report.html"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("report_list")
    extra_context = {
        "page_title": "Ubah Laporan",
        "heading": "Ubah Laporan",
        "submit_label": "Update",
    }

    def form_valid(self, form):
        messages.success(self.request, "Data laporan berhasil diperbarui.")
        return super().form_valid(form)


class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = "main_app/delete_confirm.html"
    context_object_name = "report"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("report_list")

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil dihapus.")
        return super().form_valid(form)


class ReportUpdateStatusView(AdminRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get("status")

        if new_status == report.next_status:
            report.status = new_status
            report.save(update_fields=["status"])
            messages.success(request, f"Status laporan berhasil diubah menjadi {report.get_status_display()}.")
        else:
            messages.error(request, "Perubahan status tidak sesuai alur workflow.")

        return redirect("report_list")
