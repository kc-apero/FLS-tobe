---
ten: Cổng HD2: parity từng gói báo cáo · phân bổ
cong_cu: cong_hd2
o: cong:HD2.*.dat
cong: cong_doc
loai: lam
---
Công cụ gọi `doc_cong_hd2` (cổng HD2 theo gói của FLS), trả `dat` mỗi cổng gói cha + gói con.

Cách làm (bắt buộc):
1. Gọi công cụ `cong_hd2` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
