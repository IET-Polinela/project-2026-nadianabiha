from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0003_report_add_reporter_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="report",
            old_name="Created_at",
            new_name="created_at",
        ),
        migrations.AlterField(
            model_name="report",
            name="status",
            field=models.CharField(
                choices=[
                    ("REPORTED", "Reported"),
                    ("VERIFIED", "Verified"),
                    ("IN_PROGRESS", "In Progress"),
                    ("RESOLVED", "Resolved"),
                ],
                default="REPORTED",
                max_length=20,
            ),
        ),
        migrations.AlterModelOptions(
            name="report",
            options={"ordering": ["-created_at"]},
        ),
    ]
