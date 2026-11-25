# KQ-366 — R2 CUỐI STG-WEB *(`WO-363` · soát vòng sửa sau R1 `KQ-365` — `BG-364` §12, mã `ffc2d3a`, ngọn `e821562`)*

| | |
|---|---|
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA · 4 GHI NHẬN** *(`STG-WEB-R2-01…04`; sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_STG-WEB.md` v0.2)* |
| **R1 đóng** | **8/8** *(`-01…-08` ⇒ ĐÓNG ở sổ; mỗi hàng ghi căn cứ)* |
| **Kiểm bởi** | `fls-test` *(phiên cloud · cụm PG **5435**)* · 2026-11-25 |
| **Kiểm ở** | `isp/STG-WEB` @ `e821562` + **cây gộp thử** `thu/STG-WEB` *(nhánh làm việc `69ac8ca` ⊕ `isp/STG-WEB`; ⛔ đẩy)* |
| **Chạm** | `KHONG_CHAM` — ⛔ GCP · ⛔ `gcloud` thật · ⛔ mật khẩu/băm thật *(sonde dùng chuỗi thử, bí mật giả)* |

## 1 · Soát vòng sửa
| # | Mục | Đo được |
|---|---|---|
| 1 | `-01` `aud` | Khuôn `/projects/<SỐ>/locations/<vùng>/services/<service>` **khớp** trang Google hiện hành *(tra 25/11 `docs.cloud.google.com/iap/docs/signed-headers-howto`)*; `07:97` tính từ số project + `$REGION` + `$SVC`, ghim ở `run deploy` `:139`. Đột biến đảo thứ tự khuôn ⇒ **ĐỎ** *(4 bài 07)*. JWT chữ ký ĐÚNG, `aud` app khác: **11 biến thể** *(khác project · vùng · service · `/` cuối · khoảng trắng · HOA · thừa/thiếu `/` đầu · rỗng · số · danh sách)* ⇒ 10 × `403` + 1 rớt kết nối *(`R2-03`, vẫn đóng, cửa chạm **0**)*; mẫu số dương: `aud` đúng ⇒ `/login` **200**. Hành vi `aud` thật của GCP: căn cứ tài liệu, **⛔ đo ở GCP**. |
| 2 | `-02` bền | Bí mật RIÊNG `fls-staging-phien` *(khoá HMAC + thế hệ + bộ đếm sai + mốc khoá)*. Dựng cổng MỚI trên cùng bí mật ⇒ cookie đã `/logout` **401** *(cả cookie máy thứ hai)* · khoá **429** · đăng nhập lại **303** · phiên bản cũ huỷ *(còn **1**)* — bài Dev + chạy lại ở bản chép. IAM: `07`/`08` binding mức dự án = **0**; `08` cấp `secretVersionManager` **chỉ** ở `fls-staging-phien` *(đột biến cấp thêm ở bí mật băm ⇒ ĐỎ)*. Rò rỉ mật khẩu · băm · mật khẩu sai · cookie · khoá HMAC · token SM ở nhật ký + `argv` + `environ` của 2 cổng = **0** *(8 lần ghi · 8 huỷ)*. Ghi đồng thời 2 instance: **đo tuần tự đúng; đồng thời thật = căn cứ mã** ⇒ `R2-02` *(rủi ro THẤP, `--max-instances=1`)*; đồng bộ chéo ≤ 30 s ⇒ `R2-01`. |
| 3 | `-03` điều kiện | `gcloud_gia` mặc định chính sách CÓ điều kiện. Bỏ `--condition=None` ở `01` ⇒ **ĐỎ** *(4 bài)* · ở `03` ⇒ **ĐỎ** *(2)* · đảo mặc định giả ⇒ **ĐỎ** · thêm binding mức dự án thiếu cờ vào `07` ⇒ **ĐỎ** *(4)*. `07`/`08` có **0** binding mức dự án *(⛔ có chỗ để bỏ cờ — chỉ `01`/`03` thật)*. |
| 4 | Đột biến | **15 chỗ** khác 14 của Dev: **bắt 12 · tương đương 1 · sót 2** — bắt: `07` đảo khuôn aud · `phien_hop_le` bỏ so thế hệ · bỏ huỷ phiên bản cũ · `08` cấp thêm `versionManager` · `con_khoa` bỏ `"*"` · thiếu `aud` lọt · gia mặc định không điều kiện · `01`/`03` bỏ `--condition=None` · `07` thêm binding mức dự án · so tên `==` · tên sai bỏ scrypt. **Tương đương:** lỗi ghi in giá trị bí mật vào thông điệp `SystemExit` — cổng chỉ in **tên kiểu** ngoại lệ ⇒ ⛔ ra nhật ký. **Sót** *(`R2-04`)*: `PHIEN_GIAY` 8 h → 80 h · `SAI_TOAN_CUC` 20 → 2000 — bài đọc chính hằng. |
| 5 | Cây gộp thử | Xem §2. |

## 2 · Cây gộp thử *(`origin/claude/bold-galileo-zukpaf` @ `69ac8ca` ⊕ `isp/STG-WEB` @ `e821562`)*
- **Xung đột 5 tệp**, gộp tay: `tools/dung_moi_truong_isp.sh` *(sàn)* · `tests/test_dung_moi_truong_isp.py` *(sàn + sổ gộp: giữ bản STG-WEB, thêm `+ isp/STG-NAP`)* · `tools/staging/README.md` *(trình tự `01→02→03→04→05→08→07→UAT`, giữ cả hàng **05** lẫn **08**/**07**)* · `WO-363-…md` *(trạng thái `CHO_TEST` + nhật ký)* · `08_CHANGELOG_RELEASE.md` *(giữ **cả hai** phía)*.
- ⭐ **Sàn đặt = số THẬT thu thập cây gộp:** `pytest --collect-only` = **5267** *(web **690**)* — bản STG-WEB một mình = 5182; nền nhánh làm việc thêm **85** *(gồm `isp/STG-NAP`)*. ⛔ cộng tay.
- **`--duong-nen --cong 5435`**: **`KẾT: ĐẠT`** — toàn bộ `12 failed, 5239 passed, 2 xfailed, 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** *(XFAIL 2 = 2 · thêm 0 · bớt 0 · chạy **5267** · skipped 0 · deselected 0)*; web `3 failed, 687 passed` ⇒ **3 = 3** *(chạy 690)*.
- ⚠ **Lượt đầu bị bỏ** — tự mình làm bẩn: chạy đột biến `test_01/03` *(tạo/xoá vai cụm)* **song song** ⇒ `ĐỎ` *(thêm 1: `test_02_chuyen_vai_gcp::test_tao_vai_bi_PG_tu_choi…`; chạy riêng **8/8 xanh**)*. Chạy lại **một mình** ⇒ ĐẠT như trên.
- `kiem_tai_lieu` **ĐẠT** *(533 file · 3128 bảng)* · `lint-imports` **11 kept · 0 broken** · `quet_pii_repo` **0** chỗ · 0 tệp.
- **Grep mật khẩu chung = 0:** băm scrypt đầy đủ *(muối+băm)* ở repo ngoài `tests` **0** · ở `tests` **0** *(bài sinh lúc chạy)*; `HondurasGesha` kề `mật khẩu/password = …` **0**; gán mật khẩu chữ cứng ở `tools/staging` **0** *(3 khớp thô đều là `PGPASSWORD="$MK_…"` — biến, ⛔ chữ)*; mẫu số: 24 tệp `tools/staging`.

## 3 · GHI NHẬN → backlog *(⛔ chặn gộp)*
- `R2-01` instance chung bí mật thấy nhau chậm ≤ 30 s *(cookie đã `/logout` ở B vẫn 207 ở A; khoá của B: A cho mật khẩu đúng qua)*.
- `R2-02` đọc–sửa–ghi ⛔ khoá chéo instance *(đồng thời thật ⛔ đo; rủi ro THẤP)* + `08` ⛔ huỷ phiên bản cũ.
- `R2-03` `aud` danh sách ⇒ rớt kết nối thay 403 *(đóng đúng chiều)*.
- `R2-04` hằng `PHIEN_GIAY` · `SAI_TOAN_CUC` ⛔ ghim giá trị.

## 4 · Giả định ⛔ đo được ở đây *(căn cứ mã/tài liệu, đo ở GCP)*
G-1 IAP + trang Google thật · khuôn `aud` *(đã khớp tài liệu, ⛔ đã thấy một JWT IAP thật)* · **G-9** ghi/huỷ phiên bản bí mật bằng REST với token SA · ghi **đồng thời** 2 instance. Bước chủ chạy đo G-1 *(`BG-364` §12.1)*; dòng `IAP_AUD … lech` ở nhật ký sẽ lộ khuôn sai.

## 5 · Việc kế
Gộp `isp/STG-WEB` vào nhánh làm việc theo `isp-gop-buoc`: **sàn `MONG_PYTEST_TOAN_BO` = số thu thập THẬT lúc gộp** *(cây thử: 5267)* — 5 tệp xung đột như §2.
