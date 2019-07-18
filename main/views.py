from django.http import HttpResponse
from django.shortcuts import render

from main.helper import get_hash, gen_link
from .forms import UploadFileForm
from .models import UploadModel
from django.views.generic import View


# Create your views here.
def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            link = "Not Found"
            # TODO: Zip Archive multiple files
            for file in request.FILES.getlist('file'):
                model = UploadModel(file=file, file_hash=get_hash(file), link=gen_link())
                while UploadModel.objects.all().filter(link__exact=model.link).first() is not None:
                    model.link = gen_link()
                link = model.link
                model.file.save(file.name, file)
                model.save()
            return HttpResponse("Uploaded " + link)
    else:
        form = UploadFileForm()
        return render(request, 'index.html', {"form": form})

def upload(request):
        return render(request, "upload.html")