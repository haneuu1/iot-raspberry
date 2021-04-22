from django.shortcuts import render
from django.views import generic

from rest_framework import viewsets
from mqtt.models import MqttData
from .serializers import MqttDataSerializer
# from DAO import DataDAO

# Create your views here.

# class IndexView(generic.ListView):
#     template_name = 'mqtt/index.html'
#     context_object_name = 'latest_data_list'

#     def get_queryset(self):
#         return MqttData.objects.order_by('-timestamp')[:50]

# class DetailView(generic.DetailView):
#     model = MqttData
#     template_name = 'mqtt/detail.html'


# def log(request):    
#     dao = DataDAO()
#     log = dao.get_db_data('iot/monitor/pir')[:5]

#     for i in log:

#     return JsonResponse(dao.get_db_data('iot/monitor/pir')[:5])# list로 연결. [0]: 가장 최근
#     # return HttpResponse(dao.get_db_data('iot/control/key'))


class MqttDataViewSet(viewsets.ModelViewSet):
    queryset = MqttData.objects.all().order_by('-timestamp')
    serializer_class = MqttDataSerializer

