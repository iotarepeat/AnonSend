# Register your models here.
from django.contrib.admin import AdminSite

from .models import UploadFiles, Analytics


class MyAdminSite(AdminSite):
    site_header = 'AnonSend Administration'


admin_site = MyAdminSite(name='admin_site')
admin_site.register(UploadFiles)
admin_site.register(Analytics)
