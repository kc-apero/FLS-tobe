# UAT_STAGING_E2E — kịch bản kiểm bằng NGƯỜI trên staging (sau O6)

| | |
|---|---|
| **Phiên bản** | v0.1 · 2026-11-23 · `WO-325` AC-4 · do `fls-dev` làn HẠ TẦNG soạn, **BA/PO duyệt** trước khi phát cho người test |
| **Căn cứ ký** | O6 — ThuongCT, 23/11/2026: *"Cho phép lên staging và bắt đầu test full luồng e2e bằng human."* (sổ I2 v0.4 §O6 · `TIEN_DO` 2026-11-23) |
| **Cây mã mà bảng SỐ dưới đây mô tả** | nhánh `claude/bold-galileo-zukpaf-isp/STG`, đã GỘP `origin/claude/bold-galileo-zukpaf` **có H14** (gói `WP-C5c` — 11 gói; đo 23/11: `GOI_BIET` ở `tools/do_hd2.py` = 11) **nhưng CHƯA có I2** (đo 23/11: `grep -rln "FxKho\|kiem_fx_thang" fls tools` = 0) ⇒ giữ các dòng `[CHỜ I2]`; mọi số HD2 dưới đây lấy từ `hd2_cong.json` **ở ngọn đã gộp** (`STG-R1-05`). **Dựng lại ảnh (bước 03)** sau khi gộp |
| **Nguồn của MỌI con số HD2** | `docs/ITL/_tools/hd2_cong.json` (tệp cổng HD2 theo gói). Bài `tests/staging/test_uat_doc.py` đối chiếu từng con số có thẻ `<!--hd2:…-->` với tệp ấy — **lệch ⇒ bài đỏ** (Đ2: so hai nguồn) |
| **Ai test · khi nào** | ⛔ chưa chỉ định — là **câu chủ** (BG-326 §Câu chủ). Điền ở cột "Người test" từng bước |

## 0 · Trước khi bắt đầu (người test đọc, ~5 phút)

1. **Vào bằng gì.** App ⛔ có địa chỉ công khai (cố ý: cửa chỉ phục vụ màn hình trên `127.0.0.1`, `GAP-WEB-01`). Chủ cấp quyền cho bạn (`--cap-quyen`), rồi mỗi lần test:
   `gcloud compute ssh fls-staging-app --project <PROJECT_ID> --zone asia-southeast1-b --tunnel-through-iap -- -N -L 8088:127.0.0.1:8088`
   (để cửa sổ này mở) → mở trình duyệt **http://localhost:8088/**. Đóng cửa sổ ⇒ mất đường vào.
2. **Bạn là ai trên màn hình.** Chưa có đăng nhập từng người (`GAP-WEB-01`; SSO là phase sau): cả phiên dùng **một** thẻ, và dòng đầu màn hình ghi `kế toán · <tên>`. **`<tên>` = người chủ khai khi dựng app (`--nguoi-ky`)** — mọi chữ ký bạn bấm sẽ mang TÊN ĐÓ, ⛔ tên của bạn. Nếu bạn không phải người ấy: **chỉ làm các bước đọc**; bước KÝ (U5, U9) do người ấy làm hoặc chủ dựng lại app với `--nguoi-ky` của bạn.
3. **Chế độ app.** `doc` (mặc định, CHỈ ĐỌC): mọi nút ghi trả `405`. `ghi`: ký được. Bước nào cần `ghi` có ghi rõ.
4. **Kho staging có gì.** Config `IX.*` đã ký (bước 04) · **sổ `fls_itl` = 0 dòng** (dữ liệu nguồn ⛔ nạp — câu chủ). ⇒ F01/F02 trống và cổng `KHO_SACH` đỏ là **ĐÚNG** (xem §1), ⛔ báo lỗi.
5. **Báo kết quả.** Mỗi bước điền: người test · ngày · `ĐẠT`/`ĐỎ` · ghi chú. **ĐỎ** ⇒ chép số bạn THẤY cạnh số MONG + chụp màn hình; ⛔ đoán nguyên nhân.

## 1 · Giới hạn đã ký ở O6 — ⛔ báo nhầm là lỗi

