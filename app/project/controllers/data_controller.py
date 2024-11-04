from models.datarealtime_model import DataRealTime, get_db
from datetime import datetime
from sqlalchemy.orm import Session

# Hàm để lưu dữ liệu vào bảng datarealtime
def save_sensor_data(temp, humidity, light, cb):
    # Open a new database session
    db: Session = next(get_db())  # Make sure get_db is yielding correctly
    try:
        # Create a new DataRealTime instance
        new_data = DataRealTime(
            temp=temp,
            humidity=humidity,
            light=light,
            timestamp=datetime.utcnow(),
            cb = cb
        )
        db.add(new_data)  # Add new record
        db.commit()       # Commit transaction
        print("Data saved successfully")  # Debugging statement
    except Exception as e:
        db.rollback()  # Roll back transaction on error
        print(f"Error saving data: {e}")  # Print error message for debugging
    finally:
        db.close()      # Close the session

# Hàm để lấy tất cả dữ liệu
def get_all_data():
    db: Session = next(get_db())  # Ensure get_db yields correctly
    try:
        # Query all data from DataRealTime
        data = db.query(DataRealTime).all()
        return data
    finally:
        db.close()
