import datetime

from django.db import models

from main.helper import gen_link, gen_analytic_link


def get_today():
    """
    :return: Get current time and offset by 10 Minutes
    """
    return datetime.datetime.now() + datetime.timedelta(minutes=10)


DATE_CHOICES = [
    (get_today(), "10 Minutes"),
    (get_today() + datetime.timedelta(days=1), "1 Day"),
    (get_today() + datetime.timedelta(days=3), "3 Days"),
    (get_today() + datetime.timedelta(weeks=1), "1 Week"),
    (get_today() + datetime.timedelta(weeks=2), "2 Weeks"),

]


# Create your models here.
class UploadFiles(models.Model):
    # Uniquely random fields
    public_link = models.CharField(max_length=15, primary_key=True, default=gen_link)
    analytic_link = models.CharField(max_length=15, unique=True, default=gen_analytic_link)

    # Form inputs
    file = models.FileField(upload_to="uploaded_files/")
    password = models.CharField(max_length=41, blank=True)
    expires_at = models.DateTimeField(verbose_name="Expires in", choices=DATE_CHOICES, default=DATE_CHOICES[0])
    max_downloads = models.PositiveSmallIntegerField(default=1, choices=[(i, i) for i in range(1, 11)])

    # Derived fields
    file_hash = models.CharField(max_length=41, )
    file_name = models.CharField(max_length=40)


class Analytics(models.Model):
    upload_file = models.ForeignKey(UploadFiles, on_delete=models.CASCADE)

    # From user-agent
    os = models.CharField(max_length=40, default="Unknown")
    device_type = models.CharField(max_length=40, default="Unknown")
    browser = models.CharField(max_length=40, default="Unknown")

    # From ip
    country = models.CharField(max_length=40, default="Unknown")
    region = models.CharField(max_length=40, default="Unknown")
    city = models.CharField(max_length=40, default="Unknown")

    time_clicked = models.DateTimeField(auto_now_add=True)
