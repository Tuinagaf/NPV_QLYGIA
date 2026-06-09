from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import models
from .models import DoiTac, TuyenXe, GiaCoSo, LichSuGiaCoSo, BaoGiaThongTinXe, LichSuBaoGia, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    can_delete = False
    verbose_name_plural = 'Thông tin mở rộng'

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('ThueNgoai', 'Thuê ngoài'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Vai trò", initial='ThueNgoai')

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user._temp_role = self.cleaned_data['role']
        return user

class CustomUserChangeForm(UserChangeForm):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('ThueNgoai', 'Thuê ngoài'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Vai trò", initial='ThueNgoai')

    class Meta(UserChangeForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['role'].initial = self.instance.profile.role

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    
    # Hide complex permissions in a collapsed section for adding new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password', 'role'),
        }),
    )

    # Hide complex permissions in a collapsed section for editing existing user
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'email')}),
        ('Cài đặt nâng cao (Phân quyền Django)', {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        ('Lịch sử truy cập', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            models.Q(profile__created_by=request.user) | 
            models.Q(profile__role='ThueNgoai') |
            models.Q(id=request.user.id)
        ).distinct()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        if obj == request.user:
            return False 
        try:
            profile = obj.profile
            if profile.created_by == request.user:
                return True
            if profile.role == 'ThueNgoai':
                return True
        except:
            pass
        return False

    def save_model(self, request, obj, form, change):
        is_new = not obj.pk
        super().save_model(request, obj, form, change)
        if is_new:
            role = getattr(obj, '_temp_role', 'ThueNgoai')
            UserProfile.objects.create(user=obj, created_by=request.user, role=role)
        else:
            role = form.cleaned_data.get('role', 'ThueNgoai')
            profile, _ = UserProfile.objects.get_or_create(user=obj)
            profile.role = role
            profile.save()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if hasattr(form.instance, 'profile'):
            profile = form.instance.profile
            if profile.role == 'Admin':
                form.instance.is_staff = True
                form.instance.is_superuser = False
            elif profile.role == 'ThueNgoai':
                form.instance.is_staff = True
                form.instance.is_superuser = False
            form.instance.save()

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)

class DoiTacAdmin(admin.ModelAdmin):
    list_display = ['ma_nha_xe', 'ten_nha_xe', 'nguoi_quan_ly', 'so_dien_thoai', 'tinh_san_sang', 'co_hop_dong']
    list_filter = ['tinh_san_sang', 'co_hop_dong']
    search_fields = ['ma_nha_xe', 'ten_nha_xe', 'so_dien_thoai']
    ordering = ['-id']

admin.site.register(DoiTac, DoiTacAdmin)

class TuyenXeAdmin(admin.ModelAdmin):
    list_display = ['ma_tuyen', 'tinh_nhan', 'huyen_nhan', 'tinh_giao', 'huyen_giao', 'trang_thai']
    search_fields = ['ma_tuyen', 'tinh_nhan', 'tinh_giao']

admin.site.register(TuyenXe, TuyenXeAdmin)

class GiaCoSoAdmin(admin.ModelAdmin):
    list_display = ['tuyen', 'loai_xe', 'gia_co_so', 'ngay_ap_dung', 'so_khoi']
    search_fields = ['tuyen__ma_tuyen', 'loai_xe']
    list_filter = ['loai_xe']

admin.site.register(GiaCoSo, GiaCoSoAdmin)

class BaoGiaAdmin(admin.ModelAdmin):
    list_display = ['doi_tac', 'tuyen', 'tai_trong_tan', 'muc_gia_chap_nhan', 'ngay_cap_nhat']
    search_fields = ['doi_tac__ten_nha_xe', 'tuyen__ma_tuyen']

admin.site.register(BaoGiaThongTinXe, BaoGiaAdmin)
