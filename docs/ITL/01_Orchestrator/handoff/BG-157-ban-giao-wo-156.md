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

## Vòng sửa sau R1 (KQ-158) — `DT1BM-R1-01`
*(chỉ THÊM; các mục trên là bản ghim ĐẦU, giữ làm biên bản — số "12.571 · 19" ở trên là số của lần đọc đủ số lẻ)*

**Lỗi:** SO mốc mới là CSV HIỂN THỊ (tiền làm tròn 2 số lẻ), L1 đọc `UNFORMATTED_VALUE` (đủ số lẻ) ⇒ cả 19 dòng "thiếu" chỉ lệch dưới 1 xu — ảo do làm tròn, ⛔ lệch thật.
**Sửa (MÃ):** `tools/phan_loai_ly_do.py` — khi đo mốc mới, `ps_no`/`ps_co` làm tròn `ROUND_HALF_UP` trên `Decimal` về 2 số lẻ **ở cả hai phía** trước khi băm khoá; ảnh mốc khai `do_chinh_xac_tien = 2` (cổng canh: thiếu khoá hay ≠ 2 ⇒ ĐỎ). Mốc 26/08 (xlsx) ⛔ đổi hành vi (`dp=None`, lời gọi y cũ).
**Đỏ-trước:** 7/11 bài mới ĐỎ trên mã cũ (4 ca `x.xx` ↔ `x.xx3` · 1 ca `-0,003`/`-0,999…` · khai `do_chinh_xac_tien` · mốc 26/08 giữ nguyên) — 4 ca "lệch ≥ 0,01 ⇒ vẫn `KHOA_LECH`" xanh cả hai bên (đúng: chúng canh chiều ngược). Sau sửa 22/22 bài `test_phan_loai_ly_do_moc_moi.py` xanh.

### BẢNG TÓM TẮT MỚI *(CHỈ số đếm + `dong_sheet`; ⛔ giá trị ô)*
Cùng hai nguồn (SO CSV Drive `1U-IQVO…` 10.606.726 B · L1 `1xaD1R…` cột `B` `D:G`, `UNFORMATTED_VALUE`, đọc lại 18/11 qua khoá SA; ⛔ cột `C`).

| Chỉ số | Số | Đếm gì (Đ4) |
|---|---|---|
| Dòng SO dùng | 12.590 | hàng có ≥1 ô khoá (= bản đầu) |
| Dòng L1 | 12.590 | hàng có ≥1 ô khoá |
| **Khớp 1-1** (khoá + seq, tiền ở 2 số lẻ) | **12.590** | tái lập 12.590 / 12.590 = 100 % (2 đường: Σ min theo nhóm ↔ duyệt theo seq) |
| **Thiếu** | **0** | cũ 19 |
| Nhãn `KHONG_CO_SAO_KE` · `KHOA_LECH` · `TRUNG_SEQ` · `KHAC` | 0 · 0 · 0 · 0 | cũ 12 · 7 · 0 · 0 |
| Khoá hỏng SO · L1 | 0 · 0 | |
| Đối chứng (Đ3) | cùng dữ liệu, KHÔNG làm tròn ⇒ **19 thiếu**, 19/19 đúng tập `dong_sheet` cũ; `khoa_bam` 12.590/12.590 trùng ảnh cũ ⇒ dữ liệu ⛔ đổi, chỉ luật so đổi | 0 là KẾT QUẢ trên mẫu số 12.590 > 0, ⛔ tập rỗng |

