from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import eventlet

# Connection string for MySQL (replace user, password, host, and database as per your configuration)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/iot_sms"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def perform_database_operations(data):
    """Function to perform database operations in a separate green thread."""
    with get_db() as db:
        # Perform your database operations here using the db session
        # For example, if you have a model named `SensorData`:
        # new_entry = SensorData(**data)
        # db.add(new_entry)
        # db.commit()
        pass

# Usage example: spawn the database operations in a green thread when receiving an MQTT message
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    # Here, convert payload to a dictionary or relevant format
    data = {'humidity': 67.2, 'light_level': 685, 'temperature': 28.3}  # Example data

    # Use eventlet to run the blocking function in a separate green thread
    eventlet.spawn(perform_database_operations, data)

# MQTT setup would go here, including client connection and message handling setup
