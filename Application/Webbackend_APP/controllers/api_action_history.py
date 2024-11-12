from flask import jsonify, request
from sqlalchemy.orm import Session
from Webbackend_APP.models.History_Device import DeviceHistory
from sqlalchemy import asc, desc
from database import get_db
import traceback

# API để lấy lịch sử hành động của thiết bị với chức năng phân trang, tìm kiếm và sắp xếp
def get_device_logs():
    # Bước 1: Kết nối tới cơ sở dữ liệu bằng cách khởi tạo một session
    try:
        db: Session = next(get_db())
    except Exception as e:
        # Nếu kết nối thất bại, ghi lại lỗi và trả về phản hồi lỗi
        print("Kết nối cơ sở dữ liệu thất bại:", e)
        return jsonify({"error": "Kết nối cơ sở dữ liệu thất bại"}), 500

    # Bước 2: Lấy các tham số từ chuỗi truy vấn cho phân trang, tìm kiếm và sắp xếp
    page = request.args.get('page', 1, type=int)  # Số trang hiện tại (mặc định là 1)
    limit = request.args.get('limit', 10, type=int)  # Số bản ghi trên mỗi trang (mặc định là 10)
    search_query = request.args.get('search', '').strip()  # Từ khóa tìm kiếm, mặc định là trống
    sort_order = request.args.get('sort', 'asc', type=str)  # Thứ tự sắp xếp ('asc' hoặc 'desc')
    field = request.args.get('field', 'device_name', type=str)  # Trường để áp dụng tìm kiếm, mặc định là 'device_name'

    try:
        # Bước 3: Khởi tạo truy vấn cơ bản cho model DeviceHistory
        query = db.query(DeviceHistory)

        # Bước 4: Áp dụng bộ lọc tìm kiếm dựa trên trường được chỉ định và từ khóa tìm kiếm
        # Nếu từ khóa tìm kiếm được cung cấp, lọc kết quả dựa trên trường đã chọn
        if search_query:
            if field == 'id' and search_query.isdigit():
                # Tìm kiếm theo trường 'id', đảm bảo nó là một số nguyên hợp lệ
                query = query.filter(DeviceHistory.id == int(search_query))
            elif field == 'device_name':
                # Tìm kiếm theo trường 'device_name', sử dụng 'contains' cho phép tìm kiếm một phần
                query = query.filter(DeviceHistory.device_name.contains(search_query))
            elif field == 'status':
                # Tìm kiếm theo trường 'status', sử dụng 'contains' cho phép tìm kiếm một phần
                query = query.filter(DeviceHistory.status.contains(search_query))
            elif field == 'timestamp':
                # Tìm kiếm theo trường 'timestamp', sử dụng 'like' cho phép tìm kiếm một phần
                query = query.filter(DeviceHistory.timestamp.like(f"%{search_query}%"))
            else:
                # Nếu trường tìm kiếm không hợp lệ, ghi lại lỗi và trả về phản hồi lỗi
                print("Trường tìm kiếm không hợp lệ:", field)
                return jsonify({"error": "Trường tìm kiếm không hợp lệ"}), 400

        # Bước 5: Áp dụng sắp xếp dựa trên `timestamp` và `sort_order` được chỉ định
        # Thứ tự sắp xếp được xác định bởi tham số 'sort_order', mặc định là tăng dần
        if sort_order == 'desc':
            query = query.order_by(desc(DeviceHistory.timestamp))
        else:
            query = query.order_by(asc(DeviceHistory.timestamp))

        # Bước 6: Tính tổng số bản ghi sau khi áp dụng bộ lọc để làm dữ liệu phân trang
        total_logs = query.count()

        # Bước 7: Áp dụng phân trang bằng cách thiết lập offset và limit cho truy vấn
        # Offset xác định điểm bắt đầu dựa trên trang và limit
        logs = query.offset((page - 1) * limit).limit(limit).all()

        # Bước 8: Chuyển đổi kết quả truy vấn thành định dạng JSON dễ sử dụng
        # Duyệt qua từng 'log' trong kết quả truy vấn đã được phân trang
        logs_data = []
        for log in logs:
            # Chuẩn bị một dictionary cho mỗi mục trong logs với các trường cần thiết
            log_entry = {
                "id": log.id,
                "device_name": log.device_name,
                "status": log.status,
                "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            logs_data.append(log_entry)

        # Bước 9: In dữ liệu logs để phục vụ mục đích gỡ lỗi (tùy chọn)
        # print("logs_data:", logs_data)

        # Bước 10: Xây dựng và trả về phản hồi JSON với thông tin phân trang
        response = {
            "page": page,              # Trang hiện tại
            "limit": limit,            # Giới hạn mỗi trang
            "total_count": total_logs, # Tổng số bản ghi sau tìm kiếm và lọc
            "data": logs_data          # Mảng dữ liệu chứa logs
        }
        return jsonify(response), 200

    except Exception as e:
        # Bắt lỗi, in thông báo lỗi và traceback để phục vụ gỡ lỗi
        print("Đã xảy ra lỗi khi lấy lịch sử thiết bị:", e)
        print(traceback.format_exc())  # In traceback để có ngữ cảnh chi tiết về lỗi
        # Trả về phản hồi JSON với thông báo lỗi
        return jsonify({"error": "Không thể lấy dữ liệu do lỗi"}), 500

    finally:
        # Bước 11: Đóng session cơ sở dữ liệu để giải phóng tài nguyên
        db.close()
        print("Đã đóng session cơ sở dữ liệu")  # Xác nhận đóng session cho việc gỡ lỗi
