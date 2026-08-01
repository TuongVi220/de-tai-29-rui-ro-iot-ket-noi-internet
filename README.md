# Đề tài 29 - Rủi ro thiết bị IoT kết nối trực tiếp Internet

Repository mô phỏng cục bộ quy trình đánh giá rủi ro an toàn thông tin đối với các thiết bị IoT (cụ thể là IP Camera) khi bị cấu hình phơi bày trực tiếp ra Internet. Đề tài tập trung vào việc mô phỏng rủi ro dò quét mạng (Port Scanning), đánh hơi gói tin (Sniffing) và bẻ khóa tài khoản (Brute-force). Đây là lab dùng dữ liệu giả lập (Python Web Server); hoàn toàn không kết nối, rà quét hoặc tấn công trên bất kỳ hệ thống thật nào ngoài môi trường Localhost.

## Thành viên và học phần

- Sinh viên: Phạm Thị Tường Vi - MSSV 231A010502
- Lớp học phần: 253INT441001 (Bảo mật trong IoT)
- Giảng viên hướng dẫn: ThS. Hồ Nhựt Minh
- Repository: <https://github.com/TuongVi220/de-tai-29-rui-ro-iot-ket-noi-internet>

## Phạm vi bản nộp cuối kỳ

Bộ nộp chính thức gồm báo cáo DOCX, bản PDF xuất từ cùng báo cáo và repository GitHub công khai này. Theo hướng dẫn trực tiếp của giảng viên, đề tài không phải nộp slide; repository vì vậy không chứa thư mục hoặc tệp trình chiếu.

## Cấu trúc repository

```text
configs/                    Bộ Checklist cấu hình bảo mật (VPN/VLAN, tắt NAT)
images/                     Sơ đồ kiến trúc mạng, biểu đồ lý thuyết
references/                 Danh mục tài liệu tham khảo và chuẩn OWASP
report/                     Báo cáo tiểu luận DOCX và PDF cuối kỳ
results/                    Minh chứng thực nghiệm (Log Nmap, Wireshark, Burp Suite)
src/                        Mã nguồn Python giả lập Web Server (IP Camera)
```

## Tiến độ và commit theo tuần

Bảng dưới đây ánh xạ tiến độ với lịch sử commit thực tế. Những tuần không có bản nộp riêng được ghi rõ, không tạo commit hồi tố.

| Tuần | Trạng thái thực tế | Nội dung/minh chứng |
|---|---|---|
| Tuần 01 | Đã thực hiện | Khởi tạo repo, README và cấu trúc ban đầu. Xác định đề tài 29. |
| Tuần 02 | Đã thực hiện | Xây dựng cơ sở lý thuyết, phân tích mô hình STRIDE và Attack Tree. |
| Tuần 03 | Không nộp bản riêng | Chương 2–3 được hoàn thiện tích lũy trong báo cáo cuối. Lập trình src/fake_camera.py. |
| Tuần 04 | Tích lũy trong bản cuối | Chương 4, thực nghiệm trên Localhost bằng Nmap, Wireshark, Burp Suite và chụp minh chứng. |
| Tuần 05 | Tích lũy trong bản cuối | Chương 5–6, đánh giá rủi ro và xuất bản Checklist phòng thủ. |
| Tuần 06 | Hoàn thành | Hoàn thiện bản báo cáo DOCX/PDF cuối kỳ và rà soát, đồng bộ toàn bộ lên repository. |

## Mô hình bảo vệ

