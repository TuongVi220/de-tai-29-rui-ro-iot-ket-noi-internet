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
      
# PHƯƠNG PHÁP, MÔ HÌNH, THIẾT KẾ & KẾ HOẠCH ĐÁNH GIÁ

## 1. Phương pháp nghiên cứu (Methodology)
Đề tài sử dụng phương pháp luận lai (Hybrid Methodology), kết hợp giữa việc mô hình hóa rủi ro và đánh giá dựa trên tiêu chuẩn bảo mật thực tiễn:
*   **Mô hình hóa mối đe dọa (Threat Modeling):** Áp dụng mô hình **STRIDE** của Microsoft để phân tích một cách có hệ thống các nguy cơ tiềm ẩn trên luồng dữ liệu (Data Flow) của thiết bị IoT khi mở trực tiếp ra Internet.
*   **Định lượng rủi ro:** Sử dụng **CVSS (Common Vulnerability Scoring System)** để quy đổi các mối đe dọa thành điểm số, từ đó phân loại mức độ nghiêm trọng (Thấp, Trung bình, Cao, Nghiêm trọng) nhằm ưu tiên xử lý.
*   **Khung đánh giá tiêu chuẩn:** Dựa trên **OWASP IoT Security Testing Guide (ISTG)** và **OWASP IoT Top 10** để trích xuất các lỗ hổng thực tế, xây dựng checklist và tiêu chí đánh giá an toàn mạng.

## 2. Mô hình hệ thống (System Models)
Dựa theo khuyến nghị của OWASP ISTG, quá trình phân tích rủi ro sẽ xoay quanh hai mô hình chính:
*   **Mô hình Thiết bị (IoT Device Model):** 
    *   Tài sản cốt lõi là một **IP Camera** đóng vai trò như một thiết bị ranh giới mạng (Edge Device). 
    *   Thiết bị này có giao diện Web (chạy HTTP/HTTPS) để cấu hình và dịch vụ Media (chạy RTSP) để stream video.
*   **Mô hình Kẻ tấn công (Attacker Model):** 
    *   Giả định Kẻ tấn công là **Remote Attacker (Kẻ tấn công từ xa qua Internet)**. 
    *   Kẻ tấn công không có quyền truy cập vật lý vào thiết bị hay mạng nội bộ (LAN) của nạn nhân ban đầu. Họ sử dụng các công cụ rà quét diện rộng (như Shodan) để dò tìm địa chỉ IP công cộng có mở port 80/554 và khai thác từ xa.

## 3. Thiết kế giải pháp (Solution Design)
Thiết kế của đề tài tập trung vào việc dịch chuyển từ "Kiến trúc dễ tổn thương" sang "Kiến trúc phòng thủ chiều sâu" (Defense-in-Depth):
*   **Hủy bỏ Exposed Ports:** Vô hiệu hóa tính năng Port Forwarding (NAT) trực tiếp và UPnP trên Router. Không cho phép bất kỳ kết nối chủ động nào từ Internet đi thẳng vào Camera.
*   **Thiết kế Lớp bảo vệ (Overlay Network):** 
    *   Sử dụng **VPN Gateway** (như OpenVPN, WireGuard) đặt tại Router hoặc thiết bị trung gian (Raspberry Pi/NAS). Người dùng muốn xem Camera từ xa phải thiết lập đường hầm VPN về nhà trước.
    *   *(Thiết kế thay thế)* Sử dụng **Reverse Proxy / Cloud Relay** có hỗ trợ xác thực 2 bước (2FA) và HTTPS mã hóa nếu không muốn dùng VPN.
*   **Phân vùng mạng (VLAN Segmentation):** Tách biệt Camera ra khỏi mạng LAN chính của máy tính làm việc. Nếu Camera bị xâm nhập, hacker cũng không thể tiếp cận dữ liệu của các máy tính khác.

## 4. Kế hoạch đánh giá & Mô phỏng (Evaluation Plan)
Để chứng minh tính thực tiễn của các phân tích và giải pháp, kế hoạch đánh giá (Lab Demo) được thực hiện qua các bước sau:

**Bước 1: Dựng môi trường mô phỏng (Lab Setup)**
*   Dựng một IP Camera thực tế (hoặc máy ảo mô phỏng Web Server/RTSP giả lập).
*   Thực hiện thao tác "Mở cổng" (Port forward) IP của Camera ra mạng diện rộng để giả lập kịch bản người dùng cấu hình sai.

