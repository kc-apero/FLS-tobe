# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `H15` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.2 · **Ngày:** 2026-11-22 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-289` · R2 cuối `KQ-290`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 43 · H15 · `WO-287` · `BG-288`

> **Luật của sổ:** sổ **chỉ THÊM**. R1 đầy đủ; mức **GHI NHẬN** ⇒ backlog. Lớp: **A1/A2** lỗi mã · **B1** thiếu bài/răng · **B2** spec/ISP sai. Mức: **CHẶN** · **NÊN SỬA** · **GHI NHẬN**. ⛔ giá trị ô — chỉ số đếm.

## Số đo nền *(nhãn đếm gì — Đ4)*

| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| Ô HD theo ĐƯỜNG đi qua luật *(Đ3 — mẫu số ≠ 0)* | 12.633 ô khối `hd` · 26 kỳ | `go_tay` **9.176** *(Final = Manual qua `tinh_mid`)* · Classifying trả lời **3.419** · mặc định cứng **36** · trống **2**; 3 kỳ 2024 = 15 ô 100 % `go_tay` |
| 92 ô lệch Final theo lớp | 92 ô · 8 kỳ | **B** 60 ô `svc_start/svc_end` = `Input here` mà mặc định svc chưa suy được *(`GAP-ORA-06`; 2025-02·03 mỗi kỳ 2 · 2025-05 4 · 2025-10 8 · 2025-11 18 · 2025-12 19 · 2026-01 7)* · **A** 32 ô, **cả 32 ở 2026-07 / 13 dòng**: `Final` sổ RỖNG trong khi `MID` sổ có giá trị *(cdt1 7 · id_payee 6 · invoice 9 · svc_start 5 · svc_end 5)* · lớp "lỗi đọc/kiểu" **0** |
| Đối chiếu tay ảnh ↔ tự sinh | **16** ô *(2026-07 ×7 · 2025-11 ×3 · 2025-02 ×2 · 2025-03 ×2 · 2025-05 ×2)* | 16/16 đúng lớp A hoặc B như trên |
| Hồi quy 2026-03 *(chạy `291993f` ↔ ngọn)* | 584 dòng · 4.088 ô | cả hai: HD 584/584 · ô 4.088/4.088 · MID 4.020/4.088 — **trùng** |
| `git diff 291993f HEAD -- fls/oracle/tu_soi.py` | — | **0** dòng |
| Đột biến trên bản sao `git archive` *(trả nguyên, kết quả đo lại = XANH 26 kỳ)* | **12** | **11/12 cắn** *(xem `H15-R1-01`)*; đột biến đầu vào làm ĐỎ **đúng một kỳ** ở M1·M2·M4 |
| Cổng | `--duong-nen --cong 5446` · `lint-imports` · `kiem_tai_lieu` · `quet_pii_repo` | ĐẠT: 28 = 28 *(thêm 0 · bớt 0)*, chạy 4.497 ≥ 4.497 · web 3 = 3, 681 ≥ 681 · 11 kept 0 broken · ĐẠT · 0 chỗ |

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `H15-R1-01` | H15 | R1 | B1 | GHI NHẬN | `tools/do_voi_so_luong.py` *(`MONG["tu_sinh_theo_ky"]` · `do()`)* | MONG khai **ĐẾM theo khối**, ⛔ định danh ô. Đột biến M3: đổi `svc_start_manual` 1 ô *(None→209999)* ở dòng 2025-06 mà MID sổ đã lệch ⇒ **XANH** *(lệch MID đếm vẫn 60)*; hai ô lệch bù trừ cùng khối cũng không đỏ. | Thêm vân tay tập ô lệch *(sha `dong_sheet`+khối)* vào MONG cho `lech_final`. | Cổng đếm phải khai định danh khi đếm bù trừ được. | Mở |
| `H15-R1-02` | H15 | R1 | B1 | GHI NHẬN | `BG-288` · `do_tu_sinh_ky` | "HD 12.633/12.633" **không rỗng, không vòng tròn** *(đột biến đầu vào ĐỎ đúng kỳ)*, nhưng **72,6 %** ô HD *(9.176)* chỉ là Manual đi thẳng qua `tinh_mid` (`U=T`); luật thật chỉ chịu thử ở 3.455 ô. Kỳ 2026-10/11 chỉ 24/4 ô Classifying trả lời. | BG ghi thêm cột "đường đi" cạnh 100 %. | Đ4: nói 100 % *trên đường nào*. | Mở |
| `H15-R1-03` | H15 | R1 | A2 | GHI NHẬN | `fls/ledger/final_rule.py` *(`MAC_DINH_THEO_KHOI`)* · ảnh 2026-07 | 92 ô lệch = 2 lớp có tên: **B** 60 ô mặc định svc chưa suy *(`GAP-ORA-06`, có sẵn)*; **A** 32 ô `Final` sổ rỗng ở 13 dòng 2026-07 *(sổ chưa kéo công thức — ⛔ đối chiếu sheet được, đóng băng 20/11)*. MONG che đúng số, nhưng cả hai lớp đều đã có tên + số trong bản khai. | Hỏi chủ về 13 dòng 2026-07; lớp B chờ `GAP-ORA-06`. | — | Mở |
| `H15-R1-04` | H15 | R1 | B1 | GHI NHẬN | `tests/oracle/test_tu_sinh_theo_ky.py:127` | Nhánh float→int của `_chuan` chỉ được 2026-03 *(B1·B2·B5·B6)* canh; bài B4 "đổi kiểu" ⛔ bắt nó *(bỏ nhánh ⇒ 2 B4 đỏ, bài `…khong_doi` vẫn xanh)*. Bản so kiểu thô `==` làm 3/3 B4 ĐỎ — **BG đúng**. | Thêm 1 ô float nguyên vào B4. | — | Mở |
| `H15-R2-01` | H15 | R2 | B1 | GHI NHẬN | `tools/do_voi_so_luong.py` *(`do_tu_sinh_ky` nhánh `o_loi` · `hd_k` · `loi.extend(tsk["loi"])`)* | Đột biến trên cây gộp thử: **7 chỗ mới, 4 cắn, 3 sống**. Sống: **N1** bỏ `continue` ở nhánh mã lỗi Sheets — `o_loi` = **0/26 kỳ** *(Đ3: nhánh KHÔNG BAO GIỜ chạy trên ảnh thật, bài cũng ⛔ có ca mã lỗi)*; **N5** `hd_k` đếm cả ô lệch — tương đương trên dữ liệu *(`lech_final["hd"]` = 0/26 kỳ; lệch HD vẫn lộ qua `lech_final`)*; **N2** bỏ dây `loi.extend(tsk["loi"])` — MONG `tu_sinh_so_ky=26` vẫn đỏ khi manifest rỗng nên dây thừa. Không phần nào được `fls/` đọc *(grep `tu_sinh` ở `fls/` = 0 · khối `tu_sinh` chỉ do `tools/` + `docs/` sinh)* ⇒ ⛔ rủi ro cho I1. | Thêm 1 ảnh tổng hợp có ô `#N/A` vào bài B3; bài `hd_k` có 1 ô HD lệch cưỡng bức. | — | Mở |

## Changelog
- **v0.1** *(2026-11-22, `fls-test` R1 của `H15`, `KQ-289`)*: khởi tạo — **4** phát hiện `H15-R1-01…04` *(**0 CHẶN** · **0 NÊN SỬA** · **4 GHI NHẬN**)*.
- **v0.2** *(2026-11-22, `fls-test` R2 cuối của `H15`, `KQ-290`)*: THÊM `H15-R2-01` *(GHI NHẬN · B1)*. Tổng sổ **5** phát hiện *(**0 CHẶN** · **0 NÊN SỬA** · **5 GHI NHẬN**)*; 4 GHI NHẬN R1 xét lại bằng đo — ⛔ nâng.
