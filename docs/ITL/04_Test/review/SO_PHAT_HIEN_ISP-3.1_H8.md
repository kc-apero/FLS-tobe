# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `H8` — tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`

**Version:** v0.1 · **Ngày:** 2026-11-22 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-279`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 39 · H8 · `WO-277` · `BG-278` · nhánh `isp/H8` @ `8980abd`

> Thang lớp *(A1 · A2 · B1 · B2)* và mức *(CHẶN · NÊN SỬA · GHI NHẬN)*: y như sổ chung. Sổ **chỉ THÊM**. Vai KIỂM: ⛔ sửa mã.
> ⛔ **Riêng tư:** sổ chỉ ghi số đếm, địa chỉ ô và tên cột — ⛔ giá trị tiền thật.

## Số đo nền của R1 *(nhãn đếm gì — Đ4)*

| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| Cổng `do_hd2.py --goi WP-C3d` trên kho test nạp IX.PER | ô so 6 tab × 12 khối *(417 chỉ GROUP)* = **1.289.415** | khớp **1.287.624** *(thật 42.710 trên 44.501 ô có số · 1.244.914 ô `0 = 0`)* · lệch có chủ đích **1.791** · ngoài tên **0** |
| Mẫu số tách *(đếm lại từ `hd2_cong.json`)* | Daily · Y/H/Q/M · `khong_so_duoc` | **1.193.940** · **95.475** · **46.398** *(= 11 khối × 74 mã × 57 kỳ)* — khớp BG-278 |
| `--ghi` chạy lại | `hd2_cong.json` | sha256 trước = sau, **0 byte** đổi |
| Vòng tròn: đường tính `fls/bao_cao/pla.py` | grep `dap_an` · `fixture` · `tools` · `json` · `open(` | **0** khớp; `fls/` import `tests`/`tools` **0**; `fls/` nhắc tên tab đáp án **0** |
| Đột biến đầu vào *(trong bộ nhớ)*: GL +1000 một dòng `GI` · 202503 | ô engine đổi | 414 **292** · 418 **292** · 415 **170** · 419 **170**; 416/417 **0**; ô `GROUP#GI` ĐỎ ở 414·418·415·419, ⛔ ĐỎ ở 416·417 |
| Đột biến đầu vào: HR +1000 `BA` một dòng `NIS` · 2025-03 | ô engine đổi | 416 **8** · 418 **8** · 417 **32** · 419 **32**; 414/415 **0**; ô `GROUP#NIS` ĐỎ ở 416·418·417·419 |
| Đột biến engine/cổng trên bản sao `git archive` | 10 *(M1…M10)* | cổng ĐỎ **9/10**; M7 *(D4 luật B)* cổng XANH — bài đơn vị ĐỎ ⇒ xem `H8-R1-01` |
| Đột biến dữ liệu/`mong` | 5 *(GL · HR · giá trị `mong` +1e-6 · ô đáp án vùng AS-IS · ô đáp án ngoài vùng)* | ĐỎ **5/5**; `mong` +1e-15 XANH *(trong `atol_lech` 1e-9 — đúng thiết kế)* |
| Mẫu tay độc lập *(từ cột thô BM·BA·BB·V·BP / DE·BR·BS·V·AD, ⛔ qua engine)* | **96** ô LÁ lệch trước `CA` *(416: 48 · 418: 48)* | tay = engine **96/96**; đáp án ≠ tay và đúng chữ ký bản dán cũ **96/96**; 8 ô `GAC` thiếu `CXA`: chênh = `CXA` tay **8/8** |
| Đối chứng luật cột `CA` | **20** ô CDT lá có số ≥ `CA` *(mẫu số tập ≥ `CA`, ô ≠ 0: 234)* | tay = đáp án **20/20** |
| Sàn Q8 | thu thập thật `--collect-only` | **4.426** = sàn `MONG_PYTEST_TOAN_BO` 4.426; `--duong-nen` chạy **4.426** |

## Bảng phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `H8-R1-01` | H8 | R1 | B1 | GHI NHẬN | `fls/bao_cao/pla.py` `ngay_pl` · `tools/do_hd2_c3d.py` | Đột biến M7 *(`ngay_pl` trả `pl_end`, tức luật B)* → **cổng XANH** *(1.289.415 ô, khớp y nguyên)* vì mọi `AH` của sổ là tháng ⇒ PL start = PL end = ngày 1. AC-1 *(D4 A, ⛔ luật B)* chỉ được bảo vệ bởi bài đơn vị `test_H8_B1_PL_start_15_03_den_08_toan_bo_vao_01_03` *(ĐỎ dưới M7 — đã chạy)*. Dữ liệu thật ⛔ phân biệt được D4 A với luật B; BG-278 đã khai M5/M4 tương đương, R1 xác nhận thêm M7. | Giữ bài đơn vị làm chốt AC-1; ⛔ coi cổng WP-C3d là bằng chứng D4. Khi sổ có dòng PL start ≠ PL end thì thêm ô đo vào cổng. | Cổng dữ liệu ⛔ chứng D4 — mọi luật ngày ghi nhận cần một bài đơn vị có PL start ≠ PL end. | mở |
| `H8-R1-02` | H8 | R1 | A2 | GHI NHẬN | `tools/do_hd2_c3d.py:407-429` `la_truoc_ca` · `tom_truoc_ca` · `tools/do_hd2_c3d_mong.py` `as_is_truoc_CA` | Lớp `as_is_truoc_CA` **1.783 ô** được ghim bằng đếm theo `tab\|khối` + sha256 của **chính đầu ra engine** ⇒ tự thân ⛔ phân biệt "lệch AS-IS" với "lệch FLS nằm trong vùng ấy": một lỗi engine có từ đầu ở khối CDT/`SHQ2` năm 2024 sẽ được ghim luôn. R1 đo bù độc lập: **96/96** ô lá daily và **8/8** ô `GAC` ⇒ engine đúng, lệch là của AS-IS. **Giới hạn đo:** 1.783 − 96 = **1.687** ô còn lại là `tong`/KPI/Y·H·Q·M suy ra từ lá — ⛔ tính tay riêng. | Thêm một bài tính tay độc lập *(từ BM·BA·BB·V·BP, như R1)* cho ô lá vùng trước `CA` vào bộ bài — để sha chỉ còn là chốt hồi quy, ⛔ chốt đúng. | Mọi lớp lệch khai bằng sha của đầu ra engine cần kèm một phép tính tay độc lập trên đầu vào thô. | mở |
| `H8-R1-03` | H8 | R1 | A1 | GHI NHẬN | `tools/do_hd2_c3d.py:378` · `hd2_cong.json` `WP-C3d.dung_sai.ghi_chu` | Chuỗi cứng `"atol ≥ ×30"` — sai nhãn Đ4: max\|lệch\| ô khớp đo được **5,3e-14** *(419)* ⇒ `1e-12 / 5,3e-14` = **×18,9**, ⛔ ×30 *(BG-278 ghi ×18 — đúng)*. ⛔ ảnh hưởng cổng; khối sinh bằng `--ghi` nên bản `hd2_cong.json` mang con số sai. | Tính tỉ số từ `max` đo được tại chỗ sinh *(⛔ gõ cứng)*, rồi sinh lại bằng `--ghi`. | Con số suy ra phải tính tại chỗ in, ⛔ chép tay (Đ4). | mở |

## Changelog
- **v0.1** *(2026-11-22, `fls-test` R1 của `H8`, `KQ-279`)*: khởi tạo — **3** phát hiện `H8-R1-01…03` *(**0 CHẶN** · **0 NÊN SỬA** · 3 GHI NHẬN: B1 ×1 · A2 ×1 · A1 ×1)*.
