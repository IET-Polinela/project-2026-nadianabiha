from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("reporter_name", "title", "category", "location", "status", "Created_at")
    list_filter = ("status", "category", "Created_at")
    search_fields = ("reporter_name", "title", "category", "location")
