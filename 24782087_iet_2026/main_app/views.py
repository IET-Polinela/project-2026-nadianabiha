from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReportForm, ReportUpdateForm
from .models import Report


def home(request):
    reports = Report.objects.all()
    return render(request, "main_app/home.html", {"reports": reports})


def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ReportForm()

    context = {
        "form": form,
        "page_title": "Tambah Laporan",
        "heading": "Tambah Laporan",
        "submit_label": "Simpan",
    }
    return render(request, "main_app/add_report.html", context)


def update_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)

    if request.method == "POST":
        form = ReportUpdateForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ReportUpdateForm(instance=report)

    context = {
        "form": form,
        "report": report,
        "page_title": "Ubah Laporan",
        "heading": "Ubah Laporan",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "main_app/add_report.html", context)


def delete_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)

    if request.method == "POST":
        report.delete()
        return redirect("home")

    return render(request, "main_app/delete_confirm.html", {"report": report})
