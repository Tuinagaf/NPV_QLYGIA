from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
import re
from .models import DoiTac, BaoGiaThongTinXe

class DoiTacForm(forms.ModelForm):
    phi_rot_diem = forms.CharField(label="Phí rớt điểm", required=False, widget=forms.TextInput(attrs={'class': 'form-control vn-number', 'placeholder': 'VD: 500,000'}))
    phi_boc_xep = forms.CharField(label="Phí bốc xếp", required=False, widget=forms.TextInput(attrs={'class': 'form-control vn-number', 'placeholder': 'VD: 1,000,000'}))
    phi_di_qua_tai = forms.CharField(label="Phí đi quá tải", required=False, widget=forms.TextInput(attrs={'class': 'form-control vn-number', 'placeholder': 'VD: 3,000,000'}))

    class Meta:
        model = DoiTac
        fields = [
            'ma_nha_xe', 'ten_nha_xe', 'nguoi_quan_ly', 'so_dien_thoai', 'ten_zalo',
            'dia_chi', 'tinh_san_sang', 'ma_so_thue', 'ten_don_vi_xuat_hoa_don',
            'dia_chi_xuat_hoa_don', 'nguoi_dai_dien', 'so_tai_khoan', 'ngan_hang',
            'thoi_han_thanh_toan', 'chat_luong', 'phi_rot_diem', 'phi_boc_xep', 'phi_di_qua_tai', 'ghi_chu', 'co_hop_dong'
        ]
        labels = {
            'ma_nha_xe': 'Mã nhà xe',
            'ten_nha_xe': 'Tên nhà xe',
            'dia_chi': 'Địa chỉ',
            'ten_don_vi_xuat_hoa_don': 'Tên đơn vị xuất hóa đơn',
            'dia_chi_xuat_hoa_don': 'Địa chỉ xuất hóa đơn',
            'ma_so_thue': 'Mã số thuế',
            'so_tai_khoan': 'Số tài khoản',
            'ngan_hang': 'Ngân hàng',
            'nguoi_dai_dien': 'Người đại diện',
            'nguoi_quan_ly': 'Người quản lý',
            'so_dien_thoai': 'Số điện thoại',
            'tinh_san_sang': 'Tính sẵn sàng',
            'chat_luong': 'Chất lượng (thang 10)',
            'co_hop_dong': 'Có hợp đồng',
            'ten_zalo': 'Tên Zalo',
            'thoi_han_thanh_toan': 'Thời hạn thanh toán',
            'phi_rot_diem': 'Phí rớt điểm',
            'phi_boc_xep': 'Phí bốc xếp',
            'phi_di_qua_tai': 'Phí đi quá tải',
            'ghi_chu': 'Ghi chú thêm',
        }
        widgets = {
            'ma_nha_xe': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: NX001'}),
            'ten_nha_xe': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Nhà xe Hoàng Long'}),
            'dia_chi': forms.TextInput(attrs={'class': 'form-control'}),
            'ten_don_vi_xuat_hoa_don': forms.TextInput(attrs={'class': 'form-control'}),
            'dia_chi_xuat_hoa_don': forms.TextInput(attrs={'class': 'form-control'}),
            'ma_so_thue': forms.TextInput(attrs={'class': 'form-control'}),
            'so_tai_khoan': forms.TextInput(attrs={'class': 'form-control'}),
            'ngan_hang': forms.TextInput(attrs={'class': 'form-control'}),
            'nguoi_dai_dien': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Nguyễn Văn A'}),
            'nguoi_quan_ly': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'style': 'background-color: #f1f5f9; cursor: not-allowed;'}),
            'so_dien_thoai': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: 0901234567'}),
            'tinh_san_sang': forms.Select(attrs={'class': 'form-control'}),
            'chat_luong': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1 - 10'}),
            'co_hop_dong': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ten_zalo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Tên hiển thị Zalo'}),
            'thoi_han_thanh_toan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Thanh toán sau 15 ngày'}),
            'phi_rot_diem': forms.TextInput(attrs={'class': 'form-control vn-number', 'placeholder': 'VD: 500,000'}),
            'phi_boc_xep': forms.TextInput(attrs={'class': 'form-control vn-number', 'placeholder': 'VD: 1,000,000'}),
            'phi_di_qua_tai': forms.TextInput(attrs={'class': 'form-control vn-number', 'placeholder': 'VD: 3,000,000'}),
            'ghi_chu': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ghi chú về đối tác...'}),
        }
        error_messages = {
            'ma_nha_xe': {
                'unique': 'Đối tác có Mã nhà xe này đã tồn tại.'
            }
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DoiTacForm, self).__init__(*args, **kwargs)
        
        # Strip .0 from float fields so JS vn-number doesn't multiply by 10
        if self.instance and self.instance.pk:
            for field in ['phi_rot_diem', 'phi_boc_xep', 'phi_di_qua_tai']:
                val = getattr(self.instance, field)
                if val is not None:
                    if val == int(val):
                        self.initial[field] = str(int(val))
                    else:
                        self.initial[field] = str(val)
        if self.user and self.user.is_superuser:
            from django.contrib.auth.models import User
            users = User.objects.all().values_list('username', 'username')
            choices = [('', '--- Chọn Người Quản Lý ---')] + list(users)
            self.fields['nguoi_quan_ly'].widget = forms.Select(choices=choices, attrs={'class': 'form-control', 'required': 'required'})
            self.fields['nguoi_quan_ly'].required = True
        else:
            if self.user and self.user.is_authenticated:
                self.initial['nguoi_quan_ly'] = self.user.username
            self.fields['nguoi_quan_ly'].widget = forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'style': 'background-color: #f1f5f9; cursor: not-allowed;'})
    
    def clean_ten_nha_xe(self):
        """Validate tên nhà xe không được để trống"""
        ten_nha_xe = self.cleaned_data.get('ten_nha_xe')
        if not ten_nha_xe or not ten_nha_xe.strip():
            raise ValidationError('Tên nhà xe không được để trống.')
        return ten_nha_xe.strip()
    
    def clean_so_dien_thoai(self):
        """Validate số điện thoại Việt Nam"""
        so_dien_thoai = self.cleaned_data.get('so_dien_thoai')
        if so_dien_thoai:
            # Loại bỏ khoảng trắng và dấu gạch ngang
            so_dien_thoai = re.sub(r'[\s\-]', '', so_dien_thoai)
            # Kiểm tra format số điện thoại VN (10 số, bắt đầu bằng 0)
            if not re.match(r'^0\d{9}$', so_dien_thoai):
                raise ValidationError('Số điện thoại không hợp lệ. Vui lòng nhập 10 số, bắt đầu bằng 0.')
        return so_dien_thoai
    
    def clean_ma_so_thue(self):
        """Validate mã số thuế"""
        ma_so_thue = self.cleaned_data.get('ma_so_thue')
        if ma_so_thue:
            # Loại bỏ khoảng trắng và dấu gạch ngang
            ma_so_thue = re.sub(r'[\s\-]', '', ma_so_thue)
            # MST Việt Nam có 10 hoặc 13 số
            if not re.match(r'^\d{10}(\d{3})?$', ma_so_thue):
                raise ValidationError('Mã số thuế không hợp lệ. Phải có 10 hoặc 13 chữ số.')
                
            # Kiểm tra trùng lặp
            existing = DoiTac.objects.filter(ma_so_thue=ma_so_thue)
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
                
            if existing.exists():
                partner = existing.first()
                manager = partner.nguoi_quan_ly or 'Hệ thống (Admin)'
                raise ValidationError(f'Mã số thuế này đã tồn tại trong hệ thống. Đối tác này đang được phụ trách bởi: {manager}')
                
        return ma_so_thue
    
    def clean_phi_rot_diem(self):
        val = self.data.get('phi_rot_diem')
        if val:
            val = str(val).strip().replace(' ', '').replace('.', '').replace(',', '.')
            try:
                return float(val)
            except ValueError:
                raise ValidationError('Số tiền không hợp lệ.')
        return None

    def clean_phi_boc_xep(self):
        val = self.data.get('phi_boc_xep')
        if val:
            val = str(val).strip().replace(' ', '').replace('.', '').replace(',', '.')
            try:
                return float(val)
            except ValueError:
                raise ValidationError('Số tiền không hợp lệ.')
        return None

    def clean_phi_di_qua_tai(self):
        val = self.data.get('phi_di_qua_tai')
        if val:
            val = str(val).strip().replace(' ', '').replace('.', '').replace(',', '.')
            try:
                return float(val)
            except ValueError:
                raise ValidationError('Số tiền không hợp lệ.')
        return None

    def clean_chat_luong(self):
        """Validate chất lượng từ 1-10"""
        chat_luong = self.cleaned_data.get('chat_luong')
        if chat_luong is not None:
            if chat_luong < 1 or chat_luong > 10:
                raise ValidationError('Chất lượng phải từ 1 đến 10.')
        return chat_luong

