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
# BẢNG TỔNG HỢP: TÀI SẢN - RỦI RO - BIỆN PHÁP & SƠ ĐỒ DFD

## 1. Sơ đồ Kiến trúc / DFD (Data Flow Diagram)

Sơ đồ dưới đây mô tả luồng dữ liệu (Data Flow) và cấu trúc mạng của hệ thống thiết bị IoT (Camera IP) khi phơi bày ra Internet (Không an toàn) so với giải pháp bảo vệ (An toàn).

```mermaid
graph TD
    subgraph Kiến trúc Không an toàn (Insecure)
        A1[Kẻ tấn công / Attacker] -- Scan & Exploit --> B1[Router/Modem]
        U1[Người dùng / User] -- HTTP/RTSP --> B1
        B1 -- Port Forwarding (NAT) --> C1[Camera IP]
        C1 -- Truy cập trái phép --> D1[(Dữ liệu Camera & Mạng LAN)]
    end

    subgraph Kiến trúc An toàn (Secure)
        A2[Kẻ tấn công / Attacker] -- Bị chặn (Blocked) -.-x B2[Firewall / Router]
        U2[Người dùng / User] -- Kết nối VPN (Mã hóa) --> B2
        B2 -- Tunnel --> C2[Camera IP]
        C2 -- Dữ liệu an toàn --> D2[(Dữ liệu Camera & Mạng LAN)]
    end
    
    style A1 fill:#ffcccc,stroke:#ff0000
    style C1 fill:#ffe6e6,stroke:#ff0000
    style A2 fill:#ffcccc,stroke:#ff0000
    style B2 fill:#ccffcc,stroke:#009900
    style C2 fill:#ccffcc,stroke:#009900
```

## 2. Bảng tích hợp: Tài sản - Rủi ro - Biện pháp (Asset - Risk - Mitigation Table)

| STT | Tài sản (Asset) | Rủi ro / Mối đe dọa (Risk/Threat) | Hậu quả (Impact) | Biện pháp giảm thiểu (Mitigation) |
| :-- | :--- | :--- | :--- | :--- |
| **1** | **Thông tin đăng nhập** (Username/Password) | Kẻ tấn công dò quét (Bruteforce) mật khẩu mặc định qua giao diện Web lộ lọt Internet. (OWASP T1, T2) | Mất quyền kiểm soát hệ thống; lộ lọt video. | Ép đổi mật khẩu khi thiết lập ban đầu; sử dụng mật khẩu mạnh; bật tính năng khóa tài khoản sau 5 lần nhập sai. |
| **2** | **Dữ liệu Video/Âm thanh** (Media Stream) | Luồng RTSP hoặc HTTP truyền tải không được mã hóa (Plaintext), bị chặn bắt (Sniffing/MitM) (OWASP T4). | Lộ lọt quyền riêng tư nghiêm trọng của người dùng. | Triển khai HTTPS cho giao diện Web; sử dụng RTSPS hoặc VPN để mã hóa toàn bộ đường truyền. |
| **3** | **Tài nguyên thiết bị** (CPU, Băng thông) | Thiết bị bị lây nhiễm phần mềm độc hại (Malware/Botnet như Mirai) qua cổng Telnet/SSH đang mở hớ hênh (OWASP T3). | Thiết bị chậm, sập; trở thành nguồn đi tấn công DDoS. | Vô hiệu hóa các cổng/dịch vụ không sử dụng (Telnet, SSH, UPnP). Đặt Firewall chặn truy cập từ IP lạ. |
| **4** | **Hệ điều hành / Firmware** | Lỗ hổng bảo mật (CVE) trong Firmware cũ bị khai thác để thực thi mã từ xa (RCE) (OWASP T2, T3). | Hacker chiếm đặc quyền Root, cài cắm Backdoor dai dẳng. | Bật tính năng tự động cập nhật Firmware (OTA); vô hiệu hóa giao diện dòng lệnh không bảo mật. |
| **5** | **Mạng nội bộ** (LAN) | Camera IP trở thành "bàn đạp" (Pivot point) để tấn công các thiết bị khác trong cùng mạng LAN. | Toàn bộ mạng bị xâm nhập, lây nhiễm Ransomware. | Cô lập Camera vào một mạng VLAN khách (Guest VLAN) riêng biệt; cấm Camera kết nối ngược lại các thiết bị nội bộ. |

## 3. Checklist Cấu hình an toàn (Phiên bản nháp)

Dưới đây là Checklist dành cho người dùng cuối hoặc kỹ thuật viên khi lắp đặt thiết bị IoT để ngăn ngừa các rủi ro trên:

### A. Thiết lập mạng & Tường lửa
- [ ] **Tắt tính năng UPnP trên Router:** Không cho phép Camera IP tự động mở cổng ra ngoài Internet.
- [ ] **Không Port Forwarding trực tiếp:** Tuyệt đối không NAT cổng 80, 443, 554, 23, 22 của Camera thẳng ra Internet.
- [ ] **Sử dụng VPN / Reverse Proxy:** Cấu hình VPN (như WireGuard, OpenVPN) trên Router hoặc NAS để kết nối về nhà trước khi xem Camera.
- [ ] **Cô lập thiết bị (VLAN):** Đưa toàn bộ thiết bị IoT (Camera, Smart Home) vào một mạng VLAN tách biệt với mạng dùng cho máy tính làm việc.

### B. Quản lý Tài khoản & Quyền truy cập
- [ ] **Đổi mật khẩu thiết bị ngay lập tức:** Không bao giờ dùng mật khẩu mặc định (`admin/admin`, `123456`).
- [ ] **Sử dụng tài khoản phân quyền:** Chỉ tạo tài khoản có quyền "Xem" (Viewer) để sử dụng hàng ngày trên điện thoại, giữ tài khoản Admin ở trạng thái offline.
- [ ] **Tắt các giao thức không dùng:** Truy cập vào phần cài đặt mạng của Camera và tắt bỏ Telnet, FTP, SSH, ONVIF (nếu không dùng đầu ghi).

### C. Duy trì & Cập nhật
- [ ] **Kiểm tra bản vá:** Truy cập website nhà sản xuất tối thiểu 6 tháng/lần để kiểm tra và tải về Firmware mới nhất.
- [ ] **Reboot định kỳ:** Bật tính năng "Auto Reboot" hàng tuần trên Camera (giúp làm mới bộ nhớ RAM, loại bỏ một số mã độc hoạt động trên bộ nhớ tạm).
- [ ] **Đăng ký nhận thông báo:** Đăng ký email trên trang chủ hãng để nhận thông báo khẩn cấp khi có lỗ hổng 0-day bị phát hiện.
