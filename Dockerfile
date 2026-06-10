FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update \
    && apt-get install -y gcc libffi-dev \
    && apt-get clean

# Cài đặt Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn
COPY . .

# Gom file tĩnh
RUN python manage.py collectstatic --noinput

# Khởi chạy Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "qlygia.wsgi:application"]
