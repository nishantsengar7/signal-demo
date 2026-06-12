from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'demo'

    def __str__(self):
        return self.name


class LogEntry(models.Model):
    message = models.CharField(max_length=200)

    class Meta:
        app_label = 'demo'

    def __str__(self):
        return self.message
