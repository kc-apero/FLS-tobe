# WO-345 — Đóng băng LẠI ảnh HD1/HD2 từ NGUỒN SỐNG (chủ quyết 23/11: nguồn sống là chuẩn) + đo lại `voi_so_luong.json` · `hd2_cong.json`

| | |
|---|---|
| **Trạng thái** | `MO` — giao 23/11 ~08:30 UTC |
| **Phát bởi** | orchestrator · 2026-11-23 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud **Opus 5.5 · medium** · nhánh `claude/bold-galileo-zukpaf-isp/SONG` (nền = ngọn nhánh làm việc) |
| **Dải phiếu** | `BG-346` · `KQ-347` (R1) · `KQ-348` (R2 cuối). Số trống kế tiếp sau dải: **349** |

## Vì sao — quyết chủ 23/11
- ~07:25 *"Tạo PR vào main, lấy nguồn sống làm chuẩn"*; ~08:30 *"cho phép mở"* WO này.
- WO-334/BG-335 đo: nguồn sống ≠ ảnh đóng băng 26–27/08 ở kỳ đã chốt — `Transaction Mapping L1` 10.100 → 14.265 dòng (canon 12.601: 10.187 ở 23 kỳ đã chốt · 2.414 kỳ mới); PM 3.703 → 3.909, ảnh lệch `cdt1` 534 · `hd` 117 · `status` 29 · `ref` 30; bank 37 bộ ba (ref, cur, tiền) của ảnh ⛔ còn ở nguồn sống. Mọi số HD1/HD2 (kể cả số trong PR `kc-apero/FLS-tobe#1` và số ThuongCT ký O6) đo trên ảnh cũ.
- Quyền: chủ đang cấp Viewer cho SA `fls-sheets-reader` trên `P100 | Bank Transactions` + `Copy of P100 | Cash Ledger` (trước đó 403). Workbook nào còn 403 ⇒ DỪNG phần ấy, ĐỎ có tên.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 · danh mục | liệt kê MỌI ảnh đóng băng mà cổng HD1/HD2 đang đọc (`tests/fixture/**` · ảnh của `tools/do_voi_so_luong.py` · `tests/fixture/dau_vao/*.json` · đáp án DT*) + workbook/tab/vùng nguồn + khuôn đóng băng sinh ra nó (`tools/khuon_dong_bang/*`) — Đ1: grep `docs/` LẪN `fls/` + `tools/` | BG |
| AC-2 · đóng băng lại | chạy lại KHUÔN có sẵn (⛔ chép) trên nguồn sống ⇒ ảnh MỚI có phiên bản/ngày (`…_20261123`), ảnh CŨ GIỮ làm biên bản (Đ2 — ⛔ xoá lịch sử); mỗi ảnh khai `mong` (số hàng/ô), nhãn Đ4, checksum tính lại; PII như mọi bước DT (`Email Address` ⛔ · số TK cá nhân che `TK_CA_NHAN_n` trong REPO · `quet_pii_repo` 0) | cổng `--mong` + pytest |
| AC-3 · đo lại | `do_voi_so_luong.py` + `do_hd2.py` (11 gói) trên ảnh MỚI ⇒ `voi_so_luong.json` · `hd2_cong.json` mới; **bảng CŨ ↔ MỚI từng số có nhãn** (HD1: dòng ghép 1-1, ô parity, kỳ đạt; HD2: ô so · khớp · lệch có tên · lệch FLS mỗi gói) | BG |
| AC-4 · khớp 100 % | ảnh MỚI = nguồn sống lúc chụp: Σ dòng/ô từng nguồn khớp 100 %, lệch 0 (phép ⛔ đo được ⇒ ĐỎ); lệch FLS mỗi gói HD2 vẫn **0** — gói nào ≠ 0 ⇒ ĐỎ có tên, phân lớp (⛔ nới `mong`) | pytest |
| AC-5 · cổng | `mong` của bài ghim đổi theo số đo MỚI cùng commit (⛔ nới — mỗi mong mới kèm số cũ trong chú thích); `--duong-nen` ĐẠT (tập đỏ nền — khai nếu đổi, kèm lý do từng node); `kiem_tai_lieu` · `lint-imports` · `soi_bang_tuyen` · `quet_pii_repo` 0 | `--duong-nen` |
| AC-6 · câu chủ | số MỚI khác số đã ký O6 ⇒ liệt kê để chủ/ThuongCT ký lại (⛔ tự coi là đã ký) | BG |

## Ràng buộc
- SA CHỈ-ĐỌC (⛔ ghi/nhận xét sheet — `QĐ-ITL-34`); khoá ⛔ in/commit; bản thô `/tmp` chmod 600, xoá sau. Ghi kho THẬT: `KHONG`.
- ⛔ sửa engine/tuyến; ⛔ đổi luật D1–D5. Nhánh KHÔNG gộp trước khi PR #1 merge (quyết chủ 23/11).
