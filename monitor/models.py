from settings.models import Site
from django.db import models


class Record(models.Model):
    tag_id = models.CharField(max_length=200, null=False, blank=False)
    x = models.IntegerField(null=False, blank=False)
    y = models.IntegerField(null=False, blank=False)
    z = models.IntegerField(null=False, blank=False)

    label = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(max_length=200, null=True, blank=True)

    time = models.DateTimeField(auto_now_add=True, null=True)

    site = models.ForeignKey(
        Site, related_name='record', on_delete=models.CASCADE)

    def __str__(self):
        return self.tag_id


class Alert(models.Model):
    alert_id = models.CharField(max_length=200, null=True, blank=True)
    tag1_id = models.CharField(max_length=200, null=True, blank=True)
    tag2_id = models.CharField(max_length=200, null=True, blank=True)

    start = models.DateTimeField(auto_now_add=True, null=True)
    end = models.DateTimeField(auto_now=True, null=True)

    threshold = models.IntegerField(default=0, null=True, blank=True)

    def duration(self):
        return str(self.end-self.start)
