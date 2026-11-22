# KQ-259 — biên bản kiểm `BG-258` *(R1 · ISP 3.1.2 · Step 36 · C13)*

| | |
|---|---|
| **Thuộc** | `BG-258` · `WO-257` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R1, vai KIỂM — ⛔ sửa mã)* · 2026-11-20 · `isp/C13` @ `594af39` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 3 NÊN SỬA · 4 GHI NHẬN` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C13.md`)*. Hành vi đúng ở mọi biên đo; 3 NÊN SỬA là **bài thiếu** *(ký song song · ký phiên bản ≥ 2)* và **checksum ⛔ khứ hồi** với số float biên |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `dung_moi_truong_isp.sh --cong 5434` | `KẾT: ĐẠT` · kho rỗng |
| `test_ban_ky_pg.py` | **7/7** xanh |
| `--duong-nen --cong 5434` *(một mình, 1 lần)* | `ĐẠT` · tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0; 12 failed + 14 errors + 2 xfailed)* · chạy **4226** ≥ 4226 · skipped 0 · deselected 0 |
| `lint-imports` | `11 kept, 0 broken` |
| `soi_bang_tuyen.py` | khớp SQL **48** tuyến |
| `kiem_tai_lieu.py` | ĐẠT |

## Trọng tâm
| # | Kết luận | Đo |
|---|---|---|
| 1 | **AC-1…AC-4 ĐẠT**, tái đo độc lập qua HTTP thật | ký ⇒ 201, `actor` từ thẻ · v2 `chua_ky`, v1 từng dòng 2/2 nguyên · trùng ⇒ ⛔ phiên bản · 409/400/404 có câu tiếng Việt · kỳ sai khuôn **7/7** 400 |
| 2 | **Chỉ-thêm ĐẠT** | `UPDATE`/`DELETE` 2 bảng × 2 id = **8/8** `INV-I08`; `TRUNCATE` chặn; ⛔ di trú mới |
| 3 | Checksum tất định *(đảo khoá ⇒ cùng; đổi 1 giá trị ⇒ khác)* — **nhưng ⛔ khứ hồi** | `C13-R1-01`: lệch **2/7** mẫu số *(`1e22` · `-0.0`)* |
| 4 | **Ký đua ĐÚNG**: 5 kỳ × 8 luồng ⇒ mỗi kỳ **1** `201` · **7** `409` · +1 bản ký. Bỏ khoá ⇒ **2/5** vòng có 2 chữ ký | bài tác giả ⛔ cắn *(`M7`/`M12` SỐNG)* ⇒ `C13-R1-02` |
| 5 | **Giả định 1·2·3·4: đồng ý** *(4: v1 chưa ký bị bỏ rơi ⇒ BA quyết nhãn, `-06`)*; **5: XÁC NHẬN sai ngữ cảnh** *(`message` 409 = "thang IX.FX da ky"; `goi_cua.js` nói tỷ giá)* ⇒ `-04`, đóng ở F7 | — |
| 6 | Tuyến khớp §4i: **48** · `actor` = `sub` thẻ · `actor` trong thân ⇒ 400 · §4i còn ⬜ *(orchestrator lật)* | `C13-R1-05`: POST cần thân `{}` ⇒ câu BA |

## Đột biến *(bản sao `git archive`, trả nguyên)*
**13 chỗ: 10 giết · 3 SỐNG** — `M7` · `M12` *(bỏ khoá advisory — `-02`)* · `M8` *(ký bản cũ nhất — `-03`)*.

## Việc kế
Vòng sửa *(dev)*: `-01` *(chuẩn hoá số)* · `-02` *(bài đua)* · `-03` *(bài ký phiên bản ≥ 2)*. Backlog: `-04` *(F7)* · `-05` · `-06` *(BA)* · `-07`. R2 cuối chạy trên cây gộp thử.
