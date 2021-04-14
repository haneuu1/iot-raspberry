from django.shortcuts import render
from django.views import generic
from mqtt.models import MqttData

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'mqtt/index.html'
    context_object_name = 'latest_data_list'

    def get_queryset(self):
        return MqttData.objects.order_by('-timestamp')[:50]

class DetailView(generic.DetailView):
    model = MqttData
    template_name = 'mqtt/detail.html'