from django.shortcuts import render
from django.views import generic
from mqtt.models import MqttData
from django.http import HttpResponse, JsonResponse
from django.core import serializers
# from DAO import DataDAO

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'mqtt/index.html'
    context_object_name = 'latest_data_list'

    def get_queryset(self):
        return MqttData.objects.order_by('-timestamp')[:50]

class DetailView(generic.DetailView):
    model = MqttData
    template_name = 'mqtt/detail.html'


# def log(request):    
#     dao = DataDAO()
#     log = dao.get_db_data('iot/monitor/pir')[:5]

#     for i in log:

#     return JsonResponse(dao.get_db_data('iot/monitor/pir')[:5])# list로 연결. [0]: 가장 최근
#     # return HttpResponse(dao.get_db_data('iot/control/key'))

def log(request):
    mqttdatas = MqttData.objects.filter(topic='iot/monitor/pir')
    mqttdata_list = serializers.serialize('json', mqttdatas, fields=('timestamp', 'msg'))
    return HttpResponse(mqttdata_list, content_type="application/json")


    # [{"model": "mqtt.mqttdata", "pk": 4032, "fields": {"timestamp": "2021-04-19T14:26:43Z", "topic": "iot/monitor/pir", "msg": "on"}}, {"model": "mqtt.mqttdata", "pk": 4033, "fields": {"timestamp": "2021-04-19T14:26:48Z", "topic": "iot/monitor/pir", "msg": "on"}}]

    # [{"model": "mqtt.mqttdata", "pk": 4032, "fields": {"timestamp": "2021-04-19T14:26:43Z", "msg": "on"}}, {"model": "mqtt.mqttdata", "pk": 4033, "fields": {"timestamp": "2021-04-19T14:26:48Z", "msg": "on"}}, {"model": "mqtt.mqttdata", "pk": 4034, "fields": {"timestamp": "2021-04-19T14:26:54Z", "msg": "on"}}, {"model": "mqtt.mqttdata", "pk": 4035, "fields": {"timestamp": "2021-04-19T14:26:59Z", "msg": "off"}}, {"model": "mqtt.mqttdata", "pk": 4036, "fields": {"timestamp": "2021-04-19T14:27:00Z", "msg": "on"}}, {"model": "mqtt.mqttdata", "pk": 4037, "fields": {"timestamp": "2021-04-19T14:27:05Z", "msg": "off"}}, {"model": "mqtt.mqttdata", "pk": 4038, "fields": {"timestamp": "2021-04-19T14:35:37Z", "msg": "off"}}, {"model": "mqtt.mqttdata", "pk": 4039, "fields": {"timestamp": "2021-04-19T14:35:38Z", "msg": "off"}}, {"model": "mqtt.mqttdata", "pk": 4040, "fields": {"timestamp": "2021-04-19T14:35:39Z", "msg": "on"}}]