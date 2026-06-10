from django.db import models
from django.contrib.auth.models import User

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class DoiTac(models.Model):
    ma_nha_xe = models.CharField(max_length=50, null=True, blank=True, db_index=True, verbose_name="Mã nhà xe")
    ten_nha_xe = models.CharField(max_length=255, db_index=True, verbose_name="Tên nhà xe")
    dia_chi = models.CharField(max_length=500, blank=True, null=True, verbose_name="Địa chỉ")
    ten_don_vi_xuat_hoa_don = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tên đơn vị xuất hóa đơn")
    dia_chi_xuat_hoa_don = models.CharField(max_length=500, blank=True, null=True, verbose_name="Địa chỉ xuất hóa đơn")
    ma_so_thue = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mã số thuế")
    so_tai_khoan = models.CharField(max_length=100, blank=True, null=True, verbose_name="Số tài khoản")
    ngan_hang = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ngân hàng")
    nguoi_quan_ly = models.CharField(max_length=255, blank=True, null=True, verbose_name="Người quản lý")
    nguoi_dai_dien = models.CharField(max_length=255, blank=True, null=True, verbose_name="Người đại diện")
    so_dien_thoai = models.CharField(max_length=50, blank=True, null=True, verbose_name="Số điện thoại")
    TINH_SAN_SANG_CHOICES = [
        ('Cao', 'Cao'),
        ('Trung bình', 'Trung bình'),
        ('Thấp', 'Thấp'),
    ]
    tinh_san_sang = models.CharField(max_length=50, choices=TINH_SAN_SANG_CHOICES, default='Trung bình', verbose_name="Tính sẵn sàng")
    chat_luong = models.IntegerField(blank=True, null=True, verbose_name="Chất lượng")
    co_hop_dong = models.BooleanField(default=False, verbose_name="Có hợp đồng")
    ten_zalo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tên Zalo")
    thoi_han_thanh_toan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Thời hạn thanh toán")
    phi_rot_diem = models.FloatField(blank=True, null=True, verbose_name="Phí rớt điểm")
    phi_boc_xep = models.FloatField(blank=True, null=True, verbose_name="Phí bốc xếp")
    phi_di_qua_tai = models.FloatField(blank=True, null=True, verbose_name="Phí đi quá tải")
    ghi_chu = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    class Meta:
        verbose_name = "Đối tác"
        verbose_name_plural = "Đối tác"

    objects = ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.ten_nha_xe

class TuyenXe(models.Model):
    ma_tuyen = models.CharField(max_length=50, unique=True, verbose_name="Mã tuyến")
    tinh_nhan = models.CharField(max_length=100, db_index=True, verbose_name="Tỉnh nhận")
    huyen_nhan = models.CharField(max_length=100, db_index=True, verbose_name="Huyện nhận")
    tinh_giao = models.CharField(max_length=100, db_index=True, verbose_name="Tỉnh giao")
    huyen_giao = models.CharField(max_length=100, db_index=True, verbose_name="Huyện giao")
    trang_thai = models.CharField(max_length=50, default="HoatDong", verbose_name="Trạng thái")

    class Meta:
        verbose_name = "Tuyến xe"
        verbose_name_plural = "Tuyến xe"

    def __str__(self):
        return f"{self.ma_tuyen} - {self.tinh_nhan} -> {self.tinh_giao}"

