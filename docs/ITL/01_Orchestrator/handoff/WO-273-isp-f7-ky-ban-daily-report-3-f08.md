# WO-273 — ISP 3.1.2 · Step 40 · F7: SCR-F08 ký bản Daily Report 3 (IX.TMP snapshot)

| | |
|---|---|
| **Trạng thái** | `MO` — viết 22/11 ~03:10 UTC; giao khi có ô trống (luật D ≤ 3 phiên) |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **FE** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/F7` |
| **Nền** | ngọn nhánh làm việc (đã gộp **F5** — `man_f08.js` SCR-F08 xem + ký tháng tỷ giá, hộp xác nhận `hop_thoai.js`; **C13** — `GET /api/fls/v1/report/snapshot/{ky}` · `POST …/{ky}/sign`, `07_API_CONTRACT` v3.26 §4i ✅) |
| **Dải phiếu** | `BG-274` · `KQ-275` (R1) · `KQ-276` (R2 cuối). Số trống kế tiếp sau dải: **277** |

## Vì sao
- ISP **Step 40 · F7** (wave W13). Khái niệm mới duy nhất: **hiển thị phiên bản có ký**. Phụ thuộc F5 ✅ + C13 ✅ (gộp 20/11). Là phụ thuộc của **I2** (Step 47).
- Đóng luôn `C13-R1-04` (sổ `SO_PHAT_HIEN_ISP-3.1_C13.md`): câu `message` của `409 FLS-CAUHINH-DA-KY` dùng chung mã với C7 còn nói "tháng IX.FX" — trên màn F08 phần ký bản phải hiện chữ đúng ngữ cảnh *bản báo cáo* (sửa ở chữ phía màn `goi_cua.js`/`man_f08.js` theo ngữ cảnh tuyến, hoặc câu BE nếu sửa nhỏ và có bài — ghi lựa chọn vào BG; ⛔ đổi mã lỗi).

## Spec phải đọc
| Tệp | Mục |
|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | **Step 40** (· Step 37 F5 · Step 36 C13) |
| `02_BA/06_SCREEN_SPEC.md` §9 `SCR-F08` (+ dòng 1504 "Ký bản Daily Report 3") · `02_BA/13_THUYET_MINH_MAN_HINH.md` (mục F08) · `02_BA/07_API_CONTRACT.md` §1 + §4i hai dòng `report/snapshot` | hợp đồng màn + tuyến |
| `BG-258` (C13) · `BG-254` (F5) · sổ `SO_PHAT_HIEN_ISP-3.1_C13.md` · `…_F5.md` | hành vi tuyến, khuôn hộp ký, phát hiện còn mở |
| `fls/web/tep/man_f08.js` · `hop_thoai.js` · `goi_cua.js` · `tests/web/test_isp_f08_ky_pg.py` | khuôn dùng lại |
| `CLAUDE.md` | Đ1–Đ5 |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (F7-F1) | kỳ có **2 phiên bản** (bản 1 đã ký) trong kho test ⇒ F08 hiện danh sách phiên bản (phiên bản · checksum rút gọn · trạng thái · người ký · ngày) đọc từ `GET …/snapshot/{ky}`; bấm 'Ký bản' ⇒ hộp xác nhận (`hop_thoai.js` của F5, ⛔ hộp mới) ⇒ `POST …/sign` ⇒ **cả hai** 'đã ký', checksum **khác nhau**, bản 1 giữ nguyên người ký/ngày cũ | tích hợp headless (pg) `tests/web/test_isp_f08_ky_ban_pg.py` | chưa có màn |
| AC-2 | kỳ chưa có bản ⇒ `ban: []` ⇒ chữ trạng thái rỗng có tên (⛔ bảng trống im lặng), nút ký ẩn/khoá; bản mới nhất đã ký ⇒ nút khoá | headless | — |
| AC-3 | huỷ ở hộp xác nhận ⇒ **đúng 0** POST (đếm request mạng); bấm kép nhanh ⇒ **đúng 1** POST | DOM | — |
| AC-4 | lỗi `409` (chữ ngữ cảnh *bản báo cáo* — đóng `C13-R1-04`) · `404` · `400` · `401` · lỗi mạng ⇒ hiện chữ tiếng Việt, ⛔ treo nút, ⛔ mã thô; `test_goi_cua_phu_het_ma_loi.py` xanh | pytest web | — |
| AC-5 | ⛔ gửi `actor` trong thân (bắt request body) — người ký hiện trên màn lấy từ phản hồi tuyến (THẺ) | DOM/tích hợp | — |
| AC-6 | phím: Esc/Enter theo spec §9, tiêu điểm trả về nút sau khi đóng hộp; `kiem_thuyet_minh.py` ĐẠT (cập nhật thuyết minh F08) | công cụ + DOM | — |
| AC-7 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + `MONG_PYTEST_WEB` = thu thập thật + bài ghim cùng commit; `--duong-nen` ĐẠT (tập đỏ 28 = 28 · web 3 = 3) | `--duong-nen` | — |

## Ràng buộc
- ⛔ xem nội dung báo cáo từng ô · ⛔ PDF · ⛔ huỷ ký · ⛔ phân quyền theo vai (O11) · ⛔ tuyến BE mới (ngoài sửa chữ `C13-R1-04` nếu chọn phía BE). Ghi kho THẬT: `KHONG` (chỉ kho test).
- Dữ liệu thử 2 phiên bản: đưa vào kho test bằng hàm mức repo của C13 (⛔ tuyến ghi thứ ba — `BG-258`).
- Tự chụp màn hình trước/sau ký (deviceScaleFactor 1) để đối chiếu spec — mô tả trong BG, ⛔ commit ảnh.
- Mỗi bài mới ĐỎ trước (ghi lệnh + exit code vào BG). `--duong-nen` MỘT lần cuối phiên (luật C).
