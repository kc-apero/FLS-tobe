# WO-334 — STAGING bước 05: nạp DỮ LIỆU THẬT (sổ kế toán + 4 nguồn) vào Cloud SQL `fls-staging` — khớp 100 % số đã đo

| | |
|---|---|
| **Trạng thái** | `MO` — viết 23/11 ~05:05 UTC; giao khi có chỗ phiên (≤ 3) |
| **Phát bởi** | orchestrator · 2026-11-23 |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud Sonnet 5.5 · medium · nhánh `claude/bold-galileo-zukpaf-isp/STG-NAP` (nền = ngọn `isp/STG` — tăng tốc ③) |
| **Dải phiếu** | `BG-335` · `KQ-336` (R1) · `KQ-337` (R2 cuối). Số trống kế tiếp sau dải: **338** |

## Vì sao — quyết chủ 23/11
- Chủ: *"đồng ý khuyến nghị agent + staging. Ngoại trừ C3, chạy trên dữ liệu thật"* ⇒ **BG-326 C3 = THẬT**. Ghi nhận = chủ **chấp nhận rủi ro** tên người + tiền thật trên staging (VM + Cloud SQL ở `fp-a-project`, ⛔ địa chỉ công khai — IAP).
- Các câu khác theo khuyến nghị: C1 VM `e2-small` + IAP · C2 mỗi người tự mở IAP tunnel (≤ 5 người) · C4 hai người (một ký · một soát chỉ đọc) · C5 `doc` suốt UAT, `ghi` chỉ ở bước ký.
- BG-326: bước 04 chỉ nạp config IX.*; `fls_itl` = 0 dòng; công cụ nạp nguồn sẵn có (`tools/nap_that.py` · `tools/chup_sao_ke.py` · `tools/nap_sao_ke.py` · `tools/nap_nguon_va_khai.py` · `tools/nap_mapping_master.py` …) lấy token Google Sheets bằng SA cục bộ gắn cứng ⇒ ⛔ chạy được ở Cloud Shell/VM.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 | **đo trước:** liệt kê đủ công cụ nạp nguồn đang dùng ở máy chủ để ra kho hiện hành (sổ ITL · sao kê 60 nguồn · PM/FPS · H1000 · nền tảng · Mapping Master · ảnh chụp) + thứ tự + bảng đích + số dòng mong (từ `docs/ITL/_tools/voi_so_luong.json`, ảnh đã commit, chú thích mã — Đ1: grep `docs/` LẪN `fls/` + `tools/`) | BG |
| AC-2 | `tools/staging/05_nap_nguon_that.sh --project <ID> --nguoi-nap <tên> [--kiem]`: chạy ở Cloud Shell qua Cloud SQL Auth Proxy bằng `fls_ghi`; đọc Sheets **CHỈ-ĐỌC** bằng thông tin xác thực KHÔNG gắn cứng (tham số/ADC/SA của staging — khai cách cấp quyền đọc sheet, ⛔ khoá trong repo/chat); đòi `FLS_CHO_GHI_THAT=1`; ⛔ ghi một ô nào về sheet (`QĐ-ITL-34`); chạy lại được — lần 2 ⛔ nhân đôi (`fls_itl` chỉ-THÊM `INV-I08`) | pytest (Sheets GIẢ + PG thật) |
| AC-3 | **BÁO CÁO khớp 100 %**: mỗi bảng/nguồn khai `mong` = số đã đo ở máy chủ (vd sổ 9.967 dòng · 23 kỳ · bank 8.338/8.338 · 60 nguồn …) — lệch 1 dòng ⇒ ĐỎ có tên; phép ⛔ đo được ⇒ ĐỎ; mẫu số ≠ 0 (Đ3); chứng minh ĐỎ hai chiều | pytest |
| AC-4 | riêng tư: `PM_COT_RIENG_TU = {"Email Address"}` ⛔ vào kho (bài); `Tên tài khoản` GIỮ (quyết 11/09); `sao_luu/` `hien_vat/` ⛔ tải lên; BÁO CÁO ⛔ in tên người/số TK/tiền dòng — chỉ số đếm + checksum | pytest + `quet_pii_repo` |
| AC-5 | sau nạp: chuỗi HD2 trên staging (`tools/staging/app/chay_chuoi.sh`) + `do_voi_so_luong.py` đọc kho staging ⇒ số khớp `voi_so_luong.json` / `hd2_cong.json` (khối so sánh trong BÁO CÁO) | BG + pytest |
| AC-6 | README staging thêm bước 05 + cập nhật `UAT_STAGING_E2E.md` (số mong khi có dữ liệu thật); `--duong-nen` ĐẠT; nâng sàn + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- ⛔ Claude vào GCP — viết script, CHỦ chạy. ⛔ ghi kho THẬT `fls-pg-1`. ⛔ sửa engine/tuyến/luật cửa. ⛔ `docker compose down`.
- Thiếu quyền đọc một sheet ⇒ DỪNG phần ấy, BÁO CÁO ĐỎ có tên (⛔ bỏ qua im lặng).
