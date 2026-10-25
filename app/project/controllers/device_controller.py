from flask import jsonify, request
from models.device import Device
from models.device_history import DeviceHistory  # Import model lịch sử
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
from controllers.device_history_controller import save_device_history 

# Chỉ cho phép các topic/lệnh mà giao diện thực sự dùng
ALLOWED_TOPICS = {'home/light', 'home/fan', 'home/air', 'home/all', 'home/led', 'home/error'}
ALLOWED_CMDS = {'ON', 'OFF'}

def publish_device():
    data = request.get_json(silent=True) or {}
    cmd = data.get('cmd')
    print(f"Received command: {cmd}")
    topic = data.get('topic')

    # Kiểm tra nếu thiếu cmd hoặc topic trong request
    if not cmd or not topic:
        return jsonify({"error": "Missing required fields"}), 400
    if not isinstance(cmd, str) or not isinstance(topic, str):
        return jsonify({"error": "Invalid fields"}), 400
    cmd = cmd.upper()
    if topic not in ALLOWED_TOPICS or cmd not in ALLOWED_CMDS:
        return jsonify({"error": "Invalid topic or command"}), 400

    # Tạo một thiết bị với topic và cmd, sau đó publish nó
    device = Device(topic, cmd)
    result = device.publish()

    # Lưu lịch sử điều khiển thiết bị vào cơ sở dữ liệu
    db: Session = next(get_db())
    try:
        if topic == 'home/all':
            save_device_history(db, 'FAN', cmd, cmd)
            save_device_history(db, 'LIGHT', cmd, cmd)
            save_device_history(db, 'AIR', cmd, cmd)
        else:
            save_device_history(db, topic.upper().split('/')[-1], cmd, cmd)
    finally:
        db.close()

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
