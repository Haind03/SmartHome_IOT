from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Chuỗi kết nối MySQL (Thay thế user, password, host và database theo cấu hình của bạn)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/iot_sms"

# Kết nối đến cơ sở dữ liệu
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Tạo session để thực hiện truy vấn
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base cho các model kế thừa
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
