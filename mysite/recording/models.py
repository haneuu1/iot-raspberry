from django.db import models

# Create your models here.

class RecordingData(models.Model):

    video_timestamp = models.DateTimeField()
    video_root = models.CharField(max_length=50)

    def __str__(self):
        return self.video_root