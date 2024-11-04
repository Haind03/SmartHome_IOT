from flask import jsonify, request
from sqlalchemy.orm import Session
from models.datarealtime_model import DataRealTime
from sqlalchemy import asc, desc
from database import get_db
import traceback

def get_sensor_data():
    # Connect to the database
    db: Session = next(get_db())

    # Get pagination, search, and sorting parameters from the query string
    page = request.args.get('page', 1, type=int)  # Current page (default is 1)
    limit = request.args.get('limit', 10, type=int)  # Number of logs per page (default is 10)
    search_query = request.args.get('search', '').strip()  # Search keyword (if any)
    sort_order = request.args.get('sort', 'asc', type=str)  # Sort order (asc or desc)
    field = request.args.get('field', 'cb', type=str)  # Field to search

    try:
        # Base query
        query = db.query(DataRealTime)

        # Apply search condition based on the selected field
        if search_query:
            if field == 'id' and search_query.isdigit():
                query = query.filter(DataRealTime.id == int(search_query))
            elif field == 'temp':
                query = query.filter(DataRealTime.temp == float(search_query))
            elif field == 'humidity':
                query = query.filter(DataRealTime.humidity == float(search_query))
            elif field == 'light':
                query = query.filter(DataRealTime.light == float(search_query))
            elif field == 'cb':
                query = query.filter(DataRealTime.cb == float(search_query))
            elif field == 'timestamp':
                query = query.filter(DataRealTime.timestamp.like(f"%{search_query}%"))
            else:
                return jsonify({"error": "Invalid search field"}), 400  # Return error for invalid field

        # Apply sorting based on `timestamp` and the specified `sort_order`
        if sort_order == 'desc':
            query = query.order_by(desc(DataRealTime.timestamp))
        else:
            query = query.order_by(asc(DataRealTime.timestamp))

        # Get the total count after applying the search
        total_logs = query.count()

        # Paginate the results
        logs = query.offset((page - 1) * limit).limit(limit).all()

        # Convert results to JSON format
        logs_data = [
            {
                "id": log.id,
                "temp": log.temp,
                "humidity": log.humidity,
                "light": log.light,
                "cb": log.cb,
                "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for log in logs
        ]
        # print("logs_data:", logs_data)
        # Return the result with pagination info    
        return jsonify({
            "page": page,
            "limit": limit,
            "total_count": total_logs,
            "data": logs_data
        }), 200

    except Exception as e:
        print("An error occurred while fetching sensor data:", e)
        print(traceback.format_exc())  # This will output the full traceback to the console
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()  # Ensure the session is closed after the query
