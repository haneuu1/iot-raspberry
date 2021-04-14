from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponse, StreamingHttpResponse, Http404

import threading
import time

from mysite.picam import MJpegStreamCam
from mysite.pir_sensor import pir

mjpegstream = MJpegStreamCam(pir.camera)

class CamView(TemplateView):
    template_name = "cam.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["mode"] = self.request.GET.get("mode", "#")
        return context

def mjpeg_stream(request):
    time.sleep(0.2)

    return StreamingHttpResponse(mjpegstream, content_type='multipart/x-mixed-replace;boundary=--myboundary')
