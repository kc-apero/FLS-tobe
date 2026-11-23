# KQ-317 — R1 kiểm `I2` · `WO-315` · `BG-316` *(tích hợp HD2 xuyên suốt — Step 47)*

**Kết luận: CÓ SỬA — 1 CHẶN · 2 NÊN SỬA · 3 GHI NHẬN.** Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_I2.md` v0.1. Đo trên `isp/I2` @ `ce771cc` + gộp thử cục bộ `16fbf6d` *(⛔ push)*. Vai KIỂM: ⛔ sửa mã.

| # | Việc | Kết |
|---|---|---|
| 1 | **D1 xuyên chuỗi** | bỏ ký 202510 ⇒ 8/11 gói `FX_CHAN`; **C4a·b·c vẫn ra 35 + 175 + 2.303 = 2.513 ô số**, `HD2_WP_C4` `dat=true` ⇒ **`I2-R1-01` CHẶN** *(bài B2 ghim vi phạm làm `mong`)* |
| 2 | `fx_cua` thật | thật từ kho đã ký 37 tháng, nhưng nối **trong bài** *(mock `nap_fx` 4 chỗ)* ⇒ `-02`. Đột biến tỷ giá ×1,01/×100 mọi tháng: chỉ **3/11** gói đổi số *(C2·C5b·C5c)*; C3a–d·C5a GIỮ ⇒ `-03` |
| 3 | I2-B1 | **11/11** gói khớp `hd2_cong.json` mọi khoá số, lệch FLS 0 *(C5c 86.150/77.672, `dat` null)*; `mong` cùng nguồn ⇒ `-06` |
| 4 | I2-B3 | checksum đưa = ký = JSON ô = đọc lại kho; đột biến cắn |
| 5 | F03 Chromium | C2·C3·C4 ✓ có số; C5 KHÔNG ĐO ĐƯỢC (605) — lệch có tên chấp nhận; sau bỏ ký C2 ✗ + `FX_CHAN 202510` |
| 6 | Lệnh máy chủ | dùng được: ⛔ ghi `fls`, ⛔ `FLS_CHO_GHI_THAT`, ⛔ đòi kho rỗng; Windows bỏ qua Chromium ⇒ `-05` |
| 7 | Sàn | 4.868 = thu thập thật; web 690 |
| 8 | Đột biến | **8/8 cắn** |
| 9 | Cổng | `--duong-nen --cong 5446` ĐẠT **28 = 28** · chạy 4.868 · web 3 = 3 · `lint-imports` 11 kept · `kiem_tai_lieu` ĐẠT · `kiem_thuyet_minh` 35/35 · `soi_bang_tuyen` 49/49 |

**Tập đỏ:** 28 = 28 *(0 thêm)*.
**Gửi orchestrator:** D1 là DECIDED ⇒ `-01` chặn: cần bước nối AL/C4 qua `fx_cua` *(cùng `-02`)* hoặc owner chấp nhận ngoại lệ có tên trước R2; `-03` điều tra độ nhạy; còn lại backlog.
