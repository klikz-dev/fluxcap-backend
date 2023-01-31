from django.db import models
from django.db.models.deletion import CASCADE


class Site(models.Model):
    topic = models.CharField(primary_key=True, max_length=200)

    hostname = models.CharField(
        max_length=200, default="mqtt.cloud.pozyxlabs.com", null=True, blank=True)
    port = models.IntegerField(default="443", null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)

    floor_image = models.URLField(default=None, null=True, blank=True)
    floor_width = models.IntegerField(default=500, null=True, blank=True)
    floor_height = models.IntegerField(default=750, null=True, blank=True)
    floor_x = models.IntegerField(default=500, null=True, blank=True)
    floor_y = models.IntegerField(default=80, null=True, blank=True)
    floor_border_x = models.IntegerField(default=50, null=True, blank=True)
    floor_border_y = models.IntegerField(default=70, null=True, blank=True)
    floor_ratio = models.IntegerField(default=51, null=True, blank=True)

    alert_threshold = models.IntegerField(default=100, null=True, blank=True)

    def __str__(self):
        return self.topic


class Tag(models.Model):
    tag_id = models.CharField(primary_key=True, max_length=200)
    label = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(max_length=200, null=True, blank=True)

    x = models.IntegerField(default=0, null=True, blank=True)
    y = models.IntegerField(default=0, null=True, blank=True)
    z = models.IntegerField(default=0, null=True, blank=True)

    latency = models.IntegerField(default=0, null=True, blank=True)
    success = models.FloatField(default=0, null=True, blank=True)
    update= models.FloatField(default=0, null=True, blank=True)
    loss = models.FloatField(default=0, null=True, blank=True)
    blink_index = models.CharField(max_length=200, null=True, blank=True)

    first_seen = models.DateTimeField(auto_now_add=True, null=True)
    last_seen = models.DateTimeField(auto_now=True, null=True)

    site = models.ForeignKey(
        Site, related_name='tag', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.tag_id


class Zone(models.Model):
    zone_id = models.CharField(primary_key=True, max_length=200)
    label = models.CharField(max_length=200, null=False, blank=False)
    color = models.CharField(max_length=200, null=False, blank=False)

    site = models.ForeignKey(
        Site, related_name='zone', on_delete=models.CASCADE)

    def __str__(self):
        return self.zone_id


class Point(models.Model):
    x = models.IntegerField(default=0, null=False, blank=False)
    y = models.IntegerField(default=0, null=False, blank=False)

    zone = models.ForeignKey(Zone, related_name="point", on_delete=CASCADE)
