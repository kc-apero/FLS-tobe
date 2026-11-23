---
ten: Nguồn FPS (PAY100) — PM line
cong_cu: nguon_fps
o: nguon:fps.*
cong: khop_khai:fps
loai: lam
---
Nguồn 2/4 · FPS. Công cụ đọc ảnh `[Importrange]PM_Unpivot` (một dòng mỗi PM line, `tests/fixture/pm_join.json`),
trả `so_dong` · `dem_dong` · `van_tay` · `co_ref` (dòng có Reference No).

Cách làm (bắt buộc):
1. Gọi công cụ `nguon_fps` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
