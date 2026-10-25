import os
import subprocess

class Device:
    def __init__(self, topic, cmd):
        self.topic = topic
        self.cmd = cmd
        self.broker = os.environ.get('MQTT_BROKER_URL', 'localhost')
        self.port = os.environ.get('MQTT_BROKER_PORT', '1993')
        self.username = os.environ.get('MQTT_USERNAME', '')
        self.password = os.environ.get('MQTT_PASSWORD', '')

    def publish(self):
        # Lệnh mosquitto_pub
        command = [
            'mosquitto_pub',
            '-h', self.broker,         # MQTT Broker IP
            '-u', self.username,       # MQTT username
            '-P', self.password,       # MQTT password
            '-t', self.topic,          # MQTT topic
            '-m', self.cmd,            # MQTT message (ON/OFF)
            '-p', self.port            # MQTT port
        ]

        try:
            # Thực thi lệnh sử dụng subprocess
            result = subprocess.run(command, capture_output=True, text=True)

            # Kiểm tra xem lệnh có thành công không
            if result.returncode == 0:
                return {
                    'topic': self.topic,
                    'cmd': self.cmd,
                    'status': 'self.cmd',
                    'output': result.stdout
                }
            else:
                return {
                    'topic': self.topic,
                    'cmd': self.cmd,
                    'status': self.cmd,
                    'error': result.stderr
                }
        except Exception as e:
            return {
                'topic': self.topic,
                'cmd': self.cmd,
                'status': 'error',
                'error': str(e)
            }
