import paho.mqtt.client as mqtt
import threading

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_COMMAND = "device/command"
MQTT_TOPIC_RESPONSE = "server/response"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Server connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC_RESPONSE) 
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print(f"\n{message}")

def input_thread(client):
    while True:
        command = input()
        client.publish(MQTT_TOPIC_COMMAND, command)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()
threading.Thread(target=input_thread, args=(client,)).start()