| Giới hạn | Bạn sẽ thấy gì | Vì sao là ĐÚNG (nguồn) |
|---|---|---|
| **605** (DR3 Sign off) | gói WP-C5c · 605: **ô so = 0** — "DỪNG có tên" | tab nguồn `[FS1][PLA5]` đã xoá khỏi sổ (0 ứng viên); tái lập từ `sign_off_dau_vao` là vòng tròn (đã có rào). Chủ ký "605 DỪNG có tên" 23/11 (`TIEN_DO` lượt 03:21; `BG-320` §605). Thấy ở gói `WP-C5c` (H14 đã gộp) |
| **615** (A-CCR, bản chính thức) | ô so <!--hd2x:615.o_so-->13.760 / <!--hd2x:615.o_dap_an_so-->48.021; <!--hd2x:615.chua_co_dau_vao-->5.258 ô `chua_co_dau_vao` (Σ `chua_co_dau_vao:*` = hr + raw_data_management + tien_dau_bao_cao); lệch lớp `lech_ban_ccr_vs_cf` 671 + `ite_alias` 35 | `TIEN_DO` lượt 18:00 22/11 (sửa H14) — các lớp lệch CÓ TÊN, lệch FLS = 0 |
| **D3** | WP-C5a: **`lech_D3` 3.099 ô** — By GI dùng driver `PE` khác AS-IS (tỉ lệ GI của MID3) | quyết D3: giữ driver PE, khai lệch có tên (`TIEN_DO` lượt 11:41 22/11); chờ chủ nếu muốn đổi |
| **CHECK IX.PL** | các dòng CHECK của PL (607 · 608 · 609 · 610) **đỏ**, **0 "đạt có số"** | IX.PL chưa có bằng chứng dương nào (`DT11` AC `-03`: `dat_co_so` = 0, `dat_0_0` 14/262) — đỏ ở đây là cổng trung thực, ⛔ lỗi hệ thống |
| **Sổ rỗng** | F01 hàng chờ 0 · F02 lưới 0 dòng · cổng `KHO_SACH` ĐỎ ("`fls_itl` chỉ có 0 dòng < ngưỡng 1000") · `HD1_THANG` ĐỎ | kho staging chưa nạp sổ (câu chủ dữ liệu); ⛔ "sạch" mà là "chưa đo được gì" |
| **Lệch CÓ TÊN trong HD2** | "khớp" < "tổng ô" ở WP-C3 · C4c · C5 (xem bảng U3) | mỗi lệch có nhãn + lý do (`lech_co_chu_dich`); **lệch NGOÀI tên phải = 0** — số khác 0 mới là lỗi |

## 2 · Các bước kiểm

Cột **Mong** là số/chữ phải THẤY. Số có nhãn đếm gì (Đ4): "ô" = ô đáp án so được (đã trừ ô cố ý bỏ có tên); "dòng" = dòng sổ so.

