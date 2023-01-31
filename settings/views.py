from monitor.models import Alert, Record
from settings.serializers import AlertListSerializer, PointListSerializer, PointRetrieveSerializer, RecordListSerializer, SiteListSerializer, SiteRetrieveSerializer, TagListSerializer, TagRetrieveSerializer, ZoneListSerializer, ZoneRetrieveSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from settings.models import Site, Tag, Zone, Point

from datetime import datetime


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteListSerializer

    def list(self, request):
        sites = Site.objects.all()

        page = self.paginate_queryset(sites)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(sites, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        sites = Site.objects.all()
        site = get_object_or_404(sites, topic=pk)
        serializer = SiteRetrieveSerializer(
            instance=site, context={'request': request})
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagListSerializer

    def list(self, request):
        tags = Tag.objects.all()

        page = self.paginate_queryset(tags)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        tags = Tag.objects.all()
        tag = get_object_or_404(tags, tag_id=pk)
        serializer = TagRetrieveSerializer(
            instance=tag, context={'request': request})
        return Response(serializer.data)


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneListSerializer

    def list(self, request):
        zones = Zone.objects.all()

        page = self.paginate_queryset(zones)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(zones, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        zones = Zone.objects.all()
        zone = get_object_or_404(zones, zone_id=pk)
        serializer = ZoneRetrieveSerializer(
            instance=zone, context={'request': request})
        return Response(serializer.data)


class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordListSerializer

    def list(self, request):
        params = request.query_params
        try:
            datestring = params['date']
            fromString = params['from']
            toString = params['to']

            fromDt = datetime.strptime("{} {}".format(datestring, fromString), '%Y-%m-%d %H:%M')
            toDt = datetime.strptime("{} {}".format(datestring, toString), '%Y-%m-%d %H:%M')

            records = Record.objects.filter(time__range=[fromDt, toDt])
        except Exception as e:
            print(e)
            records = Record.objects.all()

        page = self.paginate_queryset(records)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        records = Record.objects.all()
        record = get_object_or_404(records, pk=pk)
        serializer = RecordListSerializer(
            instance=record, context={'request': request})
        return Response(serializer.data)


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertListSerializer

    def list(self, request):
        alerts = Alert.objects.order_by('-start')

        page = self.paginate_queryset(alerts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        alerts = Alert.objects.all()
        alert = get_object_or_404(alerts, pk=pk)
        serializer = AlertListSerializer(
            instance=alert, context={'request': request})
        return Response(serializer.data)
