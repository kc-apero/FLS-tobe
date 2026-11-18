# KQ-154 — biên bản kiểm `BG-153` *(R1 · ISP 3.1.2 · Step 17 · C6)*

| | |
|---|---|
| **Thuộc** | `BG-153` · `WO-152` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R1)* · 2026-11-18 · `isp/C6` @ `5e57e0e` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 2 NÊN SỬA · 2 GHI NHẬN` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C6.md`)*. Hành vi đúng ở mọi biên đo; hai hàng NÊN SỬA là **bài thiếu**, ⛔ lỗi hành vi |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `dung_moi_truong_isp.sh --cong 5446` | `KẾT: ĐẠT` · kho rỗng |
| `--duong-nen --cong 5446` *(một mình)* | `ĐẠT` · toàn bộ **28 = 28** · chạy **3325** ≥ 3325 · web **3 = 3** · 667 |
| `lint-imports` | `11 kept, 0 broken` |
| `soi_bang_tuyen.py` | khớp SQL ở **43** tuyến · `OK /config/per` |
| `kiem_tai_lieu.py` | K3 đỏ 1 lỗi `TIEN_DO.md:155` — **có sẵn từ nền**, ⛔ C6 |

## AC
| AC | Đo *(nhãn · mẫu số)* | |
|---|---|---|
| AC-1 | `2026-11-05`=Y2026·H2·Q4·M11; biên đo tay: `2024-12-31` Y2024 · `2025-01-01` Y2025·H1 · `2024-02-29` Y2024·M2 · `06-30`/`07-01` H1/H2 · `09-30`/`10-01` Q3/Q4 — **đúng 7/7**; bài ⛔ phủ 09/10 và 29/02 ⇒ `C6-R1-01` | ĐẠT *(+NÊN SỬA)* |
| AC-2 | luật B ⇒ `LoiKy LUAT_CHUA_KY` ở `chon_luat`/`ngay_ghi_nhan`/`kiem`/`nap_ix_per` *(nạp bị từ chối ⇒ kho ⛔ đổi)*; mã lạ ⇒ `PER_HONG`; M5/M14 *(rơi về A)* bị giết | ĐẠT |
| AC-3 | grep `2024-10-21` ở `fls/`+`tools/` = **1** *(chú thích)*; ngày+luật đọc kho qua `0027`; kho chưa nạp ⇒ `409 FLS-CAUHINH-CHUA-KHAI` ≠ `BANG-LA`; **nhưng** M7/M8 *(gõ cứng ở handler)* SỐNG ⇒ `C6-R1-02` | ĐẠT *(+NÊN SỬA)* |
| AC-4 | trên bản `IX.PER` thật *(mẫu số 1)*: UPDATE/DELETE cả `_ban` lẫn `_dong` ⇒ `INV-I08` có tên, **4/4** | ĐẠT |
| AC-5 | `?run_id=` ⇒ 400 *(M9 giết)* · 401 · 405 · `soi` ĐẠT | ĐẠT |
| AC-6 | sàn `3325` + bài ghim cùng commit; `--duong-nen` chạy 3325 | ĐẠT |

## Đột biến *(bản sao `git archive`, gói 195 bài)*
**20 chỗ: 14 bị giết · 6 SỐNG** — M3 · M4 *(`C6-R1-01`)* · M7 · M8 *(`C6-R1-02`)* · M6 · M15 · M16 *(`C6-R1-03`)*. *(Lượt đầu tôi lỡ gộp `tests/web` có 14 bài đỏ nền ⇒ "giết" giả; đã bỏ, đo lại chỉ với `test_js_chay_duoc`.)*

## Câu hỏi
Ngày đầu 20 hay 21/10/2024 *(`C6-R1-04`)* — khuyến nghị: để H5 chốt; C6 đổi bằng nạp bản mới, ⛔ đổi mã.