class GiaCoSo(models.Model):
    tuyen = models.ForeignKey(TuyenXe, on_delete=models.CASCADE, related_name="gia_co_so", verbose_name="Tuyến xe")
    loai_xe = models.CharField(max_length=100, verbose_name="Loại xe")
    gia_co_so = models.FloatField(verbose_name="Giá cơ sở")
    ngay_ap_dung = models.DateField(verbose_name="Ngày áp dụng")
    so_khoi = models.CharField(max_length=50, blank=True, null=True, verbose_name="Số khối")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    class Meta:
        verbose_name = "Giá cơ sở"
        verbose_name_plural = "Giá cơ sở"

    objects = ActiveManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_price = 0
        if not is_new:
            old_instance = GiaCoSo.objects.get(pk=self.pk)
            old_price = old_instance.gia_co_so

        super().save(*args, **kwargs)

        if is_new or old_price != self.gia_co_so:
            LichSuGiaCoSo.objects.create(
                gia_co_so_ref=self,
                gia_cu=old_price,
                gia_moi=self.gia_co_so,
                gia_xang=getattr(self, '_gia_xang', None),
                ly_do_doi=getattr(self, '_ly_do_doi', 'Tạo mới' if is_new else 'Cập nhật giá')
            )

    def __str__(self):
        return f"{self.loai_xe} - {self.gia_co_so}"

class LichSuGiaCoSo(models.Model):
    gia_co_so_ref = models.ForeignKey(GiaCoSo, on_delete=models.CASCADE, related_name="lich_su", verbose_name="Giá cơ sở")
    gia_cu = models.FloatField(verbose_name="Giá cũ")
    gia_moi = models.FloatField(verbose_name="Giá mới")
    gia_xang = models.FloatField(blank=True, null=True, verbose_name="Giá xăng")
    ly_do_doi = models.CharField(max_length=500, blank=True, null=True, verbose_name="Lý do đổi")
    ngay_doi = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đổi")

    class Meta:
        verbose_name = "Lịch sử giá cơ sở"
        verbose_name_plural = "Lịch sử giá cơ sở"

class BaoGiaThongTinXe(models.Model):
    doi_tac = models.ForeignKey(DoiTac, on_delete=models.CASCADE, related_name="bao_gia", verbose_name="Đối tác")
    tuyen = models.ForeignKey(TuyenXe, on_delete=models.CASCADE, related_name="bao_gia", verbose_name="Tuyến xe")
    tai_trong_tan = models.FloatField(verbose_name="Tải trọng (tấn)")
    so_khoi = models.CharField(max_length=50, blank=True, null=True, verbose_name="Số khối")
    kich_thuoc = models.CharField(max_length=255, blank=True, null=True, verbose_name="Kích thước")
    loai_thung = models.CharField(max_length=100, blank=True, null=True, verbose_name="Loại thùng")
    co_ghep_hang_khong = models.BooleanField(default=False, verbose_name="Có ghép hàng không")
    co_chiu_qua_tai_khong = models.BooleanField(default=False, verbose_name="Có chịu quá tải không")
    co_di_nhieu_diem_khong = models.BooleanField(default=False, verbose_name="Có đi nhiều điểm không")
    di_1_hay_2_chieu = models.IntegerField(default=1, verbose_name="Đi 1 hay 2 chiều")
    muc_gia_chap_nhan = models.FloatField(verbose_name="Mức giá chấp nhận")
    ngay_cap_nhat = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    import django.utils.timezone
    ngay_bat_dau = models.DateField(default=django.utils.timezone.now, verbose_name="Ngày bắt đầu")
    is_deleted = models.BooleanField(default=False, verbose_name="Đã xóa")

    class Meta:
        verbose_name = "Báo giá thông tin xe"
        verbose_name_plural = "Báo giá thông tin xe"

    objects = ActiveManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        from django.utils import timezone
        is_new = self.pk is None
        old_price = 0
        if not is_new:
            old_instance = BaoGiaThongTinXe.objects.get(pk=self.pk)
            old_price = old_instance.muc_gia_chap_nhan

        price_changed = is_new or old_price != self.muc_gia_chap_nhan or getattr(self, '_force_history', False)
        
        if price_changed:
            self.ngay_bat_dau = timezone.now().date()

        super().save(*args, **kwargs)

        if price_changed:
            last_history = LichSuBaoGia.objects.filter(bao_gia_ref=self).order_by('-id').first()
            if last_history:
                last_history.ngay_ket_thuc = timezone.now().date()
                last_history.save()

            LichSuBaoGia.objects.create(
                bao_gia_ref=self,
                gia_cu=old_price,
                gia_moi=self.muc_gia_chap_nhan,
                gia_xang=getattr(self, '_gia_xang', None),
                ngay_bat_dau=self.ngay_bat_dau,
                ngay_ket_thuc=None,
                ly_do_doi=getattr(self, '_ly_do_doi', 'Tạo mới' if is_new else 'Cập nhật giá'),
                nguoi_doi=getattr(self, '_nguoi_doi', None)
            )