| # | Bạn làm gì | Mong (số + nhãn) | Người test | Ngày | ĐẠT / ĐỎ | Ghi chú |
|---|---|---|---|---|---|---|
| **U1** | Mở tunnel (§0.1) rồi mở http://localhost:8088/ | Vỏ màn hình hiện: thanh trên + 4 nút màn **① Cổng hôm nay · F03 · ② Hàng chờ · F01 · ③ Sổ ITL · F02 · ④ Nạp sao kê · F04 · ⑥ Cấu hình · F08**; **0** thông báo lỗi đỏ; trang tải < 3 giây | | | | |
| **U2** | Nhìn dòng đầu màn hình | `kế toán · <tên>` với `<tên>` = người chủ khai (`--nguoi-ky`); ⛔ **không** là `thu@apero.vn` | | | | |
| **U3** | Bấm **① Cổng hôm nay · F03**, tìm 4 thẻ **HD2 WP-C2 · WP-C3 · WP-C4 · WP-C5** | **4/4 thẻ ĐẠT** (xanh; thẻ cha `WP-C5` = **C5a + C5b + C5c**). Chi tiết từng gói: bảng U3 bên dưới. Cổng `KHO_SACH` ĐỎ + `HD1_THANG` ĐỎ là ĐÚNG (§1) | | | | |
| **U4** | Bấm **⑥ Cấu hình · F08** → bảng tỷ giá `IX.FX` | **37 dòng tháng** (202306 + 202401…202612) · tiền tệ USD · SGD · COP · VND · HKD · `thiếu` = **0** · `trùng` = **0** · `lạc` = **1** (= 202306 — dòng này ⛔ có nút ký, đúng thiết kế) · lần đầu cả 37 dòng `chưa ký` · **36** nút **Ký tháng** (đo 23/11 qua `GET /config/fx`) | | | | |
| **U5** `[cần chế độ ghi]` | Ở dòng **202401**: bấm **Ký tháng** → hộp xác nhận → **Ký tháng 202401** | Dòng đổi thành `đã ký · <tên> · <ngày>`; nút **Ký tháng** của dòng đó **khoá**; mã trả về 201. Bấm lại ⇒ không được (nút khoá); qua API ký lại = **409** `FLS-CAUHINH-DA-KY` | | | | |
| **U6** | Ở **F08**, kéo tới tháng không có trong bảng (vd 209912) — nếu màn có ô nhập; nếu ⛔ có ô, bỏ qua | tháng ngoài IX.FX ⇒ **404** có tên "⛔ tháng … ⛔ có trong IX.FX". (Bước phụ — ghi `BỎ QUA` nếu màn ⛔ cho nhập) | | | | |
| **U7** | Vào VM: `gcloud compute ssh fls-staging-app --tunnel-through-iap --zone asia-southeast1-b --project <PROJECT_ID> -- sudo docker exec fls-app bash /app/tools/staging/app/chay_chuoi.sh` — ("**chạy chuỗi**", đo, ⛔ ghi tệp) **`[chỉ CHỦ chạy — lệnh cần sudo; vai osLogin ⛔ có sudo]`** (`STG-R1-06`, phương án A) | In **<!--goi:dong-->11 dòng** `WP-C2 … WP-C5c` cột THOAT = **0**, rồi `══ CHUỖI: <!--goi:chuoi-->11 gói · ĐỎ 0 · KẾT: ĐẠT`. Tổng ~**45 giây**, đỉnh RAM ~**800 MB** (đo 23/11 trên cây đã gộp H14: 44,4 s · 797 MB, `WP-C5c` 13,2 s; trên máy dev; staging có thể chậm hơn gấp đôi — vẫn < 2 phút là ĐẠT) | | | | |
| **U8** `[cần chế độ ghi + SSH]` | Như U7 nhưng thêm `--ghi` (ghi lại `hd2_cong.json` trong container) rồi F5 trang F03 | **`[chỉ CHỦ chạy — cần sudo]`** 11/11 gói ĐẠT như U7; **F03 sau F5: 4 thẻ HD2 vẫn ĐẠT, số chi tiết ⛔ đổi** so với bảng U3 (kho + ảnh không đổi ⇒ kết quả giống từng ô) | | | | |
| **U9** `[CHỜ I2]` | Ở F08, phần **bản báo cáo kỳ** (Daily Report 3, ví dụ kỳ **202510**) → bấm **Ký bản** | Cây STG **chưa có đường tạo bản** (engine `dua_ban_ky` chỉ chạy trong luồng I2): màn báo **"kỳ 202510 chưa có bản báo cáo nào để ký"** (404), nút ký ⛔ có — đo 23/11. Sau khi gộp I2 và chạy chuỗi `--ghi`, bước này phải ký được **bản mới nhất** và dòng đổi `đã ký · <tên>`; cập nhật bước + số khi đó | | | | |
| **U10** `[CHỜ I2]` | Chưa ký tháng 202503/202510 mà chạy chuỗi (U7) | Cây STG: **vẫn ĐẠT 11/11** (chưa có chốt D1). **Sau I2**: chuỗi phải ra **0/11 gói có số** và in `FX_CHAN <tháng>` cho tháng chưa ký (`KQ-318`); ký đủ ⇒ 11 gói khớp `hd2_cong.json`. ⛔ báo ĐỎ ở cây STG — đây là hành vi sắp có | | | | |
| **U11** | Bấm **② Hàng chờ · F01** và **③ Sổ ITL · F02** | Mỗi màn hiện trạng thái **rỗng** có chữ giải thích (⛔ vòng quay mãi, ⛔ lỗi đỏ): F01 **0** dòng chờ · F02 **0** dòng sổ ITL (đo 23/11: `GET /queue` và `GET /ledger` đều `count = 0`) | | | | |
| **U12** `[chế độ chỉ-đọc]` | Khi app ở chế độ `doc`: thử một thao tác ghi (vd **Ký tháng** ở U5) | Nút/thao tác trả **405** "nhóm ghi tắt" và màn báo rõ — ⛔ im lặng, ⛔ 500 | | | | |
| **U13** | Ở **④ Nạp sao kê · F04** mở màn (⛔ nạp tệp thật nếu chủ chưa cho dùng dữ liệu nào) | Màn hiện form nạp + danh mục nguồn; ⛔ nạp gì khi chưa có câu trả lời "dữ liệu thật hay ẩn danh" | | | | |

### Bảng U3 — kết quả mong của từng gói HD2 (nguồn: `hd2_cong.json`)

"Tổng ô" = ô đáp án so được · "Khớp" = ô khớp · "Lệch có tên" = Tổng − Khớp (mỗi ô có nhãn + lý do; ⛔ là lỗi) · lệch NGOÀI tên = **0** ở mọi gói.

