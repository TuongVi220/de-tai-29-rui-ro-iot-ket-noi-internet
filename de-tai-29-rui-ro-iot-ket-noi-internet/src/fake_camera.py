import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

# Mật khẩu mặc định giả lập là admin / admin
KEY = base64.b64encode(b"admin:admin").decode("ascii")

class FakeCameraHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Kiểm tra xem trình duyệt có gửi đúng chữ Authorization: Basic YWRtaW46YWRtaW4= không
        if self.headers.get('Authorization') == f'Basic {KEY}':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Camera Control Panel</h1><p>Welcome Admin! (This is a fake camera for IoT Security Lab)</p>")
        else:
            # Nếu chưa có mật khẩu, yêu cầu đăng nhập
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="IP Camera Login"')
            self.end_headers()
            self.wfile.write(b"Unauthorized - Please login with admin/admin")

if __name__ == "__main__":
    port = 8081
    print(f"[*] Dang chay IP Camera gia lap tai cong {port}...")
    print(f"[*] Mo trinh duyet truy cap: http://localhost:{port}")
    print("[*] Nhan Ctrl+C de dung server.")
    
    # Chạy server
    try:
        HTTPServer(('0.0.0.0', port), FakeCameraHandler).serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Da tat server.")
