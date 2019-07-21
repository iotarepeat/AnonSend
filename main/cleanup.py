import os
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AnonSend.settings")

import django

django.setup()

from main.models import UploadFiles

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_FOLDER = 'uploaded_files'
if __name__ == '__main__':
    os.chdir(PROJECT_DIR)
    query = UploadFiles.objects.filter(expires_at__gt=datetime.now())
    whiteList = {x for i in
                 list(query.values_list('file')) for x in
                 i}
    for path, folder, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            file = os.path.join(path, file)
            if file not in whiteList:
                os.remove(file)
    for folder in os.listdir(UPLOAD_FOLDER):
        folder = os.path.join(UPLOAD_FOLDER, folder)
        if not os.listdir(folder):
            os.rmdir(folder)

    UploadFiles.objects.filter(expires_at__lte=datetime.now()).delete()