| Gói (thẻ) | Tổng ô | Khớp | Lệch có tên |
|---|---|---|---|
| **WP-C2** — CA.GL ↔ đáp án 406 (BM…BT × 7.877 dòng sổ) | <!--hd2:WP-C2.tong_o-->63.016 | <!--hd2:WP-C2.khop-->63.016 | 0 |
| WP-C3a — SO.CFA1 Daily ↔ 409 | <!--hd2:WP-C3a.tong_o-->205.175 | <!--hd2:WP-C3a.khop-->205.140 | <!--hd2:WP-C3a.lech-->35 |
| WP-C3b — SO.CFA1 Y/H/Q/M ↔ 410 | <!--hd2:WP-C3b.tong_o-->11.585 | <!--hd2:WP-C3b.khop-->11.543 | <!--hd2:WP-C3b.lech-->42 |
| WP-C3c — CA.GL HR ↔ 408 + CFA3 | <!--hd2:WP-C3c.tong_o-->888 | <!--hd2:WP-C3c.khop-->835 | <!--hd2:WP-C3c.lech-->53 |
| WP-C3d — SO.PLA1 · PLA3 ↔ 414–419 | <!--hd2:WP-C3d.tong_o-->1.289.415 | <!--hd2:WP-C3d.khop-->1.287.624 | <!--hd2:WP-C3d.lech-->1.791 |
| **WP-C3** (thẻ cha = C3a+C3b+C3c+C3d) | <!--hd2:WP-C3.tong_o-->1.507.063 | <!--hd2:WP-C3.khop-->1.505.142 | <!--hd2:WP-C3.lech-->1.921 |
| WP-C4a — AL.PLT GI vendor thường ↔ MID3 | <!--hd2:WP-C4a.tong_o-->420 | <!--hd2:WP-C4a.khop-->420 | 0 |
| WP-C4b — AL.PLT GI mọi vendor ↔ MID3 | <!--hd2:WP-C4b.tong_o-->1.981 | <!--hd2:WP-C4b.khop-->1.981 | 0 |
| WP-C4c — AL.PLT OMC · SC · PS ↔ MID3 | <!--hd2:WP-C4c.tong_o-->19.894 | <!--hd2:WP-C4c.khop-->19.591 | <!--hd2:WP-C4c.lech-->303 |
| **WP-C4** (thẻ cha = C4a+C4b+C4c) | <!--hd2:WP-C4.tong_o-->22.295 | <!--hd2:WP-C4.khop-->21.992 | <!--hd2:WP-C4.lech-->303 |
| WP-C5a — AL.KEY cờ IX.ALR BẬT 2025 ↔ ATL 606 | <!--hd2:WP-C5a.tong_o-->45.674 | <!--hd2:WP-C5a.khop-->40.556 | <!--hd2:WP-C5a.lech-->5.118 |
| WP-C5b — SO.PLA3-ATL (PL2…PL8 từ IX.PL) | <!--hd2:WP-C5b.tong_o-->4.102 | <!--hd2:WP-C5b.khop-->3.179 | <!--hd2:WP-C5b.lech-->923 |
| WP-C5c — RP.PL · RP.CF Daily Report 2·3 ↔ 607 · 608 · 609 · 610 · 615 (605 DỪNG có tên) | <!--hd2:WP-C5c.tong_o-->86.150 | <!--hd2:WP-C5c.khop-->77.672 | <!--hd2:WP-C5c.lech-->8.478 |
| **WP-C5** (thẻ cha = C5a+C5b+C5c) | <!--hd2:WP-C5.tong_o-->135.926 | <!--hd2:WP-C5.khop-->121.407 | <!--hd2:WP-C5.lech-->14.519 |

## 3 · Khi nào dừng và gọi chủ

- Bước U1 ⛔ qua được (tunnel/quyền) · U3 có thẻ HD2 **ĐỎ** hoặc **xám "không đo được"** · U7 có gói THOAT ≠ 0 · số THẤY ≠ số MONG ở bảng U3 · bất kỳ chỗ nào màn **quay mãi** hoặc hiện **lỗi đỏ ⛔ có chữ giải thích**.
- ⛔ Tự chạy lệnh GHI vào kho; ⛔ tự nạp tệp dữ liệu thật; ⛔ chia sẻ ảnh chụp màn hình có số tài khoản/tên người ra ngoài nhóm test.

## Changelog
- v0.1 (2026-11-23): bản đầu — 13 bước, 13 hàng số từ `hd2_cong.json`; chờ BA/PO duyệt + câu chủ "ai test".
- v0.2 (2026-11-23, vòng sửa sau `KQ-327` · `STG-R1-05/06`): gộp H14 ⇒ thêm hàng `WP-C5c`, thẻ cha `WP-C5` = a+b+c; §1·615 sửa 12.380→13.760 và 6.753→5.258 (có thẻ `hd2x`, bài canh từ `hd2_cong.json`); U7/U8 11 gói · ~45 s · ~800 MB và ghi **chỉ CHỦ chạy** (`sudo`); bỏ nhãn chờ H14.
