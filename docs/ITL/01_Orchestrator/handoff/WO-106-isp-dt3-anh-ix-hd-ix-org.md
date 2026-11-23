# WO-106 — ISP 3.1.2 · Step 10 · DT3: ảnh nguồn IX.HD · IX.ORG (cây ATL + Mapping Master + CDT Correct)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-16 |
| **Nhận** | `fls-dev` — agent làn **FE ↩ DATA** (người dùng 16/11: *"FE nhận cả DATA"*) · cụm PG **5436** · worktree `.claude/worktrees/isp-dt3` · nhánh `isp/DT3` |
| **Nền** | `isp/DT2` @ `80496ec` (đường ống đóng băng + `tools/khuon_dong_bang/` + gộp `isp/C1`) |
| **Dải phiếu** | `BG-107` (bàn giao) · `KQ-108` (R1) · `KQ-109` (R2) · `KQ-110` (R3) |

## Vì sao
- ISP **Step 10 · DT3** — nguồn sự thật duy nhất. Phụ thuộc DT2 đã bàn giao (`BG-086`) + R1 `KQ-087` **0 CHẶN** (chế độ tăng tốc).

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · Step 10 | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.2.1 IX.HD · IX.ORG · §3.2.5 · §3.5.4 WP-C1 | 3.1.2 |
| `fls/adapters/mapping_master.py` | `doc_cot` · `COT` · `DONG_DAU = 7` | — |
| `tools/dong_bang_sheet.py` · `tools/khuon_dong_bang/ix_fx.py` | khuôn mẫu DT2 | `isp/DT2` |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư | — |

## Nguồn — orchestrator đã đọc bằng connector (chỉ đọc), ⛔ agent gọi Drive
Ba tệp thô ở scratchpad orchestrator `…/scratchpad/drive_tho/` (đường dẫn tuyệt đối trong brief):
| Tệp thô | Nguồn | Đo 16/11 |
|---|---|---|
| `atl_cay_A7_F88.json` | cây ATL `A7:F88` | 81 hàng: 74 hàng mã · 6 hàng tiêu đề nhóm |
| `mapping_master_A1_P120.json` | bản sao RAW `'Mapping Master'!A1:P120` | 85 hàng; 73 mã `hd` qua `doc_cot` (H…M). ⚠ **PII:** 7 hàng có tên viết tắt NGƯỜI ở cột A · B · O (tài khoản PO cá nhân) ⇒ **băm hoặc loại, ⛔ commit tên** |
| `cdt_correct_BR11_BS23.json` | bản sao P&L `'Report I H1000 Ledge (HR Allocate HD) Y2025 \| For PL Report'!BR11:BS23` | **13** dòng; `BR24:BS32` RỖNG (đọc lại `BR8:BS32`) |

## Quyết định orchestrator *(ghi errata ⑪ ⑫ cho bản vá ISP)*
- **⑪ CDT Correct MONG = 13**, ⛔ 18: ISP/AP ghi "18 dòng (BR11:BS28)" là khoảng Ô; dòng có dữ liệu đo được 13. Câu Đ4 trong ảnh + BG: *"13 = dòng có dữ liệu ở BR11:BS23"*.
- **⑫ `AA:AD` của "Mapping Master"** ⛔ thuộc bản sao RAW: `Q1:AN120` RỖNG hoàn toàn (đo 16/11). AP Hình 3.1 ghi *"APERO \| FS2 nhập tay · R → LE · AA:AD Cash/Bank"* ⇒ đó là Mapping Master của **FS2**, phục vụ IX.ORG (C8). DT3 đóng băng `mapping_master_cfg.json` = **đầu ra `doc_cot`** (73 mã) + cột A:B · D:G thô (PII đã băm); phần FS2 `R` · `AA:AD` ⇒ ảnh riêng trước C8, ⛔ ở bước này.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (DT3-B1) | 3 ảnh trong `tests/fixture/cau_hinh/`: cây **74** dòng mã · **6** nhóm · Mapping Master **73** mã `hd` · CDT Correct **13** dòng — mỗi số có nhãn Đ4 | `tests/du_lieu/test_anh_cau_hinh.py` | ảnh chưa có |
| AC-2 (DT3-B2) | phá: xoá 1 dòng cây ở BẢN SAO ⇒ ĐỎ `73 ≠ 74`, trả nguyên ⇒ xanh (mỗi ảnh một ca phá riêng) | ghi lệnh + exit | — |
| AC-3 | ⛔ PII: quét ảnh ⇒ 0 tên người / Email / Diễn giải / Số chứng từ (máy kiểm, có ca phá) | pytest | — |
| AC-4 | khuôn mới = **tệp riêng** `tools/khuon_dong_bang/<tên>.py`, ⛔ sửa `tools/dong_bang_sheet.py` (trừ khi bài đòi — khai lý do) | diff | — |
| AC-5 (Q8) | bài mới cộng vào `MONG_PYTEST_TOAN_BO` cùng commit | `--duong-nen --cong 5436` | — |

## Dữ liệu
- Ghi kho THẬT: `KHONG`. Đầu ra là ảnh JSON đã commit.

## Câu còn treo
- không có (⑪ ⑫ đã chốt ở trên).
