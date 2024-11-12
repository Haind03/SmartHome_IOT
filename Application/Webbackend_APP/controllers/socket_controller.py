import socket
from datetime import datetime
from Webbackend_APP.models.Data_Realtime import get_db, DataRealTime
import time
import json
import random
import Webbackend_APP.controllers.Data_Sensor_List as Data_Sensor_List

def socket_server(socketio):
    host = '0.0.0.0'
    port = 4444

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print('Socket server is running on 4444...')
    while True:
        conn, addr = server_socket.accept()
        print(f'Connected to {addr}')

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                # Nhận dữ liệu từ ESP8266
                data = data.decode('utf-8')
                print(f"Received data: {data}")

                # Sửa dữ liệu: thay thế dấu ngoặc đơn bằng dấu ngoặc kép để thành JSON hợp lệ
                json_data = data.replace("'", "\"")

                # Giải mã dữ liệu nhận được
                try:
                    parsed_data = json.loads(json_data) 
                    if 'temperature' not in parsed_data or 'humidity' not in parsed_data or 'light_level' not in parsed_data:
                        raise ValueError("Missing required data fields")
                except Exception as e:
                    print(f"Error parsing data: {e}")
                    continue  # Bỏ qua vòng lặp hiện tại nếu dữ liệu không hợp lệ
                
                # data_controller.save_sensor_data(temp=parsed_data['temperature'], humidity=parsed_data['humidity'], light=parsed_data['light_level'], cb=cb_data)
                # Lưu dữ liệu vào database
                db = next(get_db())
                cb_data=random.randint(0, 100)
                new_entry = DataRealTime(
                    temp=parsed_data['temperature'],
                    humidity=parsed_data['humidity'],
                    light=parsed_data['light_level'],
                    cb=cb_data,
                    timestamp=datetime.utcnow()
                )

                db.add(new_entry)
                db.commit()
                time.sleep(3)

                # Phát dữ liệu qua WebSocket tới giao diện
                if socketio:
                    socketio.emit('sensor_data', {
                        'temp': parsed_data['temperature'],
                        'humidity': parsed_data['humidity'],
                        'light': parsed_data['light_level'],
                        'cb': cb_data,
                        'timestamp': str(datetime.utcnow())
                    })

            except Exception as e:
                print(f"Error receiving or processing data: {e}")
                break

        conn.close()
