# KQ-190 — R1 · `H6` (Step 20 · SO Y/H/Q/M theo IX.PER, WP-C3b)

| | |
|---|---|
| **Thuộc** | `WO-188` · `BG-189` · `isp/H6` @ `a0cceb5` · cụm `5435` |
| **Phát bởi** | `fls-test` R1 · 2026-11-18 |
| **Kết luận** | **ĐẠT CÓ ĐIỀU KIỆN** — 0 CHẶN · **2 NÊN SỬA** · 3 GHI NHẬN → giao R2 `KQ-191` |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H6.md` v0.1 |

## Số đo *(Đ4 — mỗi số một nhãn)*
| Nhãn | R1 đo |
|---|---|
| ô so khớp / ô so | **11.585 / 11.585** *(mong 11.585)* |
| …trong đó đáp án ≠ 0 | **2.636** *(22,8%)*; `0↔0` **8.949** |
| không so được *(tổng 21.090 = 370 × 57)* | KPI **5.700** *(≠ 0: 3.019)* · `-` **25** · kỳ 0 ngày **3.780** *(≠ 0: 65, toàn NPC)* |
| max\|lệch\| lá / cha | 1,097e-14 / 1,163e-14 *(atol 2e-13)* |
| đột biến đầu vào 1 ô *(5 dòng)* | đỏ 32·24·8·24·24 = đúng tập mong, 0 thừa/thiếu |
| đột biến mã | 15: cổng đỏ 10 · pytest đỏ 14 · **M9 lọt pytest** |
| đường nền `--duong-nen --cong 5435` | **28 = 28** · chạy 3.515 · web 3 = 3 · `KẾT: ĐẠT` |
| `lint-imports` · `kiem_tai_lieu` | 11 kept 0 broken · ĐẠT (315 tệp) |

## Phát hiện cần sửa trước R2
- **H6-R1-01 (NÊN SỬA)** — đường dương `_lich_tu_kho` ⛔ có bài; M9 *(ghi đè ngày đầu)* lọt 22/22 bài. Thêm bài nạp IX.PER ≠ 21/10 → `chay_wp_c3b`.
- **H6-R1-02 (NÊN SỬA)** — WP-C3a còn trục từ đáp án 409 + 2 chú thích *"tạm tới H6"* sai thực tế *(`do_hd2.py:469`, `:595`)*.
- GHI NHẬN: `-03` cổng CLI mù M6·M7·M8·M10·M11 (pytest bắt) · `-04` 3.019 ô KPI ≠ 0 chưa có cổng · `-05` errata ISP "410·411" + nạp IX.PER cụm mới.

⛔ Kiểm không sửa mã. Kho thật `KHONG_CHAM` *(chỉ nạp IX.PER vào cụm 5435 cục bộ)*.
