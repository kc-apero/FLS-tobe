# WO-353 — (C1) khuôn đóng băng bộ ba HD1 tháng 8 từ nguồn sống · (C3) chụp lại 615 + DR2 + số dư CÙNG một lượt

| | |
|---|---|
| **Trạng thái** | `CHO_TEST` — Dev bàn giao ở `BG-346` §WO-353 23/11 *(giao 23/11 ~11:45 UTC)* |
| **Phát bởi** | orchestrator · 2026-11-23 |
| **Nhận** | `fls-dev` làn DATA — tiếp phiên sửa SONG (`session_01Ci2qSM8bmqGM9t6nfZbDu1`) · nhánh `claude/bold-galileo-zukpaf-isp/SONG` |
| **Dải phiếu** | báo cáo trong `BG-346` mục mới · R2 cuối SONG = `KQ-354`. Số trống kế tiếp: **355** |

## Vì sao — quyết chủ 23/11 ~11:45 (BG-346 §Câu chủ, chọn khuyến nghị)
- **C1 = ⓐ:** viết khuôn `pm_join` + `l1_canon` (+ khuôn cho `itl_ledge_adjustment` · `classifying_vs_canon` nếu cùng gốc) trên hàm có sẵn (`fls.adapters.pm_join` · `fls.adapters.bank` · `tools/nap_that.py` `doc_pm`/`doc_nguon`) ⇒ đóng băng LẠI bộ ba từ nguồn sống ⇒ đo lại "HD1 kỳ đạt · dòng ghép 1-1" GIỮ NGUYÊN định nghĩa đã ký (⛔ đổi mẫu số sang ITL Ledge).
- **C3 = ⓐ:** khuôn DT13 khai lại `N_HANG` (2.502 → 2.566 nguồn sống) + `MONG_CHECK` ⇒ đóng băng 615 + DR2 + số dư **CÙNG một lượt đọc** ⇒ đo lại `WP-C5c` (mong lệch FLS 0; còn lệch ⇒ ĐỎ có tên = lỗi thật, ⛔ khai lớp `lech_thoi_diem_anh`).

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 | khuôn mới theo chuẩn `tools/khuon_dong_bang/*` (khai `mong` hàng/ô, nhãn Đ4, checksum, ⛔ PII — `Email Address` ⛔, số TK cá nhân che `TK_CA_NHAN_n`); ảnh CŨ giữ làm biên bản | cổng `--mong` + pytest |
| AC-2 | HD1 đo lại trên bộ ba MỚI: kỳ đạt · dòng ghép 1-1 · ô parity — bảng CŨ ↔ MỚI có nhãn, vào bảng "số cần ký lại" | BG-346 |
| AC-3 | 615 + DR2 + số dư một lượt (giờ đọc ghi rõ) ⇒ `WP-C5c` lệch FLS = 0 hoặc ĐỎ có tên từng ô | `do_hd2.py --goi WP-C5c` + pytest |
| AC-4 | sinh lại bản ghi phát lại + report agent nếu số đổi (KẾT ĐẠT); `--duong-nen` ĐẠT 28 = 28 · web 3 = 3; `kiem_tai_lieu` · `lint-imports` · `quet_pii_repo` 0 | `--duong-nen` |

## Ràng buộc
- SA chỉ-đọc, ⛔ ghi sheet; bản thô `/tmp` chmod 600, xoá sau; ⛔ ghi kho THẬT; ⛔ nới `mong`; ⛔ đổi định nghĩa HD1.
