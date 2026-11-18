# KQ-149 — biên bản kiểm `BG-148` *(R1 · ISP 3.1.2 · Step 19 · DT8)*

| | |
|---|---|
| **Thuộc** | `BG-148` · `WO-147` |
| **Kiểm bởi** | `fls-test` · 2026-11-18 *(cụm PG 5437 · `isp/DT8` @ `d011246`)* |
| **Phán quyết** | `ĐẠT` *(0 CHẶN)* — **4 NÊN SỬA** cần đóng ở vòng sửa trước R2 · 8 GHI NHẬN ⇒ backlog |

## Cổng chạy lại
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/du_lieu/test_dap_an_gi.py` | 28 passed | 28 passed | ✅ |
| `pytest test_anh_cau_hinh · test_dap_an_406 · test_dong_bang_sheet` *(DT2…DT5, byte)* | 367 *(cả thư mục)* | 209 passed | ✅ |
| `lint-imports` | 11 kept, 0 broken | 11 kept, 0 broken | ✅ |
| `kiem_tai_lieu.py` | ĐẠT 255 file | ĐẠT **256** file · 2356 bảng *(+sổ mới)* | ✅ |
| `dung_moi_truong_isp.sh --duong-nen --cong 5437` *(một mình)* | KẾT: ĐẠT · 3173 bài | KẾT: ĐẠT · chạy **3173** bài *(12 failed + 14 errors + 2 xfail = 28 node id = đường nền, thêm 0 · bớt 0)* · `tests/web` 667 *(3 đỏ = đường nền)* | ✅ |

## Bảng AC
| AC | Đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|
| AC-1 | 36 dòng; nhãn ≠ thường = 5 *(Max 12 · VD341 6 · VD444 8 · VD428 3 · VD62 1 · thường 6 — số **dòng** mỗi nhãn)*; khớp nguồn 252/252 ô. Nguồn còn hàng 40–45 ⇒ `-01` | ĐẠT *(+`-01`)* |
| AC-2 | Σ chia = O/P đo lại độc lập: lệch 0 trên 253 hàng số *(ảnh phủ 11)*; MONG khai, tập rỗng ⇒ ĐỎ; vế PM `0/77` ô ≠ 0 ⇒ `-02` · phạm vi `-03` | ĐẠT *(+`-02` `-03`)* |
| AC-3 | `#N/A` 176 · `#DIV/0!` 308 khớp nguồn, ghi nguyên, ghim. Cột `U`/`V` ⛔ mang; `#REF!` = 0 ở nguồn ⇒ `-04` | ĐẠT *(+`-04`)* |
| AC-4 | 0 cột cấm · 0 ký tự `@` · cổng ∈ tập đo trên 2.856/1.463 hàng đầy đủ; ca phá `vendor`/`itl_id` thiếu ⇒ `-07` | ĐẠT |
| AC-5 | khuôn riêng ×4; `so!` chỉ THÊM; DT2/DT3/DT4 tái tạo đúng từng byte 209/209 | ĐẠT |
| AC-6 | sàn 3141→3173 + bài ghim cùng commit; đột biến hạ sàn bị cắn | ĐẠT |

## Đối chiếu nguồn *(khoá SA chỉ-đọc, 100 % ô, ⛔ mẫu 20 %)*
`IX.VEN` 252 · `MID1` 19.992 · `MID2` 8.778 · `MID3` 154 ⇒ **29.176 ô · lệch 0**. Bản thô `/tmp/r1_dt8/`, ⛔ commit.

## Đột biến *(17 trên bản sao `git archive`)*: **9 cắn · 8 sống**
Sống: bỏ chiều *thừa* `ix_ven` · bỏ vế PM · bỏ chặn tập rỗng · cổng `itl_id` · `VENDOR_RE` MID2 · hàng đệm · `LOI_MONG` chiều thừa · `_la_loi`→`startswith('#')` ⇒ `-02` `-05…-09`.

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `DT8-R1-01` | NÊN SỬA | `ix_ven.py` · nguồn `M:S` hàng 40–45 | VD341 `No` 7–12 liền hàng 39; ảnh 1–6, MID1 tới 12 | BA/orch |
| `DT8-R1-02` | NÊN SỬA | `gi_mid3.py` vế PM | `0/77` ô PM ≠ 0; bỏ vế PM ⇒ 189/189 xanh | DEV |
| `DT8-R1-03` | NÊN SỬA | `gi_mid3.py` `chuan_bi` | ảnh 11/253 hàng số; 242 hàng chi tiết ngoài ảnh | orch |
| `DT8-R1-04` | NÊN SỬA | `gi_mid1/2.py` cột `U`/`V` | `U` MID1 5.390/6.336 lỗi · MID2 1.274/1.274 · `#REF!` = 0 | DEV/BA |
| `-05…-12` | GHI NHẬN | xem sổ | đột biến sống · mô tả `dem` · `×7` · quét PII vacuous | backlog |

Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT8.md` *(v0.1)*.

## Bài thử mới
Không thêm bài vào `tests/nghiem_thu/` *(vai KIỂM ⛔ sửa mã; đột biến chạy trên bản sao, trả nguyên)*.

---
Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EC3zCUgqhkiHAdLXvteBTz
