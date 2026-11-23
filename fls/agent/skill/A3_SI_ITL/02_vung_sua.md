---
ten: Vùng chỉnh tay R–AT: ô người gõ · ô mặc định · theo khối
cong_cu: vung_sua
o: voi:khoi_theo_ky.*.*, voi:theo_ky.*.o_go_that, voi:theo_ky.*.o_mac_dinh, voi:tong.o_go_that, voi:tong.o_mac_dinh, voi:tong.o_trong, voi:tong.o_de
cong: tong_ky:o_go_that+o_mac_dinh
loai: lam
---
Công cụ trả, theo kỳ × khối, cặp [máy trả lời, người phải điền]; `o_go_that` (ô người gõ giá trị thật) ·
`o_mac_dinh` (ô nhận mặc định cứng của khối) · `o_trong` · `o_de` (Final ≠ Classifying dù máy trả lời).

Cách làm (bắt buộc):
1. Gọi công cụ `vung_sua` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
