# 🚗 NPV - Hệ Thống Quản Lý Giá

Hệ thống quản lý giá xe dành cho doanh nghiệp vận tải. Được xây dựng bằng **Django + SQLite**, triển khai **All-in-one trên AWS EC2** thông qua **Docker** và tự động hóa bằng **GitHub Actions CI/CD**.

---

## ⚙️ Công Nghệ Sử Dụng

| Thành phần | Công nghệ |
| :--- | :--- |
| **Backend** | Django 4.x |
| **Cơ sở dữ liệu** | SQLite |
| **Web Server** | Gunicorn |
| **Container** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions |
| **Hosting** | AWS EC2 (Ubuntu) |
| **Tên miền** | DuckDNS (Free) |

---

## 🖥️ Chạy Ở Máy Cá Nhân (Local Development)

```bash
# 1. Clone code về máy
git clone https://github.com/Tuinagaf/NPV_QLYGIA.git
cd NPV_QLYGIA

# 2. Tạo môi trường ảo (Virtual Environment)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. Cài đặt các thư viện
pip install -r requirements.txt

# 4. Tạo bảng cơ sở dữ liệu
python manage.py migrate

# 5. Khởi chạy server
python manage.py runserver
```

Mở trình duyệt và truy cập: `http://127.0.0.1:8000`

---

## 🚀 Hướng Dẫn Triển Khai Lên AWS EC2 (Từ A-Z)

### PHẦN 1: Tạo Máy Chủ AWS EC2

1. Đăng nhập vào [AWS Console](https://console.aws.amazon.com/) và tìm dịch vụ **EC2**.
2. Bấm nút **Launch instance** (màu cam ở góc trên phải).
3. Điền thông tin:
   - **Name:** Đặt tên tùy ý, ví dụ `NPV-Server`.
   - **OS Image:** Bấm vào ô **Ubuntu** → chọn **Ubuntu Server 24.04 LTS** (Free tier eligible).
   - **Instance type:** Chọn **t2.micro** hoặc **t3.micro** (Free tier eligible).
4. **Tạo chìa khóa bảo mật (Key pair):**
   - Tại mục _Key pair (login)_, bấm **Create new key pair**.
   - **Key pair name:** Đặt tên `npv-key`.
   - Giữ nguyên tùy chọn **RSA** và **.pem**.
   - Bấm **Create key pair**. File `npv-key.pem` sẽ được tải về máy bạn. **Lưu kỹ file này!**
5. **Mở Tường lửa (Network settings):**
   - Tick ✅ vào cả **3 ô vuông**: SSH, HTTPS, HTTP.
6. **Tự động cài đặt Docker (User data):**
   - Kéo xuống cuối trang, mở rộng mục **Advanced details**.
   - Cuộn xuống ô **User data**, dán đoạn sau vào:
   ```bash
   #!/bin/bash
   apt-get update -y
   apt-get install docker.io docker-compose -y
   systemctl start docker
   systemctl enable docker
   usermod -aG docker ubuntu
   ```
7. Bấm **Launch instance**. Đợi 1-2 phút cho máy chủ khởi động.
8. Vào trang chi tiết máy chủ, **copy địa chỉ Public IPv4** (ví dụ: `13.56.78.90`).

---

### PHẦN 2: Trỏ Tên Miền DuckDNS Vào Máy Chủ

1. Vào [duckdns.org](https://www.duckdns.org/), tìm tên miền `npv-qlygia`.
2. Xóa IP cũ, dán địa chỉ **Public IPv4 của AWS** vào.
3. Bấm **update ip** → Thấy chữ `success` màu xanh là hoàn thành.

---

### PHẦN 3: Thêm Secrets Bảo Mật Vào GitHub

> Đây là bước cung cấp "chìa khóa" cho GitHub để nó tự động chui vào máy chủ deploy code.

1. Vào trang GitHub kho code: `https://github.com/Tuinagaf/NPV_QLYGIA`.
2. Bấm **Settings** → **Secrets and variables** → **Actions** → **New repository secret**.
3. Lần lượt tạo **3 biến bảo mật** như sau:

   | Tên biến (Name) | Giá trị (Secret) |
   | :--- | :--- |
   | `EC2_HOST` | Địa chỉ IP Public của AWS (VD: `13.56.78.90`) |
   | `EC2_USER` | `ubuntu` |
   | `EC2_SSH_KEY` | Toàn bộ nội dung file `npv-key.pem` (mở bằng TextEdit, copy từ dòng `-----BEGIN...` đến `-----END...`) |

---

### PHẦN 4: Deploy Lần Đầu

Sau khi cấu hình xong 3 Secrets ở trên, bạn chỉ cần đẩy code lên GitHub và GitHub Actions sẽ tự làm tất cả:

```bash
git add .
git commit -m "Deploy lên AWS EC2"
git push origin master
```

Vào tab **Actions** trên GitHub để theo dõi tiến trình. Khi thấy dấu ✅ xanh là dự án đã online!

🌐 **Truy cập tại:** `http://npv-qlygia.duckdns.org`

---

### PHẦN 5: Quy Trình Từ Đây Trở Về Sau

Mỗi khi bạn sửa code và muốn cập nhật lên web, chỉ cần chạy 3 lệnh quen thuộc:

```bash
git add .
git commit -m "Mô tả nội dung thay đổi"
git push origin master
```

GitHub Actions sẽ tự động **kéo code mới → build lại Docker → khởi động lại web** trong vòng 2-3 phút mà bạn không cần làm thêm bất cứ thao tác nào!

---

## 📁 Cấu Trúc Thư Mục Dự Án

```
NPV_QLYGIA/
├── core/                  # Ứng dụng Django chính (Models, Views, URLs, Templates)
├── qlygia/                # Cấu hình Django (settings.py, wsgi.py)
├── .github/workflows/     # Cấu hình tự động hóa GitHub Actions
│   └── deploy.yml
├── Dockerfile             # Công thức đóng gói ứng dụng vào Docker
├── docker-compose.yml     # Cấu hình chạy Docker trên máy chủ
├── requirements.txt       # Danh sách thư viện Python cần thiết
├── manage.py              # Công cụ quản lý Django
└── db.sqlite3             # File cơ sở dữ liệu (tự động tạo)
```

---

## 🔐 Tài Khoản Mặc Định

Sau khi chạy `migrate`, tài khoản admin mặc định:
- **Username:** `admin`
- **Password:** *(Xem trong file `.env` hoặc chạy `python manage.py createsuperuser`)*
