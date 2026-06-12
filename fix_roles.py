import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qlygia.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile

admin_codenames = [
    'change_giacoso', 'delete_giacoso', 'add_giacoso',
    'change_cauhinhloaixe', 'delete_cauhinhloaixe', 'add_cauhinhloaixe',
    'change_user', 'delete_user', 'add_user'
]

for user in User.objects.all():
    if user.is_superuser:
        continue
    
    role = 'Nhân viên'
    perms = user.user_permissions.all()
    if perms.filter(codename__in=admin_codenames).exists():
        role = 'Admin'
        
    profile, created = UserProfile.objects.get_or_create(user=user, defaults={'role': role})
    print(f"User {user.username} - current role: {profile.role}, new computed role: {role}")
    if not created and profile.role != role:
        profile.role = role
        profile.save()
        print(f"--> Updated role for {user.username} to {role}")

print("Done.")
