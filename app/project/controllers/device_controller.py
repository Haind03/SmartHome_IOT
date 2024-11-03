from flask import jsonify, request
from models.device import Device
from models.device_history import DeviceHistory  # Import model lịch sử
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
from controllers.device_history_controller import save_device_history 

def publish_device():
    data = request.get_json()
    cmd = data.get('cmd')
    print(f"Received command: {cmd}")
    topic = data.get('topic')

    # Kiểm tra nếu thiếu cmd hoặc topic trong request
    if not cmd or not topic:
        return jsonify({"error": "Missing required fields"}), 400

    # Tạo một thiết bị với topic và cmd, sau đó publish nó
    device = Device(topic, cmd)
    result = device.publish()

    # Kết nối cơ sở dữ liệu để lưu lịch sử điều khiển thiết bị
    db: Session = next(get_db())

    # Lưu lịch sử điều khiển thiết bị vào cơ sở dữ liệu
    db: Session = next(get_db())
    if topic == 'home/all':
        save_device_history(db, 'FAN', cmd, cmd)
        save_device_history(db, 'LIGHT', cmd, cmd)
        save_device_history(db, 'AIR', cmd, cmd)
    else:
        save_device_history(db, topic.upper().split('/')[-1], cmd, cmd)

    # Xử lý logic theo lệnh ON hoặc OFF
    if cmd.upper() == 'OFF':
        return jsonify({
            "message": "Device turned OFF",
            "device": result
        }), 200  # Mã trả về thành công

    elif cmd.upper() == 'ON':
        return jsonify({
            "message": "Device turned ON",
            "device": result
        }), 200  # Mã trả về thành công

    else:
        return jsonify({
            "message": f"Unknown command: {cmd}",
            "device": result,
            "status": "failed"
        }), 400  # Mã trả về lỗi với command không hợp lệ
