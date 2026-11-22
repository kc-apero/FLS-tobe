# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `H8` — tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`

**Version:** v0.2 · **Ngày:** 2026-11-22 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-279` · R2 cuối `KQ-280`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 39 · H8 · `WO-277` · `BG-278` · nhánh `isp/H8` @ `8980abd`

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

## Số đo nền của R2 cuối *(cây gộp thử `thu/H8` = nhánh làm việc @ `291993f` + `isp/H8` @ `518ea28`; cụm `5445`; nhãn đếm gì — Đ4)*

| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| Xung đột gộp | tệp | **2** tệp, đều là **sàn pytest**: `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` *(nhánh làm việc 4481 ↔ H8 4426)*; `hd2_cong.json` · `do_hd2.py` · bài gates · sổ · changelog gộp **sạch**, 2 khối C3c/C4c + C3d cùng có mặt |
| Sàn cây gộp | `pytest --collect-only` | **4.525** *(4.481 + 44 bài H8 · ⛔ 4.426)*; đặt = thu thập ở bản gộp thử; `--duong-nen` chạy **4.525 ≥ 4.525** |
| Ảnh `dau_vao` | **6** tệp `tests/fixture/dau_vao/*.json` | `git diff` cây gộp ↔ `isp/H8` **0 byte** · ↔ nhánh làm việc **0 byte** |
| `do_hd2.py --goi` trên cây gộp *(IX.PER + IX.ORG nạp vào `fls_test`)* | `tong_o` · `khop` · `lech_co_chu_dich` | C3a **205.175 · 205.140 · 35** · C3b **11.585 · 11.543 · 42** · C3c **888 · 835 · 53** · C3d **1.289.415 · 1.287.624 · 1.791** — y hệt `hd2_cong.json` của `isp/H8` *(0 đổi)* |
| `--ghi` chạy lại 4 gói | `hd2_cong.json` | **0 byte** đổi *(⚠ chỉ khi nạp IX.PER với đúng chuỗi `nguon` đã ghi — xem `H8-R2-01`)* |
| Bài xanh trên cây gộp | `test_isp_gates_hd2` + `test_pla` + `test_do_hd2_c3d` + `test_dung_moi_truong_isp` · `test_pla*` + CG2 + `test_do_hd2_c3a/b/c` | **183 passed** · **73 passed** |
| Tính tay lớp `as_is_truoc_CA` *(từ cột thô GL `BR·BS·AH·V·AD` / HR `BA·BB·BM·V·BP` + cây ATL, ⛔ qua engine)* | lớp **1.783** ô; trừ **133** ô `NPC` Y/H/Q/M *(hậu tố kỳ ⛔ khai ở BG)* ⇒ **1.650** tính được | engine = tay **1.650/1.650** *(lá 225 · tong 291 · KPI 1.134)*; đáp án = tay dựng lại bằng **nguyên nhân khai** *(CDT = 0 · dư = GROUP, HR trước `CA`)* **1.650/1.650** ⇒ **0** ô thực ra là lệch FLS |
| Mẫu ngẫu nhiên *(seed `20261122`)* trong tập **chưa tính tay riêng** | **1.554** ô tính được *(= 1.687 − 133 NPC)* | **60** ô *(KPI 41 · tong 12 · lá Y/H/Q/M 7)* ⇒ engine = tay **60/60** · đáp án = tay-AS-IS **60/60** |
| Đột biến mới trên bản sao `git archive` | **10** *(N1…N9 + N5b)* | cổng/bài ĐỎ **9/10**; N5 *(1 ô `GAC` đáp án lệch 2,8e-15 < `atol_lech` 1e-9)* XANH — tương đương theo thiết kế; N5b *(lệch 1,6e-6)* ĐỎ |
| `--duong-nen --cong 5445` *(một lần, một mình)* | node id đỏ + XFAIL | **28 = 28** *(thêm 0 · bớt 0)*; chạy **4.525 ≥ 4.525**; `tests/web` **3 = 3** · chạy **681** |

## Bảng phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `H8-R1-01` | H8 | R1 | B1 | GHI NHẬN | `fls/bao_cao/pla.py` `ngay_pl` · `tools/do_hd2_c3d.py` | Đột biến M7 *(`ngay_pl` trả `pl_end`, tức luật B)* → **cổng XANH** *(1.289.415 ô, khớp y nguyên)* vì mọi `AH` của sổ là tháng ⇒ PL start = PL end = ngày 1. AC-1 *(D4 A, ⛔ luật B)* chỉ được bảo vệ bởi bài đơn vị `test_H8_B1_PL_start_15_03_den_08_toan_bo_vao_01_03` *(ĐỎ dưới M7 — đã chạy)*. Dữ liệu thật ⛔ phân biệt được D4 A với luật B; BG-278 đã khai M5/M4 tương đương, R1 xác nhận thêm M7. | Giữ bài đơn vị làm chốt AC-1; ⛔ coi cổng WP-C3d là bằng chứng D4. Khi sổ có dòng PL start ≠ PL end thì thêm ô đo vào cổng. | Cổng dữ liệu ⛔ chứng D4 — mọi luật ngày ghi nhận cần một bài đơn vị có PL start ≠ PL end. | mở |
| `H8-R1-02` | H8 | R1 | A2 | GHI NHẬN | `tools/do_hd2_c3d.py:407-429` `la_truoc_ca` · `tom_truoc_ca` · `tools/do_hd2_c3d_mong.py` `as_is_truoc_CA` | Lớp `as_is_truoc_CA` **1.783 ô** được ghim bằng đếm theo `tab\|khối` + sha256 của **chính đầu ra engine** ⇒ tự thân ⛔ phân biệt "lệch AS-IS" với "lệch FLS nằm trong vùng ấy": một lỗi engine có từ đầu ở khối CDT/`SHQ2` năm 2024 sẽ được ghim luôn. R1 đo bù độc lập: **96/96** ô lá daily và **8/8** ô `GAC` ⇒ engine đúng, lệch là của AS-IS. **Giới hạn đo:** 1.783 − 96 = **1.687** ô còn lại là `tong`/KPI/Y·H·Q·M suy ra từ lá — ⛔ tính tay riêng. | Thêm một bài tính tay độc lập *(từ BM·BA·BB·V·BP, như R1)* cho ô lá vùng trước `CA` vào bộ bài — để sha chỉ còn là chốt hồi quy, ⛔ chốt đúng. | Mọi lớp lệch khai bằng sha của đầu ra engine cần kèm một phép tính tay độc lập trên đầu vào thô. | mở |
| `H8-R1-03` | H8 | R1 | A1 | GHI NHẬN | `tools/do_hd2_c3d.py:378` · `hd2_cong.json` `WP-C3d.dung_sai.ghi_chu` | Chuỗi cứng `"atol ≥ ×30"` — sai nhãn Đ4: max\|lệch\| ô khớp đo được **5,3e-14** *(419)* ⇒ `1e-12 / 5,3e-14` = **×18,9**, ⛔ ×30 *(BG-278 ghi ×18 — đúng)*. ⛔ ảnh hưởng cổng; khối sinh bằng `--ghi` nên bản `hd2_cong.json` mang con số sai. | Tính tỉ số từ `max` đo được tại chỗ sinh *(⛔ gõ cứng)*, rồi sinh lại bằng `--ghi`. | Con số suy ra phải tính tại chỗ in, ⛔ chép tay (Đ4). | mở |
| `H8-R2-01` | H8 | R2 | A1 | GHI NHẬN | `docs/ITL/_tools/hd2_cong.json` `WP-C3a`/`WP-C3b` `nguon_ngay_dau` | `--ghi` ⛔ tất định theo dữ liệu: dòng `nguon_ngay_dau` ghi **chuỗi `nguon` do người nạp IX.PER đặt** — hai gói đang mang **hai chuỗi khác nhau** *(C3a: `bai-test-h6:…Step20…` · C3b: `ISP-3.1.2 Step17 C6…`)*. Nạp IX.PER với chuỗi khác ⇒ `--ghi` đổi **2** dòng *(số y nguyên)*; phải nạp lần lượt đúng từng chuỗi mới ra **0 byte**. | Ghi chú nguồn vào `MONG` thay vì đọc chuỗi của người nạp, hoặc thống nhất một chuỗi. | Trường dẫn xuất mang chuỗi do người nạp đặt ⇒ `--ghi` không tái lập được nếu ⛔ biết chuỗi. | mở |
| `H8-R2-02` | H8 | R2 | A2 | GHI NHẬN | `tools/do_hd2_c3d.py` `la_truoc_ca` ↔ `NPC` Y/H/Q/M | **133** ô `NPC` của `pla3_pm_hr_yhqm` trong lớp `as_is_truoc_CA` ⛔ tính tay được: quy ước hậu tố kỳ của `NPC` ở 415/417/419 không khai ở BG-278 *(chỉ khai Daily)*. Phần còn lại **1.650/1.650** tính tay khớp. | BA khai công thức `NPC` Y/H/Q/M để thêm vào bài tay. | — | mở |

## Changelog
- **v0.1** *(2026-11-22, `fls-test` R1 của `H8`, `KQ-279`)*: khởi tạo — **3** phát hiện `H8-R1-01…03` *(**0 CHẶN** · **0 NÊN SỬA** · 3 GHI NHẬN: B1 ×1 · A2 ×1 · A1 ×1)*.
- **v0.2** *(2026-11-22, `fls-test` R2 cuối của `H8`, `KQ-280`)*: thêm bảng "Số đo nền của R2 cuối" + **2** phát hiện `H8-R2-01…02` *(**0 CHẶN** · **0 NÊN SỬA** · 2 GHI NHẬN: A1 ×1 · A2 ×1)*; `H8-R1-02` đo bù **1.650/1.650** ⇒ giữ GHI NHẬN *(đã có bằng chứng tay)*; `H8-R1-01` · `-03` giữ GHI NHẬN.
