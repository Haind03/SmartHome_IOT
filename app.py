from flask import Flask, render_template, request, jsonify
import json
import time
import math
import paho.mqtt.client as mqtt

app = Flask(__name__)

# MQTT setup
mqtt_broker = "broker.hivemq.com"
mqtt_port = 1883
mqtt_client = mqtt.Client()

# Logs storage
log_file = "mqtt_logs.json"
action_log_file = "action_logs.json"
state_file = "device_states.json"

# Items per page
ITEMS_PER_PAGE = 10

# Mapping device topics to user-friendly names
DEVICE_NAMES = {
    "home/device1": "Ánh sáng",
    "home/device2": "Độ ẩm",
    "home/device3": "Nhiệt độ"
}

def load_logs(log_file):
    try:
        with open(log_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_log(log, log_file):
    logs = load_logs(log_file)
    logs.insert(0, log)
    with open(log_file, "w") as f:
        json.dump(logs, f, indent=4)

def load_state():
    try:
        with open(state_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_state(state):
    with open(state_file, "w") as f:
        json.dump(state, f, indent=4)

def on_message(client, userdata, msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    date_only = time.strftime('%Y-%m-%d')
    current_state = load_state()
    
    topic = msg.topic
    value = msg.payload.decode()

    # Map device name
    device_name = DEVICE_NAMES.get(topic, topic)

    # Check if there is a change in the state
    if current_state.get(topic) != value:
        log = {
            "id": len(load_logs(log_file)) + 1,
            "device": device_name,  # Sử dụng tên thiết bị đã ánh xạ
            "value": value,
            "date": date_only,
            "timestamp": timestamp
        }
        save_log(log, log_file)
        save_log(log, action_log_file)

        # Update the state
        current_state[topic] = value
        save_state(current_state)

mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port)
mqtt_client.subscribe("home/#")
mqtt_client.loop_start()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logs')
def logs():
    page = int(request.args.get('page', 1))
    logs = load_logs(log_file)
    
    total_pages = math.ceil(len(logs) / ITEMS_PER_PAGE)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    
    logs_to_display = logs[start:end]
    
    return render_template('log.html', logs=logs_to_display, page=page, total_pages=total_pages)

@app.route('/action_history')
def action_history():
    page = int(request.args.get('page', 1))
    logs = load_logs(action_log_file)
    
    total_pages = math.ceil(len(logs) / ITEMS_PER_PAGE)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    
    logs_to_display = logs[start:end]
    
    return render_template('action_history.html', logs=logs_to_display, page=page, total_pages=total_pages)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/log_toggle', methods=['POST'])
def log_toggle():
    data = request.json
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    date_only = time.strftime('%Y-%m-%d')

    # Map device name
    device_name = DEVICE_NAMES.get(data['device'], data['device'])
    
    log_entry = {
        "id": len(load_logs(log_file)) + 1,
        "device": device_name,  # Sử dụng tên thiết bị đã ánh xạ
        "value": data['action'],
        "date": date_only,
        "timestamp": timestamp
    }
    
    save_log(log_entry, log_file)
    save_log(log_entry, action_log_file)
    
    # Update the state to keep track of the device's last known state
    current_state = load_state()
    current_state[data['device']] = data['action']
    save_state(current_state)
    
    return jsonify(success=True)

@app.route('/publish', methods=['POST'])
def publish():
    topic = request.json['topic']
    message = request.json['message']
    mqtt_client.publish(topic, message)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