**`dong_sheet` thiếu theo nhãn: ⛔ còn dòng nào** (0/12.590). 19 dòng bản đầu — nay KHỚP — để người kiểm mở đối chiếu tay (chỉ chữ "Cách kiểm" đổi):
- bản đầu gọi `KHONG_CO_SAO_KE` (12): 704 · 771 · 1024 · 1054 · 1055 · 1352 · 1602 · 1684 · 1863 · 2022 · 2371 · 2439 — cả 12 có **Số CT rỗng** (đo: 12/12) nên ⛔ bị bắt thành `KHOA_LECH` (không có Số CT để ghép ứng viên), còn tiền lệch < 1 xu (6 dòng `PS Nợ`, 6 dòng `PS Có` khác 0);
- bản đầu gọi `KHOA_LECH` (7, trường `ps_co`): 2566 · 4735 · 4736 · 4737 · 6248 · 6249 · 6250 — Số CT cùng, `PS Có` lệch < 1 xu.
- **Cách kiểm (sửa chữ):** `KHONG_CO_SAO_KE` (nếu còn về sau) ⇒ L1 **⛔ có Số CT ấy** (hoặc dòng Số CT rỗng không có bạn khoá); `KHOA_LECH` ⇒ L1 có dòng cùng Số CT nhưng tiền khác **từ 0,01 trở lên**. Lệch dưới 1 xu KHÔNG phải lệch.

### Đã đổi (vòng này)
`tools/phan_loai_ly_do.py` (`_tien(dp)` · `chuan_hoa_khoa(dp)` · `doc_khoa(dp)` · `DO_CHINH_XAC_TIEN_MOC` · `KHOA_ANH` + `do_chinh_xac_tien` · cho `thieu = 0` ở mốc mới) · `tests/fixture/dt1b_moc_20261118.json` (ghi lại: `so_khop` 12.590 · `so_thieu` 0 · `do_chinh_xac_tien` 2) · `docs/ITL/_tools/phan_loai_ly_do_moc_20261118.json` (`dong_thieu: []`) · `MONG_MOC` ghim lại `{12.590 · 12.590 · 0}` · vân tay ảnh `f40b0e92d11eeff6` · vân tay nhãn `4f53cda18c2baa0c` · `tests/du_lieu/test_phan_loai_ly_do_moc_moi.py` (+11 bài; bài ghim thật đổi: thêm 1 nhãn ⇒ ĐỎ, vì ⛔ còn dòng nào để đổi nhãn) · sàn `MONG_PYTEST_TOAN_BO` **3307 → 3318** cùng commit (Q8).
**Lệch chữ chốt (báo orchestrator):** (a) dự kiến "thiếu 12, `KHOA_LECH` 0" — đo ra **0 · 0**: 12 dòng `KHONG_CO_SAO_KE` cũng chỉ là lệch tiền < 1 xu của dòng Số CT rỗng; (b) vì thế cho phép `so_thieu = 0` ở mốc mới (trước đó công cụ coi tập thiếu rỗng là ĐỎ — mẫu số đúng là SO · L1 · ghép, đã kiểm > 0; vân tay ảnh + MONG_MOC canh ⇒ bản đọc sai ra 0 thiếu vẫn ĐỎ).
**Ghi nhận ⇒ backlog (⛔ làm):** `DT1BM-R1-02…04` theo `KQ-158`.
**Bản thô:** `/tmp/dt1bm_sua/` (700) — đã xoá khi xong; ⛔ commit.

### Cổng vòng sửa *(nguyên văn)*
| Lệnh | Kết quả |
|---|---|
| `python tools/phan_loai_ly_do.py` · `… --khoa <khoá> --moc tests/fixture/dt1b_moc_20261118.json` | `KẾT: ĐẠT — … 0 dòng sổ thiếu` (mã 0) cả hai |
| `--duong-nen --cong 5437` (MỘT lần, một mình) | `[ĐẠT] … 28 = 28 node id (XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 3318 bài (mong ≥ 3318) · skipped 0 · deselected 0` · `tests/web 3 = 3 · 667 bài` · `KẾT: ĐẠT` |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `kiem_tai_lieu.py` | K1–K2, K4–K6 OK; ⛔ **K3 ĐỎ 1 lỗi có từ trước, ngoài phạm vi**: `isp-3.1/TIEN_DO.md:155` `cot 4 != 2` (dòng "Lượt 08:43" của phiên khác; tệp này ⛔ chạm ở vòng này) — báo orchestrator |
