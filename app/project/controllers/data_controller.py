from models.datarealtime_model import DataRealTime, get_db
from datetime import datetime

# Hàm để lưu dữ liệu vào bảng datarealtime
def save_sensor_data(temp, humidity, light):
    db = next(get_db())
    try:
        new_data = DataRealTime(temp=temp, humidity=humidity, light=light, timestamp=datetime.utcnow())
        db.add(new_data)
        db.commit()
    except Exception as e:
        db.rollback()  # Quay lại nếu có lỗi
        raise e
    finally:
        db.close()

# Hàm để lấy tất cả dữ liệu
def get_all_data():
    db = next(get_db())
    try:
        data = db.query(DataRealTime).all()
        return data
    finally:
        db.close()
