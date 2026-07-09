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
