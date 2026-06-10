#!/bin/bash

# Cài đặt các thư viện Python
pip install -r requirements.txt

# Gom các file tĩnh (CSS/JS) vào thư mục staticfiles để Vercel phục vụ
python manage.py collectstatic --noinput

# Áp dụng các thay đổi cơ sở dữ liệu lên AWS Database
python manage.py migrate
