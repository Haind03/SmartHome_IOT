from simple import MQTTClient
import random
import network
import time
import dht
from machine import Pin, ADC
import socket

# Wi-Fi credentials
ssid = 'Haindok'
password = '0x27102003b'
# ssid = 'KTX-B1-T1'
# password = 'PTIT2022'
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
MQTT_SERVER = '192.168.1.7'
MQTT_PORT = 1993
CLIENT_ID = 'ESP8266_Client'
TOPIC_PUB = 'home/sensors'
TOPIC_Light = 'home/light'
TOPIC_Fan = 'home/fan'
TOPIC_Air = 'home/air'
TOPIC_all = 'home/all'
TOPIC_LED = 'home/led'
TOPIC_Error = 'home/error'

# MQTT credentials
MQTT_USERNAME = 'HaiND'
MQTT_PASSWORD = 'B21DCAT004'

# Initialize MQTT client with authentication
client = MQTTClient(
    CLIENT_ID, 
    MQTT_SERVER, 
    port=MQTT_PORT, 
    user=MQTT_USERNAME, 
    password=MQTT_PASSWORD, 
    keepalive=60
)

# Define pins for devices
Fan = Pin(16, Pin.OUT)
Light_bulb = Pin(5, Pin.OUT)
Air_Condition = Pin(4, Pin.OUT)
led = Pin(2, Pin.OUT)  # Built-in LED
external_led = Pin(2, Pin.OUT)  # LED connected to D4

# Initialize all devices to OFF state
led.value(0)
Fan.value(0)
Light_bulb.value(0)
Air_Condition.value(0)
external_led.value(0)  # Set the external LED OFF initially

# def send_data_to_flask(message):
#     try:
#         # Thiết lập socket
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         flask_server = '192.168.0.185'  # Địa chỉ IP của máy chủ Flask
#         flask_port = 4444  # Cổng socket đã được cấu hình trên Flask

#         s.connect((flask_server, flask_port))
#         s.send(message.encode('utf-8'))  # Gửi dữ liệu dưới dạng chuỗi
#         s.close()  # Đóng socket sau khi gửi dữ liệu
#         print('Data sent to Flask server')
#     except Exception as e:
#         print('Failed to send data to Flask:', e)

def connect_mqtt():
    try:
        client.connect()
        print('Connected to %s MQTT broker' % MQTT_SERVER)
    except Exception as e:
        print('Could not connect to MQTT broker:', e)

# Function to blink LED 6 times
def blink_led(led, times=3, delay=0.5):
    for _ in range(times):
        led.value(1)  # Turn LED on
        time.sleep(delay)
        led.value(0)  # Turn LED off
        time.sleep(delay)

# Callback for receiving MQTT messages
def on_message(topic, msg):
    print('Received message:', topic, msg)
    if topic == b'home/light':
        Light_bulb.value(1 if msg == b'ON' else 0)
        print('Light is', 'ON' if msg == b'ON' else 'OFF')
    elif topic == b'home/fan':
        Fan.value(1 if msg == b'ON' else 0)
        print('Fan is', 'ON' if msg == b'ON' else 'OFF')
    elif topic == b'home/air':
        Air_Condition.value(1 if msg == b'ON' else 0)
        print('Air Condition is', 'ON' if msg == b'ON' else 'OFF')
    elif topic == b'home/led':
        external_led.value(1 if msg == b'ON' else 0)
        print('External LED is', 'ON' if msg == b'ON' else 'OFF')
    elif topic == b'home/all':
        state = 1 if msg == b'ON' else 0
        Fan.value(state)
        Light_bulb.value(state)
        Air_Condition.value(state)
        external_led.value(state)
        print('All devices are', 'ON' if msg == b'ON' else 'OFF')
    elif topic == b'home/error':
        print('Error detected, blinking LED...')
        blink_led(external_led)  # Blink external LED 6 times
    

# Publish sensor data
def publish_data(temperature, humidity, light_level):
    try:
        message = {
            "temperature": temperature,
            "humidity": humidity,
            "light_level": light_level 
        }
        client.publish(TOPIC_PUB, str(message))
        # send_data_to_flask(str(message))
        print('Data published:', message)
    except Exception as e:
        print('Failed to publish message:', e)

# Setup DHT22 sensor
dht_sensor = dht.DHT22(Pin(0))  # Assuming GPIO 16 for DHT22 data pin

# Setup CDS-NVZ1 (LDR) sensor
light_sensor = ADC(0)  # A0 pin for analog input

# Connect to MQTT broker and subscribe to topics
connect_mqtt()
client.set_callback(on_message)
client.subscribe(TOPIC_Light)
client.subscribe(TOPIC_Air)
client.subscribe(TOPIC_Fan)
client.subscribe(TOPIC_all)
client.subscribe(TOPIC_LED)
client.subscribe(TOPIC_Error)

# Main loop
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

        # Wait for MQTT messages to control the light
        client.check_msg()

    except Exception as e:
        print('Error:', e)
    time.sleep(2)  # Delay for 2 seconds between readings
