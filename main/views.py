from django.http import HttpResponse
from django.shortcuts import render

from .forms import uploadFileForm


# Create your views here.
def index(request):
    if request.method == "POST":
        form = uploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Uploaded")
    else:
        form = uploadFileForm()
        return render(request, 'index.html', {"form": form})
