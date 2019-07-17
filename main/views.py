from django.http import HttpResponse
from django.shortcuts import render

from .forms import UploadFileForm
from .helper import gen_link, gen_analytic_link, get_hash
from .models import UploadFiles


# Create your views here.
def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            # TODO: Zip Archive multiple files
            for file in request.FILES.getlist('file'):
                model = UploadFiles(file=file, file_name=file.name, file_hash=get_hash(file), public_link=gen_link(),
                                    analytic_link=gen_analytic_link()
                                    , expires_at=form.cleaned_data['expires_at'])

                # Check for same file with hash
                query_set = UploadFiles.objects.all().filter(file_hash=model.file_hash)
                if query_set.exists():
                    model.file = query_set.first().file
                else:
                    name = file.name
                    name = name.split("/")
                    name.insert(0, model.file_hash)
                    name = "/".join(name)
                    model.file.save(name, file)
            ls = "Public: " + model.public_link + "\n Analytic link: " + model.analytic_link
            model.save()
            return HttpResponse(ls)
    else:
        form = UploadFileForm()
        return render(request, 'index.html', {"form": form})
