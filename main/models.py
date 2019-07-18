import datetime

from django.db import models

from main.helper import gen_link, gen_analytic_link


def get_today():
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
    expires_at = models.DateTimeField(verbose_name="Expires in", choices=DATE_CHOICES, default=get_today)
    file = models.FileField(upload_to="uploaded_files/")
    public_link = models.CharField(max_length=15, unique=True, primary_key=True, default=gen_link)
    analytic_link = models.CharField(max_length=15, default=gen_analytic_link)
    password = models.CharField(max_length=41, blank=True)
    file_hash = models.CharField(max_length=41, )
    file_name = models.CharField(max_length=40)
