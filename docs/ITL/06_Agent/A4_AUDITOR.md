# A4 · Auditor

> Sinh bởi `python tools/sinh_the_agent.py` — ⛔ sửa tay (sửa prompt ở `fls/agent/skill/A4_AUDITOR/`, rồi sinh lại).

| | |
|---|---|
| **Vai** | AP Voi v3.1.2 §4.4.1 KS.RI · KS.SI · KS.RP (PARTIAL) |
| **Đầu vào** | đầu ra A1–A3 + số máy đã đo (`voi_so_luong.json` · `hd2_cong.json` · đếm ảnh · cổng FLS) |
| **Đầu ra** | phán ĐẠT/TRƯỢT từng agent (MÃ) · ô `cong:HD1.*.dat` · `cong:HD2.*.dat` · `voi:dat_hd1.*` · `report.html` |
| **Công cụ được gọi** *(CHỈ hàm FLS có sẵn)* | `doi_chieu` (mã `fls/agent/doi_chieu.py`) · `cong_hd1` = `fls.repo.doc_bao_cao.doc_cong_tep_do` · `cong_hd2` = `doc_cong_hd2` · `report` (mã `fls/agent/report.py`) |
| **Mô hình ghim** | `gemini-3.8-flash` · họ `google` · **CHƯA ghim** (tên tạm — chủ cấp mã chính xác lúc mở tài khoản Google) · **phương án A — chủ chốt 23/11** |
| **Dữ liệu & lưu giữ** *(chủ 23/11)* | agent đọc TOÀN BỘ nội dung giao dịch + số TK + tên (chỉ bỏ `Email Address`) · vận hành: Messages API dưới **ZDR** (bật theo tổ chức qua Anthropic) · fleet eval: **gửi theo lô** (Batches API — Anthropic giữ 29 ngày, đổi lấy −50 % giá; chủ chấp nhận) |
| **Phiên bản** | checksum prompt `8160a71f8ba50465` + mô hình ghim + checksum tham chiếu (tệp số máy đã đo) |
| **Bước thông minh** | Phán là MÃ; mô hình chỉ chép cổng. Đề xuất G0 (Voi 23/11–11/12): CHỈ THÊM cờ giải thích lệch, ⛔ bỏ cờ v0. |
| **Fleet eval** | `a4-soat.eval.lot-chan` (chấm bằng họ khác: Claude Opus 5.5) |

## Bộ skill — chạy TUẦN TỰ (skill n+1 chỉ khi cổng skill n ĐẠT)

| # | skill | loại | công cụ | cổng ra |
|---|---|---|---|---|
| 01 | [Soát lớp: so TỪNG Ô agent ↔ máy đã đo (mã, ⛔ mô hình)](../../../fls/agent/skill/A4_AUDITOR/01_soat_lop.md) | ma | `doi_chieu` | `-` |
| 02 | [Cổng HD1: ô Final + kỳ đạt](../../../fls/agent/skill/A4_AUDITOR/02_cong_hd1.md) | lam | `cong_hd1` | `cong_doc` |
| 03 | [Cổng HD2: parity từng gói báo cáo · phân bổ](../../../fls/agent/skill/A4_AUDITOR/03_cong_hd2.md) | lam | `cong_hd2` | `cong_doc` |
| 04 | [Report MỘT trang (mã)](../../../fls/agent/skill/A4_AUDITOR/04_report.md) | ma | `report` | `-` |

Loại: `lam` = mô hình làm, A4 so 100 % với máy · `bong` = G0 bóng, so với đáp án giữ riêng, ⛔ ghi · `ma` = mã tất định, ⛔ mô hình.

## Cổng ra của agent

A4 (mã `fls/agent/doi_chieu.py`) so MỌI ô skill `lam` với số máy đã đo — mong: lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0. Khác ⇒ agent TRƯỢT, chuỗi DỪNG, agent sau ⛔ chạy.

## ⛔ Không được làm

- ⛔ gọi API thật khi thiếu chốt (`--that` + `FLS_CHO_GOI_API=1` + khoá + mô hình ghim)
- ⛔ ghi kho · ⛔ sửa ảnh · ⛔ sửa engine/tuyến — chỉ GỌI công cụ được cấp
- ⛔ tính lại / làm tròn / thêm ô / bịa ô — A4 so từng ô với máy
- ⛔ gửi `Diễn giải` · `Số chứng từ` · tên người · email · số TK — bộ che `NFR-I13` chạy trước mọi lời gọi
