# WO-325 — STAGING bước 02 · 03 · 04 + kịch bản test e2e bằng người (sau O6)

| | |
|---|---|
| **Trạng thái** | `MO` — giao 23/11 ~03:50 UTC |
| **Phát bởi** | orchestrator · 2026-11-23 |
| **Nhận** | `fls-dev` làn **HẠ TẦNG** — phiên cloud Sonnet 5.5 · medium · nhánh `claude/bold-galileo-zukpaf-isp/STG` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (có `tools/staging/01_dung_staging_gcp.sh`; HANDOFF 20/11 §6 khai bước 02/03) |
| **Dải phiếu** | `BG-326` · `KQ-327` (R1) · `KQ-328` (R2 cuối). Số trống kế tiếp sau dải: **329** |

## Vì sao
- **O6 ký 23/11/26** — ThuongCT, ghi chú: *"Cho phép lên staging và bắt đầu test full luồng e2e bằng human."* (sổ I2 v0.4 §O6 · TIEN_DO 2026-11-23).
- Chủ chọn 23/11: **viết ngay** script bước 02 → app → nạp, song song với lúc chủ chạy bước 01 trong Cloud Shell.
- Hiện có: **chỉ bước 01** (`tools/staging/01_dung_staging_gcp.sh` — Cloud SQL PG16, 3 vai `fls_admin`/`fls_ghi`/`fls_doc`, 5 bí mật Secret Manager, SA `fls-staging-app` có `roles/cloudsql.client`; BÁO CÁO 12 mục có `mong`; thử bằng gcloud GIẢ hai chiều). **Chưa chạy thật trên GCP.** `docs/ITL/03_Dev/06_CICD_PIPELINE.md:30` — nơi chạy staging + dữ liệu thật/ẩn danh còn `???`.

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 · bước 02 | `tools/staging/02_di_tru_phan_quyen.sh --project <ID> [--kiem]` (Cloud Shell, qua Cloud SQL Auth Proxy, mật khẩu đọc từ Secret Manager — ⛔ in): `python -m fls.db.pg_migrate` bằng `fls_admin` ⇒ `pg_verify: khop`; `fls_ghi` DML nhưng **`fls_itl` chỉ-THÊM** (`INV-I08`: ⛔ UPDATE/DELETE); `fls_doc` SELECT + `ALTER ROLE fls_doc SET default_transaction_read_only = on`. BÁO CÁO có `mong` từng mục, `KẾT: ĐẠT/ĐỎ`, exit 1 khi ĐỎ; **chứng minh ĐỎ** bằng gcloud/psql GIẢ (đúng ⇒ ĐẠT · hỏng từng mục ⇒ đúng mục ĐỎ) | pytest + chạy giả |
| AC-2 · nơi chạy app | **đo trước, rồi khuyến nghị** (Cloud Run vs VM — chi phí/tháng, cách người test vào, Cloud SQL connector, giới hạn thời gian yêu cầu của chuỗi HD2 ~3–5 phút) vào BG; dựng theo khuyến nghị: `Dockerfile` + `tools/staging/03_dung_app.sh` chạy **cửa API + màn hình** (`tools/chay_cua.py` · `fls/web`) với SA `fls-staging-app`, bí mật từ Secret Manager, ⛔ mạng công khai không xác thực *(mặc định: chỉ người được cấp quyền vào — khai cách cấp)*. Cửa vẫn TỪ CHỐI khi thiếu `FLS_JWT_SECRET` / kết nối đọc còn ghi được (đo) | pytest + chạy giả + `docker build` cục bộ |
| AC-3 · bước 04 nạp | `tools/staging/04_nap_du_lieu.sh`: nạp config IX.* đã ký + dữ liệu nguồn bằng công cụ SẴN CÓ (⛔ viết lại công cụ nạp); đòi `FLS_CHO_GHI_THAT=1`; BÁO CÁO số dòng từng bảng có `mong` (Đ3: mẫu số ≠ 0). Luật riêng tư: `PM_COT_RIENG_TU = {"Email Address"}` ⛔ vào kho; `sao_luu/` · `hien_vat/` ⛔ tải lên; dữ liệu thật hay ẩn danh = **câu chủ** (khai 2 phương án + khuyến nghị, ⛔ tự quyết) | pytest + chạy giả |
| AC-4 · kịch bản người test | `docs/ITL/04_Test/UAT_STAGING_E2E.md`: từng bước người bấm (đăng nhập → ký tỷ giá tháng → chạy chuỗi → xem F03 4 thẻ HD2 → ký bản báo cáo …), mỗi bước có **kết quả mong** bằng SỐ lấy từ `docs/ITL/_tools/hd2_cong.json` (nhãn Đ4), ô ghi người test/ngày/ĐẠT-ĐỎ/ghi chú; liệt kê giới hạn đã ký ở O6 (605 · 615 · D3 · CHECK IX.PL) để người test ⛔ báo nhầm là lỗi | BG + `kiem_tai_lieu.py` |
| AC-5 · trình tự chủ chạy | `tools/staging/README.md`: 01 → 02 → 03 → 04 → UAT, mỗi bước: chạy ở đâu, mất bao lâu, gửi lại phần nào (BÁO CÁO ⛔ chứa mật khẩu/khoá) | BG |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT (tập đỏ 28 = 28 · web 3 = 3); `kiem_tai_lieu` · `lint-imports` · `quet_pii_repo` = 0 | `--duong-nen` |

## Ràng buộc
- ⛔ Claude vào GCP (quyết chủ 20/11) — viết script, CHỦ chạy. ⛔ khoá/mật khẩu/`Client secret` trong repo hay chat. Ghi kho THẬT: `KHONG`.
- ⛔ sửa engine/tuyến; cửa API ⛔ nới luật từ chối. ⛔ `docker compose down`.
- Câu chủ (ghi vào BG, ⛔ tự quyết): nơi chạy app · cách người test vào · dữ liệu thật hay ẩn danh · ai là người test.
