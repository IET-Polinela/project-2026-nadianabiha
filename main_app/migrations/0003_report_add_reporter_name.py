from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0002_align_report_model_with_lab_instructions"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="reporter_name",
            field=models.CharField(default="Anonim", max_length=100),
        ),
    ]
