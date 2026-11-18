# KQ-162 — biên bản kiểm `BG-161` *(R1 · ISP 3.1.2 · Step 18 · F4)*

| | |
|---|---|
| **Thuộc** | `BG-161` · `WO-160` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R1)* · 2026-11-18 · `isp/F4` @ `d6a91ec` *(mã `11b4c93` + `BG-161`)* · cụm `5444` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 1 NÊN SỬA · 3 GHI NHẬN` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_F4.md`)*. AC-1…AC-5 đúng; chỗ hở là tràn ngang 390 px *(ngoài AC của `WO-160`)* |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `pytest tests/web/test_isp_f08_fx.py test_khong_ma_mau_go_tay.py test_phuc_vu.py` | `57 passed` |
| `--duong-nen --cong 5444` *(một mình)* | `KẾT: ĐẠT` · toàn bộ `12 failed · 3275 passed · 2 xfailed · 14 errors` = nền **28 = 28** node id, chạy **3303** *(mong ≥ 3303)* · `tests/web` nền **3 = 3**, chạy **674** *(mong ≥ 674)* |
| `lint-imports` | `11 kept, 0 broken` |
| `kiem_tai_lieu.py` | ĐẠT *(280 file · 2.488 bảng)* |
| `kiem_thuyet_minh.py` | `31/31 nút` ĐẠT |

## AC
| AC | Đo *(nhãn · mẫu số)* | Phán |
|---|---|---|
| AC-1 | **Chromium thật** qua `phuc_vu.py` + máy chủ thử, tab ⑥: **37** hàng `[data-thang]`, nhãn LẠC = `['202306']` *(1)*, **0** nút *(mẫu số 37 ≠ 0)* | ĐẠT |
| AC-2 | `thieu=[202408]` ⇒ đúng 1 CHẶN, vẫn 37 hàng; `trung` ⇒ 2 hàng cùng tháng, cả hai TRÙNG, ⛔ gộp | ĐẠT |
| AC-3 | tải · rỗng · lỗi `FLS-CAUHINH-CHUA-KHAI` *(0 bảng)* · có số — qua `trang_thai.js` | ĐẠT |
| AC-4 | token màu + `kiem_bang_tep` + web nền 3=3; spec §9: 7 cột, 0 nút, vùng ký ghi "chưa xây" | ĐẠT |
| AC-5 | ghim `3303`/`674` = số thu thập, `--duong-nen` ĐẠT | ĐẠT |

## Đột biến *(10, bản sao `git archive`; bài F08 + token màu)*
BỊ BẮT **9/10**: CHẶN→TRÙNG · bỏ LẠC · bỏ hàng tháng thiếu · bỏ TRÙNG · thêm nút · gộp trùng · nuốt lỗi thành rỗng · hex gõ tay *(chỉ bài token cắn)* · tắt `la_rong`.
**SỐNG 1:** lạc tự suy `< 202401` ⇒ `F4-R1-02`.

## 390 px *(Chromium thật, 37 hàng)*
`scrollWidth 475 > clientWidth 390` ⇒ **tràn ngang** *(`F4-R1-01`, NÊN SỬA)*; 1280 px: `1280 = 1280`.

## Hỏi orchestrator
Tràn 390 px: sửa ở R2 *(khuyến nghị — bọc `overflow-x:auto` + bài đo 390)* hay nhận nợ?
