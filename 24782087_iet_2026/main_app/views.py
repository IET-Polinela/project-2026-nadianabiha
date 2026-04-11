from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ReportForm, ReportUpdateForm
from .models import Report


class ReportListView(ListView):
    model = Report
    template_name = "main_app/home.html"
    context_object_name = "reports"


class ReportDetailView(DetailView):
    model = Report
    template_name = "main_app/report_detail.html"
    context_object_name = "report"
    pk_url_kwarg = "pk"


class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = "main_app/add_report.html"
    success_url = reverse_lazy("report_list")
    extra_context = {
        "page_title": "Tambah Laporan",
        "heading": "Tambah Laporan",
        "submit_label": "Simpan",
    }


class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportUpdateForm
    template_name = "main_app/add_report.html"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("report_list")
    extra_context = {
        "page_title": "Ubah Laporan",
        "heading": "Ubah Laporan",
        "submit_label": "Simpan Perubahan",
    }


class ReportDeleteView(DeleteView):
    model = Report
    template_name = "main_app/delete_confirm.html"
    context_object_name = "report"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("report_list")


class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get("status")

        if new_status == report.next_status:
            report.status = new_status
            report.save(update_fields=["status"])

        return redirect("report_list")
