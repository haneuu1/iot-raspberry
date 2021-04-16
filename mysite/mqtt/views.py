from django.shortcuts import render
from django.views import generic
from mqtt.models import MqttData
from django.http import HttpResponse
from DAO import DataDAO

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'mqtt/index.html'
    context_object_name = 'latest_data_list'

    def get_queryset(self):
        return MqttData.objects.order_by('-timestamp')[:50]

class DetailView(generic.DetailView):
    model = MqttData
    template_name = 'mqtt/detail.html'


def log(request):    
    dao = DataDAO() 
    return HttpResponse(dao.get_db_data('iot/control/voice')[:5])# list로 연결. [0]: 가장 최근
    # return HttpResponse(dao.get_db_data('iot/control/key'))
