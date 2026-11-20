# WO-257 — ISP 3.1.2 · Step 36 · C13: IX.TMP — bản báo cáo ký có phiên bản (snapshot sign-off)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao 20/11 |
| **Phát bởi** | orchestrator *(tài khoản mới)* · 2026-11-20 |
| **Nhận** | `fls-dev` làn **CF** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/C13` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` *(đã gộp C5 — kho config chỉ-thêm `0027_cau_hinh_chi_them.sql`; C7 — `POST /api/fls/v1/config/fx/{yyyymm}/sign`: `actor` từ thẻ, `201`/`409`/`400`, xem `BG-213`)* |
| **Dải phiếu** | `BG-258` · `KQ-259` (R1) · `KQ-260` (R2 cuối, cây gộp thử) |

## Vì sao
- ISP **Step 36 · C13** (wave W12). Phụ thuộc C7 — đã gộp. Mở đường **F7** (Step 40, màn F08 ký bản) · **H14** (Step 46) · **I2** (Step 47).
- Ô thứ 3 của Pha 1 lấy C13 thay DT7 vì môi trường mới **chưa có khoá SA** (DT7 cần đọc sheet) — `TIEN_DO` hàng tiếp quản 19/11.
- Review theo **luật B của chủ (18/11)**: 2 vòng — R1 đầy đủ + R2 cuối trên cây gộp thử. Chữ "R1 · R2 · R3" ở ISP §2.4/Step 36 mục 8 là bản cũ, bị luật B thay.

## Spec phải đọc
| Tệp | Mục |
|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | **Step 36** *(· Step 33 C7 · Step 13 C5 — khuôn kho config)* |
| `02_BA/07_API_CONTRACT.md` | §1 *(quy ước lỗi · `actor` từ thẻ)* + §4i hai dòng `…/report/snapshot/{ky}` *(dòng ~857–858)* |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.2.3 IX.TMP · §3.2.4 dòng "sign-off dán value ở sheet `[PLA5]`" |
| `fls/cau_hinh/fx.py` · `fls/repo/cau_hinh_repo.py` · tuyến `ky_thang_fx` ở `fls/api/bang_tuyen.py` · `BG-213` | khuôn ký C7 *(dùng lại, ⛔ chép)* |
| `CLAUDE.md` | Đ1–Đ5 |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 (C13-B1) | đưa bản kỳ 2025-12 rồi ký ⇒ `201`; `GET …/report/snapshot/{ky}` thấy **phiên bản 1** `da_ky` + checksum + người ký **lấy từ thẻ** + thời điểm | pg |
| AC-2 (C13-B2) | đưa bản mới khác **1 ô** ⇒ **phiên bản 2** `chua_ky`; phiên bản 1 giữ nguyên *(checksum, người ký, nội dung — so từng byte)* | pg |
| AC-3 | đưa bản **trùng checksum** bản mới nhất ⇒ ⛔ sinh phiên bản mới *(khai rõ hành vi trong BG; nếu chọn khác ⇒ ghi lý do)* | pg |
| AC-4 | ký phiên bản đã ký ⇒ `409` có câu tiếng Việt · `actor` trong thân ⇒ `400` *(như C7)* · kỳ sai định dạng ⇒ `400` · kỳ chưa có bản ⇒ mã + câu khai trong BG | pg |
| AC-5 | chỉ-thêm: ⛔ `UPDATE`/`DELETE` dòng bản đã ký *(bài đo trên kho)*; dùng bảng của di trú `0027` — ⛔ di trú mới | pg |
| AC-6 | `soi_bang_tuyen.py` khớp *(46 → 48 tuyến)*; `07_API_CONTRACT` §4i: **⛔ tự lật** ⬜ → ✅ (orchestrator lật khi gộp) | công cụ |
| AC-7 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc · quyết sẵn
- **Đưa bản vào** (nội dung JSON ô) là **hàm mức module/repo** gọi từ bài — ⛔ thêm tuyến ghi thứ ba *(§4i chỉ có GET + POST sign)*. Engine thật nối ở I2 *(ISP Step 36 mục 3)*.
- **Định dạng `{ky}`:** theo quy ước đã có ở hợp đồng/C7 *(`yyyymm`)*; nếu §1/§4i nói khác ⇒ theo hợp đồng và ghi vào BG.
- **Checksum:** tất định trên JSON chuẩn hoá *(khoá sắp xếp)* — khai thuật toán trong BG.
- ⛔ huỷ ký · ⛔ phân quyền theo vai *(O11 = A: mọi thẻ hợp lệ ký được)* · ⛔ khuôn trình bày Templ 1–5 · ⛔ PDF · ⛔ màn *(F7)*.
- Ghi kho THẬT: `KHONG` (chỉ kho test).
- Chỗ mơ hồ ngoài các quyết trên ⇒ chọn phương án hẹp nhất, ghi "Giả định" + khuyến nghị vào BG *(⛔ dừng chờ — orchestrator soát ở R1)*.
