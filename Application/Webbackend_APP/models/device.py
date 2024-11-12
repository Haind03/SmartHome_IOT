import subprocess

class Device:
    def __init__(self, topic, cmd):
        self.topic = topic
        self.cmd = cmd
        # self.broker = '192.168.1.5'        
        self.broker = '172.20.10.2'
        self.port = '1993'
        self.username = 'HaiND'
        self.password = 'B21DCAT004'

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
