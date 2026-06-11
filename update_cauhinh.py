import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qlgia.settings')
django.setup()

from core.models import CauHinhLoaiXe

new_defaults = {
    "1.25T": 9, 
    "2.5T": 13, 
    "3.5T": 18, 
    "5T": 23, 
    "7T": 35, 
    "8T": 54, 
    "9T": 40, 
    "15T": 54
}

prev_max = 0
for loai_xe, khoi_den in new_defaults.items():
    if loai_xe == "1.25T":
        khoi_tu = 0
    else:
        khoi_tu = prev_max

    CauHinhLoaiXe.objects.update_or_create(
        loai_xe=loai_xe,
        defaults={'khoi_tu': khoi_tu, 'khoi_den': khoi_den}
    )
    prev_max = khoi_den

print("Updated CauHinhLoaiXe!")
