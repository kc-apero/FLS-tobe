---
ten: Cổng HD1: ô Final + kỳ đạt
cong_cu: cong_hd1
o: cong:HD1.*.dat, voi:dat_hd1.so_ky_dat, voi:dat_hd1.mau_so.so_ky, voi:dat_hd1.theo_ky.*.dat
cong: cong_doc
loai: lam
---
Công cụ gọi `doc_cong_tep_do` (cổng FINAL · HD1_THANG của FLS) và trả phán từng kỳ của HD1.
`dat` = true / false / null (null = CHƯA ĐO ĐƯỢC — chép null, ⛔ đổi thành true).

Cách làm (bắt buộc):
1. Gọi công cụ `cong_hd1` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
