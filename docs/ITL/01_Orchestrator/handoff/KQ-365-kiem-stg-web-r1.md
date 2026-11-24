# KQ-365 — R1 STG-WEB *(`WO-363` · `BG-364`: link web sau Google IAP + màn `/login` một tài khoản chung)*

| | |
|---|---|
| **Phán quyết** | **`ĐẠT CÓ ĐIỀU KIỆN`** — **0 CHẶN · 3 NÊN SỬA · 5 GHI NHẬN** *(`STG-WEB-R1-01…08`, sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_STG-WEB.md` v0.1)* |
| **Chủ chạy `07`/`08` được chưa** | **CÓ** *(0 CHẶN)* — 3 NÊN SỬA đưa vào vòng sửa trước R2 cuối; ⛔ phải chờ sửa mới chạy |
| **Kiểm bởi** | `fls-test` *(phiên cloud · cụm PG **5435**)* · 2026-11-24 |
| **Kiểm ở** | `isp/STG-WEB` @ `d1add69` · đột biến trên bản chép / sửa-rồi-`git checkout` *(`git status` = 0 dòng sau mỗi lượt)* |
| **Chạm** | `KHONG_CHAM` — ⛔ GCP · ⛔ `gcloud` thật · ⛔ kho thật · ⛔ mật khẩu/băm thật *(mật khẩu sonde ngẫu nhiên, ⛔ in)* |

## Sáu mục được giao
| # | Kiểm | Đo được |
|---|---|---|
| 1 | An toàn cửa | Cổng thật, khoá ES256 riêng: **23/23** ca âm → `403` *(không JWT · rác · khoá khác · hết hạn · `iat` tương lai · sai `iss` · `alg=none`/`HS256` · `kid` lạ · thiếu `email` · sai/thiếu `aud` · chữ ký 0/cụt · sửa thân · 5 phương thức)*, **cửa bị chạm 0**; mẫu số dương: JWT đúng → `200`. Khoá IAP hỏng → `503` *(đóng)*. Ngoài Cloud Run / `--cong`=`--cong-cua` → exit `2`. Cửa thật `--dia-chi 0.0.0.0 --cho-web` ⇒ vẫn từ chối *(`GAP-WEB-01`)*; nghe ngoài loopback chỉ có cổng. ⚠ **`aud` ⛔ ghim ở bản dựng 07** *(đếm `FLS_IAP_AUD` trong mã chạy = 0)* ⇒ `aud` lạ **vào được** → `-01`. Thân khổng lồ không JWT treo cổng → `-05`. |
| 2 | `/login` | scrypt `N=16384 r=8 p=1` · so thời gian hằng *(46 vs 45 ms)* · khoá tạm **N = 5** theo email IAP / 900 s *(đúng mật khẩu khi khoá vẫn `429`)* · cookie `__Host-` `HttpOnly` `Secure` `SameSite=Strict` `Path=/` ⛔ `Domain` · đăng xuất ⇒ cookie cũ `401` · hết 8 giờ ⇒ từ chối · sang email khác / sửa chữ ký ⇒ `401`. **Rò mật khẩu · băm · cookie · JWT trong nhật ký = 0 · 0 · 0 · 0**; `grep HondurasGesha` = 10 tệp, **0** chứa mật khẩu *(9 đúng vai tên tài khoản; BG-364 W4 gọi nhầm "mật khẩu" → `-08`)*. Hụt: đăng xuất/khoá tạm mất khi instance dậy lại → `-02`; khoá phiên suy từ băm → `-06`; khoá theo email → `-07`. |
| 3 | `07` gcloud GIẢ | Từ trống `--kiem` ⇒ **0 ĐẠT · 28 ĐỎ** *(mong 0/28)*; dựng ⇒ **29/29 ĐẠT**; GHI ⊆ danh sách *(**0** ngoài; **0** `delete`/`compute`/`firewall`/`set-iam`/`keys`)*; dịch vụ đụng `{fls-staging-web}`; chạy lại ⇒ tập IAP **3** không nhân đôi, `builds submit` **0**; **12/12** phá trạng thái ⇒ đúng mục ĐỎ. Binding **mức dự án** của 07/08 = **0** ⇒ `--condition=None` ⛔ áp *(01 · 03 có, nhưng ⛔ bài canh → `-03`)*. |
| 4 | Màn hình THẬT | Chromium headless → cổng → `chay_cua.py --cho-web` thật: `/` chưa đăng nhập ⇒ `303 /login`; API ghi chưa đăng nhập **401**; sai ⇒ `⛔ Sai tên đăng nhập hoặc mật khẩu.` *(tên-sai ≡ mật-khẩu-sai, ⛔ lộ tồn tại)*; đúng ⇒ `FLS · Sổ ITL`, F03 hiện số, ⛔ `FLS-TRA-LOI-LA`/`FLS-MAT-KET-NOI`; `/logout` ⇒ `/login`; 5 sai ⇒ `Sai quá 5 lần — khoá tạm 15 phút`; ⛔ JWT IAP ⇒ **403**. |
| 5 | Đột biến | **20** chỗ ⇒ **15 bắt · 5 sót**. Sót: bỏ `--condition=None` ở `03` và `01` *(49/49 · 9/9 xanh — `-03`)*; so **tên** bằng `==` · in **băm** vào nhật ký · tên sai bỏ scrypt *(81/81 xanh — `-04`)*. Bắt: bỏ `aud` · bỏ khoá tạm · thiếu `Secure`/`HttpOnly` · `Lax` · so băm `==` · bỏ chữ ký ES256 · bỏ kiểm hết hạn · phiên bỏ gắn email · `/logout` không thu hồi · API lọt khi chưa đăng nhập · in mật khẩu · 07 bỏ `--no-allow-unauthenticated` · 07 không gỡ `allUsers` · 08 `read` hiện. |
| 6 | Cổng | §Cổng: ĐẠT 28 = 28 · web 3 = 3 · sàn 5168 |

## NÊN SỬA *(vào vòng sửa, ⛔ chặn chủ)*
- **`STG-WEB-R1-01`** `aud` ⛔ ghim ở 07 *(lớp ba hở với JWT IAP của app khác)* — 07 đọc `IAP_AUD` từ nhật ký, ghim `FLS_IAP_AUD`, thêm mục `mong` "aud đã ghim".
- **`STG-WEB-R1-02`** `/logout` + khoá tạm chỉ ở bộ nhớ instance *(`min-instances=0`)*: cookie đã đăng xuất **hợp lệ lại** sau khởi động lại ≤ 8 giờ — ghi giới hạn hoặc rút `PHIEN_GIAY`/`min-instances=1`.
- **`STG-WEB-R1-03`** `--condition=None` ở `01`·`03` ⛔ bài canh; `gcloud_gia.py` ⛔ mô phỏng chính sách có điều kiện *(lỗi THẬT 24/11)*.

## GHI NHẬN *(⛔ chặn)*
`-04` 3 đột biến sót *(so tên `==` · in băm · scrypt tên sai)* · `-05` đọc thân trước JWT *(50 MB không JWT ⇒ không phản hồi 4 s)* · `-06` đọc được bí mật `fls-staging-login` ⇒ rèn cookie hợp lệ **207** ⛔ mật khẩu · `-07` khoá tạm theo email, ⛔ toàn cục · `-08` BG-364 W4 gọi tên tài khoản là "mật khẩu".

## Giả định ⛔ đo được ở đây *(căn cứ mã, đo ở GCP)*
G-1 trang đăng nhập Google thật + cookie IAP · khuôn `aud` Cloud Run · khoá chú thích `run.googleapis.com/iap-enabled` · `--iap` ở `gcloud run` GA · `gcloud iap web add-iam-policy-binding` với `--resource-type=cloud-run`. Bước ③ của chủ đo G-1.

## Cổng
`--duong-nen --cong 5435` MỘT lần, một mình: **`KẾT: ĐẠT`** — toàn bộ **28 = 28** *(XFAIL 2 = 2 · thêm 0 · bớt 0 · chạy **5168** · skipped 0 · deselected 0)* · web **3 = 3** *(chạy **690**)* · sàn 5168 giữ. `kiem_tai_lieu` ĐẠT *(518 file)* · `lint-imports` 11 kept 0 broken · `quet_pii_repo` **0**. ⚠ Lần chạy đầu bị bỏ vì còn 2 tiến trình sonde thừa; chạy lại sau khi dọn.
