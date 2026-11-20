# WO-261 — ISP 3.1.2 · Step 31 · DT7: ảnh đáp án PLA1 · PLA3 HR · PLA3 PM+HR (PD 414–419)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao 20/11 |
| **Phát bởi** | orchestrator *(tài khoản mới)* · 2026-11-20 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/DT7` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` *(đã gộp DT2…DT6 · DT8 · DT9 · DT10 — công cụ chung `tools/dong_bang_sheet.py` + `tools/khuon_dong_bang/*.py`; khuôn gần nhất: CFA3 của DT6 `BG-193`, MID của DT9 `WO-220`)* |
| **Dải phiếu** | `BG-262` · `KQ-263` (R1) · `KQ-264` (R2 cuối, cây gộp thử) |

## Vì sao
- ISP **Step 31 · DT7** (wave W10). Phụ thuộc DT2 — đã gộp. Đầu ra là đáp án cho **H8** (Step 39, SO.PLA1 + SO.PLA3) — bước nằm trên **đường găng** H7 → H8 → H12 → H13 → H14 → I2.
- Chủ đặt khoá SA cho môi trường 20/11 và giao "mở DT7".
- Review theo **luật B của chủ (18/11)**: 2 vòng *(chữ "R1 · R2 · R3" ở ISP Step 31 mục 8 là bản cũ)*.

## Spec phải đọc
| Tệp | Mục |
|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | **Step 31** *(· Step 23 DT6 · Step 34 DT9 làm khuôn)* |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.3.1 PD **414–419** · §3.5.3 **D4** *(PLA1 dồn ngày 1 tháng PL start)* |
| `tools/dong_bang_sheet.py` · `tools/khuon_dong_bang/*.py` *(gần nhất: `cfa1_daily.py` · `cfa1_yhqm.py` — AP: PLA1 "như CFA1")* · `BG-193` (DT6 CFA3) · `BG-221` (DT9) | khuôn đóng băng *(hợp đồng bản thô = LƯỚI SA)* |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư |

## Nguồn — phiên cloud TỰ tìm bằng khoá SA *(CHỈ-ĐỌC)*
Sổ **CF report** *(cùng sổ đã dùng cho GL/CFA3 ở DT6 · H5)*, 6 tab theo AP §3.3.1:

| PD | Tab (tên theo AP — đối chiếu tên thật) |
|---|---|
| 414 | `[MID] Report I PLA1 Daily I PM only` |
| 415 | `[MID] Report I PLA1 Y H Q M \| PM Only` |
| 416 | `[MID] Report I PLA3 Daily \| HR Only` |
| 417 | `[MID] Report I PLA3 Y H Q M \| HR Only` |
| 418 | `[MID] Report I PLA3 Daily I PM + HR` |
| 419 | `Report I PLA3 Y H Q M \| PM + HR` |

- Tìm bằng `docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/cong_cu/sa_ds.py` + `sa_meta.py`. **Tên tab không khớp, ≥ 2 ứng viên, hoặc 403 ⇒ DỪNG**, báo tin nhắn cuối kèm danh sách ứng viên *(id sổ + tên tab + kích thước lưới)* và khuyến nghị — ⛔ đoán.
- Đọc GIÁ TRỊ bằng `UNFORMATTED_VALUE` *(⛔ `FORMATTED_VALUE` — bài học DT1b)*. Đọc công thức của **hàng tiêu đề + 1 hàng mẫu** mỗi tab (`sa_cong_thuc.py`) để xác nhận quan hệ "PM + HR = PLA1 + PLA3 HR cùng vị trí" — ghi nguyên văn vào BG.
- Bản thô chỉ ở `/tmp` của phiên (chmod 600), xoá sau dùng, ⛔ commit.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 | 3 ảnh `tests/fixture/dap_an/pla1.json` · `pla3_hr.json` · `pla3_pm_hr.json`; mỗi ảnh mang **cả** khối Daily và Y/H/Q/M của nó (hoặc 6 ảnh — khai lý do); số hàng · cột · ô ≠ 0 theo khối khai `mong` trước (Đ5 hai chiều; tập rỗng ⇒ ĐỎ, Đ3); mỗi số kèm nhãn nó đếm gì (Đ4) | cổng `dong_bang_sheet.py … --mong` + `tests/du_lieu/test_dap_an_pla.py` | ảnh chưa có |
| AC-2 (DT7-B1) | **tự kiểm cộng theo VỊ TRÍ ô** ngay trên đáp án: `PM+HR[i,j] = PLA1[i,j] + PLA3_HR[i,j]` cho Daily và Y/H/Q/M; số ô lệch của chính AS-IS **đo lần đầu rồi khai `mong`** + liệt kê ô lệch (khoá ô · ba giá trị · chênh); dung sai khai rõ | pytest | đột biến 1 ô ở một ảnh ⇒ ĐỎ *(chứng minh, ghi BG)* |
| AC-3 | **mẫu số**: đếm ô so được, ô `0 = 0 = 0`, ô có số thật — tách nhãn (bài học `H7-R1-02`: 835/888 giấu 619 ô `0=0`) | pytest | — |
| AC-4 | dải ngày Daily *(AP: từ 21/10/2024)* và các kỳ Y/H/Q/M thật của nguồn — khai trong ảnh + BG; kỳ thiếu ghi `chua_co_du_lieu` có tên, ⛔ hoá 0 | pytest | — |
| AC-5 | hàng **KPI** công thức chéo (EBITDA · NCF · PL2 …) ⇒ đóng băng nhưng **khai riêng** (`ma_kpi`, đếm) — bước KPI riêng của chủ dùng sau; ⛔ trộn vào số ô khớp | pytest | — |
| AC-6 | `#REF!`/`#N/A` ở nguồn ghi NGUYÊN chuỗi, ĐẾM theo cột, ghim phân bố (luật `DT5-R1-04`); lời lỗi ⛔ in giá trị ô (`DT5-R1-02`) | pytest | — |
| AC-7 | khuôn mới = tệp riêng `tools/khuon_dong_bang/…`; sửa công cụ chung chỉ khi bài đòi — mọi ảnh cũ đúng từng byte | diff | — |
| AC-8 | PII: `python tools/quet_pii_repo.py` = 0 trên worktree; ảnh ⛔ cột tên/email/số TK | công cụ | — |
| AC-9 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` | — |

## Ràng buộc
- ⛔ engine PLA (H8) · ⛔ quyết cách ghi nhận kỳ D4 — chỉ đóng băng số AS-IS.
- Ghi kho THẬT: `KHONG`. Ảnh > 2 MB ⇒ BG ghi kích thước + nguyên nhân (luật `DT4-R1-07`).
- Chỗ mơ hồ ngoài các mục trên ⇒ chọn phương án hẹp nhất, ghi "Giả định" + khuyến nghị vào BG; chỉ **DỪNG** ở trường hợp nguồn nói trên.
