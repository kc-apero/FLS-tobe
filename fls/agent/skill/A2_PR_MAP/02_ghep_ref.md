---
ten: Ghép bank ↔ PM theo Reference No (hình A–F)
cong_cu: ghep_ref
o: voi:bank_tong.dong_theo_hinh.*, voi:theo_ky.*.map_fls, voi:theo_ky.*.pm_noi, voi:tong.map_fls, voi:tong.pm_noi, voi:pm_tong.pm_noi_tong, voi:pm_tong.pm_co_ref
cong: tong_ky:map_fls+pm_noi
loai: lam
---
Công cụ chạy `pm_join.xep_ca_lat`: xếp dòng bank theo hình ghép A (1×1) · B (1×N) · C (N×1) · D (N×M, để người) ·
E (khác tiền tệ, để người) · F (Σ lệch, để người); trả số dòng mỗi hình, `map_fls` (dòng ghép được A·B·C theo kỳ),
`pm_noi` (PM line đã nối theo kỳ).

Cách làm (bắt buộc):
1. Gọi công cụ `ghep_ref` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
