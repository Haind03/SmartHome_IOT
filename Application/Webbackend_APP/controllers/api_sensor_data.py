from flask import jsonify, request
from sqlalchemy.orm import Session
from Webbackend_APP.models.Data_Realtime import DataRealTime
from sqlalchemy import asc, desc
from database import get_db
import traceback

# API lấy dữ liệu cảm biến với phân trang, tìm kiếm và sắp xếp
def get_sensor_data():
    # Thiết lập kết nối tới cơ sở dữ liệu
    db: Session = next(get_db())

    # Lấy các tham số phân trang từ chuỗi truy vấn
    # 'page' là trang hiện tại được người dùng yêu cầu; giá trị mặc định là 1
    page = request.args.get('page', 1, type=int)
    
    # 'limit' xác định số bản ghi trả về trên mỗi trang; giá trị mặc định là 10
    limit = request.args.get('limit', 10, type=int)

    # Lấy từ khóa tìm kiếm, nếu có, để lọc kết quả theo giá trị cụ thể
    search_query = request.args.get('search', '').strip()

    # Định nghĩa thứ tự sắp xếp, hoặc tăng dần hoặc giảm dần, mặc định là 'asc'
    sort_order = request.args.get('sort', 'asc', type=str)

    # Trường đại diện cho cột cần áp dụng bộ lọc tìm kiếm
    # Mặc định ở đây là 'cb', là một thuộc tính trong model DataRealTime
    field = request.args.get('field', 'cb', type=str)

    try:
        # Bước 1: Khởi tạo truy vấn cơ bản trên bảng DataRealTime
        query = db.query(DataRealTime)

        # Bước 2: Áp dụng bộ lọc tìm kiếm dựa trên trường được chọn và từ khóa tìm kiếm
        # Sử dụng các điều kiện để xử lý các loại dữ liệu và trường khác nhau
        if search_query:
            if field == 'id':
                # Bộ lọc tìm kiếm trên trường 'id', đảm bảo nó là một số nguyên hợp lệ
                if search_query.isdigit():
                    query = query.filter(DataRealTime.id == int(search_query))
            elif field == 'temp':
                # Bộ lọc tìm kiếm trên trường 'temp', giả sử là giá trị số thực
                try:
                    query = query.filter(DataRealTime.temp == float(search_query))
                except ValueError:
                    return jsonify({"error": "Nhiệt độ phải là một số hợp lệ"}), 400
            elif field == 'humidity':
                # Bộ lọc tìm kiếm trên trường 'humidity'
                try:
                    query = query.filter(DataRealTime.humidity == float(search_query))
                except ValueError:
                    return jsonify({"error": "Độ ẩm phải là một số hợp lệ"}), 400
            elif field == 'light':
                # Bộ lọc tìm kiếm trên trường 'light'
                try:
                    query = query.filter(DataRealTime.light == float(search_query))
                except ValueError:
                    return jsonify({"error": "Mức ánh sáng phải là một số hợp lệ"}), 400
            # elif field == 'cb':
            #     # Bộ lọc tìm kiếm trên trường 'cb'
            #     try:
            #         query = query.filter(DataRealTime.cb == float(search_query))
            #     except ValueError:
            #         return jsonify({"error": "CB phải là một số hợp lệ"}), 400
            elif field == 'timestamp':
                # Bộ lọc tìm kiếm trên trường 'timestamp' bằng cách khớp một phần với LIKE
                query = query.filter(DataRealTime.timestamp.like(f"%{search_query}%"))
            else:
                # Trường tìm kiếm không hợp lệ, trả về lỗi
                return jsonify({"error": "Trường tìm kiếm không hợp lệ"}), 400

        # Bước 3: Áp dụng sắp xếp vào kết quả truy vấn dựa trên cột 'timestamp'
        # Thứ tự sắp xếp được định nghĩa bởi 'sort_order', là 'asc' hoặc 'desc'
        if sort_order == 'desc':
            query = query.order_by(desc(DataRealTime.timestamp))
        else:
            query = query.order_by(asc(DataRealTime.timestamp))

        # Bước 4: Lấy tổng số bản ghi sau khi áp dụng bộ lọc tìm kiếm
        total_logs = query.count()

        # Bước 5: Thực hiện phân trang, bù đắp bằng số trang và giới hạn kết quả trên mỗi trang
        logs = query.offset((page - 1) * limit).limit(limit).all()

        # Bước 6: Chuyển đổi kết quả truy vấn thành dạng dictionary tương thích với JSON
        # Vòng lặp này duyệt qua từng 'log' trong kết quả truy vấn đã được lọc và phân trang
        logs_data = []
        for log in logs:
            # Tạo dictionary cho từng bản ghi trong logs, bao gồm các trường cần thiết
            log_entry = {
                "id": log.id,
                "temp": log.temp,
                "humidity": log.humidity,
                "light": log.light,
                # "cb": log.cb,
                "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            # Thêm từng dictionary vào danh sách 'logs_data'
            logs_data.append(log_entry)

        # Bước 7: In logs_data để gỡ lỗi (đã bình luận)
        # print("logs_data:", logs_data)

        # Bước 8: Trả về phản hồi JSON với thông tin phân trang và dữ liệu log
        return jsonify({
            "page": page,                # Trang hiện tại
            "limit": limit,              # Giới hạn mỗi trang
            "total_count": total_logs,   # Tổng số bản ghi sau tìm kiếm
            "data": logs_data            # Mảng dữ liệu chứa logs
        }), 200  # Mã HTTP 200 báo hiệu thành công

    except Exception as e:
        # Bắt các ngoại lệ, ghi lỗi ra console, và in traceback để gỡ lỗi
        print("Đã xảy ra lỗi khi lấy dữ liệu cảm biến:", e)
        print(traceback.format_exc())  # Xuất traceback chi tiết ra console

        # Trả về phản hồi JSON với thông báo lỗi
        return jsonify({"error": str(e)}), 500  # Mã HTTP 500 báo hiệu lỗi máy chủ

    finally:
        # Luôn đóng session cơ sở dữ liệu để giải phóng tài nguyên sau mỗi yêu cầu
        db.close()
