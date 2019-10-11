import os
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AnonSend.settings")

import django

django.setup()

from main.models import UploadFile

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_FOLDER = 'uploaded_files'
if __name__ == '__main__':
    """
        Intended to run at scheduled intervals by the OS
        Removes unnecessary links in database:
            - Links are removed on blackList basis
            - All links with expiry < current_time are deleted
        Remove unnecessary files and directories:
            - Directories are deleted on whitelist basis
            - All files that are currently active (expiry >= current time) are whitelisted
            - Remaining files are deleted
            - Finally delete all empty directories
            
    """
    os.chdir(PROJECT_DIR)
    query = UploadFile.objects.filter(expires_at__gte=datetime.now())
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

    UploadFile.objects.filter(expires_at__lte=datetime.now()).delete()
