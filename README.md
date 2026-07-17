# Đề tài 29: Đánh giá Rủi ro Thiết bị IoT Kết nối Trực tiếp Internet
Dự án nghiên cứu và phân tích các rủi ro bảo mật khi thiết bị IoT (điển hình là Camera IP) được mở cổng trực tiếp ra không gian mạng, đồng thời thiết kế giải pháp cấu hình an toàn dựa trên hướng dẫn tiêu chuẩn của OWASP, NIST và ENISA.
---
## 1. Thành phần và kiến trúc bảo vệ
Hệ thống cung cấp giải pháp đồng bộ và các hàng rào phòng thủ nhiều lớp nhằm ngăn chặn rủi ro khi thiết bị IoT phải giao tiếp với Internet:
* **Che giấu bề mặt tấn công**: Vô hiệu hóa tính năng Port Forwarding (NAT) và UPnP, đặt thiết bị vào VLAN nội bộ (Isolation) để cô lập khỏi mạng máy tính.
* **Xác thực và phân quyền**: Cấu hình Reverse Proxy đảm nhận quá trình xác thực đa yếu tố (MFA) trước khi cho phép truy cập luồng dữ liệu của thiết bị.
* **Mã hóa kênh truyền**: Bắt buộc mọi kết nối từ xa phải được mã hóa thông qua đường hầm ảo (VPN Gateway như OpenVPN/WireGuard) hoặc TLS 1.2+ để chống nghe lén.
* **Đánh giá rủi ro chủ động**: Sử dụng mô hình STRIDE để nhận diện đe dọa, đo lường điểm số nghiêm trọng bằng CVSS và ánh xạ các tiêu chí kiểm thử theo OWASP ISVS.
---
## 2. Yêu cầu hệ thống và công cụ cần thiết
Toàn bộ quy trình đánh giá, vẽ sơ đồ và thực hành bảo mật được dựa trên các bộ khung chuẩn và công cụ sau:
| Hạng mục | Công cụ / Tiêu chuẩn áp dụng |
| :--- | :--- |
| Khung lý thuyết & Đánh giá | OWASP IoT Project, OWASP ISVS, OWASP ISTG |
| Mô hình hóa rủi ro | Mô hình STRIDE, Hệ thống điểm CVSS v3.1 |
| Trực quan hóa kiến trúc mạng | Markdown, Mermaid JS |
| Công cụ dò quét và kiểm thử | Nmap, Shodan (chỉ dùng cho mục đích minh họa) |
---
## 3. Hướng dẫn thực hành và triển khai cấu hình
> ⚠️ Mọi thao tác dò quét, khai thác thử nghiệm (pentest) phải được thực thi **cục bộ** trên môi trường Lab mô phỏng (Local network) hoặc thiết bị thuộc quyền sở hữu hợp pháp. Không quét các IP công cộng trên Internet.
>
> # PHÂN TÍCH RỦI RO & BẢNG STRIDE / CVSS (Bản nháp)

## 1. Phạm vi hệ thống (System Scope)
*   **Hệ thống phân tích:** Một thiết bị IP Camera được triển khai tại hộ gia đình hoặc văn phòng nhỏ.
*   **Trạng thái kết nối:** Camera được kết nối với mạng nội bộ (LAN) và được người dùng cấu hình "Mở cổng" (Port Forwarding / NAT) trên Router để có thể xem video và quản lý từ xa qua Internet.
*   **Các cổng (Ports) lộ lọt ra Internet:**
    *   `80` hoặc `443` (Giao diện Web quản trị).
    *   `554` (Luồng dữ liệu video RTSP).
    *   *(Tùy chọn)* `23` (Telnet) hoặc `22` (SSH) - thường bị mở vô ý.

## 2. Danh sách tài sản (Asset List)
Nhận diện các tài sản có giá trị cần được bảo vệ trong hệ thống:
1.  **Thông tin xác thực (Credentials):** Username và Password dùng để đăng nhập vào giao diện Web và tài khoản RTSP.
2.  **Dữ liệu hình ảnh/video:** Các luồng video trực tiếp (Live stream) hoặc dữ liệu đã ghi lại liên quan đến quyền riêng tư của cá nhân/tổ chức.
3.  **Tài nguyên thiết bị (CPU/RAM/Băng thông):** Sức mạnh xử lý và băng thông mạng của Camera.
4.  **Mạng nội bộ (LAN):** Các thiết bị khác đang kết nối chung mạng với Camera IP (như máy tính, NAS).
5.  **Hệ điều hành / Firmware:** Trạng thái nguyên bản và an toàn của hệ thống chạy trên Camera.

## 3. Ma trận STRIDE & Chấm điểm rủi ro (Risk Register)
Dựa trên OWASP IoT Top 10, dưới đây là bảng phân tích các mối đe dọa theo mô hình STRIDE và đánh giá mức độ nghiêm trọng bằng CVSS (ước lượng):

