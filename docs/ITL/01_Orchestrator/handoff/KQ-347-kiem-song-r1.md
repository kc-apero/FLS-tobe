# KQ-347 — biên bản kiểm `BG-346` *(R1 · `WO-345`)*

| | |
|---|---|
| **Thuộc** | `BG-346` · `WO-345` |
| **Kiểm bởi** | `fls-test` · 2026-11-23 · nhánh `claude/bold-galileo-zukpaf-isp/SONG` @ `26edcf1` |
| **Phán quyết** | **TRƯỢT** — **2 CHẶN · 1 NÊN SỬA · 3 GHI NHẬN** *(sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_SONG.md`)* |

## Năm mục kiểm
| # | Mong | Đo được *(nhãn · mẫu số)* | |
|---|---|---|:-:|
| 1 | Ảnh mới = nguồn sống | Tự đọc `ITL Ledge` lúc **10:03Z**: Σ cột A **12.722** = manifest *(lệch 0)*; 5 kỳ: 2026-11 · 748 dòng · 22.440 ô · 2025-10 · 487 · 14.610 · 2026-03 · 584 · 17.520 · 2025-01 *(≡)* 748 · 22.440 · 2025-07 *(≡)* 546 · 16.380 ⇒ **ô lệch 0**, checksum tính lại = manifest cả 5. Ảnh cũ: diff `c173338..26edcf1` ⛔ sửa/xoá tệp ảnh nào | ✅ |
| 2 | Đo lại đúng | `do_voi_so_luong.py --ghi` sinh lại = `voi_so_luong.json` **diff 0**; 11 gói HD2 ảnh MỚI = bảng BG; CŨ↔MỚI: **10/11 gói y hệt**, `WP-C5c` × số dư mới `khop` 77.593 *(cũ 77.672)* · lệch FLS **79** *(lớp lệch thời điểm, G3)*. `hd2_cong.json` chỉ có `WP-C2` ⇒ `SONG-R1-03` | ⚠ |
| 3 | ⛔ nới `mong` | Mọi `mong` đổi có số cũ trong chú thích = số đo mới *(2026-11 748/5.236 · 2026-03 MID 4.022 · Σ 88.962/89.054 · HD 12.722)*; ⛔ hạ ngưỡng; `duong_nen_bai_do.txt` ⛔ đổi — nhưng tập đỏ nền thực đo **34** ≠ 28 ⇒ mục 5 | ⚠ |
| 4 | Riêng tư | 5 ảnh mới: "email" xuất hiện **1 lần/tệp, chỉ trong `ghi_chu`**, `@` = 0; `quet_pii_repo` **0 chỗ · 0 tệp** *(cây gộp thử)* | ✅ |
| 5 | Cây gộp thử | `--duong-nen --cong 5447` **KẾT: ĐỎ**: toàn bộ **18 failed · 14 errors · 2 xfailed**, tập đỏ 34 vs mong 28 *(thêm **6** = 5 `tests/agent/test_chuoi.py` + 1 `test_dau_vao_dt13` · bớt 0)*, chạy 4.961 ≥ sàn; web **3 = 3** ĐẠT. Cổng giấy ĐẠT: `kiem_tai_lieu` (509 tệp) · `lint-imports` 11 kept · `soi_bang_tuyen` 49/49 · `quet_pii_repo` 0 | ⛔ |

## Vì sao TRƯỢT
- **`SONG-R1-01`** `.DO.json` bị `.gitignore:26` ⇒ bài DT13 đỏ trên cây sạch *(Dev chạy xanh vì tệp có sẵn ở máy)*.
- **`SONG-R1-02`** số HD1 mới làm hỏng bản ghi PHÁT LẠI agent `WO-329`: nhánh nền `test_chuoi.py` 13 passed ↔ cây gộp 5 failed.

## Số cần chủ / ThuongCT ký lại *(tóm tắt — ⛔ tự coi đã ký)*
1. HD1 tự sinh 26 kỳ: ô Final 88.339/88.431 → **88.962/89.054**; HD 12.633 → **12.722**; MID 82.362 → **82.987** (/89.054).
2. 2026-11: 659 dòng · 4.613 ô → **748 · 5.236**. 2026-03 MID 4.020 → **4.022**.
3. HD1 5/23 kỳ đạt · 9.845/9.967: **chưa đo lại được** *(bộ ba ảnh tháng 8 ⛔ khuôn — câu C1)*.
4. HD2: 10 gói ⛔ đổi; `WP-C5c` đọc số dư mới ⇒ 79 lệch FLS *(C3)*.
5. Số kèm: bản ghi agent A3 + report HTML của `WO-329` phải ghi lại theo số mới *(`SONG-R1-02`)*.
