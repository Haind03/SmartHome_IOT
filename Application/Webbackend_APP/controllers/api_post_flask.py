from flask import jsonify, request
from models.device import Device
from Webbackend_APP.models.History_Device import DeviceHistory  # Import model lịch sử thiết bị
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
from Webbackend_APP.controllers.Data_History_List import save_device_history 

# API xử lý yêu cầu POST để điều khiển thiết bị
def publish_device():
    # Bước 1: Lấy dữ liệu từ yêu cầu JSON
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Thiếu dữ liệu trong yêu cầu"}), 400
    
    cmd = data.get('cmd')
    topic = data.get('topic')
    print(f"Lệnh nhận được: {cmd}, cho chủ đề: {topic}")

    if not cmd or not topic:
        return jsonify({"error": "Thiếu trường bắt buộc: 'cmd' hoặc 'topic'"}), 400

    try:
        device = Device(topic, cmd)
        result = device.publish()
    except Exception as e:
        print("Lỗi khi gửi lệnh đến thiết bị:", e)
        return jsonify({"error": "Gửi lệnh điều khiển đến thiết bị thất bại"}), 500

    db = None
    try:
        db: Session = next(get_db())

        if topic == 'home/all':
            save_device_history(db, 'FAN', cmd, cmd)
            save_device_history(db, 'LIGHT', cmd, cmd)
            save_device_history(db, 'AIR', cmd, cmd)
        else:
            device_name = topic.upper().split('/')[-1]
            save_device_history(db, device_name, cmd, cmd)
    except Exception as e:
        print("Lỗi khi lưu lịch sử thiết bị:", e)
        return jsonify({"error": "Lưu lịch sử thiết bị thất bại"}), 500
    finally:
        if db:
            db.close()
            print("Đã đóng session cơ sở dữ liệu")

    if cmd.upper() == 'OFF':
        return jsonify({
            "message": "Thiết bị đã được TẮT",
            "device": result
        }), 200
    elif cmd.upper() == 'ON':
        return jsonify({
            "message": "Thiết bị đã được BẬT",
            "device": result
        }), 200
    else:
        print(f"Lệnh không xác định nhận được: {cmd}")
        return jsonify({
            "message": f"Lệnh không xác định: {cmd}",
            "device": result,
            "status": "failed"
        }), 400
