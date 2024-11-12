from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime,timedelta
from database import Base

class DeviceHistory(Base):
    __tablename__ = 'DeviceHistory'  # Tên bảng trong MySQL

    id = Column(Integer, primary_key=True, autoincrement=True)  # Khóa chính
    device_name = Column(String(50), nullable=False)  # Tên thiết bị
    command = Column(String(50), nullable=False)  # Lệnh điều khiển (ON/OFF)
    status = Column(String(50), nullable=False)  # Trạng thái của lệnh
    timestamp = Column(DateTime, default=datetime.utcnow)  # Thời gian thực thi lệnh

    def __init__(self, device_name, command, status):
        self.device_name = device_name
        self.command = command
        self.status = status
        self.timestamp = datetime.utcnow() + timedelta(hours=7)  # Mặc định là thời gian hiện tại
    