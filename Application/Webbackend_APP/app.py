import eventlet
eventlet.monkey_patch()  # Ensure compatibility with Eventlet
import sys
import random
import json
sys.path.append('d:/PTIT_Project/IOTapp/Application')

import ast
import os

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from flask_cors import CORS
from Webbackend_APP.controllers.api_post_flask import publish_device
from Webbackend_APP.controllers.api_action_history import get_device_logs
from Webbackend_APP.controllers.api_sensor_data import get_sensor_data
from Webbackend_APP.controllers.Data_Sensor_List import save_sensor_data
# Initialize Flask app
app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = os.environ.get('MQTT_BROKER_URL', 'localhost')
app.config['MQTT_BROKER_PORT'] = int(os.environ.get('MQTT_BROKER_PORT', '1993'))
app.config['MQTT_USERNAME'] = os.environ.get('MQTT_USERNAME', '')
app.config['MQTT_PASSWORD'] = os.environ.get('MQTT_PASSWORD', '')
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = os.environ.get('MQTT_TLS_ENABLED', 'false').lower() == 'true'

# Enable CORS
# Chỉ cho phép các origin được cấu hình (mặc định: same-origin)
ALLOWED_ORIGINS = [o for o in os.environ.get('CORS_ORIGINS', '').split(',') if o]
CORS(app, origins=ALLOWED_ORIGINS)

# Initialize Flask-SocketIO and Flask-MQTT
mqtt = Mqtt(app)
socketio = SocketIO(app, cors_allowed_origins=ALLOWED_ORIGINS or None, async_mode="eventlet")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')

@app.route('/action_history')
def action_history():
    return render_template('action_history.html')

@app.route('/sensor_data')
def log_history():
    return render_template('sensor_data.html')

@app.route('/users_profile')
def users_profile():
    return render_template('users_profile.html')

# API to publish device
@app.route('/api/v1/device/publish', methods=['POST'])
def api_publish_device():
    return publish_device()

# API to get device logs
@app.route('/api/v1/device/logs', methods=['GET'])
def api_get_device_logs():
    return get_device_logs()

# API to get sensor data
@app.route('/api/v1/sensor/data', methods=['GET'])
def api_get_sensor_data():
    return get_sensor_data()

def parse_sensor_payload(payload):
    """Parse payload cảm biến (JSON hoặc repr dict từ ESP8266) một cách an toàn."""
    try:
        data = json.loads(payload)
    except ValueError:
        try:
            data = ast.literal_eval(payload)
        except (ValueError, SyntaxError):
            print("Invalid sensor payload")
            return None
    if not isinstance(data, dict):
        return None
    try:
        return {k: float(data[k]) for k in ("temperature", "humidity", "light_level")}
    except (KeyError, TypeError, ValueError):
        print("Invalid sensor payload")
        return None

# MQTT Event Handlers
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with code {rc}")
    mqtt.subscribe('home/sensors')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    payload = message.payload.decode()
    print(f"Received MQTT message: {payload} on topic: {message.topic}")
    
    try:
        tmp = parse_sensor_payload(payload)
        if tmp is None:
            return

        tmp["cb"] = round(random.uniform(0, 100), 1)  # Add a random value between 0 and 100
        
        save_sensor_data(tmp["temperature"], tmp["humidity"], tmp["light_level"], tmp["cb"])
        print(tmp)
        socketio.emit('sensor_data', {
            'topic': message.topic, 
            'message': json.dumps(tmp)  # Send the modified payload as a JSON string
        })
    except json.JSONDecodeError:
        print("Failed to decode JSON payload")

# Run the Flask app with Socket.IO and MQTT support using Eventlet
if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    socketio.run(app, port=5000, debug=debug, use_reloader=False)
