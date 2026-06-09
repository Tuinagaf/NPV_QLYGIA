# Hướng Dẫn Deploy Django Lên VPS (Ubuntu) Với Tên Miền Riêng

Dưới đây là hướng dẫn chi tiết từng bước để đưa dự án Django của bạn lên máy chủ VPS (chạy hệ điều hành Ubuntu) kết hợp **Gunicorn** (Web Server Gateway Interface) và **Nginx** (Reverse Proxy).

Lưu ý: Bài hướng dẫn này giả định máy chủ (VPS) của bạn đang chạy hệ điều hành **Ubuntu 20.04** hoặc **22.04**, và bạn đã có quyền truy cập root hoặc sudo qua SSH.

---

## 1. Kết nối vào VPS và cập nhật hệ thống
Đầu tiên, bạn mở Terminal (hoặc PowerShell) trên máy tính và SSH vào VPS:
```bash
ssh root@dia_chi_ip_vps_cua_ban
```
Sau khi đăng nhập thành công, cập nhật các gói phần mềm trên Ubuntu:
```bash
sudo apt update
sudo apt upgrade -y
```

## 2. Cài đặt các phần mềm cần thiết
Bạn cần cài đặt Python, pip, môi trường ảo và Nginx:
```bash
sudo apt install python3-pip python3-venv nginx -y
```

## 3. Đưa Source Code lên VPS
Bạn có thể dùng `git clone` để tải code từ GitHub về VPS.
Giả sử bạn để code ở thư mục `/home/ubuntu/NPV_QLYGIA`:
```bash
# Tạo thư mục và di chuyển vào đó
cd /home/ubuntu/
git clone https://github.com/Ten_Cua_Ban/Repo_Cua_Ban.git NPV_QLYGIA
cd NPV_QLYGIA
```

## 4. Thiết lập Môi trường Ảo (Virtual Environment)
Tạo và kích hoạt môi trường ảo, sau đó cài đặt các thư viện:
```bash
# Tạo môi trường ảo có tên là "venv"
python3 -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate

# Cài đặt thư viện từ requirements.txt
pip install -r requirements.txt

# Cài đặt thêm gunicorn
pip install gunicorn
```

## 5. Cấu hình dự án Django (settings.py)
Bạn cần sửa file `settings.py` trong thư mục `NPV_QLYGIA/NPV_QLYGIA/settings.py` (bạn có thể dùng `nano settings.py` trên VPS):

1. **Tắt chế độ Debug:**
   ```python
   DEBUG = False
   ```
2. **Khai báo tên miền của bạn:**
   ```python
   ALLOWED_HOSTS = ['tenmiencuaban.com', 'www.tenmiencuaban.com', 'dia_chi_ip_vps']
   ```
3. **Cấu hình Static Files:** Thêm dòng này vào cuối file `settings.py` nếu chưa có:
   ```python
   import os
   STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
   ```

Sau khi lưu file `settings.py`, chạy lệnh gom file tĩnh và migrate (đảm bảo đang bật môi trường ảo):
```bash
python manage.py collectstatic
python manage.py migrate
```

## 6. Cấu hình Gunicorn (Chạy ngầm dự án)
Thay vì tự chạy `python manage.py runserver`, ta sẽ dùng `systemd` để Gunicorn chạy tự động ngay cả khi server khởi động lại.

Tạo một file service cho Gunicorn:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
Dán đoạn nội dung sau vào (Nhớ sửa `/home/ubuntu/NPV_QLYGIA` thành đường dẫn thực tế chứa code của bạn):
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/ubuntu/NPV_QLYGIA/NPV_QLYGIA
ExecStart=/home/ubuntu/NPV_QLYGIA/NPV_QLYGIA/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/NPV_QLYGIA/NPV_QLYGIA/NPV_QLYGIA.sock NPV_QLYGIA.wsgi:application

[Install]
WantedBy=multi-user.target
```
Lưu lại (Bấm `Ctrl+O`, `Enter`, `Ctrl+X`). Sau đó khởi động Gunicorn:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## 7. Cấu hình Nginx (Đón truy cập từ tên miền)
Tạo file cấu hình Nginx mới cho dự án:
```bash
sudo nano /etc/nginx/sites-available/npv_qlygia
```
Dán nội dung sau (Thay `tenmiencuaban.com` bằng tên miền thật của bạn):
```nginx
server {
    listen 80;
    server_name tenmiencuaban.com www.tenmiencuaban.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    # Cấu hình đường dẫn cho static file
    location /static/ {
        root /home/ubuntu/NPV_QLYGIA/NPV_QLYGIA;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/NPV_QLYGIA/NPV_QLYGIA/NPV_QLYGIA.sock;
    }
}
```
Lưu lại. Kích hoạt cấu hình này và khởi động lại Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/npv_qlygia /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 8. Cấu hình Tường lửa (UFW)
Mở port 80 (HTTP), 443 (HTTPS) và 22 (SSH) trên VPS:
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

QUAN TRỌNG
**Bước trỏ tên miền:** Tại trình quản lý tên miền của bạn (ví dụ: Mắt Bão, Tenten, Cloudflare...), bạn hãy thêm một bản ghi **A record** trỏ từ `tenmiencuaban.com` về địa chỉ IP của VPS.

## 9. Cài đặt chứng chỉ SSL (HTTPS) miễn phí với Certbot
Để trang web có ổ khóa xanh bảo mật (HTTPS), chạy lệnh sau:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tenmiencuaban.com -d www.tenmiencuaban.com
```
Certbot sẽ tự động cấu hình lại Nginx để trang web chạy qua HTTPS.

---
**Hoàn tất!** Giờ đây bạn đã có thể truy cập vào tên miền của mình để sử dụng dự án. Mọi thay đổi code sau này, bạn chỉ cần kéo (pull) code mới về VPS và chạy lệnh: `sudo systemctl restart gunicorn`.
