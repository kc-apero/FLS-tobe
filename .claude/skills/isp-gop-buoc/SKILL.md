---
name: isp-gop-buoc
description: Gộp một nhánh bước ISP 3.1.2 (`<nhánh làm việc>-isp/<ID>`) vào nhánh làm việc sau khi R2 cuối ĐẠT 0 CHẶN · 0 NÊN SỬA — thủ tục 11 bước, có công cụ `tools/gop_buoc_isp.py`. Dùng khi orchestrator hoặc chủ nói "gộp bước", "gộp H7", "merge isp/…", "R2 ĐẠT rồi gộp", "đặt sàn", "nâng MONG_PYTEST", "gộp sổ phát hiện".
---

# isp-gop-buoc — gộp một bước ISP vào nhánh làm việc

Nguồn: `HANDOFF_ORCHESTRATOR_2026-11-19.md` §5.3 · bảng quyết §5.2. Chỉ orchestrator gộp, trên cụm **5433**.

## Điều kiện vào
- R2 cuối (`KQ-(n+3)`, chạy trên **cây gộp thử**) **ĐẠT 0 CHẶN · 0 NÊN SỬA**. Có NÊN SỬA ⇒ 1 vòng sửa + R2b nhẹ trước.
- Cây làm việc sạch, HEAD = nhánh làm việc, PG 5433 bật (skill `fls-moi-truong` §2).

## Thủ tục (máy làm ⚙ · người làm ✋)

| # | Việc | Ai |
|---|---|---|
| 1–2 | `python tools/gop_buoc_isp.py bat-dau <ID>` — fetch `refs/heads/<nhánh làm việc>-isp/<ID>` → `isp/<ID>` → `git merge --no-ff --no-commit`. Exit 2 = còn xung đột MÃ | ⚙ |
| 3 | Gỡ xung đột MÃ — **giữ CẢ HAI** khi hai bước thêm khối song song: `docs/ITL/_tools/hd2_cong.json` · `tools/do_hd2.py` · `fls/repo/cau_hinh_repo.py` · changelog `07_API_CONTRACT`. `git add` từng tệp | ✋ |
| 4–7, 9 | `python tools/gop_buoc_isp.py tiep <ID> <YYYY-MM-DD>` — `--ours` hai tệp sàn · đếm thu thập THẬT cây gộp (toàn bộ + `tests/web`) · đặt `MONG_PYTEST_*` + bài ghim + chú thích chuỗi gộp · `gop_so.py` (bump `v0.NN`) · cổng `kiem_tai_lieu` · `lint-imports` 11 kept · `soi_bang_tuyen` · `quet_pii_repo` 0 | ⚙ |
| 8 | Bước mở tuyến/đổi hợp đồng ⇒ `docs/ITL/02_BA/07_API_CONTRACT.md` §4i ⬜ → ✅ + bump version + changelog | ✋ |
| — | Chạy bài liên quan của bước (`pytest tests/<thư mục bước>`) | ✋ |
| 10 | Commit `Gộp isp/<ID> (<Step NN · tên ngắn>): R2 cuối KQ-… ĐẠT 0 · 0` + trailer của phiên → `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5433` chạy NỀN (~25 phút) → **chỉ push khi `KẾT: ĐẠT`** (28 = 28 · web 3 = 3, hoặc tập đỏ nền hiện hành) | ✋ |
| 11 | Hàng `docs/ITL/01_Orchestrator/isp-3.1/TIEN_DO.md` (dấu `\|` trong ô phải thoát) → `kiem_tai_lieu.py` → commit → push | ✋ |

## Khi đỏ
- Công cụ in `ĐỎ (Đ5): mẫu … khớp k lần, mong 1` ⇒ mẫu sàn/bài ghim đã đổi dạng — sửa tay, ⛔ nới mẫu cho xanh. Công cụ ⛔ ghi gì khi một mẫu trượt.
- `--duong-nen` đỏ ⇒ ⛔ push; `git reset --hard origin/<nhánh làm việc>` (chỉ bỏ commit CHƯA push); giao **phiên sửa tích hợp** trên nhánh bước (mẫu `sua.md`).
- Thu thập pytest lỗi ⇒ còn dấu xung đột hoặc import vỡ — công cụ đã ĐỎ, ⛔ đặt sàn tay.

## Bẫy đã cắn
- Sàn ở nhánh bước lệch cây gộp 2–9 bài ⇒ luôn đếm trên CÂY GỘP sau khi hết dấu xung đột.
- Khối HD2 gói mới thiếu `tong_o`/`khop` ⇒ `/gates` null + bài CG2 đỏ khi gộp (cắn 2 lần) — R2 phải chạy trên cây gộp thử.
- Bước có ảnh dữ liệu mới ⇒ `quet_pii_repo.py` trên cây gộp đòi 0.
- ⭐ **24/11 — cụm gộp ở container cloud = `5434`, ⛔ `5433`.** `NAP-R1-05` (gộp STG-NAP) cho `tools/staging/05_*` CHẶN `PG_DSN` cổng 5433 vì trên máy chủ 5433 = `fls-pg-1` THẬT ⇒ chạy đường nền ở 5433 container ⇒ **15** bài `test_05` ĐỎ đúng thiết kế. Dùng `dung_moi_truong_isp.sh --cong 5434` + `--duong-nen --cong 5434` (226/226 bài staging xanh ở 5434). `gop_buoc_isp.py` vẫn ghi `5433` trong lời nhắc — theo dòng này.
- `gop_buoc_isp.py tiep` tìm sổ riêng `SO_PHAT_HIEN_ISP-3.1_<ID>.md` theo ĐÚNG mã nhánh ⇒ nhánh `STG-NAP` có sổ `_NAP.md` ⇒ công cụ bỏ bước 7 ⇒ chạy tay `gop_so.py <R> NAP v0.NN <ngày> <sha>`.
- Sổ riêng khác khuôn **10 cột** (AG 6 · HELD 4 · SONG 5) ⇒ `gop_so.py` chép hàng lệch cột ⇒ `kiem_tai_lieu` K3 ĐỎ ⇒ đổi cột tay trước commit (mẫu prompt R1/R2/sửa nay đòi 10 cột).
- Nhánh đã gộp **giữ nguyên** làm lịch sử (⛔ xoá). ⛔ PR · ⛔ force push.
