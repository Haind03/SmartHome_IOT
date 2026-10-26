import paho.mqtt.client as mqtt
import base64
import os


# mqtt info
mqtt_broker_ip = os.environ.get("MQTT_BROKER_URL", "172.20.10.3")
port = int(os.environ.get("MQTT_BROKER_PORT", "1993"))
topic = "home/sensors"
username = os.environ.get("MQTT_USERNAME", "")
passwd = os.environ.get("MQTT_PASSWORD", "")

# call back function
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker on port: {port}")
        client.subscribe(topic)  
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.topic} -> {msg.payload.decode('utf-8')}")


def main():
    # create mqtt object
    client = mqtt.Client()

    # set username & password
    client.username_pw_set(username, passwd)

    # assign callback function
    client.on_connect = on_connect
    client.on_message = on_message

    # connect to broker
    client.connect(mqtt_broker_ip, port, 60)

    # loop
    client.loop_forever()

main()