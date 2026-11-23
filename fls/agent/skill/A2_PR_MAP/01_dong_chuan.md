---
ten: Dựng dòng chuẩn 1-1 với sổ AS-IS theo kỳ
cong_cu: dong_chuan
o: voi:theo_ky.*.co, voi:theo_ky.*.chay, voi:tong.co, voi:tong.chay
cong: tong_ky:co+chay
loai: lam
---
Công cụ chạy engine FLS (`pm_join` + canon) trên ảnh đóng băng, trả theo kỳ: `co` = dòng sổ AS-IS ·
`chay` = dòng FLS dựng lại và ghép 1-1 được với dòng sổ (khoá Số CT · PS Nợ · PS Có · TK · tiền tệ).

Cách làm (bắt buộc):
1. Gọi công cụ `dong_chuan` ĐÚNG MỘT LẦN, input `{}`.
2. Trả về DUY NHẤT một đối tượng JSON `{"<mã ô>": <giá trị>, …}` gồm MỌI ô công cụ trả, giá trị CHÉP NGUYÊN.
3. ⛔ tính lại · ⛔ làm tròn · ⛔ đổi kiểu (số giữ là số, chuỗi giữ là chuỗi) · ⛔ thêm ô công cụ không trả ·
   ⛔ bịa ô công cụ thiếu (bỏ trống — A4 sẽ bắt). ⛔ chữ nào ngoài JSON.
