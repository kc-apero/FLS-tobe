---
ten: Ô Final 7 khối + khối HD theo kỳ (parity)
cong_cu: final_7_khoi
o: voi:theo_ky.*.o_parity, voi:theo_ky.*.o_parity_khop, voi:theo_ky.*.hd_parity, voi:theo_ky.*.hd_parity_khop, voi:tong.o_parity, voi:tong.o_parity_khop, voi:tong.hd_parity, voi:tong.hd_parity_khop, voi:tong.loai_tu_soi
cong: khop_le_mau:o_parity+hd_parity
loai: lam
---
Công cụ chạy `final_rule.tinh_final` + `tu_soi.soi_mot_dong` trên sổ đóng băng: `o_parity` = ô Final 7 khối
được so · `o_parity_khop` = ô FLS = Final sổ · `hd_parity(_khop)` = riêng khối HD · `loai_tu_soi` = dòng tự-soi loại.

Cách làm (bắt buộc):
1. Gọi công cụ `final_7_khoi` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