class LichSuBaoGia(models.Model):
    bao_gia_ref = models.ForeignKey(BaoGiaThongTinXe, on_delete=models.CASCADE, related_name="lich_su", verbose_name="Báo giá đối tác")
    gia_cu = models.FloatField(verbose_name="Giá cũ")
    gia_moi = models.FloatField(verbose_name="Giá mới")
    gia_xang = models.FloatField(blank=True, null=True, verbose_name="Giá xăng")
    ngay_bat_dau = models.DateField(blank=True, null=True, verbose_name="Ngày bắt đầu")
    ngay_ket_thuc = models.DateField(blank=True, null=True, verbose_name="Ngày kết thúc")
    ly_do_doi = models.CharField(max_length=500, blank=True, null=True, verbose_name="Lý do đổi")
    nguoi_doi = models.CharField(max_length=255, blank=True, null=True, verbose_name="Người đổi")
    ngay_doi_gia = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đổi giá")

    class Meta:
        verbose_name = "Lịch sử báo giá"
        verbose_name_plural = "Lịch sử báo giá"

class DeXuatGiaCoSo(models.Model):
    tuyen = models.ForeignKey(TuyenXe, on_delete=models.CASCADE, related_name="de_xuat_gia", verbose_name="Tuyến xe")
    loai_xe = models.CharField(max_length=100, verbose_name="Loại xe")
    so_khoi = models.CharField(max_length=50, blank=True, null=True, verbose_name="Số khối")
    gia_hien_tai = models.FloatField(blank=True, null=True, verbose_name="Giá hiện tại")
    gia_de_xuat = models.FloatField(verbose_name="Giá đề xuất")
    ly_do_de_xuat = models.TextField(verbose_name="Lý do đề xuất")
    nguoi_de_xuat = models.CharField(max_length=255, verbose_name="Người đề xuất")
    
    TRANG_THAI_CHOICES = [
        ('ChoDuyet', 'Chờ duyệt'),
        ('DaDuyet', 'Đã duyệt'),
        ('TuChoi', 'Từ chối'),
    ]
    trang_thai = models.CharField(max_length=50, choices=TRANG_THAI_CHOICES, default='ChoDuyet', verbose_name="Trạng thái")
    is_read = models.BooleanField(default=False, verbose_name="Đã đọc")
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    ngay_cap_nhat = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Đề xuất giá cơ sở"
        verbose_name_plural = "Đề xuất giá cơ sở"

    def __str__(self):
        return f"Đề xuất {self.tuyen} - {self.loai_xe} - {self.trang_thai}"

# Add to models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Tài khoản")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_users', verbose_name="Người tạo")
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('ThueNgoai', 'Thuê ngoài'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ThueNgoai', verbose_name="Vai trò")

    class Meta:
        verbose_name = "Hồ sơ nhân sự"
        verbose_name_plural = "Hồ sơ nhân sự"

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class CauHinhLoaiXe(models.Model):
    loai_xe = models.CharField(max_length=50, unique=True, verbose_name="Loại xe (Tấn)")
    so_khoi_mac_dinh = models.CharField(max_length=50, blank=True, null=True, verbose_name="Số khối mặc định")
    thu_tu = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")

    class Meta:
        verbose_name = "Cấu hình Loại xe & Số khối"
        verbose_name_plural = "Cấu hình Loại xe & Số khối"
        ordering = ['thu_tu', 'loai_xe']

    def __str__(self):
        return f"{self.loai_xe} -> {self.so_khoi_mac_dinh}"
