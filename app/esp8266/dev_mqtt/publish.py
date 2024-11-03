from simple import MQTTClient
import network
import time
import dht
from machine import Pin, ADC

ssid = 'haind03'
password = 'haind03456'

# Connect to Wi-Fi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

# Wait for Wi-Fi connection
while not station.isconnected():
    print('Connecting to Wi-Fi...')
    time.sleep(1)

print('Connected to WiFi')
print('Network config:', station.ifconfig())

# MQTT broker details
MQTT_SERVER = '172.20.10.2'
MQTT_PORT = 1993
CLIENT_ID = 'ESP8266_Client'
TOPIC_PUB = 'home/sensors'

# MQTT credentials
MQTT_USERNAME = 'KienNV'
MQTT_PASSWORD = 'B21DCAT009'

# Initialize MQTT client with authentication
client = MQTTClient(
    CLIENT_ID, 
    MQTT_SERVER, 
    port=MQTT_PORT, 
    user=MQTT_USERNAME, 
    password=MQTT_PASSWORD, 
    keepalive=60
)

def connect_mqtt():
    try:
        client.connect()
        print('Connected to %s MQTT broker' % MQTT_SERVER)
    except Exception as e:
        print('Could not connect to MQTT broker:', e)

def publish_data(temperature, humidity, light_level):
    try:
        # Prepare data payload
        message = {
            "temperature": temperature,
            "humidity": humidity,
            "light_level": light_level
        }
        # Publish data to the MQTT broker
        client.publish(TOPIC_PUB, str(message))
        print('Data published:', message)
    except Exception as e:
        print('Failed to publish message:', e)

# Setup DHT22 sensor
dht_sensor = dht.DHT22(Pin(4))  # Assuming GPIO 4 for DHT22 data pin
print('reading dht sucess')

# Setup CDS-NVZ1 (LDR) sensor
light_sensor = ADC(0)  # A0 pin for analog input
print('reading light sucess')

# Connect to MQTT broker
connect_mqtt()

# Publish data continuously
while True:
    try:
        # Read data from DHT22
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        
        # Read data from CDS-NVZ1 (LDR)
        light_level = light_sensor.read()  # Analog output (0-1023)

        # Publish the sensor data
        
        publish_data(temperature, humidity, light_level)

        time.sleep(5)
    except Exception as e:
        print('Error:', e)
        time.sleep(5)

