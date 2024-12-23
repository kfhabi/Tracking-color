import cv2
import urllib.request
import numpy as np
import time

def nothing(x):
    pass

# URL với độ phân giải QQVGA (160x120)
url = 'http://172.16.24.172/cam-lo.jpg'  # Thay URL phù hợp nếu cần

# Tạo cửa sổ hiển thị cho "live transmission"
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)

# Định nghĩa các ngưỡng HSV cho các màu
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

lower_yellow = np.array([22, 93, 0])
upper_yellow = np.array([45, 255, 255])

lower_blue = np.array([94, 80, 2])
upper_blue = np.array([126, 255, 255])

lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 30])

lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 20, 255])

while True:
    try:
        # Tải dữ liệu từ URL
        img_resp = urllib.request.urlopen(url)
        img_data = img_resp.read()

        # Kiểm tra xem dữ liệu hình ảnh có trống không
        if len(img_data) == 0:
            print("No data received from URL")
            continue

        # Giải mã ảnh
        imgnp = np.array(bytearray(img_data), dtype=np.uint8)
        frame = cv2.imdecode(imgnp, cv2.IMREAD_COLOR)

        # Kiểm tra xem frame có hợp lệ không
        if frame is None or frame.size == 0:
            print("Error: Frame is empty or not valid")
            continue  # Tiếp tục vòng lặp mà không xử lý thêm

        # Áp dụng bộ lọc Gaussian để giảm nhiễu
        frame = cv2.GaussianBlur(frame, (5, 5), 0)

        # Chuyển đổi ảnh sang không gian màu HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    except (urllib.error.URLError, cv2.error) as e:
        print(f"Error: {e}")
        time.sleep(2)  # Đợi một chút trước khi thử lại
        continue  # Tiếp tục vòng lặp nếu có lỗi khi tải hoặc giải mã ảnh

    # Tạo mask cho mỗi màu
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    # Kết hợp các mask
    mask = mask_red | mask_yellow | mask_blue | mask_black | mask_white

    # Tìm các đối tượng trong mask của mỗi màu
    cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Xử lý các đối tượng trong mask
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 2000:  # Lọc các đối tượng có diện tích nhỏ
            # Vẽ các đường viền và xác định màu
            (x, y, w, h) = cv2.boundingRect(c)
            color = "unknown"
            color_bgr = (255, 255, 255)
            if cv2.countNonZero(cv2.inRange(hsv[y:y+h, x:x+w], lower_red1, upper_red1) | cv2.inRange(hsv[y:y+h, x:x+w], lower_red2, upper_red2)) > 0:
                color = "red"
                color_bgr = (0, 0, 255)
                cv2.drawContours(frame, [c], -1, color_bgr, 3)
            elif cv2.countNonZero(cv2.inRange(hsv[y:y+h, x:x+w], lower_yellow, upper_yellow)) > 0:
                color = "yellow"
                color_bgr = (0, 255, 255)
                cv2.drawContours(frame, [c], -1, color_bgr, 3)
            elif cv2.countNonZero(cv2.inRange(hsv[y:y+h, x:x+w], lower_blue, upper_blue)) > 0:
                color = "blue"
                color_bgr = (255, 0, 0)
                cv2.drawContours(frame, [c], -1, color_bgr, 3)
            elif cv2.countNonZero(cv2.inRange(hsv[y:y+h, x:x+w], lower_black, upper_black)) > 0:
                color = "black"
                color_bgr = (0, 0, 0)
                cv2.drawContours(frame, [c], -1, color_bgr, 3)
            elif cv2.countNonZero(cv2.inRange(hsv[y:y+h, x:x+w], lower_white, upper_white)) > 0:
                color = "white"
                color_bgr = (255, 255, 255)
                cv2.drawContours(frame, [c], -1, (0, 0, 0), 3)  # Draw white contours with black for better visibility

            # Thay print bằng cv2.putText để hiển thị màu trên hình ảnh
            # Thêm lớp nền màu cho chữ
            cv2.rectangle(frame, (x, y-30), (x + w, y), color_bgr, -1)
            cv2.putText(frame, color, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0) if color == "white" else (255, 255, 255), 2)

    # Kết hợp ảnh với mask
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Làm sắc nét hình ảnh
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    res = cv2.filter2D(res, -1, kernel)

    # Hiển thị hình ảnh
    cv2.imshow("live transmission", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)

    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
