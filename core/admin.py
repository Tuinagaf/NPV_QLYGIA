from django.contrib import admin
from .models import DoiTac, TuyenXe, GiaCoSo, LichSuGiaCoSo, BaoGiaThongTinXe, LichSuBaoGia

@admin.register(DoiTac)
class DoiTacAdmin(admin.ModelAdmin):
    list_display = ['ma_nha_xe', 'ten_nha_xe', 'nguoi_quan_ly', 'so_dien_thoai', 'tinh_san_sang', 'co_hop_dong']
    list_filter = ['tinh_san_sang', 'co_hop_dong']
    search_fields = ['ma_nha_xe', 'ten_nha_xe', 'nguoi_quan_ly', 'so_dien_thoai']
    list_per_page = 20
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('ma_nha_xe', 'ten_nha_xe', 'dia_chi', 'nguoi_quan_ly', 'nguoi_dai_dien', 'so_dien_thoai', 'ten_zalo')
        }),
        ('Thông tin hóa đơn', {
            'fields': ('ten_don_vi_xuat_hoa_don', 'dia_chi_xuat_hoa_don', 'ma_so_thue', 'so_tai_khoan', 'ngan_hang')
        }),
        ('Đánh giá & Hợp đồng', {
            'fields': ('tinh_san_sang', 'chat_luong', 'co_hop_dong', 'thoi_han_thanh_toan')
        }),
        ('Ghi chú', {
            'fields': ('ghi_chu',),
            'classes': ('collapse',)
        }),
    )

@admin.register(TuyenXe)
class TuyenXeAdmin(admin.ModelAdmin):
    list_display = ['ma_tuyen', 'tinh_nhan', 'huyen_nhan', 'tinh_giao', 'huyen_giao', 'trang_thai']
    list_filter = ['trang_thai', 'tinh_nhan', 'tinh_giao']
    search_fields = ['ma_tuyen', 'tinh_nhan', 'tinh_giao']
    list_per_page = 20

@admin.register(GiaCoSo)
class GiaCoSoAdmin(admin.ModelAdmin):
    list_display = ['tuyen', 'loai_xe', 'gia_co_so', 'so_khoi', 'ngay_ap_dung']
    list_filter = ['loai_xe', 'ngay_ap_dung']
    search_fields = ['tuyen__ma_tuyen', 'loai_xe']
    date_hierarchy = 'ngay_ap_dung'
    list_per_page = 20

@admin.register(LichSuGiaCoSo)
class LichSuGiaCoSoAdmin(admin.ModelAdmin):
    list_display = ['gia_co_so_ref', 'gia_cu', 'gia_moi', 'gia_xang', 'ngay_doi', 'ly_do_doi']
    list_filter = ['ngay_doi']
    search_fields = ['ly_do_doi']
    date_hierarchy = 'ngay_doi'
    readonly_fields = ['ngay_doi']
    list_per_page = 20

@admin.register(BaoGiaThongTinXe)
class BaoGiaThongTinXeAdmin(admin.ModelAdmin):
    list_display = ['doi_tac', 'tuyen', 'tai_trong_tan', 'loai_thung', 'muc_gia_chap_nhan', 'di_1_hay_2_chieu', 'ngay_cap_nhat']
    list_filter = ['loai_thung', 'di_1_hay_2_chieu', 'co_ghep_hang_khong', 'ngay_cap_nhat']
    search_fields = ['doi_tac__ten_nha_xe', 'tuyen__ma_tuyen']
    date_hierarchy = 'ngay_cap_nhat'
    readonly_fields = ['ngay_cap_nhat']
    list_per_page = 20
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('doi_tac', 'tuyen', 'tai_trong_tan', 'kich_thuoc', 'loai_thung')
        }),
        ('Điều kiện vận chuyển', {
            'fields': ('co_ghep_hang_khong', 'co_chiu_qua_tai_khong', 'co_di_nhieu_diem_khong', 'di_1_hay_2_chieu')
        }),
        ('Giá cả', {
            'fields': ('muc_gia_chap_nhan',)
        }),
        ('Thông tin khác', {
            'fields': ('ngay_cap_nhat',),
            'classes': ('collapse',)
        }),
    )

@admin.register(LichSuBaoGia)
class LichSuBaoGiaAdmin(admin.ModelAdmin):
    list_display = ['bao_gia_ref', 'gia_cu', 'gia_moi', 'gia_xang', 'nguoi_doi', 'ngay_doi_gia', 'ly_do_doi']
    list_filter = ['ngay_doi_gia', 'nguoi_doi']
    search_fields = ['ly_do_doi', 'nguoi_doi']
    date_hierarchy = 'ngay_doi_gia'
    readonly_fields = ['ngay_doi_gia']
    list_per_page = 20