1. Router được cấu hình vô hiệu hóa hoàn toàn cơ chế Port Forwarding (NAT) trực tiếp vào IP Camera để chặn đứng rà quét từ Internet.
2. Thiết bị IP Camera được cô lập vào một mạng ảo riêng biệt (VLAN) chuyên dụng cho IoT, không giao tiếp tự do với mạng LAN chính chứa thiết bị cá nhân.
3. Người dùng từ xa cài đặt VPN Client và tiến hành quy trình xác thực an toàn với máy chủ VPN Gateway đặt tại biên mạng.
4. Sau khi xác thực thành công, một đường hầm mã hóa (VPN Tunnel) được thiết lập nối thẳng thiết bị cá nhân vào mạng nội bộ.
5. Toàn bộ lưu lượng truyền phát video (RTSP) và xác thực (HTTP Basic Auth) được đóng gói và mã hóa an toàn chạy ngầm bên trong đường hầm VPN.
6. Camera chỉ tiếp nhận giao tiếp cục bộ, triệt tiêu hoàn toàn nguy cơ bị bắt lén gói tin (Sniffing) và tấn công dò mật khẩu (Brute-force) từ môi trường Internet.

Kiến trúc mạng riêng ảo VPN đóng vai trò là lớp bảo vệ mã hóa kênh truyền cốt lõi ở vòng ngoài. Việc thay đổi mật khẩu mặc định thành chuỗi mạnh là cơ chế xác thực bổ sung trên thiết bị, không thay thế cho khả năng ẩn danh thiết bị của VPN.

## Cách chạy demo

Yêu cầu máy tính cài đặt Python 3.10+ cùng các công cụ kiểm thử: Nmap (Zenmap), Wireshark và Burp Suite Community Edition.

### 1. Giả lập mục tiêu (IP Camera)
1. Mở Command Prompt tại thư mục `src/` của dự án.
2. Khởi chạy Web Server đóng vai trò là IP Camera mục tiêu:
   ```powershell
   python fake_camera.py
   ```
   *(Lưu ý: Không tắt cửa sổ Terminal này trong suốt quá trình kiểm thử).*

### 2. Kịch bản 1: Quét mạng (Port Scan) bằng Nmap
1. Mở giao diện Zenmap, mục **Target** nhập: `localhost`.
2. Mục **Command**, gõ lệnh: `nmap -p 8081 localhost` và nhấn **Scan**.
3. Kết quả trả về `8081/tcp open http`, xác nhận lỗ hổng do cấu hình hở cổng (mô phỏng rủi ro Port Forwarding).

### 3. Kịch bản 2: Bắt gói tin (Sniffing) bằng Wireshark
1. Mở Wireshark, chọn card mạng `Adapter for loopback traffic capture`.
2. Mở trình duyệt truy cập `http://localhost:8081`, đăng nhập bằng tài khoản `admin` / mật khẩu `admin`.
3. Tại Wireshark, lọc gói tin với cú pháp `tcp.port == 8081`. 
4. Click chuột phải vào gói tin HTTP (GET), chọn **Follow -> HTTP Stream**. 
5. Thông tin đăng nhập bị lộ rõ dưới dạng Base64 (`Authorization: Basic YWRtaW46YWRtaW4=`), minh chứng cho rủi ro truyền tải không mã hóa HTTPS.

### 4. Kịch bản 3: Vét cạn mật khẩu (Brute-force) bằng Burp Suite
1. Bật Burp Suite (bật tính năng **Intercept is on** tại thẻ Proxy), dùng trình duyệt tích hợp mở trang `http://localhost:8081`.
2. Gói tin bị chặn lại, click chuột phải chọn **Send to Intruder**.
3. Tại thẻ **Intruder > Positions**, cấu hình biến payload cho chuỗi Authorization: `Authorization: Basic §payload§`.
4. Tại thẻ **Payloads**, nạp danh sách từ điển (vd: *admin:1234, admin:password, admin:admin, root:root*). Thiết lập **Payload Processing** tự động mã hóa chuỗi thành Base64.
5. Nhấn **Start Attack**. Kết quả trả về cho thấy payload `admin:admin` có mã HTTP Status là `200 OK` (Hack thành công), trong khi các payload khác trả về `401 Unauthorized`. Thiết bị không hề tự động khóa tài khoản sau nhiều lần thử sai.
