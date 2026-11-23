---
ten: Nguồn Bank txns — ảnh sao kê + sổ AS-IS
cong_cu: nguon_bank
o: nguon:bank.*, nguon:so_asis.*
cong: khop_khai:bank+so_asis
loai: lam
---
Nguồn 1/4 · Bank txns. Công cụ đọc ảnh đóng băng giao dịch bank (`tests/fixture/pm_join.json`, 9 992 dòng tự khai)
và ảnh sổ AS-IS `ITL Ledge` (`tests/fixture/itl_ledge_adjustment.json`), trả cho mỗi ảnh: `so_dong` (ảnh tự khai) ·
`dem_dong` (máy đếm lại) · `van_tay` (checksum nội dung 16 hex).

Cách làm (bắt buộc):
1. Gọi công cụ `nguon_bank` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
