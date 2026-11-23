---
ten: Hàng chờ người + mốc NOW (VLOOKUP)
cong_cu: hang_cho
o: voi:theo_ky.*.map_now, voi:theo_ky.*.day_nguoi, voi:tong.map_now, voi:tong.day_nguoi, voi:dat_hd1.theo_ky.*.thieu, voi:dat_hd1.dem.thieu
cong: tong_ky:map_now+day_nguoi
loai: lam
---
Công cụ trả `map_now` (dòng mà VLOOKUP của Gsheet AS-IS trả được mã HD — mốc so sánh) · `day_nguoi` (dòng đẩy
cho người) theo kỳ, và `thieu` (dòng sổ chưa dựng 1-1) theo kỳ của phán HD1.

Cách làm (bắt buộc):
1. Gọi công cụ `hang_cho` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
