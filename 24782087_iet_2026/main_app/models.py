from django.db import models


class Report(models.Model):
    STATUS_REPORTED = "REPORTED"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_RESOLVED = "RESOLVED"

    reporter_name = models.CharField(max_length=100, default="Anonim")
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default=STATUS_REPORTED)
    Created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-Created_at"]

    @property
    def created_at(self):
        return self.Created_at

    def get_status_display(self):
        return self.status.replace("_", " ").title()

    def __str__(self):
        return self.title
