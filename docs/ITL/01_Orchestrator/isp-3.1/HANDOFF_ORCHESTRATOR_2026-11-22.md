# HANDOFF — orchestrator ISP 3.1.2 · 2026-11-22 *(tổng kết ngày)*

> **Dành cho:** chủ, và phiên orchestrator tiếp quản.
> **Kế thừa** `HANDOFF_ORCHESTRATOR_2026-11-20.md` (§2 quyết · §6 staging · §7 bẫy vẫn đúng) — tệp này **thay** nó ở chỗ khác nhau. Nhật ký đầy đủ từng lượt: `TIEN_DO.md` (các hàng 2026-11-22).

---

## 0. Câu mở đầu để dán khi quay lại
```
Bạn là orchestrator của ISP 3.1.2 dự án FLS (repo kc-apero/FLS-tobe). Đọc
docs/ITL/01_Orchestrator/isp-3.1/HANDOFF_ORCHESTRATOR_2026-11-22.md trên nhánh
claude/bold-galileo-zukpaf (mục "Trạng thái cuối" trước), dùng skill
isp-orchestrator · isp-gop-buoc · fls-moi-truong, rồi làm §4 "Việc kế".
Trả lời chủ bằng tiếng Việt; mọi câu hỏi kèm khuyến nghị.
```

## 1. Một màn hình
| | |
|---|---|
| **Tiến độ (đếm THẬT, xem §3)** | **46/48 Step ISP đã gộp.** Còn **H14** (R2b ĐẠT — chờ chủ ký 605) · **I2** (Step cuối — R2 cuối đang/đã chạy, xem "Trạng thái cuối") |
| **Gộp hôm nay** | DT7 · DT12 · DT11 · F7 · H8 · H15 · H12 · C10 · I1 · H13 (10 Step) + bổ sung DT7b · C13b · DT13 |
| **Sàn** | `MONG_PYTEST_TOAN_BO=4772` · `MONG_PYTEST_WEB=690` · tập đỏ nền **28** · web **3** (sau gộp DT13) |
| **Đường nền gần nhất** | sau gộp DT13 `dcee514`: `KẾT: ĐẠT` — 28 = 28 · chạy 4772 · web 3 = 3 · 690 |
| **Số phiếu trống kế tiếp** | **324** |
| **Chi phí phiên con hôm nay (ước)** | ≈ 150–170 USD (Opus engine: H8 14,6 · H12 9 + 9,4 · H13 6,2 · H14 10,3 + 6,5 + sửa tích hợp · I2 6,6 + 3,5 …; Sonnet review/sửa/dữ liệu ≈ 0,7–5,6 mỗi phiên) |

## 2. Quyết của chủ HÔM NAY — ⛔ hỏi lại
| Giờ (UTC) | Quyết |
|---|---|
| ~02:20 | DT7: dùng sổ `[COPY] Report I General Ledger \| P&L Report` làm nguồn 6 tab PLA · chạy tiếp orchestrator |
| ~10:05 | **Ký BẬT luật phân bổ IX.ALR năm 2025 giống AS-IS** (chờ R1 H12) ⇒ đã làm: `ix_alr_2025_bat.json` v1, người ký `KhanhCQ` |

Quyết của orchestrator đáng nhớ: DT12 phương án (a) · DT11 đóng băng thêm 607–609 + 615 · che 7 nhãn `PO USD_<tên>` ở ảnh 615 · tên viết tắt đứng riêng GIỮ (quyết chủ 11/09) · 72 cột 2024 của 416 = lệch AS-IS (⛔ chép lỗi) · cổng HD1 phán 26 kỳ · C10 bảng nối tên driver phía config · F7 tải lại trước POST · D1 ngoại lệ có giới hạn cho phép sửa AL tối thiểu để chặn tỷ giá.

## 3. ⛔⛔ Đính chính đếm — C10 BỊ RƠI (bài học)
`HANDOFF_ORCHESTRATOR_2026-11-19.md` ghi "34/48" nhưng bảng của chính nó chỉ có 33; **C10** vắng ở cả "đã gộp" lẫn "còn lại" ⇒ mọi "x/48" từ 19/11 lệch +1. Phát hiện 22/11 nhờ phiên H12 ("C10 ⛔ có trong cây"), mở `WO-295`, làm + gộp trong ngày. **Luật:** số "x/48" dựng lại từ bảng 48 Step × bằng chứng (commit gộp / quyết chủ), ⛔ cộng dồn từ lượt trước.

