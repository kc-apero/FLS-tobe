# KQ-337 — R2 cuối `WO-334` + `WO-352` / `BG-335` §10–§11 *(staging bước 05: nạp dữ liệu thật)*

| | |
|---|---|
| **Thuộc** | `BG-335` §10 *(vòng sửa sau `KQ-336`)* · §11 *(`WO-352`)* |
| **Kiểm bởi** | `fls-test` · 2026-11-24 · phiên cloud, cụm PG `5445` |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA · 4 GHI NHẬN** *(`NAP-R2-01…04`, sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_NAP.md` v0.2)* |
| **Cây kiểm** | `isp/STG-NAP` @ `9b2335b` *(= sha mong ✅)*. Cây gộp thử `thu/STG-NAP` @ `460a0c2` = `origin/claude/bold-galileo-zukpaf` @ `d0bb8bf` ⊕ `9b2335b` *(⛔ đẩy)* |
| **Kho thật** | `KHONG_CHAM` — cụm `5445`, kho trống; ⛔ GCP · ⛔ `fls-pg-1` · ⛔ ghi sheet. Live: SA chỉ-đọc có trong container; chỉ SỐ ĐẾM |

## Xung đột khi gộp thử *(ghi lại, gộp tay)*
3 tệp: `08_CHANGELOG_RELEASE.md` *(giữ CẢ HAI hàng)* · `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` *(sàn pytest: nhánh làm việc 5126 ↔ NAP 5128 ⇒ **đặt = `pytest --collect-only` cây gộp = 5172**, web 690; ⛔ cộng tay; script + bài ghim cùng commit thử)*. Đo mẫu số: 5126 + (5128 − 5082) = 5172 = thu thập thật ✅.

## Cổng *(tự chạy, dán số)*
| Lệnh | Mong | Đo | |
|---|---|---|:-:|
| `--duong-nen --cong 5445` *(MỘT lần, một mình)* | tập đỏ 28 = 28 · web 3 = 3 | `12 failed · 5144 passed · 2 xfailed · 14 errors` = **28 = 28** node id *(thêm 0 · bớt 0 · XFAIL 2)* · chạy **5172 ≥ sàn 5172** · skipped 0 · deselected 0; web **3 = 3**, chạy 690 ≥ 690. 2 bài `STG-R1-02` **hết** ✅ | ✅ |
| `lint-imports` | 11 kept | **11 kept, 0 broken** | ✅ |
| `kiem_tai_lieu` | ĐẠT | `✅` *(529 tệp · 3.112 bảng · 993 ô ngày · 104 mã QĐ)* | ✅ |
| `soi_bang_tuyen` | 0 lệch | **49/49** tuyến khớp SQL | ✅ |
| `quet_pii_repo` | 0 | **0 chỗ số TK cá nhân · 0 tệp** | ✅ |

## `NAP-R1` đóng **8/8** *(1 CHẶN + 7 NÊN SỬA)*
| Mã | Đo ở R2 *(nhãn đếm gì)* | |
|---|---|:-:|
| `-01` CHẶN | Live `--kiem` `2026-11-24`: khối `ⓑ` in **từng kỳ** trong **23** kỳ chốt: **13** bằng · **9** thấp *(2025-06 −2 · 07 −3 · 11 −2 · 2026-02 −1 · 03 −2 · 04 −1 · 05 −1 · 06 −2 · 07 −3)* **Σ −17** · **1** cao *(2026-08 +237)* · 0 kỳ mất hết dòng · kỳ mới 2.414. Σ −17 tự cộng lại đúng; số **−19** ở `KQ-336` là **lỗi cộng của Test**, nay đính chính *(`−17`)*. Vế "kỳ chốt ↔ số cũ" **được giao**, lệch có tên. Đột biến M9 *(đảo thấp/cao)* ⇒ `test_so_theo_ky_pure…` ĐỎ. ⚠ Theo quyết chủ *(nguồn sống là chuẩn)* khối **không có `mong`** ⇒ không ĐỎ — ghi `NAP-R2-04` | ✅ *(theo quyết chủ)* |
| `-02` | 4 đột biến sống **nay CHẾT 4/4**: M7 *(Σ-kho Mapping `mong = kho`)* · M10 *(PM `mong = kho`, 2 chỗ)* ⇒ `test_DOI_CHIEU_kho_RONG…` ĐỎ · M9 ⇒ ĐỎ · M11 *(mẫu số Mapping = hằng 73)* ⇒ `test_BON_BUOC_tong_hop…` ĐỎ | ✅ |
| `-03` | Đột biến bỏ nhánh "mẫu số 0 ⇒ ĐỎ có tên" ⇒ `test_RIENG_TU_mau_so_PM_kho_bang_0…` ĐỎ. Đ3: mẫu số `fls_pm_line` ở kho scratch = **0** ⇒ phép `Email Address = 0` in `ĐỎ có tên`, ⛔ ĐẠT; hàng `mẫu số ≠ 0` ĐỎ khi 0 *(bài chứng minh cả hai chiều)* | ✅ |
| `-04` | Live stdout: **0** dòng ≥ 9 chữ số liền *(`grep -cE '[0-9]{9,}'` trên 140 dòng)*. Đột biến `chi_tiet_loai=True` ⇒ `test_STDOUT_o_loi_mang_chuoi_12_so…` ĐỎ. ⚠ lớp che ≥ 6 chữ số **sống** ⇒ `NAP-R2-01` | ✅ |
| `-05` | Test tự gọi `kiem_dsn` trên **10** dạng DSN cổng 5433 *(URI · `05433` · `?port=` · khoá-giá-trị · `port='5433'` · không `/` sau cổng · `[::1]` · `127.0.0.1` · `host=` trong query · `postgres://`+`sslmode`)*: bị chặn **10/10** *(R1: lọt 5/10)*; bài `test_kiem_dsn_*` của Dev = 9 dạng chặn + 3 cho qua + 1 hỏng; đột biến "chỉ bắt `:5433/`" ⇒ ĐỎ đúng ca `…:05433/…` | ✅ |
| `-06` | `nap_nguon_dai`: BG **4** · README **1** *(trước: 0·0·0)*; `fls_nguon_dai` ở `fls/*.py` = **3** tệp *(`grep -rl`; `KQ-336` ghi 7 — khác phương pháp đếm, không đổi kết luận)* | ✅ |
| `-12` | Cờ `--doi-chieu` + Σ nguồn = Σ kho từng nguồn, ĐỎ hai chiều *(bài chốt `…SAU_NAP…`; kho rỗng ⇒ ĐỎ)*; M7/M10 chết | ✅ |
| `-13` | ID Quỹ khai MỘT chỗ `cred_sheets.ID_QUY`; ID bản copy `1RmmkOSC…` trong **mã** = **0** *(3 lần xuất hiện đều ở chú thích, đã cắt cụt)*; live Bank + Quỹ + RAW **HTTP 200 ×3** | ✅ |

## `WO-352` — sàn `T · CDT1`
- Luật làm tròn **xuống hàng trăm** giữ nguyên; kiểm lại số đo sống → sàn: S 3.422 → **3.400** · H 3.549 → **3.500** · **T 3.056 → 3.000** · AB 2.525 → **2.500** · AC 2.518 → **2.500** · Y 463 → **400** — **6/6 đúng luật**.
- So **sàn cũ**: chỉ **MỘT** cột giảm — `T · CDT1` **3.300 → 3.000** *(số đo 3.339 → 3.056, −283 ô; số dòng nguồn L1 tăng 10.100 → 14.265)*; S/H/AB/AC tăng, Y giữ 400. Chú thích mã mỗi dòng có `do <mới> (23/11) · cu <cũ> (27/08) · san cu`; BG-335 §11.2 ghi tên cột giảm — ⛔ che.
- **ĐỎ hai chiều** *(đột biến)*: sàn CDT1 3.100 ⇒ `test_nguong_san_phu_sau_cot_then_chot_va_deu_duoi_so_da_do` ĐỎ · sàn Y 500 *(trên số đo)* ⇒ cùng bài ĐỎ · nguồn rỗng *(bỏ qua khi `lan_lat = 0`)* ⇒ `test_DO_cong_doc_du_do_thi_KHONG_ghi…` ĐỎ. Live: cổng đọc-đủ ĐẠT với sàn mới.

## Đột biến *(12 chỗ trên cây thử, mỗi lần `git checkout` trả nguyên; `diff` sau = 0)*
**Chết 11 / sống 1.** Chết: M7 · M10 · M9 · M11 · `-03` · `-04` · `-05` · W1 · W2 · W3 · X1 *(bỏ đòi `FLS_CHO_GHI_THAT=1` ⇒ `test_TU_CHOI_thieu_cong_ghi…` ĐỎ)*. **Sống:** lớp che `\d{6,}` ở `dem_ly_do_loai` → `NAP-R2-01`. *(Ba chỗ do Test tự chọn ngoài danh sách R1: W3 · X1 · lớp che.)*

## IAM — dự án GCP dùng chung `fp-a-project` *(chủ chấp nhận 24/11)*
⛔ **Đo live = ĐỎ của phép này** *(R2 không có quyền GCP; chỉ đọc mã `tools/staging/01/03*.sh`, ⛔ "không thấy lệch")*. Đọc mã:
- ✅ `secretAccessor` hẹp **đúng 3 bí mật**; `compute.osLogin` hẹp theo **VM**; `artifactregistry.reader` theo **repo**.
- ⚠ `roles/cloudsql.client` ở cấp **dự án**, `--condition=None` *(`01…sh:178`)* ⇒ `NAP-R2-02`.
- ⚠ `roles/iap.tunnelResourceAccessor` ở cấp **dự án**, `--condition=None` *(`03…sh:164`)* ⇒ `NAP-R2-03`.
Không có `roles/owner` / `roles/editor` trong 3 tệp `0[1-3]*.sh` *(`grep` = 0, mẫu số: 3 tệp)*. Staging tạm ⇒ không chặn, nhưng chủ nên biết hai gán rộng này trong dự án chung.

## Việc kế
`ĐẠT` ⇒ orchestrator gộp bước theo `isp-gop-buoc` *(sàn = thu thập cây gộp thật; số tại thời điểm gộp có thể khác 5172)*. 4 GHI NHẬN ⇒ backlog: `-01` bài che số *(DEV)* · `-02`/`-03` IAM hẹp *(DEV/chủ)* · `-04` bản ghi `QĐ` *(BA)*.
