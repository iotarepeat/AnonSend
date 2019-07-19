from collections import Counter
from datetime import datetime

from django.http import FileResponse, Http404
from django.shortcuts import render, redirect

from .forms import UploadFileForm
from .helper import get_hash, get_analytics
from .models import UploadFiles, Analytics


# Create your views here.
def index(request):
    return render(request, 'index.html', {"form": UploadFileForm()})


def uploaded_link(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            # TODO: Zip Archive multiple files
            for file in request.FILES.getlist('file'):
                model = UploadFiles(file=file, file_name=file.name, file_hash=get_hash(file),
                                    expires_at=form.cleaned_data['expires_at'],
                                    max_downloads=form.cleaned_data['max_downloads'])
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
                # noinspection PyArgumentList,PyArgumentList
                model.save()
            # noinspection PyUnboundLocalVariable
            return render(request, 'upload_success.html',
                          {"public_link": model.public_link, "analytic_link": model.analytic_link})
        else:
            # Form is invalid
            return redirect(index)

    else:
        # Request is not post
        return redirect(index)


def public_link_handle(request, public_link):
    query = UploadFiles.objects.all().filter(public_link=public_link)
    if query.exists():
        upload_file = query.first()
        if len(Analytics.objects.filter(
                upload_file=upload_file)) < upload_file.max_downloads and upload_file.expires_at.timestamp() > datetime.now().timestamp():
            results = get_analytics(request)
            Analytics(upload_file_id=public_link, **results).save()
            # TODO: Add password support
            return FileResponse(query.first().file, as_attachment=True, filename=query.first().file_name)
        else:
            raise Http404()
    else:
        raise Http404()


def analytic_link_handle(request, analytic_link):
    query = UploadFiles.objects.all().filter(analytic_link=analytic_link)
    if query.exists():
        if query.first().expires_at.timestamp() > datetime.now().timestamp():
            results = Analytics.objects.filter(upload_file=query.first())
            chart_data = {}
            chart_attributes = ['os', 'device_type', 'browser']
            for data in chart_attributes:
                chart_data[data] = Counter([i[0] for i in list(results.values_list(data))]).items()
            detailed = list(
                results.values_list('os', 'device_type', 'browser', 'country', 'region', 'city', 'time_clicked'))
            return render(request, 'analytics.html', {"chart_data": chart_data, "detailed": detailed})
        else:
            raise Http404()
    else:
        raise Http404()