## 4. Việc kế (theo thứ tự)
1. **Đọc "Trạng thái cuối"** + `list_sessions children` — R2 cuối I2 (`KQ-318`).
2. **H14 — chờ chủ ký "605 DỪNG có tên"** (khuyến nghị: KÝ — tab nguồn `[FS1][PLA5]` đã xoá khỏi sổ, 0 ứng viên; tái lập 605 bằng `sign_off_dau_vao` = vòng tròn, đã có rào). Có chữ ký ⇒ phiên sửa NHỎ H14: thêm `DUNG_KY["605"]` có tên người ký + ngày (⛔ chuỗi bất kỳ — `H14-R2-02`) ⇒ R2b nhẹ ⇒ gộp ⇒ **47/48**.
3. **I2 — điều kiện MERGE của ISP** (khác điều kiện xong bước): (a) H14 gộp trước; (b) **chủ chạy lại trên máy `fls-pg-1`** (lệnh §6); (c) **ThuongCT ký** (O6). Đủ ⇒ gộp ⇒ **48/48**.
4. Bước dữ liệu còn mở (không chặn ISP): HR DR2 (610 `hr` 1.537 ô) + By NOEM (`[H1.2026][2025]H1000 I HR Report`, soát PII) · luỹ kế FS1 các tháng sau Sign off · Raw Data Management / Daily Transactions của 615.
5. Backlog GHI NHẬN các sổ `SO_PHAT_HIEN_ISP-3.1_*.md` · errata v3.1.3 (ISP sai số kỳ/sổ: DT7 sổ P&L · DT12 26 kỳ · H15/I1 26 kỳ ⛔ 23 · C10 bị rơi · ISP H12 "ATL = đáp án cờ tắt" sai).
6. **Staging** — vẫn chờ chủ chạy `tools/staging/01_dung_staging_gcp.sh` và gửi BÁO CÁO (HANDOFF 20/11 §6). Bài e2e HD2 (I2) là bài sẽ chạy trên staging sau bước 03.

## 5. Câu hỏi mở cho chủ (kèm khuyến nghị)
| # | Câu | Khuyến nghị | Chặn? |
|---|---|---|---|
| 1 | Ký "605 DỪNG có tên"? | **Ký** | **Chặn H14 → I2** |
| 2 | FS3 nghĩa là gì (BA)? Sổ ghi "mức tin cậy cao nhất (PI&PM; Finance&Non-Finance) cho Audits/DD" — engine hiện dựng `FS1_FS2_gop`, FS3 DỪNG có tên | BA định nghĩa | ⛔ |
| 3 | D3: giữ By GI = PE (khai `lech_D3` 3.099 ô WP-C5a) hay đổi theo AS-IS (tỉ lệ GI MID3)? | Giữ, xem lại khi có số sau DT13 | ⛔ |
| 4 | CHECK IX.PL đỏ có chặn đóng sổ không? (29 kỳ ATL; DR 607/609/610 hàng trăm ô) | Chưa chặn ở giai đoạn này | ⛔ |
| 5 | PII: nhãn `R \| <số>_PO USD_<tên>` còn ở `02_BA/Artifacts/Ket-qua-Phan-loai-4-loai-o.md` (dòng 83 · 91 · 92) + commit `34a119c` nhánh DT11 đã push — che + mở rộng `quet_pii_repo`? viết lại/xoá nhánh remote (cần force — chủ quyết)? | Che + mở rộng máy quét | ⛔ |
| 6 | DT12-R1-05: đóng băng lại ảnh Manual input 2026-03 (lệch sổ hiện tại 6.294/16.184 ô)? | Có | ⛔ |
| 7 | Có cần ảnh COM theo khối CDT để đo PL5 đủ khối? (DT13 đã đóng băng `noem_com_cdt`) | Đã làm phần lớn — xác nhận | ⛔ |

## 6. Lệnh chủ chạy lại I2 trên máy (`fls-pg-1`, chỉ đọc kho `fls`) — trích `BG-316`
```powershell
docker start fls-pg-1                                    # ⛔⛔ KHÔNG `docker compose down`
$env:PG_DSN='postgresql://fls:fls@localhost:5433/fls'
$env:PG_DSN_TEST='postgresql://fls:fls@localhost:5433/fls_test'
$env:PYTHONUTF8='1'
.venv\Scripts\python.exe -m pytest tests/tich_hop/test_hd2_xuyen_suot.py -p no:cacheprovider
```
- Chạy trên nhánh `claude/bold-galileo-zukpaf-isp/I2` (hoặc nhánh làm việc sau khi gộp H14 + I2 nếu orchestrator đã gộp thử).
- **Mong:** `28 passed` · thiếu Chromium ⇒ `27 passed, 1 skipped` = chấp nhận được. Bài chỉ DROP/CREATE kho `fls_test` + `fls_test_i2`, ⛔ ghi kho `fls`, ⛔ cần `FLS_CHO_GHI_THAT`.
- Gửi orchestrator: dòng tổng kết pytest + (nếu đỏ) tên bài đỏ.

