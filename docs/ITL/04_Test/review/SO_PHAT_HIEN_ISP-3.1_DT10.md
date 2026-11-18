# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `DT10` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.1 · **Ngày:** 2026-11-18 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-198`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 27 · DT10 · `WO-196` · `BG-197` · nhánh `isp/DT10` @ `e3fe912`

> **Luật của sổ:** sổ **chỉ THÊM**; vòng sau chỉ đổi ô `Trạng thái` của hàng đã có và thêm hàng mới.
> Lớp: **A1** lỗi mã · **B1** lệch spec / thiếu bài · **B2** spec/ISP/hợp đồng sai — chuyển orchestrator. Mức: **CHẶN** · **NÊN SỬA** · **GHI NHẬN**.
> ⛔ **Riêng tư:** sổ chỉ ghi số đếm, địa chỉ ô và tên cột — ⛔ giá trị ô. Bản đọc thô nằm ở scratchpad của phiên, ⛔ commit.

## Số đo nền của R1 *(nhãn đếm gì — Đ4)*

| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| Đọc lại nguồn `19NNTb…EU2g` bằng khoá SA chỉ-đọc `UNFORMATTED_VALUE`, **so TỪNG Ô bằng script riêng** *(⛔ dùng khuôn)* — ATL `B7:BK1110` hàng 8…1030 | 829 hàng × 62 cột = **51.398 ô** | lệch **0** |
| …`ix_drv` ba bảng `D:O` | 21 dòng × 12 = **252 ô** *(238 số + 14 rỗng GI 202501)* | lệch **0** |
| …`nb_le` BALANCE hàng 5–308 | 304 × 12 = **3.648 ô** | lệch **0** |
| …`nguon_noem`: công thức `FORMULA` `D27:O34` · tử HR `A4289:Q4300` | **96** công thức · **84** tử | khớp **96/96** · **84/84** |
| Tái chạy khuôn trên bản thô dựng từ lần đọc của TÔI | `dong` + `phu` của 2 ảnh | **giống từng byte**; chỉ `nguon`/`cach_doc`/`checksum` khác *(chuỗi nguồn khác nhau)* |
| 146 ô thiếu — nguồn thật sự thiếu | 384 − 238 | CMN: **0** hàng nhãn `CMN` ở `A1:Z35` · GI 202501: dòng `TOTAL` MID3 = **11** *(202502…202512)* ⇒ công thức `iferror` ⇒ rỗng · NB: ma trận **From × To** *(LE)* ⇒ không khoá CDT1 |
| Mẫu số 34 tổng Σ7 CDT1 | 34 *(NOEM 12 + GI-PE 11 + GI-PM 11)* | lệch > 1e-9: **0** |
| `P:Z` hàng 1–35 | 385 ô | khác rỗng: **0** |
| ATL đếm hàng khác rỗng theo cột *(`-` = rỗng)* | 57 cột | 33 cột = **824** · 24 cột = **816** *(khớp `MONG_KY`)* |
| ATL lỗi | 161 | `y2024_y` 77 `#N/A` · `y2024_q1…q4` 21 `#VALUE!` ⇒ khớp; KIỂM 80 hàng: **560** `#VALUE!` · **1.997** bool; gạch `-` **120** |
| PII | 2 ảnh | `@` = **0** · "email" = **1**/ảnh *(câu khai)* · cột `Email Address` = 0 |
| Công cụ chung | `tools/dong_bang_sheet.py` | sha256[:16] `ae917adbf80b1c14` · `git diff fba4849..HEAD` = **0** |
| Đột biến *(bản sao `git archive`)* | **20** | **20 cắn · 0 sống** *(10 ảnh · 7 bản thô qua khuôn · 3 khuôn)* |
| `--duong-nen --cong 5437` *(một lần, một mình)* | 3588 bài | ĐẠT: `12 failed · 3560 passed · 2 xfailed · 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** · thêm 0 · bớt 0 · chạy 3588 |
| `lint-imports` · `kiem_tai_lieu` | — | **11 kept / 0 broken** · ĐẠT *(K1–K6)* |

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `DT10-R1-01` | DT10 | R1 | B2 | GHI NHẬN | `BG-197` §DT10-B1 *(câu "BALANCE 304 hàng … 16 From × 19 To")* | Nhãn Đ4 sai: đo lại ma trận NB = **16** `From` × **19 hàng** mỗi `From` = 304; số `To` khác nhau = **49** *(`OTH-LE-…` · `OTH-LE-V-…` · `All`)*, ⛔ 19. Ảnh + bài đúng *(`test_dap_an_atl.py:224` "16 From × 6 To loại V")*; chỉ lời BG sai. | Sửa chữ BG ở lần ghi sau; ⛔ đổi ảnh. | Bài đếm `To` khác nhau = 49 nếu cần | Mở |
| `DT10-R1-02` | DT10 | R1 | B2 | GHI NHẬN | `tests/fixture/cau_hinh/cdt_correct.json:59` ↔ `ix_drv` `o_thieu` *(CMN)* | **Đồng ý** với BG: AP §3.2.2 "8 CDT1" ⇒ 7 + CMN gộp SHQ1 *(CDT Correct dòng `CMN_Management` → `SHQ1`, đo)*. Nhưng ảnh ghi một câu hai ý: "CMN gộp SHQ1 … ở NOEM rơi vào phần dư của SHQ2" — headcount CMN (`A4300`, 5→4 người) **không** vào ô `SHQ1` mà vào `=100% − Σ6` ⇒ driver NOEM-SHQ1 **không gồm CMN** dù GL gộp CMN vào SHQ1. Đây là lệch ngữ nghĩa cho H12 *(AL.KEY)*, ⛔ lỗi ảnh. | Orchestrator chốt: AP ghi "7 + CMN"; H12 quyết CMN vào SHQ1 hay SHQ2 ở NOEM. | — | Mở |
| `DT10-R1-03` | DT10 | R1 | B1 | GHI NHẬN | `tests/du_lieu/test_dap_an_atl.py:332` | Bài AC4 `…ghim_phan_bo` đọc `loi_mong`/`loi_theo_cot` **khai trong ảnh**, ⛔ đếm lại từ `dong`. Đột biến M10 *(đổi 1 ô `#N/A` thành `0`)* chỉ bị **checksum** cắn *(1 bài đỏ)*; luật `DT5-R1-04` vẫn giữ nhờ checksum, nhưng bài ghim phân bố không tự đo. | Thêm 1 phép đếm lại ô lỗi từ `anh["dong"]` so `loi_mong`. | — | Mở |
| `DT10-R1-04` | DT10 | R1 | A1 | GHI NHẬN | `tools/dong_bang_sheet.py:866` | `KeyError` đo **thật**: bỏ khoá `y2026_m12` khỏi `LOI_MONG` ⇒ khuôn chạy ĐẠT nhưng crash ở dòng tổng kết, **exit 1 *(trùng mã cổng ĐỎ)*** *sau khi ảnh đã ghi*. Hướng **an toàn** *(đỏ giả, ⛔ xanh giả)*; khuôn `atl` đã khai đủ 57 cột. Mức: thấp. | Bước nhỏ riêng: `anh["loi_mong"].get(c2, 0)` — ⛔ sửa ở bước này *(sha ghim)*. | Bài khuôn thiếu khoá ⇒ lỗi có tên | Mở |
| `DT10-R1-05` | DT10 | R1 | B1 | GHI NHẬN | `tools/khuon_dong_bang/atl.py` ① *(chọn hàng)* · `BG-197` §AC-3/4 | Nhãn Đ4: "**829** hàng" = hàng có ≥ 1 ô **khác rỗng kể cả `-`**; trong đó **5** hàng *(sheet 998–1002)* chỉ có `-` *(0 ô số)* ⇒ hàng **có giá trị** thật = **824**. Khớp `MONG_KY` *(824)*, ⛔ sai số; chỉ nhãn "829 hàng dữ liệu" thiếu chữ. | Ghi "829 = 824 hàng có giá trị + 5 hàng chỉ gạch" ở `ghi_chu`. | — | Mở |

