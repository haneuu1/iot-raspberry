from django.db import models

# Create your models here.

class RecordingData(models.Model):

    video_timestamp = models.DateTimeField()
    video_root = models.CharField(max_length=50)
    video_length = models.CharField(max_length=10)

    def __str__(self):
        return self.video_root