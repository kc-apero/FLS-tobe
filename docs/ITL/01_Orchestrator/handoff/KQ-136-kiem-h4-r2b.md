# KQ-136 — biên bản kiểm `BG-133` *(R2b NHẸ · Step 13 · H4 · vòng sửa sau `KQ-135`)*

| | |
|---|---|
| **Thuộc** | `BG-133` *(mục "Vòng sửa sau R2")* · `WO-132` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con của orchestrator ISP 3.1.2)* · 2026-11-18 |
| **Đối tượng** | `git diff 9d45847 isp/H4` — `isp/H4` @ `f7c45da`; cụm PG `5435` |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA · 0 GHI NHẬN mới** *(sổ `SO_PHAT_HIEN_ISP-3.1_H4.md` v0.3: `H4-R2-01…04` ĐÃ ĐÓNG; `H4-R1-05` chờ gộp)* |

## Tái đột biến *(bản sao `git archive isp/H4`; ⛔ chạm worktree)*
| Mã | Đột biến | Kết |
|---|---|---|
| `H4-R2-01` | `BM +1 VND` ds1960 *(`\|BM\|` lớn nhất)* | **ĐỎ** *(`dat=False`, 1 lệch)* |
| `H4-R2-01` | `BQ +1e-9` ds10 *(`\|BQ\|`=1,5)* | **ĐỎ** *(1 lệch)* |
| `H4-R2-01` | `BO +9e-7` · `BR +9e-7` *(hàng lớn nhất)* | **ĐỎ ×2** |
| `H4-R2-02` | xoá `BN[4962]` | **ĐỎ** — `ô đáp án bỏ 35 ≠ mong 36` |
| `H4-R2-03` | `#NGUYENVANA0912345678` · `Nguyen Van A 0912345678` ở cột R | **TỪ CHỐI** ×2; `#N/A ()` chấp nhận |
| `H4-R2-04` | `BG-133:128` | đính chính THÊM *(câu cũ giữ)*: 2 bVND/mUSD + 3 tiền tệ ✔ |

Gốc: `63016/63016` · hàng đáp án `7883` · ô bỏ `36` · ngoài tên `0` · `KẾT: DAT` *(`do_hd2 --goi WP-C2`)*. Mẫu số mỗi phép khác rỗng *(Đ3)*: `63016`.
Ghi chú: `BR/BS rtol 1e-14` ⛔ quyết gì *(`\|exp\|` nhỏ ⇒ `atol` quyết)* — tác giả đã khai trong chú thích; orchestrator chốt.

## Cây gộp thử *(`/tmp/r2b_h4/gop` = `origin/moi/lam_viec` @ `b7154d1` + `merge --no-ff --no-commit isp/H4`; ⛔ commit/push)*
| Hạng mục | Đo |
|---|---|
| Xung đột | **2** *(đúng hai tệp dự kiến)*: `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` ⇒ `--ours`; **0** ở tệp khác *(`CALC_ZONE_406.md` gộp sạch; mục Số dư: 9 dòng khớp ⇒ `H4-R1-05` đóng khi gộp)* |
| Thu thập | **3262** bài *(tổng `pytest --collect-only`; web **667**)* ⇒ `MONG_PYTEST_TOAN_BO = 3262` ở script **và** bài ghim |
| `--duong-nen --cong 5435` *(MỘT lần)* | `12 failed · 3234 passed · 2 xfailed · 14 errors`; nền `28 = 28 (thêm 0 · bớt 0)`; chạy `3262 (mong ≥ 3262)`; skipped 0 · web `3 failed · 664 passed`, nền `3 = 3`; **`KẾT: ĐẠT`** |
| `lint-imports` | `11 kept, 0 broken` |
| `kiem_tai_lieu.py` | `✅ DAT` *(271 file · 2453 bảng · 800 ô ngày · 104 mã QĐ)* |

## Phát hiện
Không có phát hiện mới.
