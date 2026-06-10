from django import forms

from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reporter_name", "title", "category", "description", "location"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["reporter_name"].widget.attrs["placeholder"] = "Masukkan nama pelapor"
        self.fields["title"].widget.attrs["placeholder"] = "Masukkan judul laporan"
        self.fields["category"].widget.attrs["placeholder"] = "Contoh: Jalan rusak"
        self.fields["description"].widget.attrs.update(
            {"rows": 5, "placeholder": "Jelaskan permasalahan yang ingin dilaporkan"}
        )
        self.fields["location"].widget.attrs["placeholder"] = "Masukkan lokasi kejadian"


class ReportUpdateForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["reporter_name", "title", "category", "description", "location"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["reporter_name"].widget.attrs["placeholder"] = "Masukkan nama pelapor"
        self.fields["title"].widget.attrs["placeholder"] = "Masukkan judul laporan"
        self.fields["category"].widget.attrs["placeholder"] = "Contoh: Jalan rusak"
        self.fields["description"].widget.attrs.update(
            {"rows": 5, "placeholder": "Jelaskan permasalahan yang ingin dilaporkan"}
        )
        self.fields["location"].widget.attrs["placeholder"] = "Masukkan lokasi kejadian"
