from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Cấu hình SQLAlchemy
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/iot_sms"  # Cập nhật thông tin kết nối
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Mô hình cho bảng 'datarealtime'
class DataRealTime(Base):
    __tablename__ = 'datarealtime'

    id = Column(Integer, primary_key=True, autoincrement=True)
    temp = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    light = Column(Float, nullable=False)
    cb = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Khởi tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
