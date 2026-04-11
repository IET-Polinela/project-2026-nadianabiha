from django import forms

from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reporter_name", "title", "category", "description", "location"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["reporter_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Masukkan nama pelapor"}
        )
        self.fields["title"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Masukkan judul laporan"}
        )
        self.fields["category"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Contoh: Jalan rusak"}
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "rows": 5,
                "placeholder": "Jelaskan permasalahan yang ingin dilaporkan",
            }
        )
        self.fields["location"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Masukkan lokasi kejadian"}
        )


class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reporter_name", "title", "category", "description", "location"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["reporter_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Masukkan nama pelapor"}
        )
        self.fields["title"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Masukkan judul laporan"}
        )
        self.fields["category"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Contoh: Jalan rusak"}
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "rows": 5,
                "placeholder": "Jelaskan permasalahan yang ingin dilaporkan",
            }
        )
        self.fields["location"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Masukkan lokasi kejadian"}
        )
