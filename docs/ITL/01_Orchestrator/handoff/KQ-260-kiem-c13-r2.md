# KQ-260 — biên bản kiểm `BG-258` *(R2 cuối · ISP 3.1.2 · Step 36 · C13)*

| | |
|---|---|
| **Thuộc** | `BG-258` *(mục "Vòng sửa sau R1 (KQ-259)")* · `WO-257` · tiếp `KQ-259` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2 cuối, vai KIỂM — ⛔ sửa mã)* · 2026-11-20 · `isp/C13` @ `889caec` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C13.md` v0.2: `C13-R2-01…03`)*. `C13-R1-01·02·03` **ĐÓNG** |

## Soát vòng sửa
| # | Mã | Kết luận | Đo *(mỗi số nói nó đếm gì)* |
|---|---|---|---|
| 1 | `C13-R1-01` | ĐÓNG | khứ hồi checksum *(đưa → đọc lại từ kho → băm)* khớp **17/17** mẫu hợp lệ = 7 mẫu R1 + 10 mới *(số lớn âm · `-1.5e300` · `5e-324` · `1.797e308` · lồng 9 tầng · chuỗi Unicode · `1e16` …)*; cặp giá trị toán học khác nhau ra cùng checksum **0/5** |
| 2 | `C13-R1-02` | ĐÓNG | `M12` *(bỏ khoá `dua_ban_ky`)* cắn **5/5** · `M7` *(bỏ khoá `ky_ban`)* cắn **5/5**; mã đúng chạy lại **5/5** xanh ⇒ ⛔ chập chờn |
| 3 | `C13-R1-03` | ĐÓNG | `M8` *(`cu[0]`)* ĐỎ **3/3** |
| 4 | đột biến thêm | 5 chỗ trên `git archive`, trả nguyên | `N1` *(trùng với mọi bản)* · `N2` *(bỏ khứ hồi số)* · `N3` *(bỏ sort_keys)* · `N4` *(ký lại)* · `N7` *(tháng 13)* **cắn 5/5**; `N5` *(nhận bool — tương đương, vô hại)* · `N6` *(bỏ chặn actor rỗng ở `ky_ban`)* sống ⇒ GHI NHẬN |

## Cây gộp thử
Nhánh làm việc + `isp/C13`: **xung đột 2 tệp**, chỉ ở sàn `MONG_PYTEST_*` *(`tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py`)* ⇒ giữ bản nhánh làm việc, đặt sàn = **thu thập thật 4278** *(4267 + 11 bài C13; web 681)*. ⛔ commit cây gộp thử *(orchestrator tự gộp)*.

| Lệnh | Kết quả |
|---|---|
| `--duong-nen --cong 5434` *(một lần, một mình, 12m50s)* | `ĐẠT` · tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)* · chạy **4278** ≥ 4278 · web **681** ≥ 681 · skipped 0 · deselected 0 |
| `lint-imports` | `11 kept, 0 broken` |
| `kiem_tai_lieu.py` | ĐẠT *(413 tệp · 2791 bảng)* |
| `soi_bang_tuyen.py` | khớp SQL **48** tuyến |

## GHI NHẬN → backlog
`C13-R2-01` chuỗi `\u0000` qua `chuan_hoa` rồi nổ ở `jsonb` *(⛔ `LoiBanKy`; chưa có tuyến chạm — H14)* · `C13-R2-02` thiếu bài `ky_ban(actor rỗng)` · `C13-R2-03` `-0.0`≡`0.0`, `1e22`≡`10**22` cùng checksum, `1`≠`1.0` *(ghi vào hợp đồng đưa bản)*. Còn từ R1: `-04` *(F7)* · `-05`·`-06` *(BA)* · `-07`.

## Việc kế
Orchestrator gộp `isp/C13` vào nhánh làm việc *(`isp-gop-buoc`)*; lật `07 §4i` `⬜`→`✅`; đặt sàn 4278 ở cây gộp thật.