BaoGiaFormSet = inlineformset_factory(
    DoiTac,
    BaoGiaThongTinXe,
    fields=['tuyen', 'tai_trong_tan', 'loai_thung', 'muc_gia_chap_nhan'],
    extra=1,
    can_delete=True,
    widgets={
        'tuyen': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        'tai_trong_tan': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
        'loai_thung': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        'muc_gia_chap_nhan': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
    }
)

class BaoGiaThongTinXeForm(forms.ModelForm):
    class Meta:
        model = BaoGiaThongTinXe
        exclude = ['doi_tac']
        widgets = {
            'tuyen': forms.Select(attrs={'class': 'form-control'}),
            'tai_trong_tan': forms.NumberInput(attrs={'class': 'form-control'}),
            'kich_thuoc': forms.TextInput(attrs={'class': 'form-control'}),
            'loai_thung': forms.TextInput(attrs={'class': 'form-control'}),
            'co_ghep_hang_khong': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'co_chiu_qua_tai_khong': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'co_di_nhieu_diem_khong': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'di_1_hay_2_chieu': forms.NumberInput(attrs={'class': 'form-control'}),
            'muc_gia_chap_nhan': forms.NumberInput(attrs={'class': 'form-control'}),
            'thoi_han_thanh_toan': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_tai_trong_tan(self):
        """Validate tải trọng phải > 0"""
        tai_trong = self.cleaned_data.get('tai_trong_tan')
        if tai_trong is not None and tai_trong <= 0:
            raise ValidationError('Tải trọng phải lớn hơn 0.')
        return tai_trong
    
    def clean_muc_gia_chap_nhan(self):
        """Validate giá phải >= 0"""
        gia = self.cleaned_data.get('muc_gia_chap_nhan')
        if gia is not None and gia < 0:
            raise ValidationError('Giá không được âm.')
        return gia
    
    def clean_di_1_hay_2_chieu(self):
        """Validate chiều đi chỉ được 1 hoặc 2"""
        chieu = self.cleaned_data.get('di_1_hay_2_chieu')
        if chieu not in [1, 2]:
            raise ValidationError('Chiều đi chỉ được là 1 hoặc 2.')
        return chieu
