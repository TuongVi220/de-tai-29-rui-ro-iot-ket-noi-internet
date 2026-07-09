Đề tài 29: Rủi ro thiết bị IoT kết nối trực tiếp Internet
IoT SecurityOWASP ISVSSTRIDE Model

Chào mừng đến với repository lưu trữ tài liệu nghiên cứu và thực hành của Đề tài 29: Đánh giá rủi ro thiết bị IoT khi mở cổng trực tiếp ra Internet. Dự án này được thực hiện nhằm cung cấp một cái nhìn chuyên sâu và thực tiễn về những sai lầm phổ biến trong triển khai thiết bị IoT (điển hình là Camera IP) và cách khắc phục.

Giới thiệu (Introduction)
Sự phát triển mạnh mẽ của IoT mang lại nhiều tiện ích, nhưng một sai lầm chết người thường xuyên xảy ra ở các doanh nghiệp vừa và nhỏ (SME) hoặc người dùng gia đình là: Mở cổng thiết bị IoT (Port Forwarding) trực tiếp ra Internet.

Hành động này gỡ bỏ lớp bảo vệ tự nhiên của mạng nội bộ, biến thiết bị thành "con mồi" cho các công cụ dò quét toàn cầu như Shodan. Kết hợp với việc sử dụng mật khẩu mặc định, firmware cũ không được vá lỗi, thiết bị IoT dễ dàng bị chiếm quyền điều khiển, rò rỉ dữ liệu, hoặc trở thành một phần của các mạng Botnet tàn phá (ví dụ: Mirai).

Repository này phân tích chi tiết bề mặt tấn công đó và đưa ra các thiết kế kiến trúc an toàn, tuân thủ các chuẩn mực quốc tế.

Mục tiêu dự án (Objectives)

Đánh giá rủi ro (Risk Assessment): Phân tích các vector tấn công khi mở port thiết bị dựa trên mô hình STRIDE và tính điểm CVSS.

So sánh mô hình (Architecture Comparison): Xây dựng sơ đồ đối chiếu giữa việc triển khai sai (lộ lọt trực tiếp) và triển khai chuẩn bảo mật.

Đề xuất giải pháp (Security Solutions): Hướng dẫn thiết lập VPN, Firewall, và Reverse Proxy/Cloud Relay có xác thực.\

Chuẩn hóa quy trình (Standardization): Biên soạn Checklist cấu hình và quản lý thiết bị an toàn dựa trên OWASP.

Cấu trúc Repository (Repository Structure)

📁 /docs - Chứa các tài liệu tiểu luận, slide thuyết trình và báo cáo.

📁 /diagrams - Chứa mã nguồn (Mermaid) và hình ảnh sơ đồ triển khai kiến trúc (sai/đúng).

📁 /checklists - Chứa biểu mẫu, checklist cấu hình an toàn cho người triển khai.

pham_vi_tai_san_rui_ro.md - Danh sách tài sản và Bảng phân tích ma trận rủi ro (Risk Matrix).

 de_cuong_tieu_luan.md - Đề cương chi tiết của tiểu luận.
 
 Phương pháp và Tiêu chuẩn áp dụng (Methodology & Standards)
Dự án này sử dụng các khung chuẩn bảo mật uy tín trên thế giới làm kim chỉ nam:

OWASP Internet of Things Project: Nhận diện các lỗ hổng IoT phổ biến (Top 10 IoT Vulnerabilities).

OWASP ISVS (IoT Security Verification Standard): Tiêu chuẩn xác minh bảo mật hệ sinh thái IoT.

OWASP ISTG (IoT Security Testing Guide): Hướng dẫn kiểm thử bảo mật cho thiết bị.

NISTIR 8259 & ENISA IoT Baseline: Khuyến nghị quản trị và cấu hình an toàn mạng.

📝 Ví dụ kịch bản (Case Study)
Dự án sử dụng Camera IP (IP Camera) làm thiết bị ví dụ xuyên suốt:

Kịch bản lỗi: Camera IP được NAT Port 80/554 ra Internet $\rightarrow$ Attacker dùng Shodan quét IP $\rightarrow$ Brute-force mật khẩu mặc định $\rightarrow$ Chiếm quyền xem camera & leo thang đặc quyền.
Kịch bản an toàn: Đưa Camera IP vào VLAN cô lập $\rightarrow$ Chặn toàn bộ kết nối Inbound $\rightarrow$ Yêu cầu truy cập qua OpenVPN/WireGuard Server $\rightarrow$ Attacker không thể định vị được cổng dịch vụ từ bên ngoài.
