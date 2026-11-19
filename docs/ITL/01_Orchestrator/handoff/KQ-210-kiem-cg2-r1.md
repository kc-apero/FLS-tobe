# KQ-210 — biên bản kiểm `BG-209` *(R1 · Step 30 · CG2)*

| | |
|---|---|
| **Thuộc** | `BG-209` · `WO-208` · nhánh `isp/CG2` @ `5beac8c` |
| **Kiểm bởi** | `fls-test` · 2026-11-18 *(⛔ sửa mã)* |
| **Phán quyết** | **`ĐẠT CÓ ĐIỀU KIỆN`** — **0 CHẶN · 2 NÊN SỬA · 3 GHI NHẬN** *(sổ `SO_PHAT_HIEN_ISP-3.1_CG2.md` v0.1)* |

## Cổng
| Lệnh | Đo |
|---|---|
| `pytest tests/api/test_isp_gates_hd2.py` | 31 passed · `tests/api -k gate/cong/hd2/cg1` 108 passed *(bài CG1 cũ xanh)* |
| `soi_bang_tuyen.py` | ĐẠT 45/45 tuyến |
| `--duong-nen --cong 5446` *(1 lần)* | ĐẠT — toàn bộ 12F·3619P·14E = 28 = 28 node id *(thêm 0 · bớt 0)*, chạy 3647; web 3 = 3, chạy 675 |
| `lint-imports` · `kiem_tai_lieu.py` | 11 kept · 0 broken · K1–K6 ĐẠT *(332 file)* |

## Trọng tâm
1. **`lat_bo` vắng ⇒ `true` im lặng = họ "0 lệch khi chưa đo"** → `CG2-R1-01` **NÊN SỬA** *(⛔ CHẶN: `true` vẫn dựa `khop == tong_o` + `dong_so`)*. Khoá có **0** lần ở tệp thật và ở `do_hd2.py`; `lat_truot=0` gõ cứng 3 lần. Cần ít nhất `da_do` khai lỗ; hoặc `null`.
2. Đột biến từng ca trên tệp thật *(35 ca)*: `dat` ∈ {`"true"`, `1`, `None`, vắng} · `lat_bo` ∈ {`"0"`, `True`, `None`, `-1`, `0.0`} · `tong_o` {`"…"`, `True`, 0} · `khop≠tong_o` · vắng/hỏng/BOM/`[]`/`{}` ⇒ **luôn `null`**, ⛔ `true`; `lat_bo=2` ⇒ `false`. **Lỗ:** khối gói mang kiểu ⛔ dict bị bỏ im ⇒ `C3` `true` → `CG2-R1-02` **NÊN SỬA**.
3. Cha `true` ⇔ mọi con `true` ∧ ≥1 con: đúng *(false thắng null · null nếu còn null · không con ⇒ null · `C4a` thêm vào tự hiện, `C4 true`)*. Hệ quả: xoá hẳn khối con ⇒ cha vẫn `true` → `-03` GHI NHẬN.
4. Hợp đồng cũ giữ *(chỉ THÊM, bài CG1 xanh, `soi` ĐẠT)*.
5. Ba tệp ngoài phiếu *(`cua.py` · `xu_ly.py` · `chay_cua.py`)*: **đúng khuôn CG1** `tep_do` *(đường dẫn TRUYỀN VÀO — cửa ⛔ tự chọn tệp)*, bắt buộc để truyền; `lint-imports` 11/11 ⇒ ⛔ rủi ro lớp. Dây `cua`/`xu_ly` có bài *(đột biến chết)*; `chay_cua` ⛔ → `-05`.

## Đột biến *(bản sao `git archive`; mỗi phép ÁP, trả nguyên)* — 11/13 CHẾT
M1 `dat` kiểu bool · M2 `lat>0⇒false` · M3 null che false · M4 cha rỗng ⇒ true · M5 kiểu `lat_bo` · M6 `khop≠tong_o` · M7 `tong_o=0` · M9 bỏ nối `doc_cong` · M10 `cua.py` · M11 `xu_ly.py` · M12 tệp vắng ⇒ true: **CHẾT**. **SỐNG:** M8 `goi≠khoá` → `-04` · M13 `chay_cua` → `-05`.

## Việc kế
`DEV`: sửa `-01` *(tối thiểu `da_do`)* + `-02` + bài ghim `-04` · `-05`; `do_hd2.py` xuất `lat_bo` ⇒ WO riêng *(orchestrator)*. R2 chạy lại đột biến.
