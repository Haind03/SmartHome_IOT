import eventlet
eventlet.monkey_patch()  # Ensure compatibility with Eventlet
import sys
import random
import json
sys.path.append('d:/PTIT_Project/IOTapp/Application')

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
# app.config['MQTT_BROKER_URL'] = '192.168.1.5'  # Set your broker's URL
app.config['MQTT_BROKER_URL'] = '172.20.10.3'  # Set your broker's URL
app.config['MQTT_BROKER_PORT'] = 1993  # Set your broker's port
app.config['MQTT_USERNAME'] = 'HaiND'  # Set broker username if needed
app.config['MQTT_PASSWORD'] = 'B21DCAT004'  # Set broker password if needed
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False  # Set to True if using TLS

# Enable CORS
CORS(app)

# Initialize Flask-SocketIO and Flask-MQTT
mqtt = Mqtt(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

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
        tmp = eval(payload)
        
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
    socketio.run(app, port=5000, debug=True, use_reloader=False)
