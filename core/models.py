from django.db import models

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class DoiTac(models.Model):
    ma_nha_xe = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    ten_nha_xe = models.CharField(max_length=255, db_index=True)
    dia_chi = models.CharField(max_length=500, blank=True, null=True)
    ten_don_vi_xuat_hoa_don = models.CharField(max_length=255, blank=True, null=True)
    dia_chi_xuat_hoa_don = models.CharField(max_length=500, blank=True, null=True)
    ma_so_thue = models.CharField(max_length=50, blank=True, null=True)
    so_tai_khoan = models.CharField(max_length=100, blank=True, null=True)
    ngan_hang = models.CharField(max_length=255, blank=True, null=True)
    nguoi_quan_ly = models.CharField(max_length=255, blank=True, null=True)
    nguoi_dai_dien = models.CharField(max_length=255, blank=True, null=True)
    so_dien_thoai = models.CharField(max_length=50, blank=True, null=True)
    TINH_SAN_SANG_CHOICES = [
        ('Cao', 'Cao'),
        ('Trung bình', 'Trung bình'),
        ('Thấp', 'Thấp'),
    ]
    tinh_san_sang = models.CharField(max_length=50, choices=TINH_SAN_SANG_CHOICES, default='Trung bình')
    chat_luong = models.IntegerField(blank=True, null=True)
    co_hop_dong = models.BooleanField(default=False)
    ten_zalo = models.CharField(max_length=255, blank=True, null=True)
    thoi_han_thanh_toan = models.CharField(max_length=255, blank=True, null=True)
    phi_rot_diem = models.FloatField(blank=True, null=True)
    phi_boc_xep = models.FloatField(blank=True, null=True)
    phi_di_qua_tai = models.FloatField(blank=True, null=True)
    ghi_chu = models.TextField(blank=True, null=True, verbose_name="Ghi chú")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Đối tác"
        verbose_name_plural = "Đối tác"

    objects = ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.ten_nha_xe

class TuyenXe(models.Model):
    ma_tuyen = models.CharField(max_length=50, unique=True)
    tinh_nhan = models.CharField(max_length=100, db_index=True)
    huyen_nhan = models.CharField(max_length=100, db_index=True)
    tinh_giao = models.CharField(max_length=100, db_index=True)
    huyen_giao = models.CharField(max_length=100, db_index=True)
    trang_thai = models.CharField(max_length=50, default="HoatDong")

    def __str__(self):
        return f"{self.ma_tuyen} - {self.tinh_nhan} -> {self.tinh_giao}"

class GiaCoSo(models.Model):
    tuyen = models.ForeignKey(TuyenXe, on_delete=models.CASCADE, related_name="gia_co_so")
    loai_xe = models.CharField(max_length=100)
    gia_co_so = models.FloatField()
    ngay_ap_dung = models.DateField()
    so_khoi = models.CharField(max_length=50, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

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
    gia_co_so_ref = models.ForeignKey(GiaCoSo, on_delete=models.CASCADE, related_name="lich_su")
    gia_cu = models.FloatField()
    gia_moi = models.FloatField()
    gia_xang = models.FloatField(blank=True, null=True)
    ly_do_doi = models.CharField(max_length=500, blank=True, null=True)
    ngay_doi = models.DateTimeField(auto_now_add=True)

class BaoGiaThongTinXe(models.Model):
    doi_tac = models.ForeignKey(DoiTac, on_delete=models.CASCADE, related_name="bao_gia")
    tuyen = models.ForeignKey(TuyenXe, on_delete=models.CASCADE, related_name="bao_gia")
    tai_trong_tan = models.FloatField()
    so_khoi = models.CharField(max_length=50, blank=True, null=True)
    kich_thuoc = models.CharField(max_length=255, blank=True, null=True)
    loai_thung = models.CharField(max_length=100, blank=True, null=True)
    co_ghep_hang_khong = models.BooleanField(default=False)
    co_chiu_qua_tai_khong = models.BooleanField(default=False)
    co_di_nhieu_diem_khong = models.BooleanField(default=False)
    di_1_hay_2_chieu = models.IntegerField(default=1)
    muc_gia_chap_nhan = models.FloatField()
    ngay_cap_nhat = models.DateTimeField(auto_now=True)
    import django.utils.timezone
    ngay_bat_dau = models.DateField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(default=False)

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
    bao_gia_ref = models.ForeignKey(BaoGiaThongTinXe, on_delete=models.CASCADE, related_name="lich_su")
    gia_cu = models.FloatField()
    gia_moi = models.FloatField()
    gia_xang = models.FloatField(blank=True, null=True)
    ngay_bat_dau = models.DateField(blank=True, null=True)
    ngay_ket_thuc = models.DateField(blank=True, null=True)
    ly_do_doi = models.CharField(max_length=500, blank=True, null=True)
    nguoi_doi = models.CharField(max_length=255, blank=True, null=True)
    ngay_doi_gia = models.DateTimeField(auto_now_add=True)

class DeXuatGiaCoSo(models.Model):
    tuyen = models.ForeignKey(TuyenXe, on_delete=models.CASCADE, related_name="de_xuat_gia")
    loai_xe = models.CharField(max_length=100)
    so_khoi = models.CharField(max_length=50, blank=True, null=True)
    gia_hien_tai = models.FloatField(blank=True, null=True)
    gia_de_xuat = models.FloatField()
    ly_do_de_xuat = models.TextField()
    nguoi_de_xuat = models.CharField(max_length=255)
    
    TRANG_THAI_CHOICES = [
        ('ChoDuyet', 'Chờ duyệt'),
        ('DaDuyet', 'Đã duyệt'),
        ('TuChoi', 'Từ chối'),
    ]
    trang_thai = models.CharField(max_length=50, choices=TRANG_THAI_CHOICES, default='ChoDuyet')
    is_read = models.BooleanField(default=False)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Đề xuất {self.tuyen} - {self.loai_xe} - {self.trang_thai}"

    @property
    def can_undo(self):
        from django.utils import timezone
        from datetime import timedelta
        return self.trang_thai in ['DaDuyet', 'TuChoi'] and (timezone.now() - self.ngay_cap_nhat) <= timedelta(minutes=5)

# Add to models