**Bước 2: Kịch bản kiểm thử bảo mật (Offensive Testing)**
*   **Scan & Discovery:** Sử dụng Nmap dò quét các cổng đang mở (80, 554, 23).
*   **Exploitation:** Dùng các công cụ Brute-force (như Hydra) tấn công vào trang đăng nhập bằng danh sách mật khẩu mặc định phổ biến (admin/admin, root/12345).
*   **Sniffing:** Thử nghiệm dùng Wireshark bắt gói tin RTSP/HTTP để chứng minh luồng video và mật khẩu truyền đi là văn bản gốc (Plaintext).

**Bước 3: Triển khai giải pháp & Đánh giá lại (Defensive Verification)**
*   Đóng port trên Router, thiết lập VPN / VLAN theo **Thiết kế giải pháp**.
*   Sử dụng lại Nmap rà quét từ bên ngoài Internet để xác nhận thiết bị Camera đã hoàn toàn "tàng hình".
*   Ghi nhận sự cải thiện về mặt bảo mật (Giảm thiểu 100% rủi ro bị Bruteforce từ bên ngoài) và hoàn thiện Checklist cấu hình.

# NỘI DUNG CHI TIẾT 6 BƯỚC TRIỂN KHAI TIỂU LUẬN

## Bước 1: Chọn thiết bị ví dụ
**Thiết bị lựa chọn:** Camera IP giám sát an ninh (hướng tới phân khúc hộ gia đình và văn phòng nhỏ - SOHO).
*   **Lý do chọn:** Đây là thiết bị IoT phổ biến nhất bị rò rỉ trên Internet hiện nay.
*   **Giao diện & Dịch vụ:** Camera này có giao diện quản trị Web (chạy HTTP trên port 80) để cài đặt, và dịch vụ phát luồng video (chạy RTSP trên port 554). Một số dòng còn vô tình mở sẵn port Telnet (23) hoặc SSH (22).

---

## Bước 2: Sơ đồ triển khai sai (Insecure Architecture)
Cách thiết lập truyền thống nhưng cực kỳ nguy hiểm: Quản trị viên sử dụng tính năng **Port Forwarding (NAT)** trên Router để ánh xạ trực tiếp port 80 và 554 của Camera ra IP Public để xem từ xa.

```mermaid
graph LR
    subgraph Mạng Internet (Internet)
        A[Kẻ tấn công / Hacker]
        U[Người dùng hợp lệ / User]
    end

    subgraph Mạng LAN (Nội bộ)
        R[Router / Modem]
        C[Camera IP (Port 80/554)]
        PC[Các thiết bị LAN khác]
    end

    U -- HTTP/RTSP --> R
    A -- Quét IP/Cổng, Brute-force --> R
    R -- Port Forwarding (Trực tiếp) --> C
    C -.-> PC
    
    style A fill:#ffcccc,stroke:#ff0000
    style R fill:#fff5e6,stroke:#ff9900
    style C fill:#ffe6e6,stroke:#ff0000
```
*Hậu quả:* Camera bị "phơi bày" hoàn toàn ra Internet, trở thành mồi ngon cho các công cụ rà quét như Shodan.

---

## Bước 3: Sơ đồ đề xuất an toàn (Secure Architecture)
Nguyên tắc: Không mở cổng trực tiếp cho thiết bị IoT. Xây dựng rào chắn bảo vệ nhiều lớp.

```mermaid
graph LR
    subgraph Mạng Internet (Internet)
        A[Kẻ tấn công / Hacker]
        U[Người dùng hợp lệ / User]
    end

    subgraph Ranh giới mạng (Edge)
        F[Firewall / Router]
        VPN[VPN Gateway / Reverse Proxy]
    end

    subgraph Mạng IoT Cô lập (VLAN)
        C[Camera IP]
    end

    A -- Bị chặn hoàn toàn -.-x F
    U -- Xác thực an toàn (VPN/2FA) --> VPN
    VPN -- Kết nối mã hóa --> C
    
    style A fill:#ffcccc,stroke:#ff0000
    style F fill:#ccffcc,stroke:#009900
    style VPN fill:#ccffcc,stroke:#009900
    style C fill:#e6ffe6,stroke:#00cc00
```
**Các thành phần bảo vệ:**
1.  **VPN Gateway / Cloud Relay:** Yêu cầu người dùng phải kết nối qua đường hầm mạng riêng ảo (như WireGuard/Tailscale) hoặc qua Cloud Relay có xác thực trước khi chạm tới IP Camera.
2.  **Firewall Rule:** Router chặn toàn bộ kết nối Inbound (từ ngoài vào) nhắm trực tiếp đến Camera.
3.  **VLAN / Network Segmentation:** Cô lập Camera vào một mạng riêng, không cho phép kết nối ngược vào máy tính cá nhân.

---

