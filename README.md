# Smart Home

## I. Mô tả hệ thống

### Mục Đích
Hệ thống sử dụng các cảm biến để thông báo nhiệt độ, độ ẩm và ánh sáng cho người dùng thông qua một trang web có thể truy cập trong mạng LAN. Trang web cung cấp các thông tin về nhiệt độ, độ ẩm và ánh sáng với giao diện dashboard dễ nhìn, cho phép người dùng xem trực tiếp các thông tin này theo thời gian thực.

### Các Thiết Bị Sử Dụng Trong Hệ Thống

#### Phần Cứng
- 1 kit ESP8266 NodeMCU 0.9
- 1 cảm biến nhiệt độ và độ ẩm DHT22
- 1 cảm biến ánh sáng
- 3 đèn LED
- 1 bảng mạch
- Các loại dây dẫn đi kèm

#### Phần Mềm
- PlatformIO trên VSCode chạy trên nền Arduino
- Mosquitto server trên Windows
- Framework Flask + Flask-SocketIO (Backend)
- Framework ReactJS (Client)


## II. MQTT

Cài đặt `mqtt` set username và password cho người dùng.

```
C:\Program Files\mosquitto>mosquitto_passwd.exe -c "D:\PTIT_Project\IOTapp\mosquitto\passwdfile.txt" HaiND
Password:
Reenter password:
```

Setting port và sử dụng passwordfile.txt trong file config mosquitto.

```
listener 1993 0.0.0.0
password_file D:\PTIT_Project\IOTapp\mosquitto\passwdfile.txt
allow_anonymous false
```

Kết quả sau khi sửa port và sử dụng với conf mới.

```
C:\Program Files\mosquitto>mosquitto.exe -c mosquitto.conf -v
1730648360: mosquitto version 2.0.20 starting
1730648360: Config loaded from mosquitto.conf.
1730648360: Opening ipv4 listen socket on port 1993.
1730648360: mosquitto version 2.0.20 running
```

## II. Xây dựng flash và esptool.

### Ardruino and device.
Cài đặt esptools trên `https://micropython.org/download/ESP8266_GENERIC/`

```
pip install esptool
```
Sử dụng json này cho vào url để cài esp8266 trên arduno và cài đặt driver cho port arduino ide.
```json
https://arduino.esp8266.com/stable/package_esp8266com_index.json
```

```driver
https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads
```

Cài arduino và xem cổng trên máy kết nối, check cổng kết nối trên device. Thường sẽ là COM3.

![alt text](/Baocao/image.png)

### Flash esp8266.
```
esptool --port COM3 erase_flash
esptool --port COM3 --baud 115200 write_flash --flash_size=detect 0x0 ESP8266_GENERIC-20240602-v1.23.0.bin
```

Sau khi import file vào esp8266 tiếp tục cài mpremote
```
pip install mpremote
```

Tiếp tục thêm file vào esp8266

```
mpremote connect COM3 fs cp simple.py :
mpremote connect COM3 fs cp esp8266.py :
mpremote connect COM3 run esp8266.py
```


Kết Quả:
```
PS D:\PTIT_Project\IOTapp\app\esp8266\dev_mqtt> esptool --port COM3 erase_flash
esptool.py v4.8.1
Serial port COM3
Connecting....
Detecting chip type... Unsupported detection protocol, switching and trying again...
Connecting....
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
Crystal is 26MHz
MAC: ec:64:c9:d3:dd:51
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 7.5s
Hard resetting via RTS pin...
PS D:\PTIT_Project\IOTapp\app\esp8266\dev_mqtt> esptool --port COM3 --baud 115200 write_flash --flash_size=detect 0x0 ESP8266_GENERIC-20240602-v1.23.0.bin
esptool.py v4.8.1
Serial port COM3
Connecting....
Detecting chip type... Unsupported detection protocol, switching and trying again...
Connecting....
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
Crystal is 26MHz
MAC: ec:64:c9:d3:dd:51
Uploading stub...
Running stub...
Stub running...
Configuring flash size...
Auto-detected Flash size: 4MB
Flash will be erased from 0x00000000 to 0x0009afff...
Flash params set to 0x0040
Compressed 633048 bytes to 423611...
Wrote 633048 bytes (423611 compressed) at 0x00000000 in 37.8 seconds (effective 134.0 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```

- Sau khi nạp xong test thử và đã nhận được thông tin từ firmware.

    ![alt text](/Baocao/image-1.png)

## IV. Giao diện người dùng.

### 1. Giao diện dashboard

![alt text](/Baocao/image-3.png)

### 2. Giao diện lịch sử điều khiển thiết bị- Action History

![alt text](/Baocao/image-4.png)

### 3. Giao diện ghi lại dữ liệu Sensor theo thời gian thực- Data Sensor

![alt text](/Baocao/image-5.png)

### 4. Giao diện profile

![alt text](/Baocao/image-6.png)

## V. Xây dựng mô hình hệ thống.

### Sơ đồ Giao tiếp

1. **Thiết bị -> MQTT Broker -> Flask MQTT Client:** 
   - Thiết bị gửi dữ liệu lên MQTT broker.
   - Flask MQTT Client nhận dữ liệu từ MQTT broker.

2. **Flask MQTT Client -> Backend/WebSocket:**
   - Flask xử lý dữ liệu và gửi qua WebSocket hoặc HTTP API.
   - Cập nhật thông tin tới các client hoặc lưu trữ vào backend.

3. **Backend -> Flask -> MQTT Broker (nếu cần):**
   - Flask có thể gửi tin nhắn đến các thiết bị qua MQTT broker.
   - Publish tin nhắn đến các chủ đề tương ứng trên MQTT broker.

    ![alt text](/Baocao/image-2.png)


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

## VI. Mô tả sơ đồ luồng hoạt động.


## VII. API document.

Nội dung chi tiết bên trong poshman.
`https://documenter.getpostman.com/view/39489332/2sAY4ye1DQ
`

[Tài liệu API](https://documenter.getpostman.com/view/39489332/2sAY4ye1DQ)

