from django.db import models

# Create your models here.
class uploadModel(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="uploaded_files/")
