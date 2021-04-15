from django.shortcuts import render
from django.views import generic
from recording.models import RecordingData

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'recording/index.html'
    context_object_name = 'latest_data_list'

    def get_queryset(self):
        return RecordingData.objects.order_by('-video_timestamp')[:50]

class DetailView(generic.DetailView):
    model = RecordingData
    template_name = 'recording/detail.html'
