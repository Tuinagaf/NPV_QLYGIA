import os
import django

# Cấu hình môi trường Django để script có thể chạy độc lập
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qlygia.settings')
django.setup()

from django.contrib.auth.models import User, Permission

def setup_accounts():
    # 1. Tạo tài khoản Admin tổng (Superuser)
    admin_name = 'AdminTong'
    admin_user, created = User.objects.get_or_create(username=admin_name)
    if created:
        admin_user.set_password('12345678') # Đặt mật khẩu mặc định
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print(f"[*] Đã tạo thành công Superuser: {admin_name}")
    else:
        print(f"[-] Tài khoản {admin_name} đã tồn tại.")

    # Lấy toàn bộ các quyền (Thêm, Sửa, Xóa, Xem) của app 'core' - Nơi chứa các bảng dữ liệu chính
    # Bạn có thể đổi 'core' thành app khác nếu cần
    core_permissions = Permission.objects.filter(content_type__app_label='core')

    # Danh sách các tài khoản nhân viên cần tạo và gán quyền thủ công
    staff_accounts = ['ThueNgoai01.NPV', 'ThueNgoai02.NPV']
    
    for username in staff_accounts:
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password('12345678') # Đặt mật khẩu mặc định
            
        user.is_staff = True          # Bật quyền đăng nhập Admin (Staff status)
        user.is_superuser = False     # KHÔNG cho phép Superuser (để phải tuân theo phân quyền)
        user.save()
        
        # Gán toàn bộ quyền (add, change, delete, view) của app core cho tài khoản này
        user.user_permissions.set(core_permissions)
        
        if created:
            print(f"[*] Đã tạo và cấp quyền cho: {username}")
        else:
            print(f"[*] Đã cập nhật lại quyền cho tài khoản tồn tại: {username}")

if __name__ == '__main__':
    print("--- BẮT ĐẦU QUÁ TRÌNH TẠO TÀI KHOẢN VÀ PHÂN QUYỀN ---")
    setup_accounts()
    print("--- HOÀN TẤT ---")
