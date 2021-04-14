from django.contrib import admin
from django.urls import path
from mjpeg.views import *

urlpatterns = [
    path('', CamView.as_view()),
    path('stream/', mjpeg_stream, name='stream'),
    ]