from datetime import datetime

from django.http import FileResponse, Http404
from django.shortcuts import render, redirect

from .forms import UploadFileForm
from .helper import gen_link, gen_analytic_link, get_hash
from .models import UploadFiles


# Create your views here.
def index(request):
    return render(request, 'index.html', {"form": UploadFileForm()})


def uploaded_link(request):
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
                model.save()
            return render(request, 'upload_success.html',
                          {"public_link": model.public_link, "analytic_link": model.analytic_link})
        else:
            # Form is invalid
            raise Http404()
    else:
        # Request is not post
        redirect('')


def public_link_handle(request, public_link):
    query = UploadFiles.objects.all().filter(public_link=public_link)
    if query.exists():
        if query.first().expires_at.timestamp() > datetime.now().timestamp():
            return FileResponse(query.first().file, as_attachment=True)
        else:
            raise Http404()
    else:
        raise Http404()
