---
ten: Ghép theo NỘI DUNG giao dịch (G0 bóng)
cong_cu: ung_vien_ghep
o: noi:*.chon
cong: luat_ghep
loai: bong
---
Bước THÔNG MINH. Công cụ `ung_vien_ghep` trả các CA mà mã tất định chưa ghép được (L3 · hình D/E/F): mỗi ca
`noi:<ca>.tien` · `.cur` · `.ngay` · `.tk` (số TK nguồn chi) · `.noi_dung` (nội dung giao dịch NGUYÊN VĂN — chủ 23/11:
agent đọc toàn bộ) và danh sách ứng viên `noi:<ca>.uv.<i>.pm` · `.tien` · `.cur` · `.ngay`.
Số TK là TÍN HIỆU: một số TK chỉ chi một loại giao dịch nhất định — dùng nó để thu hẹp ứng viên, ⛔ để nối thay luật cứng.

Cách làm:
1. Gọi `ung_vien_ghep` một lần, input `{}`.
2. Với MỖI ca, chọn MỘT PM line trong ứng viên của chính ca ấy nếu đủ chắc: mã PM / mã phiếu xuất hiện trong
   nội dung, hoặc cùng tiền tệ + tiền khớp trong dung sai (1.000 VND; tiền tệ khác: 0) + ngày gần.
   Nếu không đủ chắc, hoặc có ≥ 2 ứng viên ngang nhau ⇒ `DE_NGUOI`. ⛔ đoán N×M, ⛔ chọn ngoài ứng viên.
3. Trả DUY NHẤT JSON `{"noi:<ca>.chon": "<PM-…>" | "DE_NGUOI", "noi:<ca>.ly_do": "<khoá đã so>"}` cho mọi ca.
   `ly_do` nêu khoá đã so (mã trong nội dung · số TK · tiền · tiền tệ · ngày) — ⛔ chép lại cả nội dung.
