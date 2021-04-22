from django.shortcuts import render
from django.views import generic

from rest_framework import viewsets
from recording.models import RecordingData
from .serializers import RecordingDataSerializer

# Create your views here.

# class IndexView(generic.ListView):
#     template_name = 'recording/index.html'
#     context_object_name = 'latest_data_list'

#     def get_queryset(self):
#         return RecordingData.objects.order_by('-video_timestamp')[:50]

# class DetailView(generic.DetailView):
#     model = RecordingData
#     template_name = 'recording/detail.html'

class RecordingDataViewSet(viewsets.ModelViewSet):
    queryset = RecordingData.objects.all().order_by('-video_timestamp')
    serializer_class = RecordingDataSerializer