## 7. Bẫy / bài học mới hôm nay
| Bẫy | Cách chặn |
|---|---|
| Đếm "x/48" cộng dồn ⇒ C10 rơi 3 ngày | dựng lại từ bảng 48 × bằng chứng mỗi lần báo |
| Dấu `\|` trần trong ô bảng (kể cả `\|x\|` trị tuyệt đối) — cắn 5 lần hôm nay (sổ DT12 · WO-277 · WO-291 · sổ H12 · BG DT13) | lệnh nối dừng khi `kiem_tai_lieu` ĐỎ: `… \|\| { echo DOCS-DO; exit 1; }`; prompt phiên con nhắc rõ |
| `--duong-nen` đỏ do bài đua chập chờn có sẵn (C13 `dua_ban_ky` đọc phiên bản sau khi nhả khoá) | đo dưới tải vs rảnh trên ngọn remote + HEAD; diff vùng mã; chạy lại MỘT lần; mở bước sửa gốc (C13b) |
| Cụm PG 5433 tắt giữa lượt (container khởi động lại — 3 lần hôm nay) | `pg_isready` + vòng bật lại skill `fls-moi-truong` §2 trước mỗi gộp |
| Gán lớp lệch bằng quy tắc khối × năm làm cổng xanh giả (H12) | lớp phải đo bằng truy ngược thật; R1 lấy mẫu ≥ 20 ô mỗi lớp |
| "Đầu vào" trùng y hệt đáp án (DT13 `sign_off_dau_vao` = 605; `ccr_daily_report_2` ≈ 610) | rào `DAU_VAO_CHO` / `CAM_CHO` + bài đỏ khi vi phạm; tách đếm `khop_chep` / `khop_tinh` |
| Cổng `true` khi một đáp án ô so = 0 (H14 605/615) | Đ5: ⛔ đo được ⇒ `None`/ĐỎ có tên; chỉ ngoại lệ có chữ ký chủ |
| Tăng tốc ③ (dựng trên nhánh chưa gộp) ⇒ lỗi tích hợp khi nhánh nền đổi (H14 thiếu sửa H13; I2 thiếu sửa H14) | R2 luôn trên cây gộp thử; nhắn phiên phụ thuộc gộp lại ngọn mới |

---

## Trạng thái cuối
*(lượt kiểm cuối 23:05 UTC 22/11)* — **mọi phiên con đã DỪNG**; orchestrator **⛔ còn hẹn giờ** (chờ chủ).

**I2 — R2 cuối ĐẠT** (`KQ-318` @ `b978030`; 0 CHẶN · 0 NÊN SỬA · 4 GHI NHẬN): D1 bỏ ký 202510 ⇒ **0/11** gói ra số, 11/11 `FX_CHAN 202510`; bỏ ký 202503 ⇒ 0/11; 15 cổng liên quan `dat = false` có chữ; ký lại ⇒ 11 gói khớp `hd2_cong.json`, 0 lệch. `fls/` 0 tệp đổi (chặn tỷ giá ở `tools/do_hd2.py`: `FxKho` · `ty_gia_kho` · `kiem_fx_thang` · `chay_goi`); đủ ký ⇒ `--goi WP-C4a/b/c --ghi` 0 byte đổi; `fx_cua` ở mã sản phẩm. Lệnh máy chủ bản cloud tương đương **28 passed**. F03 Chromium thật: đủ ký C2/C3/C4 có số, C5 "KHÔNG ĐO ĐƯỢC" (605); bỏ ký ⇒ 4 thẻ đỏ có `FX_CHAN`. Cây gộp thử (nhánh làm việc + H14 + I2) sạch, 4.871 bài, `--duong-nen` 28 = 28 · web 3 = 3. GHI NHẬN: `--ghi` ghi đè khối ĐỎ · D1 chỉ chặn tháng gói đọc (bỏ ký 202607 ⇒ 3/11) · C4 ⛔ nhạy giá trị tỷ giá · lời BG về `FLS_*`.

**Nhánh chờ gộp (cả hai XONG kỹ thuật):**
| Bước | Ngọn | Điều kiện còn lại (CHỦ) |
|---|---|---|
| **H14** · Step 46 | `…-isp/H14` @ `854550b` (R2b `KQ-323` ĐẠT 0 · 0) | chủ **ký "605 DỪNG có tên"** ⇒ phiên sửa nhỏ thêm `DUNG_KY["605"]` (tên người ký + ngày) ⇒ R2b nhẹ ⇒ gộp ⇒ **47/48** |
| **I2** · Step 47 | `…-isp/I2` @ `b978030` (R2 `KQ-318` ĐẠT 0 · 0) | H14 gộp trước · **chủ chạy lại trên `fls-pg-1`** (§6, mong `28 passed` / `27 passed, 1 skipped`) · **ThuongCT ký** (O6) ⇒ gộp (gộp lại nhánh làm việc + `--duong-nen`) ⇒ **48/48** |

**Số phiếu trống kế tiếp: 324.** Câu hỏi chủ: §5 (câu 1 chặn).
