from django.http import HttpResponse
from django.shortcuts import render

from .forms import uploadFileForm
from .models import uploadModel


# Create your views here.
def index(request):
    if request.method == "POST":
        form = uploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            model = uploadModel()
            for file in request.FILES.getlist('file'):
                model.file = file
                model.file.save(file.name, file)
            model.save()
            return HttpResponse("Uploaded")
    else:
        form = uploadFileForm()
        return render(request, 'index.html', {"form": form})
