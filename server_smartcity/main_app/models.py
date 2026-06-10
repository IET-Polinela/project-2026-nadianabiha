from django.conf import settings
from django.db import models


STATUS_CHOICES = [
    ('DRAFT', 'Draft'),
    ('REPORTED', 'Reported'),
    ('VERIFIED', 'Verified'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
]


class Report(models.Model):
    STATUS_REPORTED = "REPORTED"
    STATUS_VERIFIED = "VERIFIED"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_RESOLVED = "RESOLVED"
    STATUS_CHOICES = STATUS_CHOICES
    STATUS_TRANSITIONS = {
        STATUS_REPORTED: STATUS_VERIFIED,
        STATUS_VERIFIED: STATUS_IN_PROGRESS,
        STATUS_IN_PROGRESS: STATUS_RESOLVED,
    }

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True,
    )
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
    updated_at = models.DateTimeField(auto_now=True)

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

    @property
    def status_badge_class(self):
        return {
            self.STATUS_REPORTED: "secondary",
            self.STATUS_VERIFIED: "primary",
            self.STATUS_IN_PROGRESS: "warning",
            self.STATUS_RESOLVED: "success",
        }.get(self.status, "secondary")

    @property
    def next_status_button_class(self):
        return {
            self.STATUS_VERIFIED: "btn-primary",
            self.STATUS_IN_PROGRESS: "btn-warning",
            self.STATUS_RESOLVED: "btn-success",
        }.get(self.next_status, "btn-secondary")

    @property
    def is_resolved(self):
        return self.status == self.STATUS_RESOLVED

    def __str__(self):
        return self.title
