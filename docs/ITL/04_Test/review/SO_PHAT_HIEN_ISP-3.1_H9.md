# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `H9` + `DT8b` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.1 · **Ngày:** 2026-11-18 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-202` · R2 `KQ-203`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 24 · H9 · `WO-200` · `BG-201` *(+ «Sau DT8b»)* · `WO-204` · `BG-205`

> **Luật của sổ:** chỉ THÊM; vòng sau chỉ đổi ô *Trạng thái*. Thang lớp *(A1 · A2 · B1 · B2)* và mức *(CHẶN · NÊN SỬA · GHI NHẬN)* y như sổ chung. Hàng `DT8B-R1-…` là phát hiện của ảnh DT8b *(nhánh `isp/H9` đã gộp `833a273`)*, ghi cùng sổ theo lệnh orchestrator. Lúc ghi cả 6 hàng đều `mở`.
>
> ⛔ **Riêng tư:** sổ chỉ ghi số đếm, mã sheet và tên cột — ⛔ giá trị ô. Bản đọc thô SA nằm ở scratchpad của phiên, ⛔ commit.

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `H9-R1-01` | H9 *(WP-C4a)* | R1 | B1 | **NÊN SỬA** | `tools/do_hd2.py:1118-1121` *(nhánh `o_khong += 1 … continue`)* · `tests/oracle/test_do_hd2_c4a.py` | **196** ô PM *(28 Vendor-tháng × 7)* ⛔ so được vì `P` là chữ — nhưng phía ĐÁP ÁN MID3 ở đúng 196 ô ấy R1 đo **≠ 0 = 0/196**, và cổng ⛔ khai `mong` cho điều đó. Đột biến `gi_mid3` VD336·202506 `cvl_pm = 1` *(Vendor-tháng P-chữ)* ⇒ `do_hd2 --goi WP-C4a` **XANH** `DAT`; cùng đột biến ở Vendor-tháng P-số *(VD336·202502)* ⇒ ĐỎ. Đ5 một chiều: ô ⛔ so được là vùng mù không `mong`. | Thêm đếm `o_khong_so_khac_0` *(đáp án ≠ 0 trong 196 ô)* với `mong = 0` + bài đột biến ở Vendor-tháng P-chữ. | Mọi ô ⛔ so được phải có `mong` về giá trị phía còn lại *(Đ5)*. | mở |
| `H9-R1-02` | H9 | R1 | B1 | GHI NHẬN | `tools/do_hd2.py:1128` · `:1153` *(`ks_al_vm`)* | `chia_nen_tang` đã gọi `ks_al` bên trong; lần gọi thứ hai ở cổng chỉ để lấy mẫu số. Đột biến `ks = 44` *(bỏ gọi, hằng)* ⇒ **12/12** bài C4a + 15 bài engine **SỐNG** — bài ghim `ks_al_vm == 44` trùng hằng. Vô hại hôm nay *(KS.AL còn chạy trong engine, đột biến M7 dung sai cắn)*. | Ghim `ks_al_vm` bằng phép đo độc lập, hoặc bỏ trường. | — | mở |
| `H9-R1-03` | H9 *(⇒ H10)* | R1 | B1 | GHI NHẬN | `tools/do_hd2.py:1096` *(`{k: {} for k in o}`)* · `fls/bao_cao/phan_bo.py:93-141` | Cổng truyền **PE rỗng** *(⛔ có ảnh Looker PD 502)* ⇒ RATE ⛔ bao giờ chạy trên dữ liệu thật; Vendor-tháng thường ≠ 0 ⇒ ĐỎ vì `LoiPhanBo` *(đúng Đ5 — ⛔ đo được là ĐỎ)*, ⛔ vì `o_khac_0`. Mọi bằng chứng RATE = bài đơn vị tổng hợp. R1 đo độc lập: **2.934** ca ngẫu nhiên chia được *(2.220 theo tổng tháng)* so `Fraction` ⇒ lệch RATE 0, Σ chia = O/P 0 lệch; 15 đột biến, 13 cắn *(M14 = `H9-R1-02`; M15 là lệnh rỗng ⇒ ⛔ tính)*. Đã chuyển H10 *(orchestrator chốt)*. | Chuyển H10: nguồn PE theo CDT1 + so ô ≠ 0 vendor đặc biệt *(165/165 Vendor-tháng PE ≠ 0)*. | — | mở |
| `H9-R1-04` | H9 *(⇒ BA/H10)* | R1 | B2 | GHI NHẬN | `fls/bao_cao/phan_bo.py:93-99` *(`tong_thang`)* · `:116` *(`pk > 0`)* · `tests/bao_cao/test_phan_bo.py:72-81` | Hai quyết ngầm ⛔ có chữ trong ISP Step 24: ⓐ *"tổng tháng"* tính trên **MỌI vendor của tháng, kể cả đặc biệt** *(bài ghim 23)*; ⓑ luật chỉ kích khi `P > 0` — `O = 0 ∧ P < 0` rơi vào RATE riêng ⇒ `Σ PE = 0` ⇒ `LoiPhanBo` có tên *(R1 gọi: P = −3 ⇒ lỗi, ⛔ im)*. Đột biến M5 *(tổng tháng chỉ vendor thường)* cắn bài B2 — nên ⓐ có bảo vệ; ⓑ ⛔ bài. | BA xác nhận ⓐ ⓑ bằng một dòng ở ISP/AP trước H10; nếu `P < 0` hợp lệ thì thêm bài. | — | mở |
| `H9-R1-05` | H9 | R1 | B1 | GHI NHẬN | `tools/do_hd2.py:1123-1127` *(`bo`, `vbo`)* | Vendor đặc biệt bỏ qua có ĐẾM *(5 nhãn · 15 vendor — đúng)* nhưng chỉ đếm Vendor-tháng, ⛔ giá trị: đổi `pe` VD62·202505 ở CFA1 ⇒ cổng **XANH**. Đúng thiết kế *(H10)*; ghi để H10 khai `mong` giá trị. | H10 so ô vendor đặc biệt. | — | mở |
| `DT8B-R1-01` | DT8b | R1 | B1 | GHI NHẬN | `tools/khuon_dong_bang/gi_cfa1.py:117` *(`float(d["pe"])`)* | Cột số `pe` mang chữ *(R1 chèn tên giả vào ô `T` của bản thô SA)* ⇒ khuôn **nổ `TypeError`** *(`float()` nhận `dict`)* thay vì nhãn có tên *(`pe_la@dong_sheet`)* như `vendor_la@` · `thang_la@`. An toàn: ⛔ in giá trị *(grep tên giả = 0 trong stdout)*, ⛔ ghi tệp, exit ≠ 0. Chỉ thiếu lời lỗi có tên *(Đ5)*. | Thêm kiểm `pe`/`no` kiểu số trước `float`, nhãn `pe_la@`. | — | mở |

