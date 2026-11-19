# KQ-215 — biên bản kiểm vòng sửa sau R1 `BG-213` *(R2 CUỐI · ISP 3.1.2 · Step 33 · C7)*

| | |
|---|---|
| **Thuộc** | `BG-213` *(mục "Vòng sửa sau R1 (KQ-214)")* · `WO-212` · tiếp `KQ-214` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2, vai KIỂM — ⛔ sửa mã)* · 2026-11-19 · `isp/C7` @ `7d7f0ca` · cây gộp thử `thu/C7` = `934f1e2` + `isp/C7` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C7.md` v0.2)* |

## Đóng `R1`
| Mã | Kết | Đo |
|---|---|---|
| `C7-R1-01` | **đóng** | `M7` *(bỏ `HKD` khỏi dấu vân)* ⇒ ĐỎ `test_C7_R1_01[HKD-…]` · `M16` *(GET bỏ so dấu vân)* ⇒ ĐỎ `[USD-…]` |
| `C7-R1-02` | **đóng** | bỏ `pg_advisory_xact_lock` ⇒ ĐỎ bài HTTP `…SONG_SONG_cung_thang` *(không chỉ script R1)*; bản ký mới bỏ chữ ký cũ ⇒ ĐỎ |
| `C7-R1-03` | **đóng** | `25000` ≡ `25000.0` ≡ `25000.00` cùng dấu vân; thay `normalize` bằng `str` ⇒ ĐỎ `C7_R1_03` |
| `C7-R1-05` | **đóng** | `FLS-FX-CHAN` ∈ `bao.MA_LOI` *(409)* + câu `goi_cua.js`; đổi tên mã ⇒ ĐỎ |
| `C7-R1-07` | **đóng** | `M2` · `M19` ⇒ ĐỎ `test_C7_R1_07` *(4 lý do chặn khác nhau)* |
| `-04` · `-06` | **mở — backlog BA** | câu BA, ⛔ mã *(`C7-R2-01`)* |

**Đột biến R1 nay chết 4/4** *(`M2` `M7` `M16` `M19`)*.

## Trọng tâm
- **`the.kiem` trên cây gộp** — token hỏng/rác/hết hạn/`none` ⇒ 401: đột biến `except` về `JSONDecodeError` ⇒ ĐỎ `C7_B5` *(`rac.rac.rac`)* · bỏ `exp` ⇒ ĐỎ · bỏ chặn `alg` ⇒ ĐỎ · bỏ `sub` ⇒ ĐỎ *(4 ca ≥ 2)*.
- **Đột biến thêm 11 chỗ trên mã sửa: 11/11 giết** *(tổng R2: 16/16 kể cả 5 chỗ R1)*; mỗi mẫu thay khớp đúng 1 chỗ.
- **Gộp thử:** xung đột **2 tệp** *(`tools/dung_moi_truong_isp.sh` sàn · `tests/test_dung_moi_truong_isp.py` bài ghim)* — giữ bản nhánh làm việc `3699`, đặt sàn = thu thập cây gộp **3717** *(= 3699 + 9 + 9; web 675 giữ)*. `07_API_CONTRACT.md` tự gộp, không xung đột.

## Cổng *(cây gộp thử)*
| Lệnh | Kết quả |
|---|---|
| `dung_moi_truong_isp.sh --cong 5434` | `KẾT: ĐẠT` · kho rỗng |
| `test_ky_fx_pg.py` + `tests/api/test_the.py` | **46/46** xanh |
| `--duong-nen --cong 5434` *(một mình, 1 lần)* | `ĐẠT` · tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0; 12 failed + 14 errors + 2 xfailed)* · chạy **3717** ≥ 3717 · skipped 0 · deselected 0 |
| `lint-imports` | `11 kept, 0 broken` |
| `kiem_tai_lieu.py` | ĐẠT |
| `soi_bang_tuyen.py` | khớp SQL **46** tuyến |

⛔ Cây gộp thử **không commit** vào `isp/C7`. Orchestrator gộp `isp/C7` và đặt sàn **3717**.
