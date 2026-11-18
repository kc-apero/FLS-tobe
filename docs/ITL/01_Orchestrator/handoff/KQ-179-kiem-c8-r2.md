# KQ-179 — biên bản kiểm `BG-177` *(R2 CUỐI · ISP 3.1.2 · Step 22 · C8)*

| | |
|---|---|
| **Thuộc** | `BG-177` · `WO-176` · tiếp `KQ-178` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2)* · 2026-11-18 · `isp/C8` @ `92d3682` · cụm `5447` |
| **Phán quyết** | **`ĐẠT` — đủ điều kiện GỘP.** Sổ `SO_PHAT_HIEN_ISP-3.1_C8.md` v0.2: **0 CHẶN · 0 NÊN SỬA mở** *(3 đóng)* · `4` GHI NHẬN mở *(`R1-04`…`-06`, `R2-01`)* |

## Ba lỗi R1 *(`git diff 5a8215c isp/C8` = 5 tệp: 2 bài + 2 dòng hằng + `BG-177`; ⛔ đổi mã `fls/`)*
| Mã | Đo | Phán |
|---|---|---|
| `C8-R1-01` | Bài đọc hàng `CN`/`Cash Treasury` **từ ảnh lúc chạy**, đòi mẫu số `≥ 4`. Quét `git diff ffe06b8..isp/C8`: **0** dòng có chuỗi ≥ 8 chữ số; tập số CN đối chiếu **4** *(≠ 0; đối chứng dương: cả 4 có trong ảnh, và diff R1 `ffe06b8..7d17b48` trúng **1**)* | ĐÓNG |
| `C8-R1-02` | Bài `…02_hai_CDT_la…`: 2 sự kiện ⇒ `/queue` ra mới nhất, oracle khớp, mẫu số 1 hàng. **M5** *(sự kiện cũ nhất)* ⇒ `1 failed, 18 passed` *(nền `19 passed`)* | ĐÓNG |
| `C8-R1-03` | Bài lỗi có tên + `nap` từ chối rác trước ghi + `actor` rỗng. **M10** *(bỏ `TK_TRUNG`)* · **M11** *(bỏ `_kiem_org`)* · **M12** *(bỏ kiểm `actor`)* ⇒ mỗi cái `1 failed, 18 passed`; trả nguyên ⇒ `19 passed` | ĐÓNG |

Đột biến trên bản sao `git archive`; mỗi đột biến áp đúng `1` chỗ rồi trả nguyên.

## Cây gộp thử *(`origin/moi/lam_viec` @ `4ce762e` + `merge --no-ff --no-commit isp/C8`; ⛔ commit/push)*
**0 xung đột** *(⛔ phải `checkout --ours`)*. Thu thập cây gộp = hằng `MONG_PYTEST_TOAN_BO=3426` *(`lam_viec` chưa mang nhánh ISP khác)*.
| Lệnh | Kết quả |
|---|---|
| `--duong-nen --cong 5447` *(một lần)* | **`KẾT: ĐẠT`** · toàn bộ `12 failed · 3398 passed · 2 xfailed · 14 errors` = nền **28 = 28** node id *(thêm 0 · bớt 0)*, chạy **3426** *(mong ≥ 3426)* · `tests/web` nền **3 = 3**, chạy **675** |
| `lint-imports` | `11 kept, 0 broken` |
| `soi_bang_tuyen.py` | khớp SQL **43** tuyến |
| `kiem_tai_lieu.py` | ĐẠT *(302 file · 2.554 bảng)* |

## Riêng tư
Quét TK cá nhân toàn diff C8: **0** trúng *(mẫu số 4, có đối chứng dương)*. Ảnh DT3 vẫn mang số CN có sẵn — `C8-R1-06` ghi nhận, ngoài phạm vi C8.

## Ghi nhận mới
`C8-R2-01`: hằng thu thập phải đo lại ở cây gộp mỗi lần gộp thêm nhánh *(luật 17/11)*.