## Số đo nền của R1 *(nhãn đếm gì — Đ4)*

| Nhãn | Giá trị |
|---|---|
| ảnh `gi_cfa1.json` tái đo bằng khoá SA chỉ-đọc *(6 cột `M K Q T S R`, hàng 10…417)* | **408 dòng × 6 cột = 2.448 ô, lệch 0** |
| ảnh `gi_mid3.json` tái đo *(14 cột số + `H` + `F`, 253 hàng)* | **3.542 ô số + 253 khoá, lệch 0** *(209 hàng khoá = 19 vendor × 11 tháng; 44 hàng tổng ⛔ khoá)* |
| 14 cột cũ + `thu_tu` + `dong_sheet` so `gi_mid3.json` @ `6afb0ce` *(trước DT8b)* | **4.048 / 4.048 giống từng byte** *(253 × 16)* |
| Σ `pe` CFA1 theo Vendor-tháng = `pe` MID3 | **209/209**; `pm` số **209/209**; đặc biệt Σ chia = O **165/165** |
| cột H MID3 / cột M CFA1 khớp `VD[0-9]+` | **209/209** *(19 mã khác nhau)* · **408/408** — 0 tên người |
| `pm_ghi_chu` đã hoá 0 | **0** *(232 `pm` số · 176 chữ; ⛔ hàng nào mang cả hai)* |
| PII ảnh mới: cột cấm `Email Address` | **0** cột; ca phá tên người ở vendor/itl ⇒ `vendor_la@`·`itl_la@` ĐỎ, ⛔ in giá trị |
| đường nền `--duong-nen --cong 5444` | **28 = 28** *(thêm 0 · bớt 0)* · chạy **3.629** · web **3 = 3** · `KẾT: ĐẠT` |
| `lint-imports` · `kiem_tai_lieu.py` | 11 kept 0 broken · ĐẠT *(328 tệp)* |

## Changelog
- **v0.1** *(2026-11-18, `fls-test` R1 của `H9`, `KQ-202`)*: khởi tạo tệp riêng — **6** phát hiện *(0 CHẶN · **1** NÊN SỬA `H9-R1-01` · 5 GHI NHẬN gồm `DT8B-R1-01`)*.
