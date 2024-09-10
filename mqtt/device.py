import paho.mqtt.client as mqtt
import json
import random
import time

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "temperature/data"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

client = mqtt.Client()

client.on_connect = on_connect

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

while True:
    data = {"temperature": round(random.uniform(15.0, 25.0), 2)}
    result = client.publish(MQTT_TOPIC, json.dumps(data))
    print(f"Sent data: {data}, Response: {result.rc}")
    time.sleep(5)
