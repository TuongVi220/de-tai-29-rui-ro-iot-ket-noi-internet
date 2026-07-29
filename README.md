# Đánh giá rủi ro thiết bị IoT kết nối trực tiếp Internet

## Giới thiệu

Đây là repository lưu trữ toàn bộ tài liệu, cấu hình và kết quả của đề tài cuối kỳ môn **Bảo mật trong IoT**.

Đề tài tập trung phân tích và đánh giá rủi ro của việc cấu hình phơi bày thiết bị IP Camera trực tiếp ra Internet (thông qua Port Forwarding). Hệ thống sử dụng một máy chủ Web Python để giả lập môi trường IP Camera có lỗ hổng xác thực cơ bản (Basic Auth). Thông qua đó, đề tài thực hiện các bài kiểm thử bằng công cụ chuyên dụng nhằm minh chứng lỗ hổng, đồng thời đề xuất giải pháp phòng thủ ứng dụng đường hầm mã hóa (VPN) để bảo vệ mạng nội bộ.

---

## Mục tiêu

- Xây dựng thành công môi trường giả lập IP Camera trên Localhost phục vụ việc kiểm thử an toàn.
- Chứng minh mức độ nguy hiểm của kỹ thuật chuyển tiếp cổng (Port Forwarding) thông qua việc bị quét mở hớ hênh.
- Minh chứng rủi ro lộ lọt gói tin và bẻ khóa mật khẩu khi giao thức truyền tải thiếu mã hóa và thiếu cơ chế chống tấn công vét cạn.
- Đề xuất và xây dựng một bộ Checklist cấu hình an toàn bằng Mạng riêng ảo (VPN/VLAN) cho người dùng triển khai.

---

## Công nghệ sử dụng

- Python (Giả lập Web Server Camera)
- Nmap / Zenmap (Quét mạng và phát hiện dịch vụ)
- Wireshark (Bắt và phân tích luồng gói tin)
- Burp Suite (Thực thi tấn công vét cạn Brute-force)
- VPN (OpenVPN / WireGuard)
- HTTP / Basic Authentication

---

## Cấu trúc repository

```
.
├── configs/         # Lưu trữ cấu hình VPN mẫu và Checklist bảo mật
├── images/          # Lưu trữ sơ đồ mạng, hình ảnh kiến trúc báo cáo
├── references/      # Lưu trữ tài liệu tham khảo, chuẩn OWASP
├── report/          # Lưu trữ báo cáo cuối kỳ (Word, PDF) và Slide
├── results/         # Lưu trữ kết quả thực nghiệm, hình ảnh chứng minh
├── src/             # Lưu trữ mã nguồn Python giả lập IP Camera
└── README.md        # File hướng dẫn và giới thiệu đề tài
```
