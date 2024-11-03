from sqlalchemy.orm import Session
from models.device_history import DeviceHistory

def save_device_history(db: Session, device_name: str, command: str, status: str):
    # Tạo một bản ghi lịch sử mới
    new_history = DeviceHistory(
        device_name=device_name,
        command=command,
        status=status
    )
    db.add(new_history)  # Thêm bản ghi mới vào session
    db.commit()  # Lưu thay đổi vào cơ sở dữ liệu
    db.refresh(new_history)  # Cập nhật đối tượng với thông tin từ DB
    return new_history
