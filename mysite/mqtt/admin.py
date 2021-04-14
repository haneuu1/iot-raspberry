from django.contrib import admin
from mqtt.models import MqttData, AudioData

admin.site.register(MqttData)
admin.site.register(AudioData)
