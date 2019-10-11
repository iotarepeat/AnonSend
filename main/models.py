import datetime

from django.db import models

from main.helper import gen_link, gen_analytic_link


def get_today():
    """
    :return: Get current time
    """
    return datetime.datetime.now()


REPORT_CHOICES = [
    ("malicious", "Malicious file"),
    ("inappropriate", "Inappropriate / Illegal Content"),
    ("dmca", "DMCA violation"),
]

DATE_CHOICES = [
    (get_today() + datetime.timedelta(minutes=10), "10 Minutes"),
    (get_today() + datetime.timedelta(days=1), "1 Day"),
    (get_today() + datetime.timedelta(days=3), "3 Days"),
    (get_today() + datetime.timedelta(weeks=1), "1 Week"),
    (get_today() + datetime.timedelta(weeks=2), "2 Weeks"),
]


# Create your models here.
class UploadFile(models.Model):
    # Uniquely random fields
    public_link = models.CharField(max_length=15, primary_key=True, default=gen_link)
    analytic_link = models.CharField(max_length=15, unique=True, default=gen_analytic_link)

    # Form inputs
    file = models.FileField(upload_to="uploaded_files/")
    password = models.CharField(max_length=100, blank=True)
    expires_at = models.DateTimeField(verbose_name="Expires in", choices=DATE_CHOICES, default=DATE_CHOICES[0])
    max_downloads = models.PositiveSmallIntegerField(default=1, choices=[(i, i) for i in range(1, 11)])

    # Derived fields
    file_hash = models.CharField(max_length=41, )
    file_name = models.CharField(max_length=40)

    def __str__(self):
        return self.public_link

    def expiry(self):
        return self.expires_at


class Analytic(models.Model):
    upload_file = models.ForeignKey(UploadFile, on_delete=models.CASCADE)

    # From user-agent
    os = models.CharField(max_length=40, default="Unknown")
    device_type = models.CharField(max_length=40, default="Unknown")
    browser = models.CharField(max_length=40, default="Unknown")

    # From ip
    country = models.CharField(max_length=40, default="Unknown")

    time_clicked = models.DateTimeField(auto_now_add=True)


class ReportLink(models.Model):
    upload_file = models.ForeignKey(UploadFile, on_delete=models.CASCADE)
    reason = models.CharField(max_length=10, choices=REPORT_CHOICES, default=REPORT_CHOICES[0])
    description = models.TextField(max_length=150)
    report_time = models.DateTimeField(auto_now_add=True)
