from monitor.models import Alert, Record
from settings.models import Site, Tag
from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt
import ssl
import json
from math import sqrt
import time


class Command(BaseCommand):
    help = 'Get MQTT Data'

    def handle(self, *args, **options):
        sites = Site.objects.all()
        for site in sites:
            self.process(site)

    def process(self, site):
        host = site.hostname
        port = site.port
        topic = site.topic
        username = site.username
        password = site.password

        client = mqtt.Client(transport="websockets")
        client.username_pw_set(username, password=password)

        client.tls_set_context(context=ssl.create_default_context())

        def on_connect(client, userdata, flags, rc):
            print(mqtt.connack_string(rc))

        activeAlerts = []

        def on_message(client, userdata, msg):
            payload = json.loads(msg.payload.decode())[0]

            tagId = payload['tagId']
            status = payload['success']
            if status == True:
                coordinates = payload['data']['coordinates']
                try:
                    tags = Tag.objects.all()
                    label = [t.label for t in tags if t.tag_id == tagId]
                    if label == None or label == [None]:
                        label = ""
                    else:
                        label = label[0]
                    color = [t.color for t in tags if t.tag_id == tagId]
                    if color == None or color == [None]:
                        color = ""
                    else:
                        color = color[0]
                    Record.objects.create(
                        tag_id=tagId, x=coordinates['x'], y=coordinates['y'], z=coordinates['z'], label=label, color=color, site=site)
                except Exception as e:
                    print(e)

                try:
                    tag = Tag.objects.get(tag_id=tagId)
                    tag.x = coordinates['x']
                    tag.y = coordinates['y']
                    tag.z = coordinates['z']

                    tag.latency = payload['data']['metrics']['latency']
                    tag.success = payload['data']['metrics']['rates']['success']
                    tag.update = payload['data']['metrics']['rates']['update']
                    tag.loss = payload['data']['metrics']['rates']['packetLoss']
                    tag.blink_index = payload['data']['tagData']['blinkIndex']

                    tag.save()
                except Tag.DoesNotExist:
                    Tag.objects.create(
                        tag_id=tagId, x=coordinates['x'], y=coordinates['y'], z=coordinates['z'], site=site)
                except Exception as e:
                    print(e)

            tags = Tag.objects.filter(site=site)

            siteinfo = Site.objects.get(topic=topic)
            alert_threshold = siteinfo.alert_threshold

            for i in range(len(tags) - 1):
                tag1 = tags[i]
                for j in range(i + 1, len(tags)):
                    tag2 = tags[j]

                    alert_id = "{}{}".format(
                        tag1.tag_id, tag2.tag_id)

                    distance = sqrt((tag1.x - tag2.x) ** 2
                                    + (tag1.y - tag2.y) ** 2)

                    if distance < alert_threshold:
                        if alert_id not in activeAlerts:
                            activeAlerts.append(alert_id)
                            Alert.objects.create(
                                alert_id=alert_id, tag1_id=tag1.tag_id, tag2_id=tag2.tag_id, threshold=alert_threshold)
                        else:
                            try:
                                alert = Alert.objects.filter(
                                    alert_id=alert_id).order_by('-start')[0]
                                alert.save()
                            except:
                                pass
                    else:
                        if alert_id in activeAlerts:
                            activeAlerts.remove(alert_id)

        def on_subscribe(client, userdata, mid, granted_qos):
            print("Subscribed to topic!")

        client.on_connect = on_connect
        client.on_message = on_message
        client.on_subscribe = on_subscribe
        client.connect(host, port=port)
        client.subscribe(topic)

        client.loop_forever()
