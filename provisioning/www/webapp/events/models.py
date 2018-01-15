from django.db import models


class Event(models.Model):
    timestamp = models.IntegerField('timestamp')
    message = models.TextField()
