import datetime
from django.db import models


class MqttData(models.Model):
    def __str__(self):
        return f"topic : {self.topic}, msg: {self.msg}, time: {self.timestamp}"

    timestamp = models.DateTimeField(auto_now = True)
    topic = models.CharField(max_length = 50)
    msg = models.CharField(max_length = 100)