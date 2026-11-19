# KQ-191 — R2 CUỐI · `H6` (Step 20 · SO Y/H/Q/M theo IX.PER)

| | |
|---|---|
| **Thuộc** | `WO-188` · `BG-189` *(Vòng sửa sau R1)* · `KQ-190` · `isp/H6` @ `5c0fa7b` · cụm `5435` |
| **Phát bởi** | `fls-test` R2 · 2026-11-18 |
| **Kết luận** | **ĐẠT** — 0 CHẶN · 0 NÊN SỬA · 1 GHI NHẬN *(`H6-R2-01`)* |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H6.md` v0.2 |
| **Cây gộp thử** | `thu/H6` = `origin/claude/bold-galileo-zukpaf` + `isp/H6`: **0 xung đột**; ⛔ commit |

## Số đo *(Đ4)*
| Nhãn | R2 đo |
|---|---|
| WP-C3a ô khớp / ô so | **205.175 / 205.175** *(KPI loại 76.000 · `-` 25 · 760 cột)* |
| WP-C3b ô khớp / ô so | **11.585 / 11.585** *(≠ 0: 2.636 · lá 1,097e-14 · cha 1,163e-14)* |
| bài c3a + c3b + cuộn kỳ | 40 passed |
| đột biến mã *(5)* | M9 ⇒ 3 đỏ *(gồm bài R1-01)* · A1 ⇒ 2 · A2 ⇒ 6 *(+cổng đỏ)* · A3 ⇒ 1 · A4 ⇒ 3 |
| đường nền *(cây gộp)* | 28 = 28 · chạy 3.521 *(sàn 3.521 = đếm thật)*; web riêng 3 failed/672 passed = 675 |
| `lint-imports` · `kiem_tai_lieu` · `soi_bang_tuyen` | 11 kept 0 broken · ĐẠT *(317 tệp)* · 44/44 |

## Kết quả
- `H6-R1-01` **ĐÓNG** — M9 giờ ĐỎ trong pytest. `H6-R1-02` **ĐÓNG** — trục C3a từ IX.PER kho; `C3A_NGAY_TRUOC_PER = 1` có lý do errata ㉑; kho ⛔ IX.PER/tắt ⇒ ĐỎ có tên.
- `H6-R2-01` GHI NHẬN → backlog: cổng CLI C3a một mình mù A1·A3·A4 *(pytest bắt)*, cùng họ `H6-R1-03`.
- ⚠ Script `--duong-nen` bị harness cắt ở tầng web; chạy web riêng *(số trên)*. `-03·-04·-05` của R1 vẫn backlog.

⛔ Kiểm không sửa mã. Kho thật `KHONG_CHAM` *(IX.PER chỉ nạp vào cụm cục bộ 5435)*.
