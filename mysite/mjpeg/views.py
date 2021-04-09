from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponse, StreamingHttpResponse, Http404
from picam import MJpegStreamCam

mjpegstream = MJpegStreamCam()
class CamView(TemplateView):
    template_name = "cam.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["mode"] = self.request.GET.get("mode", "#")
        return context

    def motion_detected(request):
        image = mjpegstream.motion_detected()
        return HttpResponse(image, content_type ="image/.h264")

    def mjpeg_stream(request):
        return StreamingHttpResponse(mjpegstream,
        content_type='multipart/x-mixed-replace;boundary=--myboundary')
