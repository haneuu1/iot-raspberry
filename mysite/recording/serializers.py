from rest_framework import serializers
from .models import RecordingData

class RecordingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingData
        fields = ('id', 'video_timestamp', 'video_root', 'video_length')