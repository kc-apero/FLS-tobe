---
ten: Chế độ tự sinh MID (FLS tự tính từ Manual input)
cong_cu: tu_sinh
o: voi:tu_sinh.o, voi:tu_sinh.hd, voi:tu_sinh.mid, voi:tu_sinh.so_dong, voi:tu_sinh.o_loi, voi:tu_sinh.theo_ky.*.o, voi:tu_sinh.theo_ky.*.hd
cong: so_khong_am
loai: lam
---
Công cụ chạy chế độ tự sinh: FLS tự tính MID từ ảnh Manual input rồi Final; trả `[khớp, mẫu]` cho ô 7 khối (`o`),
khối HD (`hd`), MID (`mid`), theo kỳ có ảnh.

Cách làm (bắt buộc):
1. Gọi công cụ `tu_sinh` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
