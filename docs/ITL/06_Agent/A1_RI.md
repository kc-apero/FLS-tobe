# A1 · Collect_raw_data (4 nguồn raw)

> Sinh bởi `python tools/sinh_the_agent.py` — ⛔ sửa tay (sửa prompt ở `fls/agent/skill/A1_RI/`, rồi sinh lại).

| | |
|---|---|
| **Vai** | AP Voi v3.1.2 §4.1 — RI.BANK · RI.PAY (PARTIAL) · §4.5 RI.HR · RI.PLT (PROPOSED) |
| **Đầu vào** | ảnh đóng băng 4 nguồn raw: Bank (`tests/fixture/pm_join.json` bank + `itl_ledge_adjustment.json` sổ AS-IS) · FPS (`pm_join.json` pm) · H1000 (`dau_vao/hr_ledger_2024/2025.json`) · PLT (`dau_vao/gi_cfa1.json` + `dap_an/{omc,sc,ps}_mid1.json`) |
| **Đầu ra** | ô `nguon:<nguồn>.so_dong · dem_dong · van_tay` (+ `fps.co_ref`) — 9 ảnh |
| **Công cụ được gọi** *(CHỈ hàm FLS có sẵn)* | `nguon_bank` · `nguon_fps` · `nguon_h1000` · `nguon_plt` = đếm dòng + đọc vân tay ảnh (`tools/chay_agent_voi.py:dem_nguon`) |
| **Mô hình ghim** | `claude-opus-5-5` · họ `anthropic` · ghim — **CHƯA gọi thật** (bản phát lại do mô hình GIẢ sinh) · **quyết chủ 23/11 ~12:45 (`WO-355`): MỘT nhà cung cấp Anthropic — Opus 5.5 cho agent LÀM** |
| **Dữ liệu & lưu giữ** *(chủ 23/11)* | agent đọc TOÀN BỘ nội dung giao dịch + số TK + tên (chỉ bỏ `Email Address`) · vận hành: Messages API dưới **ZDR** (bật theo tổ chức qua Anthropic) · fleet eval: **gửi theo lô** (Batches API — Anthropic giữ 29 ngày, đổi lấy −50 % giá; chủ chấp nhận) |
| **Phiên bản** | checksum prompt `9f84a5b36e62d7b0` + mô hình ghim + checksum tham chiếu (tệp số máy đã đo) |
| **Bước thông minh** | Hôm nay chỉ đếm + vân tay. Đề xuất G1 (Voi roadmap 01/03): đề xuất bản khai cho sheet mới · báo đổi bố cục cột. |
| **Fleet eval** | chưa có thẻ riêng (Voi: `a1-khai-chup.eval.lech-cot-ngay` PROPOSED) |

## Bộ skill — chạy TUẦN TỰ (skill n+1 chỉ khi cổng skill n ĐẠT)

| # | skill | loại | mô hình skill gọi | công cụ | cổng ra |
|---|---|---|---|---|---|
| 01 | [Nguồn Bank txns — ảnh sao kê + sổ AS-IS](../../../fls/agent/skill/A1_RI/01_nguon_bank.md) | lam | `claude-opus-5-5` | `nguon_bank` | `khop_khai:bank+so_asis` |
| 02 | [Nguồn FPS (PAY100) — PM line](../../../fls/agent/skill/A1_RI/02_nguon_fps.md) | lam | `claude-opus-5-5` | `nguon_fps` | `khop_khai:fps` |
| 03 | [Nguồn H1000 — sổ lương HR Allocate](../../../fls/agent/skill/A1_RI/03_nguon_h1000.md) | lam | `claude-opus-5-5` | `nguon_h1000` | `khop_khai:hr2024+hr2025` |
| 04 | [Nguồn PLT — 4 nền tảng GI · OMC · SC · PS](../../../fls/agent/skill/A1_RI/04_nguon_plt.md) | lam | `claude-opus-5-5` | `nguon_plt` | `khop_khai:gi+omc+sc+ps` |

Loại: `lam` = mô hình làm, A4 so 100 % với máy · `bong` = G0 bóng, so với đáp án giữ riêng, ⛔ ghi · `ma` = mã tất định, ⛔ mô hình.

## Cổng ra của agent

A4 (mã `fls/agent/doi_chieu.py`) so MỌI ô skill `lam` (và skill `ma` có công cụ) với số máy đã đo — mong: lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0. Khác ⇒ agent TRƯỢT, chuỗi DỪNG, agent sau ⛔ chạy.

## ⛔ Không được làm

- ⛔ gọi API thật khi thiếu chốt (`--that` + `FLS_CHO_GOI_API=1` + khoá + mô hình ghim)
- ⛔ ghi kho · ⛔ sửa ảnh · ⛔ sửa engine/tuyến — chỉ GỌI công cụ được cấp
- ⛔ tính lại / làm tròn / thêm ô / bịa ô — A4 so từng ô với máy
- ⛔ gửi `Email Address` (`PM_COT_RIENG_TU`) — bộ che chạy trước mọi lời gọi; mặc định `mo` (chủ 23/11: nội dung · số TK · tên đi nguyên văn) ⇒ chạy thật đòi thêm chốt `FLS_ZDR_DA_BAT=1` (ZDR); `--che che_noi_dung`/`che_het` che lại
