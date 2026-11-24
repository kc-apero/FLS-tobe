# A3 · SI.ITL — Adjust + Allocate

> Sinh bởi `python tools/sinh_the_agent.py` — ⛔ sửa tay (sửa prompt ở `fls/agent/skill/A3_SI_ITL/`, rồi sinh lại).

| | |
|---|---|
| **Vai** | AP Voi v3.1.2 §4.3.2 SI.ITL (PARTIAL) + CALCULATE/ALLOCATE/REPORT (gói HD2 WP-C2…C5) |
| **Đầu vào** | sổ ITL đóng băng 23 kỳ + ảnh Manual input 2026-03 + kết quả 10 gói engine HD2 |
| **Đầu ra** | ô `voi:theo_ky.*.{o_parity,hd_parity,o_go_that,o_mac_dinh}(_khop)` · `voi:khoi_theo_ky.*.*` · `voi:tu_sinh.*` · `hd2:<gói>.{khop,tong_o,lech_co_chu_dich}` |
| **Công cụ được gọi** *(CHỈ hàm FLS có sẵn)* | `final_7_khoi` · `vung_sua` · `tu_sinh` = `do_voi_so_luong.do()` (`final_rule.tinh_final` · `tu_soi.soi_mot_dong`) · `phan_bo_bao_cao` = số gói HD2 (`hd2_cong.json`, ghi bởi `tools/do_hd2.py`) |
| **Mô hình ghim** | `claude-opus-5-5` · họ `anthropic` · ghim — **CHƯA gọi thật** (bản phát lại do mô hình GIẢ sinh) · **quyết chủ 23/11 ~12:45 (`WO-355`): MỘT nhà cung cấp Anthropic — Opus 5.5 cho agent LÀM** |
| **Dữ liệu & lưu giữ** *(chủ 23/11)* | agent đọc TOÀN BỘ nội dung giao dịch + số TK + tên (chỉ bỏ `Email Address`) · vận hành *(chủ 24/11, `WO-359`)*: **Claude trên Vertex AI** của `fp-a-project` — dữ liệu ở GCP công ty, Google quản xử lý dữ liệu; request-response logging TẮT; ZDR đối tác xin qua account team (BG-360) · dự phòng: Messages API dưới **ZDR** · ⚠ Batches API ⛔ có trên Vertex ⇒ fleet eval gửi TỪNG lời (⛔ −50 %) |
| **Phiên bản** | checksum prompt `fe71100066e826c8` + mô hình ghim + checksum tham chiếu (tệp số máy đã đo) |
| **Bước thông minh** | Hôm nay chép số engine. Đề xuất G0 (Voi roadmap 23/11): gợi ý ô vùng sửa khối 2 Loại GD + 7 Hoá đơn (ô máy ⛔ trả lời) — CHƯA dựng; cần ảnh Manual input 22 tháng. |
| **Fleet eval** | `a3-2-luong` · `a3-3-nen-tang` (H1000 · nền tảng — PROPOSED) |

## Bộ skill — chạy TUẦN TỰ (skill n+1 chỉ khi cổng skill n ĐẠT)

| # | skill | loại | mô hình skill gọi | công cụ | cổng ra |
|---|---|---|---|---|---|
| 01 | [Ô Final 7 khối + khối HD theo kỳ (parity)](../../../fls/agent/skill/A3_SI_ITL/01_final_7_khoi.md) | lam | `claude-opus-5-5` | `final_7_khoi` | `khop_le_mau:o_parity+hd_parity` |
| 02 | [Vùng chỉnh tay R–AT: ô người gõ · ô mặc định · theo khối](../../../fls/agent/skill/A3_SI_ITL/02_vung_sua.md) | lam | `claude-opus-5-5` | `vung_sua` | `tong_ky:o_go_that+o_mac_dinh` |
| 03 | [Chế độ tự sinh MID (FLS tự tính từ Manual input)](../../../fls/agent/skill/A3_SI_ITL/03_tu_sinh.md) | lam | `claude-opus-5-5` | `tu_sinh` | `so_khong_am` |
| 04 | [Calculate · Allocate · Report — parity 10 gói HD2](../../../fls/agent/skill/A3_SI_ITL/04_phan_bo_bao_cao.md) | lam | `claude-opus-5-5` | `phan_bo_bao_cao` | `hd2_dem` |

Loại: `lam` = mô hình làm, A4 so 100 % với máy · `bong` = G0 bóng, so với đáp án giữ riêng, ⛔ ghi · `ma` = mã tất định, ⛔ mô hình.

## Cổng ra của agent

A4 (mã `fls/agent/doi_chieu.py`) so MỌI ô skill `lam` (và skill `ma` có công cụ) với số máy đã đo — mong: lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0. Khác ⇒ agent TRƯỢT, chuỗi DỪNG, agent sau ⛔ chạy.

## ⛔ Không được làm

- ⛔ gọi API thật khi thiếu chốt (`--that` + `FLS_CHO_GOI_API=1` + mô hình ghim + đường: Vertex `FLS_GCP_PROJECT` ∈ GCP công ty · hoặc khoá API)
- ⛔ ghi kho · ⛔ sửa ảnh · ⛔ sửa engine/tuyến — chỉ GỌI công cụ được cấp
- ⛔ tính lại / làm tròn / thêm ô / bịa ô — A4 so từng ô với máy
- ⛔ gửi `Email Address` (`PM_COT_RIENG_TU`) — bộ che chạy trước mọi lời gọi; mặc định `mo` (chủ 23/11: nội dung · số TK · tên đi nguyên văn) ⇒ chạy thật đòi thêm chốt `FLS_VERTEX_DU_LIEU_XAC_NHAN=1` (đường Vertex, WO-359) hoặc `FLS_ZDR_DA_BAT=1` (đường API); `--che che_noi_dung`/`che_het` che lại
