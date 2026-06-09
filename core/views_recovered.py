Created At: 2026-06-04T01:48:40Z
Completed At: 2026-06-04T01:48:40Z
File Path: `file:///d:/NPV/NPV_QLYGIA/core/views.py`
Total Lines: 1091
Total Bytes: 48329
Showing lines 168 to 967
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
168:             huyen_giaos = request.POST.getlist('huyen_giao[]')
169:             tai_trongs = request.POST.getlist('tai_trong_tan[]')
170:             so_khois = request.POST.getlist('so_khoi[]')
171:             kich_thuocs = request.POST.getlist('kich_thuoc[]')
172:             loai_thungs = request.POST.getlist('loai_thung[]')
173:             muc_gias = request.POST.getlist('muc_gia_chap_nhan[]')
174:             ghep_hangs = request.POST.getlist('co_ghep_hang_khong[]')
175:             qua_tais = request.POST.getlist('co_chiu_qua_tai_khong[]')
176:             nhieu_diems = request.POST.getlist('co_di_nhieu_diem_khong[]')
177:             chieu_dis = request.POST.getlist('di_1_hay_2_chieu[]')
178:             
179:             new_routes_data = []
180:             for i in range(len(tinh_nhans)):
181:                 new_routes_data.append({
182:                     'tinh_nhan': tinh_nhans[i],
183:                     'huyen_nhan': huyen_nhans[i] if i < len(huyen_nhans) else '',
184:                     'tinh_giao': tinh_giaos[i] if i < len(tinh_giaos) else '',
185:                     'huyen_giao': huyen_giaos[i] if i < len(huyen_giaos) else '',
186:                     'tai_trong_tan': tai_trongs[i] if i < len(tai_trongs) else '',
187:                     'so_khoi': so_khois[i] if i < len(so_khois) else '',
188:                     'kich_thuoc': kich_thuocs[i] if i < len(kich_thuocs) else '',
189:                     'loai_thung': loai_thungs[i] if i < len(loai_thungs) else '',
190:                     'muc_gia_chap_nhan': muc_gias[i] if i < len(muc_gias) else '',
<truncated 36242 bytes>
(p): tinh_giao = tinh_giao[len(p):]
929:             
930:         gcs = GiaCoSo.objects.filter(tuyen__tinh_nhan=tinh_nhan, tuyen__tinh_giao=tinh_giao, loai_xe=loai_xe).first()
931:         if gcs:
932:             return JsonResponse({'success': True, 'gia_co_so': gcs.gia_co_so, 'so_khoi': gcs.so_khoi})
933:         return JsonResponse({'success': True, 'gia_co_so': None})
934:     except Exception as e:
935:         return JsonResponse({'success': False, 'error': str(e)})
936: 
937: @login_required
938: def api_delete_partner(request, pk):
939:     if request.method != 'POST': return JsonResponse({'success': False})
940:     try:
941:         if request.user.is_superuser: p = DoiTac.objects.get(pk=pk)
942:         else: p = DoiTac.objects.get(pk=pk, nguoi_quan_ly=request.user.username)
943:         p.is_deleted = True; p.save()
944:         return JsonResponse({'success': True})
945:     except Exception as e: return JsonResponse({'success': False})
946: 
947: @login_required
948: def api_delete_base_price(request, pk):
949:     if request.method != 'POST': return JsonResponse({'success': False})
950:     try:
951:         if not request.user.is_superuser: return JsonResponse({'success': False})
952:         p = GiaCoSo.objects.get(pk=pk)
953:         p.is_deleted = True; p.save()
954:         return JsonResponse({'success': True})
955:     except Exception as e: return JsonResponse({'success': False})
956: 
957: 
958: @login_required
959: def api_check_duplicate_partner_routes(request):
960:     if request.method != 'POST':
961:         return JsonResponse({'success': False, 'error': 'Invalid method'})
962:         
963:     try:
964:         data = json.loads(request.body)
965:         partner_id = data.get('partner_id')
966:         new_routes = data.get('new_routes', [])
967:         
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
