from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url
from . import views

urlpatterns = [path('', views.index, name="index"),
               path('upload.html', views.upload, name='upload')]
