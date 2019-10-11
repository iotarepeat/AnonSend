# Register your models here.
from django.contrib import admin

from .models import UploadFile, Analytic, ReportLink


@admin.register(UploadFile)
class UploadFilesAdmin(admin.ModelAdmin):
    list_display = ('public_link', 'analytic_link', 'file_name', 'expiry')


@admin.register(Analytic)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ('upload_file', 'country', 'time_clicked')


@admin.register(ReportLink)
class ReportLinksAdmin(admin.ModelAdmin):
    list_display = ('upload_file', 'reason', 'report_time')
