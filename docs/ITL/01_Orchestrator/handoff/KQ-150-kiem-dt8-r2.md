# KQ-150 — biên bản kiểm R2 CUỐI `BG-148` *(ISP 3.1.2 · Step 19 · DT8)*

| | |
|---|---|
| **Thuộc** | `BG-148` · `WO-147` · sau `KQ-149` |
| **Kiểm bởi** | `fls-test` · 2026-11-18 *(cụm PG 5445 · `isp/DT8` @ `d063a97`)* |
| **Phán quyết** | `ĐẠT` — **đủ điều kiện GỘP** *(0 CHẶN · 0 NÊN SỬA · 1 GHI NHẬN `DT8-R2-01`)* |

## 1 · Bốn NÊN SỬA R1 — tái đột biến trên bản sao `git archive` *(`57118ff`+`d063a97`)*
| Mã | Đột biến đúng ca R1 | Bài ĐỎ | Kết |
|---|---|---|---|
| `-01` | ảnh `ix_ven` cắt còn **36**/42 dòng | 4 *(checksum · tái tạo byte · 42 dòng · dải liền 4–45)* | đóng |
| `-02` | bỏ vế PM khỏi so `Σ chia` · bỏ dòng khai mẫu số PM | 2 · 8 | đóng |
| `-03` | chọn lại theo `AE∧AF` · ảnh `gi_mid3` cắt 11/253 hàng | 5 · 7 | đóng |
| `-04` | bỏ `u`,`v` khỏi `KIEU_COT` · phân bố chỉ đếm tổng · xoá `LOI_MONG` MID1 | 4 · 3 *(loại→loại, `#VALUE!`↔`#N/A`, `#DIV/0!`↔`#REF!`)* · 1 | đóng |
Nền chưa đột biến: `test_dap_an_gi.py` **43/43** xanh. *(3/8 ca phân bố ĐỎ ở đột biến "chỉ đếm tổng" — các ca còn lại đổi tổng nên ĐỎ bằng cổng khác.)*

## 2 · Đối chiếu nguồn PHẦN MỚI *(khoá SA chỉ-đọc, 100 % ô; bản thô `/tmp/r2_dt8/`, ⛔ commit)*
| Vùng | Ô so | Lệch |
|---|---|---|
| `IX.VEN` `M4:S45` — 42 hàng, trong đó **6 hàng mới** 40–45 | 294 *(mới: 42)* | **0** |
| `MID3` `O10:AF273` — 253 hàng `O` là số = tập ảnh *(trùng tập: có)*; **242 hàng mới** | 3.542 *(mới: 3.388)* | **0** |
| `MID1` `U`,`V` 2.856 hàng ảnh | 5.712 | **0** |
| `MID2` `U`,`V` 1.463 hàng | 2.926 | **0** |
| Tổng | **12.474 ô** | **0** |

## 3 · Cây gộp thử `/tmp/r2_dt8/gop` *(`origin/moi/lam_viec` + `isp/DT8`; ⛔ commit/push)*
- Xung đột: **2 tệp** — `tools/dung_moi_truong_isp.sh`, `tests/test_dung_moi_truong_isp.py` ⇒ `--ours`. Không tệp nào khác.
- Thu thập cây gộp: **3343** bài *(= 3296 + 32 + 15)*; `tests/web` 667.
- `--duong-nen` *(một lần)*: lần chạy ấy **ĐỎ** vì tôi nâng hằng `3343` mà quên nâng literal `3296` trong bài ghim `S0_R2_03` ⇒ đo 29 ≠ 28, *thêm đúng 1 node = bài ghim ấy*; web 3 = 3 ✅; di trú · lint · HD1 ✅. Sửa literal ⇒ `test_dung_moi_truong_isp.py` **60/60** xanh. ⛔ chạy lại toàn bộ *(lệnh: một lần)* ⇒ KẾT toàn bộ **chưa quan sát ĐẠT**; còn lại ngoài bài ghim = 28 = 28.
- `lint-imports` 11 kept, 0 broken · `kiem_tai_lieu.py` ĐẠT *(281 file · 2.496 bảng)*.

## 4 · GHI NHẬN mới *(chỉ ghi sổ)*
`DT8-R2-01` — sàn gộp phải nâng ở **cả** hằng lẫn bài ghim = **3343**.

## Kết luận
Đủ điều kiện GỘP. Khi gộp thật: giải xung đột `--ours`, đặt `3343` ở hai chỗ, đo lại `--collect-only`, chạy `--duong-nen` một lần để xác nhận KẾT ĐẠT.
Errata cho orchestrator *(đã có ở `BG-148`)*: AP "Block 1 = 36" → 42; "U3 `#REF!`" → `#VALUE!`+`#DIV/0!`.
