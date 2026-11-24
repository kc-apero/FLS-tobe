# A4 · Auditor

> Sinh bởi `python tools/sinh_the_agent.py` — ⛔ sửa tay (sửa prompt ở `fls/agent/skill/A4_AUDITOR/`, rồi sinh lại).

| | |
|---|---|
| **Vai** | AP Voi v3.1.2 §4.4.1 KS.RI · KS.SI · KS.RP (PARTIAL) |
| **Đầu vào** | đầu ra A1–A3 + số máy đã đo (`voi_so_luong.json` · `hd2_cong.json` · đếm ảnh · cổng FLS) |
| **Đầu ra** | phán ĐẠT/TRƯỢT từng agent (MÃ) · ô `cong:HD1.*.dat` · `cong:HD2.*.dat` · `voi:dat_hd1.*` · `report.html` |
| **Công cụ được gọi** *(CHỈ hàm FLS có sẵn)* | `doi_chieu` (mã `fls/agent/doi_chieu.py`) · `cong_hd1` = `fls.repo.doc_bao_cao.doc_cong_tep_do` · `cong_hd2` = `doc_cong_hd2` · `report` (mã `fls/agent/report.py`) |
| **Mô hình** | **MÃ THUẦN tới G1** (quyết chủ C2) — ⛔ gọi mô hình, ⛔ dựng nhà cung cấp · phán cuối = MÃ `doi_chieu` · dự kiến G1 (phần KIỂM, `WO-355`): `claude-sonnet-5-5` họ `anthropic` (ghim) |
| **Dữ liệu & lưu giữ** *(chủ 23/11)* | agent đọc TOÀN BỘ nội dung giao dịch + số TK + tên (chỉ bỏ `Email Address`) · vận hành *(chủ 24/11, `WO-359`)*: **Claude trên Vertex AI** của `fp-a-project` — dữ liệu ở GCP công ty, Google quản xử lý dữ liệu; request-response logging TẮT; ZDR đối tác xin qua account team (BG-360) · dự phòng: Messages API dưới **ZDR** · ⚠ Batches API ⛔ có trên Vertex ⇒ fleet eval gửi TỪNG lời (⛔ −50 %) |
| **Phiên bản** | checksum prompt `0388cc6a6ab210f0` + mô hình ghim + checksum tham chiếu (tệp số máy đã đo) |
| **Bước thông minh** | MÃ THUẦN tới G1 (quyết chủ C2): phán và đọc cổng đều là mã, ⛔ lượt API. Đề xuất G0 (Voi 23/11–11/12): CHỈ THÊM cờ giải thích lệch, ⛔ bỏ cờ v0. |
| **Fleet eval** | `a4-soat.eval.lot-chan` (phần KIỂM dùng mô hình ở G1: `claude-sonnet-5-5` — cùng hãng, KHÁC mô hình A1–A3; WO-355) |

## Bộ skill — chạy TUẦN TỰ (skill n+1 chỉ khi cổng skill n ĐẠT)

| # | skill | loại | mô hình skill gọi | công cụ | cổng ra |
|---|---|---|---|---|---|
| 01 | [Soát lớp: so TỪNG Ô agent ↔ máy đã đo (mã, ⛔ mô hình)](../../../fls/agent/skill/A4_AUDITOR/01_soat_lop.md) | ma | MÃ — ⛔ lượt API | `doi_chieu` | `-` |
| 02 | [Cổng HD1: ô Final + kỳ đạt](../../../fls/agent/skill/A4_AUDITOR/02_cong_hd1.md) | ma | MÃ — ⛔ lượt API | `cong_hd1` | `cong_doc` |
| 03 | [Cổng HD2: parity từng gói báo cáo · phân bổ](../../../fls/agent/skill/A4_AUDITOR/03_cong_hd2.md) | ma | MÃ — ⛔ lượt API | `cong_hd2` | `cong_doc` |
| 04 | [Report MỘT trang (mã)](../../../fls/agent/skill/A4_AUDITOR/04_report.md) | ma | MÃ — ⛔ lượt API | `report` | `-` |

Loại: `lam` = mô hình làm, A4 so 100 % với máy · `bong` = G0 bóng, so với đáp án giữ riêng, ⛔ ghi · `ma` = mã tất định, ⛔ mô hình.

## Cổng ra của agent

A4 (mã `fls/agent/doi_chieu.py`) so MỌI ô skill `lam` (và skill `ma` có công cụ) với số máy đã đo — mong: lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0. Khác ⇒ agent TRƯỢT, chuỗi DỪNG, agent sau ⛔ chạy.

## ⛔ Không được làm

- ⛔ gọi API thật khi thiếu chốt (`--that` + `FLS_CHO_GOI_API=1` + mô hình ghim + đường: Vertex `FLS_GCP_PROJECT` ∈ GCP công ty · hoặc khoá API)
- ⛔ ghi kho · ⛔ sửa ảnh · ⛔ sửa engine/tuyến — chỉ GỌI công cụ được cấp
- ⛔ tính lại / làm tròn / thêm ô / bịa ô — A4 so từng ô với máy
- ⛔ gửi `Email Address` (`PM_COT_RIENG_TU`) — bộ che chạy trước mọi lời gọi; mặc định `mo` (chủ 23/11: nội dung · số TK · tên đi nguyên văn) ⇒ chạy thật đòi thêm chốt `FLS_VERTEX_DU_LIEU_XAC_NHAN=1` (đường Vertex, WO-359) hoặc `FLS_ZDR_DA_BAT=1` (đường API); `--che che_noi_dung`/`che_het` che lại
