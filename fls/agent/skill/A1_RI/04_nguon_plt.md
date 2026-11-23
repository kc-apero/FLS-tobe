---
ten: Nguồn PLT — 4 nền tảng GI · OMC · SC · PS
cong_cu: nguon_plt
o: nguon:gi.*, nguon:omc.*, nguon:sc.*, nguon:ps.*
cong: khop_khai:gi+omc+sc+ps
loai: lam
---
Nguồn 4/4 · PLT. Công cụ đọc ảnh GI (CFA1 GI Platform Data Ledger) và MID1 của OMC · SC · PS,
trả cho mỗi nguồn `so_dong` · `dem_dong` · `van_tay`.

Cách làm (bắt buộc):
1. Gọi công cụ `nguon_plt` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
