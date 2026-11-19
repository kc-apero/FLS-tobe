# KQ-222 — biên bản kiểm `BG-221` *(R1 · Step 34 · DT9)*

| | |
|---|---|
| **Thuộc** | `BG-221` · `WO-220` · nhánh `isp/DT9` @ `4e49253` |
| **Kiểm bởi** | `fls-test` · 2026-11-19 *(⛔ sửa mã)* |
| **Phán quyết** | **`ĐẠT CÓ ĐIỀU KIỆN`** — **0 CHẶN · 2 NÊN SỬA · 4 GHI NHẬN** *(sổ `SO_PHAT_HIEN_ISP-3.1_DT9.md` v0.1)* |

## Cổng
| Lệnh | Đo |
|---|---|
| `pytest tests/du_lieu/test_dap_an_nen_tang.py` | 129 passed |
| `--duong-nen --cong 5445` *(1 lần, một mình)* | ĐẠT — toàn bộ tập đỏ 28 = 28 node id *(thêm 0 · bớt 0)*, chạy **3892** *(= sàn mới)*; web 3 = 3, chạy 675 |
| `lint-imports` · `kiem_tai_lieu.py` | 11 kept · 0 broken · K1–K6 ĐẠT *(349 file)* |

## Trọng tâm
1. **Tái đo độc lập** *(khoá SA chỉ-đọc, 100 % ô)*: **298.166/298.166 ô** khớp, 0 hàng thiếu/thừa, số dòng theo tháng khớp 9/9. Phép so được chứng minh cắn: đổi 1 ô ảnh ⇒ lệch 1.
2. **Tháng 2026:** **0** ô `2026…` ở cả 9 tab MID và ở cột ngày 4 tab thượng nguồn ⇒ 7/7 tháng `202603…202609` có 0 dòng ở **cả ba** sổ. Tái lập kết luận của Dev; tiêu chí `DT9-B1` đúng chữ ⛔ đạt được ⇒ `-01` NÊN SỬA (B2, orchestrator).
3. **⛔ vòng tròn:** toàn tab MID1 *(178.177 ô công thức)* + bao đóng *(OMC 15 tab · SC 7 · PS 7)*: **0** nhắc MID2/MID3, **0** vòng; 2 nhắc `CFA2` là chuỗi chữ.
4. **72 hàng SC:** tập 72/72 trùng nguồn; nhưng 70 là *chưa chia* (Σ=0), 2 là chia lệch thật ⇒ `-03`; bài ghim chỉ đếm ⇒ `-02` NÊN SỬA.
5. **PII:** 0 `@` thật · vendor 100 % `VD\d+` · 0 cột lạ; máy quét có ca phá *(email · tên người ⇒ ĐỎ)*.
6. **> 2 MB:** thêm nguyên nhân `o_loi` nhân đôi ô lỗi 25–39 % ⇒ `-05`. Công cụ chung `git diff` **0** dòng.

## Đột biến *(bản sao `git archive`)* — 14/15 CHẾT
Bỏ dòng · đổi ô · tháng 2026 · vendor tên/email · `lech_pe` 72→71 · bỏ `f==pe` · AP 7→6 tháng · nới `VENDOR_RE` · đổi ô chia · sha ảnh GI · cột Email · PM hoá 0 · `pm_chu`: **CHẾT**. **SỐNG:** đổi tên một hàng trong `lac` *(đếm vẫn 72)* → `DT9-R1-02`.

## Việc kế
`DEV`: sửa `-02`. Orchestrator: `-01` *(AP/ISP hoặc sổ kỳ 2026)*. R2 chạy lại đột biến.