| Ký tự | Mối đe dọa (Threat) | Mô tả lỗ hổng trên IP Camera lộ lọt Internet | OWASP IoT Link | Mức độ CVSS (Ước lượng) |
| :--- | :--- | :--- | :--- | :--- |
| **S** | Spoofing<br>*(Giả mạo)* | Kẻ tấn công sử dụng mật khẩu mặc định (admin/admin) hoặc brute-force để giả mạo chủ sở hữu đăng nhập vào giao diện Web. | T1: Mật khẩu yếu/Mặc định | **Cao (7.5 - 8.5)**<br>*(Dễ khai thác, tác động lớn)* |
| **T** | Tampering<br>*(Thay đổi)* | Kẻ tấn công lợi dụng giao diện Web bị lỗi để tải lên một bản cập nhật Firmware giả mạo (chứa mã độc) nhằm cài cắm backdoor. | T3: Các dịch vụ mạng không an toàn | **Nghiêm trọng (9.0 - 9.8)**<br>*(Mất kiểm soát thiết bị)* |
| **R** | Repudiation<br>*(Chối bỏ)* | Thiết bị Camera không có chức năng lưu lại lịch sử truy cập (Log), dẫn đến việc khi bị hack, quản trị viên không có dấu vết để điều tra. | T9: Thiết lập mặc định không an toàn | **Thấp (3.0 - 4.0)**<br>*(Tác động gián tiếp)* |
| **I** | Information Disclosure<br>*(Lộ lọt thông tin)*| Luồng video (RTSP) hoặc trang đăng nhập Web không sử dụng mã hóa (chỉ dùng HTTP/RTSP thường). Kẻ tấn công có thể chặn bắt (Sniffing) dữ liệu trên mạng. | T4: Thiếu mã hóa dữ liệu | **Trung bình (5.5 - 6.5)**<br>*(Phụ thuộc vị trí chặn bắt)* |
| **D** | Denial of Service<br>*(Từ chối dịch vụ)* | Thiết bị bị lây nhiễm malware (VD: Mirai) biến thành một phần của mạng Botnet, làm nghẽn băng thông mạng hoặc đánh sập chính Camera. | T3 & T6: Thiếu cơ chế bảo mật | **Cao (7.0 - 8.0)**<br>*(Mất tính khả dụng)* |
| **E** | Elevation of Privilege<br>*(Leo thang đặc quyền)*| Giao diện Web có lỗi Injection (VD: Command Injection). Kẻ tấn công gửi payload qua HTTP để chiếm quyền root trên hệ điều hành Linux của Camera, từ đó làm bàn đạp tấn công mạng LAN. | T2: Giao diện không an toàn | **Nghiêm trọng (9.0 - 10.0)**<br>*(Tấn công sâu vào mạng)* |

## 4. Checklist giảm thiểu rủi ro (Phiên bản nháp)
Đây là danh sách kiểm tra các biện pháp cấu hình an toàn, được trích xuất từ các khuyến nghị của OWASP ISTG:

### 4.1. Về mặt Mạng lưới (Network & Exposure)
- [ ] **KHÔNG** mở cổng (Port Forwarding/NAT) thiết bị IP Camera trực tiếp ra ngoài Internet.
- [ ] Vô hiệu hóa tính năng **UPnP** (Universal Plug and Play) trên Router để ngăn thiết bị tự động mở cổng.
- [ ] Sử dụng **VPN (Virtual Private Network)** trên Router để kết nối an toàn từ xa thay vì truy cập trực tiếp vào Camera.

### 4.2. Về Xác thực & Ủy quyền (Authentication)
- [ ] Ngay khi cài đặt, **THAY ĐỔI** mật khẩu mặc định của thiết bị. Sử dụng mật khẩu mạnh (trên 12 ký tự, bao gồm số và ký tự đặc biệt).
- [ ] Thiết lập tài khoản khách (Guest/View only) cho những người chỉ cần xem video, KHÔNG dùng tài khoản Admin cho nhu cầu xem hàng ngày.
- [ ] Đổi tên tài khoản mặc định "admin" thành một tên khác (nếu firmware cho phép).

### 4.3. Về Quản lý thiết bị & Dịch vụ (Services & Maintenance)
- [ ] Tắt toàn bộ các dịch vụ mạng không sử dụng (Telnet, SSH, FTP) trong phần cài đặt của Camera.
- [ ] Bật chế độ truy cập HTTPS và RTSPS (có mã hóa TLS/SSL) nếu Camera hỗ trợ.
- [ ] Kiểm tra và cập nhật Firmware lên phiên bản mới nhất từ trang chủ của nhà sản xuất.
- [ ] Cấu hình khởi động lại (Reboot) định kỳ tự động để xóa bỏ mã độc chạy trên RAM (như biến thể Mirai).

