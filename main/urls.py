from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('upload_success', views.uploaded_link, name="upload_success"),
    path('<public_link>', views.public_link_handle, name="public_link"),
    path('analytics/<analytic_link>', views.analytic_link_handle, name="analytic_link"),
    path('csv/<analytic_link>', views.downloadAsCsv, name="download_csv"),
]
