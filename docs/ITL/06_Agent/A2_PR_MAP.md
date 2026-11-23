# A2 · Generate Group Ledger + Mapping

> Sinh bởi `python tools/sinh_the_agent.py` — ⛔ sửa tay (sửa prompt ở `fls/agent/skill/A2_PR_MAP/`, rồi sinh lại).

| | |
|---|---|
| **Vai** | AP Voi v3.1.2 §4.2 PR.BANK · PR.PAY · §4.3.1 SI.MAP (PARTIAL) |
| **Đầu vào** | ảnh của A1 (bank · PM line) — engine FLS chạy trên ảnh đóng băng |
| **Đầu ra** | ô `voi:theo_ky.*.{co,chay,map_fls,pm_noi,map_now,day_nguoi}` · `voi:bank_tong.dong_theo_hinh.A–F` · `voi:dat_hd1.theo_ky.*.thieu` · G0: `noi:<ca>.chon` + `ly_do` |
| **Công cụ được gọi** *(CHỈ hàm FLS có sẵn)* | `dong_chuan` · `ghep_ref` · `hang_cho` = `tools/do_voi_so_luong.do()` (gọi `pm_join.xep_ca_lat` · `moi_noi`) · `ung_vien_ghep` = bể ca (dựng trong repo / GIỮ RIÊNG qua `FLS_HELDOUT_NOI_DUNG`) |
| **Mô hình ghim** | `claude-opus-5-5` · họ `anthropic` · ghim ✅ · phương án A (PROPOSED — câu chủ C1) |
| **Phiên bản** | checksum prompt `e9d149e87fff5474` + mô hình ghim + checksum tham chiếu (tệp số máy đã đo) |
| **Bước thông minh** | Skill 04 ghép theo NỘI DUNG giao dịch (G0 bóng): mã PM trong nội dung đã che + tiền + tiền tệ + ngày; luật cứng chặn chọn ngoài ứng viên / lệch tiền / dùng lại PM line. Gửi nội dung TẮT mặc định — câu chủ C4. |
| **Fleet eval** | `a3-1-ref.eval.ghep-sai` (rubric 0–2; bar: 0 ca phải-để-người bị nối) — vòng: `docs/ITL/05_FleetEval/vong/TONG_HOP.md` |

## Bộ skill — chạy TUẦN TỰ (skill n+1 chỉ khi cổng skill n ĐẠT)

| # | skill | loại | công cụ | cổng ra |
|---|---|---|---|---|
| 01 | [Dựng dòng chuẩn 1-1 với sổ AS-IS theo kỳ](../../../fls/agent/skill/A2_PR_MAP/01_dong_chuan.md) | lam | `dong_chuan` | `tong_ky:co+chay` |
| 02 | [Ghép bank ↔ PM theo Reference No (hình A–F)](../../../fls/agent/skill/A2_PR_MAP/02_ghep_ref.md) | lam | `ghep_ref` | `tong_ky:map_fls+pm_noi` |
| 03 | [Hàng chờ người + mốc NOW (VLOOKUP)](../../../fls/agent/skill/A2_PR_MAP/03_hang_cho_nguoi.md) | lam | `hang_cho` | `tong_ky:map_now+day_nguoi` |
| 04 | [Ghép theo NỘI DUNG giao dịch (G0 bóng)](../../../fls/agent/skill/A2_PR_MAP/04_ghep_noi_dung.md) | bong | `ung_vien_ghep` | `luat_ghep` |

Loại: `lam` = mô hình làm, A4 so 100 % với máy · `bong` = G0 bóng, so với đáp án giữ riêng, ⛔ ghi · `ma` = mã tất định, ⛔ mô hình.

## Cổng ra của agent

A4 (mã `fls/agent/doi_chieu.py`) so MỌI ô skill `lam` với số máy đã đo — mong: lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0. Khác ⇒ agent TRƯỢT, chuỗi DỪNG, agent sau ⛔ chạy.

## ⛔ Không được làm

- ⛔ gọi API thật khi thiếu chốt (`--that` + `FLS_CHO_GOI_API=1` + khoá + mô hình ghim)
- ⛔ ghi kho · ⛔ sửa ảnh · ⛔ sửa engine/tuyến — chỉ GỌI công cụ được cấp
- ⛔ tính lại / làm tròn / thêm ô / bịa ô — A4 so từng ô với máy
- ⛔ gửi `Diễn giải` · `Số chứng từ` · tên người · email · số TK — bộ che `NFR-I13` chạy trước mọi lời gọi