## Ghi chú kiểm *(⛔ phát hiện)*
- Tập con `test_dap_an_atl.py` + `test_dung_moi_truong_isp.py` chạy riêng đỏ **1** bài `S0_R3_02` *(đếm bài THU THẬP toàn cây)* — đúng thiết kế, `--duong-nen` toàn bộ xanh.
- Đột biến đầu tiên của tôi *(bớt hàng ATL)* trúng hàng **rỗng sẵn** ⇒ exit 0 *(đột biến vô hiệu, lỗi của tôi)*; làm lại trên hàng sheet 393 ⇒ ĐỎ `828 ≠ 829 · thiếu 57`.
- 20 đột biến: ảnh *(sửa 1 ô driver · sửa 1 ô ATL · bớt 1 hàng ATL · lấp ô mong-thiếu · `nam=2026` · `ngoai=1` · thêm ô `y2026_m12` · cột `Email Address` · `loi_mong` 77→76 · `#N/A`→`0`)* · bản thô *(mất 1 ô NOEM ⇒ ĐỎ · tiêu đề NOEM 2026 ⇒ TỪ CHỐI exit 2 · lấp GI 202501 ⇒ ĐỎ · ô `P:Z` ⇒ ĐỎ · bớt hàng ATL ⇒ ĐỎ · sửa+thêm ô ATL ⇒ ĐỎ · tiêu đề ATL 2027 ⇒ exit 2)* · khuôn *(`MONG_KY` 824→825 ⇒ ĐỎ thiếu 14 · bỏ CMN GI_PM ⇒ ĐỎ thiếu 12 · `LOI_MONG` thiếu khoá ⇒ `KeyError`, `-04`)*.
- Kích thước ATL 1.571.277 B: nguyên nhân khai ở BG khớp — JSON thụt dòng, 829 + 80 hàng × 62 khoá lặp mỗi hàng, **10.693** ô số ≥ 15 ký tự; < 2 MB.

## Changelog
- **v0.1** *(2026-11-18, `fls-test` R1 của `DT10`, `KQ-198`)*: khởi tạo — **5** phát hiện `DT10-R1-01…05` *(**0 CHẶN** · **0 NÊN SỬA** · 5 GHI NHẬN: B2 ×2 · B1 ×2 · A1 ×1)*. Nguồn khớp **100 %** *(51.398 + 252 + 3.648 ô)*; đột biến **20/20 cắn**.
