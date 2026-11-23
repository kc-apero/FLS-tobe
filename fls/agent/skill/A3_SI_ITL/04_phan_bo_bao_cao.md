---
ten: Calculate · Allocate · Report — parity 10 gói HD2
cong_cu: phan_bo_bao_cao
o: hd2:*.khop, hd2:*.tong_o, hd2:*.lech_co_chu_dich
cong: hd2_dem
loai: lam
---
Công cụ trả kết quả engine HD2 từng gói: WP-C2 GL · C3a CFA1 Daily · C3b CFA1 Y/H/Q/M · C3c GL HR + CFA3 ·
C3d PLA · C4a/b/c phân bổ nền tảng · C5a khoá ALR · C5b ATL — `tong_o` ô đáp án so · `khop` ô khớp ·
`lech_co_chu_dich` ô lệch CÓ TÊN (AS-IS sai đã khai, ⛔ lỗi FLS).

Cách làm (bắt buộc):
1. Gọi công cụ `phan_bo_bao_cao` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
