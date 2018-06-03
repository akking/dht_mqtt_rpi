import json
import logging
import time
import sys

import Adafruit_DHT
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__).addHandler(logging.StreamHandler())

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
    mqtt_host = sys.argv[3]
    name = sys.argv[4]
    topic = 'home/sensor/{}'.format(name)
    topic_temp = topic + '_temperature'
    topic_humi = topic + '_humidity'
else:
    sensor = sensor_args['22']
    pin = 4
    mqtt_host = 'nas.home'
    name = 'livingroom_dht22'
    topic = 'home/sensor/{}'.format(name)
    topic_temp = topic + '_temperature'
    topic_humi = topic + '_humidity'

mqttc = mqtt.Client()
mqttc.connect(mqtt_host)
mqttc.loop_start()

payload_temp_conf = json.dumps({"name": name + '_temperature',
                                "device_class": "temperature",
                                "unit_of_measurement": "°C"})
mqttc.publish(topic_temp+'/config', payload=payload_temp_conf, retain=True)

payload_humi_conf = json.dumps({"name": name + '_humidity',
                                "device_class": "humidity",
                                "unit_of_measurement": "%"})
mqttc.publish(topic_humi+'/config', payload=payload_humi_conf, retain=True)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        mqttc.publish(topic_temp+'/state', payload=round(temperature, 1), retain=True)
        mqttc.publish(topic_humi+'/state', payload=round(humidity, 1), retain=True)
        time.sleep(30)
    else:
        time.sleep(3)
