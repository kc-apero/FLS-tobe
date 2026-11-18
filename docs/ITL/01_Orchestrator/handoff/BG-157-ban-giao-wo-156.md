# BG-157 — bàn giao `WO-156` (DT1b nhãn THẬT trên mốc mới 18/11)

| | |
|---|---|
| **Thuộc** | `WO-156` |
| **Phát bởi** | `fls-dev` (phiên cloud con, làn DATA) · 2026-11-18 |
| **Nhận** | người dùng kiểm bảng §Tóm tắt ⇒ `fls-test` (`KQ-158` R1) |
| **Commit** | `isp/DT1BM` → nhánh `claude/bold-galileo-zukpaf-isp/DT1BM` @ `c98f1df` (mã+bài+ảnh mốc+nhãn) · BG @ `<SHA-②>` |

## ⭐ Tóm tắt cho người dùng kiểm *(CHỈ số đếm + `dong_sheet`; ⛔ giá trị ô)*
Mốc: SO = CSV Drive `1U-IQVOXBbGE6X6n0i0mi3IG9VWc9J_Ap` (đọc 18/11 09:3x UTC) · L1 = RAW `1xaD1R…`/`Transaction Mapping L1` (cột `B` `D:G`, ⛔ `C`; đọc `UNFORMATTED_VALUE`). `dong_sheet` = số bản ghi CSV = hàng sheet SO.

| Chỉ số | Số | Đếm gì (Đ4) |
|---|---|---|
| Hàng CSV SO (cả đầu/đuôi) | 12.621 | bản ghi CSV; tiêu đề hàng 7, dữ liệu từ hàng 10 ⇒ 12.612 hàng |
| **Dòng SO dùng** | **12.590** | hàng có ≥1 ô khoá. **Loại 22 hàng** (dòng 12600–12621): chỉ có cột công thức phụ, 0 ô khoá — ⛔ phải giao dịch |
| Dòng L1 | 12.590 | hàng có ≥1 ô khoá (= SO: hai nguồn khớp số) |
| **Khớp 1-1** (khoá + seq) | **12.571** | dòng SO có bạn L1 cùng khoá; tái lập tính bằng 2 đường (Σ min theo nhóm ↔ duyệt theo seq) đều 12.571 |
| **Thiếu** | **19** | = 0,15 % SO (ngưỡng "lạ" của lệnh: > 20 %) |
| Nhãn `KHONG_CO_SAO_KE` | 12 | L1 ⛔ có dòng khoá ấy, ⛔ dòng L1 mồ côi cùng Số CT |
| Nhãn `KHOA_LECH` | 7 | cả 7 lệch đúng trường `ps_co` |
| Nhãn `TRUNG_SEQ` · `KHAC`/"chưa rõ" | 0 · 0 | khoá hỏng SO/L1 = 0 · 0 |
| Số CT dạng khoa học | SO 43 · L1 43 | chẩn đoán |