## Bước 4: Lập bảng rủi ro (Risk Exposure Table)
Dựa trên kịch bản Bước 2, đây là các rủi ro cụ thể thiết bị phải đối mặt:

| Rủi ro / Mối đe dọa | Kịch bản tấn công | Hậu quả |
| :--- | :--- | :--- |
| **Quét Internet (Internet Scan)** | Kẻ tấn công dùng Zmap/Shodan rà quét hàng loạt IP Public mở port 80/554/23. | Đưa Camera vào "tầm ngắm", chuẩn bị cho đợt tấn công tiếp theo. |
| **Brute-force / Lộ Admin** | Dùng Hydra để chạy hàng ngàn mật khẩu mặc định (admin/admin, 12345). | Chiếm toàn quyền quản trị, tắt camera hoặc xem lén hình ảnh. |
| **Lỗ hổng dịch vụ (Services)** | Lỗ hổng tràn bộ đệm trên dịch vụ Web/RTSP/UPnP của Camera bị khai thác từ xa. | Hacker thực thi lệnh (RCE) để cài malware, biến thiết bị thành Botnet (Mirai). |
| **Firmware cũ (Outdated OS)** | Thiết bị sử dụng Firmware cũ có chứa lỗ hổng bảo mật (CVE) đã được công bố rộng rãi. | Bị tấn công leo thang đặc quyền mà không cần tài khoản admin. |
| **Không mã hóa (Plaintext)** | Luồng video RTSP truyền qua Internet không có SSL/TLS. | Kẻ tấn công MitM có thể bắt gói tin và xem được toàn bộ nội dung. |

---

## Bước 5: Đề xuất Test Point theo OWASP ISTG/ISVS
Áp dụng **OWASP IoT Security Testing Guide (ISTG)** để lập bộ tiêu chí kiểm soát (Test Points) cho thiết bị:

1.  **Network Interfaces (ISTG-NET):**
    *   *Test Point 1:* Dùng Nmap quét từ WAN IP, đảm bảo không có cổng (Port) nào của Camera bị lộ ra ngoài.
    *   *Test Point 2:* Đảm bảo tính năng UPnP trên Router bị vô hiệu hóa, ngăn Camera tự động đàm phán NAT.
2.  **Web / API Interfaces (ISTG-WEB):**
    *   *Test Point 3:* Kiểm tra cơ chế chống Brute-force: Trang Web quản trị phải tự động khóa IP (Lockout) sau 5 lần nhập sai mật khẩu.
    *   *Test Point 4:* Cấm sử dụng thông tin xác thực mặc định (Bắt buộc người dùng đổi mật khẩu khi cấu hình lần đầu).
3.  **Encryption & Communication (ISTG-CRYPTO):**
    *   *Test Point 5:* Đảm bảo giao diện quản trị chỉ cho phép truy cập qua HTTPS thay vì HTTP.
    *   *Test Point 6:* Luồng truyền phát video phải dùng RTSPS (RTSP over TLS) hoặc đi qua hầm VPN.

---

## Bước 6: Checklist không mở cổng bừa bãi dành cho người triển khai
Tài liệu hướng dẫn (Guidelines) dành cho IT nội bộ hoặc kỹ thuật viên lắp đặt:

- [ ] **Tuyệt đối KHÔNG sử dụng Port Forwarding / NAT trực tiếp:** Không mở các port của thiết bị IoT (80, 443, 554, 8080, v.v.) ra ngoài Internet.
- [ ] **Tắt UPnP trên Router:** Truy cập Modem nhà mạng / Router, tìm mục `UPnP` và chuyển sang `Disable`.
- [ ] **Thay đổi mật khẩu thiết bị ngay lập tức:** Đặt mật khẩu mạnh (chữ hoa, chữ thường, số, ký tự đặc biệt) ngay trong quá trình Unbox.
- [ ] **Vô hiệu hóa các dịch vụ không cần thiết:** Tắt Telnet, SSH, FTP, ONVIF trên Camera nếu bạn không có nhu cầu sử dụng.
- [ ] **Sử dụng giải pháp truy cập từ xa an toàn:** 
    *   *Cá nhân:* Cài đặt **Tailscale / ZeroTier** để tạo mạng LAN ảo giữa điện thoại và Camera.
    *   *Doanh nghiệp:* Thiết lập **VPN Gateway** (OpenVPN / WireGuard) trên Router/Firewall tổng.
- [ ] **Tách biệt mạng lưới (VLAN):** Đưa toàn bộ Camera vào lớp mạng Guest/IoT, giới hạn quyền truy cập từ lớp mạng này sang hệ thống lưu trữ dữ liệu của doanh nghiệp.


