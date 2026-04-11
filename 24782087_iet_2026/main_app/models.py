from django.db import models


class Report(models.Model):
    STATUS_REPORTED = "REPORTED"
    STATUS_VERIFIED = "VERIFIED"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_RESOLVED = "RESOLVED"
    STATUS_CHOICES = [
        (STATUS_REPORTED, "Reported"),
        (STATUS_VERIFIED, "Verified"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_RESOLVED, "Resolved"),
    ]
    STATUS_TRANSITIONS = {
        STATUS_REPORTED: STATUS_VERIFIED,
        STATUS_VERIFIED: STATUS_IN_PROGRESS,
        STATUS_IN_PROGRESS: STATUS_RESOLVED,
    }

    reporter_name = models.CharField(max_length=100, default="Anonim")
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_REPORTED,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def next_status(self):
        return self.STATUS_TRANSITIONS.get(self.status)

    @property
    def next_status_label(self):
        if not self.next_status:
            return ""
        return dict(self.STATUS_CHOICES)[self.next_status]

    def __str__(self):
        return self.title
