# Dự án: Máy nhận diện màu sắc (Tracking color)
## Đặt vấn đề
### Lý do chọn đề tài: 
- Ý tưởng ban đầu: Giúp cho các bạn nam có thể nhận diện được màu son khi mua tặng người yêu.
- Phát triển ý tưởng: 
+ Hỗ trợ người mù màu: Máy nhận diện màu sắc có thể giúp người mù màu phân biệt các vật thể, quần áo, hoặc thực phẩm theo màu.
+ Phân loại sản phẩm trong nghiên cứu và sản xuất: Tự động hóa việc phân loại sản phẩm trong dây chuyền, như mẫu máu/mẫu xét nghiệm trong y tế; quần áo, phụ kiện trong thời trang;...
+ Nhận diện và kiểm tra: Từ việc phân loại sản phẩm, có thể tích hợp với các công nghệ khác nhằm đưa ra đánh giá khách quan về chất lượng, tình trạng sản phẩm. Ví dụ kiểm tra chất lượng cây lanh trong công nghiệp dệt may; kiểm tra màu sắc của mỹ phẩm để đảm bảo chất lượng và tính đồng đều;... 
### Lý do sử dụng ESP32-CAM:
- Hiệu năng xử lý: ESP32 có đủ hiệu năng để xử lý dữ liệu từ cảm biến màu như TCS34725, bao gồm đọc tín hiệu I2C và phân tích giá trị RGB cơ bản. Tốc độ 240 MHz và RAM 520 KB là dư thừa cho các thuật toán nhận diện màu.
- Độ ổn định và khả năng hoạt động trong thực tiễn: Hỗ trợ Arduino IDE và MicroPython, dễ dàng cho người mới hoặc các nhóm phát triển nhỏ.
- Khả năng mở rộng: Kết nối không dây tích hợp là điểm mạnh lớn nhất của ESP32. Điều này cho phép mở rộng dự án thành hệ thống IoT: Gửi dữ liệu màu sắc đến ứng dụng di động hoặc web/ Điều khiển máy từ xa.
- Hỗ trợ giao tiếp cảm biến: Số lượng I2C và UART nhiều hơn so với các vi mạch cơ bản (ATmega328P, RP2040). Lập trình dễ dàng, đặc biệt với Arduino IDE.
## Tổng quan nghiên cứu 
### Máy nhận diện màu sắc là gì?
- Một hệ thống sử dụng cảm biến để phát hiện và phân tích màu sắc của vật thể, hoạt động dựa trên cảm biến màu sắc kết hợp với bộ xử lý trung tâm (ESP32).
- Bao gồm:
+ ESP32-CAM
+ Màn I2C
+ FTDI
+ Thẻ nhớ Micro SD
+ Dây nối
- Tính năng nổi bật:
+ Phát hiện chính xác các màu sắc cơ bản.
+ Kết nối không dây qua WiFi/Bluetooth để mở rộng ứng dụng.
+ Tích hợp dễ dàng với các thiết bị IoT.
### Nguyên lý hoạt động:
- Trong môi trường ánh sáng ổn định, khi đưa vật có màu sắc đến camera, hình ảnh được thu nhận.
- Dữ liệu này được đưa vào ESP32-CAM để chuyển hình ảnh gốc sang không gian HSV.
- Sau khi xác định được màu cụ thể, ESP32-CAM xuất kết quả ra màn hình.
## Đánh giá sản phẩm
- Điểm mạnh:
+ Dễ lắp ráp, lập trình.
+ Hiệu quả vừa với chi phí thấp: Tổng chi phí: 305k, chưa kể chi phí màn hình.
+ Tính linh hoạt trong ứng dụng.
- Điểm yếu:
+ Chất lượng sản phẩm: Hiển thị chưa rõ nét; Độ nhạy chưa cao.
+ Giới hạn trong nhận diện màu sắc phức tạp: Chỉ nhận diện được các màu cơ bản.
+ Tính cạnh tranh thấp
- Tiềm năng phát triển:
+ Phát triển công nghệ: Tích hợp với hệ thống IoT để gửi dữ liệu màu sắc lên cloud/ Kết hợp với camera để phân tích màu sắc trong ảnh phức tạp.
+ Mở rộng lĩnh vực: Tối ưu hóa sản phẩm cho các môi trường công nghiệp khắt khe.
+ Tối ưu nguồn lực: Tối ưu hóa kích thước và tái phân bổ nguồn nhằm tăng hiệu năng.