`dong_sheet` mẫu để mở sheet SO đối chiếu tay *(đủ cả 19 dòng, vì ít)*:
- `KHONG_CO_SAO_KE` (12): 704 · 771 · 1024 · 1054 · 1055 · 1352 · 1602 · 1684 · 1863 · 2022 · 2371 · 2439
- `KHOA_LECH` (7, trường lệch `ps_co`): 2566 · 4735 · 4736 · 4737 · 6248 · 6249 · 6250 *(4735–4737 · 6248–6250 là hai cụm liền nhau)*
- Cách kiểm: mở dòng đó ở SO, so Số CT/Tiền/TK với L1 (`KHOA_LECH` ⇒ L1 có dòng cùng Số CT nhưng `PS Có` khác; `KHONG_CO_SAO_KE` ⇒ L1 ⛔ có).

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/phan_loai_ly_do.py` | **mốc tham số** `--moc`: `do_moc_moi` (tập thiếu từ khoá+seq), `kiem_anh_moc`, `moc_tu_anh`, `MONG_MOC` (ghim); `kiem`/`phan_xu` nhận mốc (K1/K3/K9/K10/K11 theo số KHAI, ⛔ gõ cứng 9.967/9.845/122); mặc định 26/08 ⛔ đổi; cổng tự nhận mốc theo `nguon.anh_so` của tệp nhãn |
| `tools/xuat_khoa_dt1b.py` | `--so-csv` + `doc_so_csv` (CSV SO, từ hàng 10, ⛔ cột `Diễn giải`, bỏ hàng 0 ô khoá) |
| `tests/fixture/dt1b_moc_20261118.json` | ảnh mốc gọn: `nguon` (id · tên · thời điểm) · `so_dong` · `so_khop` · `so_thieu` · mỗi dòng `{dong_sheet, khoa_bam, khop}` — ⛔ PII (782 KB) |
| `docs/ITL/_tools/phan_loai_ly_do_moc_20261118.json` | tệp nhãn: 19 dòng, mỗi dòng ĐÚNG một nhãn |
| `tests/du_lieu/test_phan_loai_ly_do_moc_moi.py` | +11 bài (TDD: ĐỎ trước — fixture/`do_moc_moi` chưa có) |
| `tests/du_lieu/test_phan_loai_ly_do.py` | `RA_THAT` trỏ tệp mới; nhánh "tệp thật" canh `MONG_MOC` khi tệp khai mốc mới |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | sàn `MONG_PYTEST_TOAN_BO` 3296 → 3307 (+11) cùng commit (Q8) |

## ⚠ Lệch chữ WO — cần orchestrator quyết
1. **Tên tệp nhãn** `phan_loai_ly_do_moc_20261118.json`, ⛔ `phan_loai_ly_do.json` như WO §3. Lý do đo được: H2 `tools/do_voi_so_luong.py:113` đọc đúng tên cũ và đòi tập dòng = 122 dòng thiếu 26/08 ⇒ ghi nhãn mốc mới vào đó làm ĐỎ H2 (`tests/oracle/test_do_voi_hd1.py` ≥4 bài + `do_voi_so_luong.py` báo "dong_sheet … ngoài tập 158"). Đổi tên về cũ = một dòng (`RA`), nhưng cần H2 hiểu mốc mới (= phương án B). Đến lúc đó H2 đọc nhãn **vắng** ("chưa có nhãn") như trước.
2. **22 hàng đuôi SO loại** (xem trên) — giữ lại ⇒ 22 dòng "thiếu" giả (đo: thiếu 41 thay vì 19).
3. **Lần đọc đầu L1 dùng `FORMATTED_VALUE` ⇒ thiếu 7.153 (56,7 %)** — làm tròn theo định dạng hiển thị (2.893 dòng lệch < 1 đơn vị). DỪNG, tìm ra nguyên nhân là cách ĐỌC của tôi, đổi `UNFORMATTED_VALUE` ⇒ 19. Ghi lại vì L1 đọc kiểu nào cũng là một mốc: **ghim ảnh mốc kèm cách đọc này**.
4. `ky` của mốc mới = `"-"` (mốc mới ⛔ xuất cột ngày): `nhan_theo_ky` chỉ có một nhóm.

## Cổng *(nguyên văn)*
| Lệnh | Kết quả |
|---|---|
| `python tools/phan_loai_ly_do.py` | `KẾT: ĐẠT — … 19 dòng sổ thiếu, mỗi dòng đúng một nhãn` (mã 0) |
| `… --khoa <khoá> --moc tests/fixture/dt1b_moc_20261118.json` | `KẾT: ĐẠT` (K10 · K11 so với số KHAI trong ảnh) |
| `pytest tests/du_lieu tests/oracle/test_do_voi_hd1.py` | xanh |
| `--duong-nen` (MỘT lần cuối) | `ĐẠT — tập đỏ = đường nền 28 = 28 (thêm 0 · bớt 0) · chạy 3307 bài (mong ≥ 3307) · skipped 0 · deselected 0; tests/web 3 = 3 · 667 bài` |
| K10 / K11 / PII | K10 tái lập 12.571 = khai 12.571 · K11 tập 12.590 dòng = ảnh · R1–R8 (PII) ĐẠT, 0 token Số CT/tiền |

## Bằng chứng từng AC
| AC | Bằng chứng |
|---|---|
| AC-1 | `tests/du_lieu` (435 bài cũ) xanh; `MONG` 26/08 ⛔ đổi (`…::test_AC1_mac_dinh_van_la_moc_26_08`); ảnh 26/08 ⛔ chạm (`git diff` rỗng) |
| AC-2 | `test_AC2_K10…` · `test_AC2_K11…` · `test_AC2_pha_anh_moc_them_bot_1_dong…` (thêm/bớt 1 dòng ⇒ ĐỎ, trả nguyên ⇒ ĐẠT); chạy thật: K10/K11 ĐẠT |
| AC-3 | cổng `python tools/phan_loai_ly_do.py` ĐẠT; mỗi dòng 1 nhãn (12+7+0+0 = 19); máy PII ĐẠT |
| AC-4 | `MONG_MOC` ghim: phân bố `{12,7,0,0}` · vân tay nhãn `566b677f3b1ad2d4` · vân tay ảnh `39620e6d87dcd75a` · 12.590/12.571/19; `test_AC4_*` đổi 1 nhãn ⇒ ĐỎ |
| AC-5 | sàn 3307 cùng commit; `--duong-nen` xem trên |

## Kho thật
- `KHONG_CHAM` (PG chỉ cụm test 5437). Bản thô (SO CSV · L1 · khoá 7 cột) CHỈ ở `/tmp/dt1bm/` (700/600) — **đã xoá khi xong**; ⛔ commit.

## Dev tự thấy còn yếu
- Ảnh mốc nói "khớp" theo thứ tự `dong` trong nhóm khoá (dòng SO thứ i ↔ L1 thứ i): khi nhóm trùng khoá có thiếu, dòng nào bị gọi "thiếu" là dòng seq cuối — đúng luật khoá+seq của mã gốc nhưng người kiểm tay có thể thấy dòng khác trong nhóm. 19 dòng hiện đều không trùng lớn (`TRUNG_SEQ` = 0).
- `dong_sheet` mốc mới = số bản ghi CSV (⛔ đối chiếu với `dong` xlsx cũ — hệ khác, mốc 26/08 9.967 dòng ≠ 12.590).
