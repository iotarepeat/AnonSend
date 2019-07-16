from datetime import timedelta

from django.db import models


# Create your models here.
class UploadModel(models.Model):
    duration = models.DurationField(default=timedelta(minutes=10))
    file = models.FileField(upload_to="uploaded_files/")
    link = models.CharField(max_length=10, unique=True, )
    file_hash = models.CharField(max_length=41, default="")
