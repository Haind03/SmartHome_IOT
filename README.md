# Smart Home

## I. Giao diện người dùng.

### 1. Giao diện dashboard

![alt text](https://raw.githubusercontent.com/Haind03/IOT/main/BaoCao/image-3.png)

### 2. Giao diện lịch sử điều khiển thiết bị- Action History

![alt text](https://raw.githubusercontent.com/Haind03/IOT/main/BaoCao/image-4.png)

### 3. Giao diện ghi lại dữ liệu Sensor theo thời gian thực- Data Sensor

![alt text](https://raw.githubusercontent.com/Haind03/IOT/main/BaoCao/image-5.png)

### 4. Giao diện profile

![alt text](https://raw.githubusercontent.com/Haind03/IOT/main/BaoCao/image-6.png)

# II. Sơ đồ Giao tiếp

1. **Thiết bị -> MQTT Broker -> Flask MQTT Client:** 
   - Thiết bị gửi dữ liệu lên MQTT broker.
   - Flask MQTT Client nhận dữ liệu từ MQTT broker.

2. **Flask MQTT Client -> Backend/WebSocket:**
   - Flask xử lý dữ liệu và gửi qua WebSocket hoặc HTTP API.
   - Cập nhật thông tin tới các client hoặc lưu trữ vào backend.

3. **Backend -> Flask -> MQTT Broker (nếu cần):**
   - Flask có thể gửi tin nhắn đến các thiết bị qua MQTT broker.
   - Publish tin nhắn đến các chủ đề tương ứng trên MQTT broker.

    ![alt text](https://raw.githubusercontent.com/Haind03/IOT/main/BaoCao/image-2.png)


### Kiến Trúc Hệ Thống

#### MQTT Broker
- **Kết nối:** Kết nối tới `mqtt://localhost:1993`.
- **Thông tin đăng nhập:** Yêu cầu đăng nhập với:
  - **Username:** `HaiND`
  - **Password:** `B21DCAT004`

#### Flask Server (HTTP Server)
- **Cổng:** Lắng nghe trên cổng `4444`.
- **Routes:** Xử lý các yêu cầu từ client với các route sau:
  - `/api/v1/sensor/*`
  - `/api/v1/device/*`

#### WebSocket
- **Máy chủ:** Được tạo trên cùng máy chủ với Flask.
- **Thư viện:** Sử dụng `eventlet` để quản lý luồng.
- **Chức năng:** 
  - Lắng nghe kết nối WebSocket từ client.
  - Hiển thị thông tin cảm biến theo thời gian thực.

#### Cơ Sở Dữ Liệu SQLite
- **Vị trí:** Tệp CSDL nằm ở thư mục gốc của server backend.
- **Bảng dữ liệu:**
  - `DataRealTime`: Lưu trữ dữ liệu cảm biến thời gian thực.
  - `DeviceHistory`: Lưu trữ lịch sử điều khiển thiết bị.

#### Giao Diện Web
- **Tính năng:**
  - Hiển thị đo lường theo thời gian thực của cảm biến DHT22.
  - Hiển thị thông tin lịch sử đo lường của cảm biến.
  - Hiển thị thông tin lịch sử điều khiển thiết bị.
  - Hỗ trợ lọc và tìm kiếm dữ liệu để hiển thị.


### Thiết Kế Database

Hệ thống bao gồm 2 bảng được sử dụng để lưu trữ dữ liệu của cảm biến và lịch sử điều khiển thiết bị, lần lượt là:

#### Bảng `DataRealTime`

```sql
CREATE TABLE `DataRealTime` (
`id` INT NOT NULL AUTO_INCREMENT,
`temp` VARCHAR(255) NOT NULL,
`humidity` INT NOT NULL,
`light` INT NOT NULL,
`timestamp` DATETIME NULL DEFAULT NULL,
PRIMARY KEY (`id`)
);
```

#### Bảng `DeviceHistory`

```sql
CREATE TABLE `DeviceHistory` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `device_name` VARCHAR(50) NOT NULL,
  `command` VARCHAR(50) NOT NULL,
  `status` VARCHAR(50) NOT NULL,
  `timestamp` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
);
```

## III. API document.

Nội dung chi tiết bên trong poshman.
`https://documenter.getpostman.com/view/39489332/2sAY4ye1DQ
`

[Tài liệu API](https://documenter.getpostman.com/view/39489332/2sAY4ye1DQ)

