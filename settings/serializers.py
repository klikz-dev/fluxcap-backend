from django.db.models import fields
from monitor.models import Alert, Record
from settings.models import Site, Tag, Zone, Point
from rest_framework import serializers


class PointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['x', 'y']


class PointRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['x', 'y']


class ZoneListSerializer(serializers.ModelSerializer):
    point = PointListSerializer(many=True, read_only=True)

    class Meta:
        model = Zone
        fields = ['url', 'zone_id', 'label', 'color', 'point']


class ZoneRetrieveSerializer(serializers.ModelSerializer):
    point = PointListSerializer(many=True, read_only=True)

    class Meta:
        model = Zone
        fields = ['url', 'zone_id', 'label', 'color',
                  'x', 'y', 'z', 'point']


class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'tag_id', 'label', 'color',
                  'x', 'y', 'z', 'latency', 'success', 'update', 'loss', 'blink_index', 'site']


class TagRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['url', 'tag_id', 'label', 'color', 'site']


class SiteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['url', 'hostname', 'port', 'username', 'password', 'topic', 'floor_image', 'floor_width',
                  'floor_height', 'floor_x', 'floor_y', 'floor_border_x', 'floor_border_y', 'floor_ratio', 'alert_threshold']


class SiteRetrieveSerializer(serializers.ModelSerializer):
    tag = TagListSerializer(many=True, read_only=True)
    zone = ZoneListSerializer(many=True, read_only=True)

    class Meta:
        model = Site
        fields = ['url', 'hostname', 'port', 'username', 'password', 'topic', 'floor_image', 'floor_width', 'floor_height',
                  'floor_x', 'floor_y', 'floor_border_x', 'floor_border_y', 'floor_ratio', 'alert_threshold', 'tag', 'zone']


class RecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['tag_id', 'x', 'y', 'z', 'time']


class AlertListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['tag1_id', 'tag2_id', 'start', 'end', 'threshold']
