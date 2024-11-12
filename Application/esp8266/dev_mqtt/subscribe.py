import paho.mqtt.client as mqtt
import base64


# mqtt info
mqtt_broker_ip = "172.20.10.3"
port = 1993
topic = "home/sensors"
username = "haind"         
passwd = "B21DCAT004"     

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