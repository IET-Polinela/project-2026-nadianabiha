from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="report",
            old_name="created_at",
            new_name="Created_at",
        ),
        migrations.AlterField(
            model_name="report",
            name="status",
            field=models.CharField(default="REPORTED", max_length=20),
        ),
        migrations.AlterModelOptions(
            name="report",
            options={"ordering": ["-Created_at"]},
        ),
    ]
