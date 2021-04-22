from rest_framework import serializers
from .models import MqttData

class MqttDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MqttData
        fields = ('id', 'timestamp', 'topic', 'msg')