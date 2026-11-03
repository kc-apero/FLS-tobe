# 15 — HƯỚNG DẪN OWNER: ba việc để mở chỗ chạy

**Version:** v0.1 · **Ngày:** 2026-09-11 · **Chủ sở hữu:** Tech Lead
**Đi cùng:** `14_CHO_CHAY_VA_DANG_NHAP` v0.1 `§5` *(ba việc)* · `§0b` *(vì sao ⛔ CHƯA bật `tailscale serve`)*

> Tệp này ⛔ không giải thích **vì sao** — cái đó ở `DEV-14`. Nó chỉ nói **bấm vào đâu**, và **làm sao biết mình đã xong**.

---

## ⛔⛔⛔ §0 · Đọc ô này trước khi bấm gì

| | |
|---|---|
| ⛔ **Thứ tự bắt buộc** | **ⓑ Tailscale → ⓐ Google → ⓒ danh sách.** `redirect_uri` của ⓐ **phải là URL có thật**, và tên ấy chỉ tồn tại **sau** ⓑ |
| ⛔ **CHƯA chạy** `tailscale serve` | Cả ba việc dưới đây **⛔ không phơi FLS ra đâu cả**. Chỉ **một** lệnh làm điều đó — `tailscale serve` — và nó phải **đợi** tôi xong việc `1`+`1b` của `DEV-14 §4`. Chạy sớm = phát thẻ + **73 mã hợp đồng** cho cả mạng riêng *(`§0b`)* |
| ⛔ **Đừng dán bí mật vào chat** | `Client secret` ở ⓐ ⛔ không được đi qua tay tôi. Bạn tự đặt nó vào biến môi trường — `§3` chỉ cách |
| ⏱ | ⓑ ~15′ · ⓐ ~10′ · ⓒ ~1′ |

---

## §1 · Việc ⓑ — Tailscale *(làm TRƯỚC)*

### ⓑ1 · Tạo mạng riêng của công ty — 3 phút

1. Mở **`tailscale.com`** → **`Get started`**.
2. Chọn đăng nhập bằng **Google**, và dùng **tài khoản `@apero.vn` của bạn**.
   ⛔ ĐỪNG dùng Gmail cá nhân — tên mạng riêng sinh ra từ tài khoản này, và ⛔ không đổi được về sau mà ⛔ không dựng lại.
3. Khi nó hỏi loại dùng, chọn phương án **công ty / team** *(⛔ không phải personal)*.

⚠ **Kiểm hạn mức gói miễn phí ngay lúc này** — bạn cần **3 người dùng**. Nếu gói miễn phí hiện tại ⛔ không đủ 3, dừng lại và nói tôi: có đường khác *(2 kế toán dùng chung một máy đã kết nạp)*, ⛔ nhưng nó đổi vế *"ai đang gõ"* nên tôi phải biết trước.

### ⓑ2 · Cài lên máy này — 4 phút

1. Tải bản **Windows** ở `tailscale.com/download/windows`, cài.
2. Mở Tailscale ở khay hệ thống → **`Log in`** → cùng tài khoản `@apero.vn`.
3. Mở PowerShell, kiểm:

```powershell
tailscale status
```

✅ **Xong khi:** dòng đầu ra có tên máy này kèm một địa chỉ dạng `100.x.y.z`.

### ⓑ3 · Bật MagicDNS + HTTPS — 3 phút

⛔ **Hai công tắc này ⛔ không bật sẵn, và thiếu chúng thì ⓐ ⛔ không làm được** *(⛔ không có tên HTTPS để khai `redirect_uri`)*.

1. Vào **`login.tailscale.com/admin/dns`**.
2. Bật **`MagicDNS`**.
3. Ngay dưới đó, bật **`HTTPS Certificates`**.
4. **Chép lại `Tailnet name`** hiện trên chính trang ấy — dạng `<gì đó>.ts.net`.

### ⓑ4 · Lấy tên đầy đủ của máy này — 2 phút

```powershell
tailscale cert --help
```

⛔ Đừng chạy `tailscale cert` thật vội. Tên đầy đủ đọc ở **`login.tailscale.com/admin/machines`** — cột `Machine`, dạng:

```
<ten-may>.<tailnet-name>.ts.net
```

✅ **Xong khi:** bạn có **một chuỗi** như `fls-may-dung.tailXXXX.ts.net`.
⭐ **Chuỗi này là thứ bạn đưa tôi** — nó ⛔ không phải bí mật.

### ⓑ5 · Kết nạp 2 kế toán — 3 phút

1. Vào **`login.tailscale.com/admin/users`** → **`Invite users`**.
2. Nhập email `@apero.vn` của từng kế toán.
3. Họ nhận thư → cài Tailscale trên máy họ → đăng nhập bằng chính email ấy.

✅ **Xong khi:** trang `admin/machines` hiện **3 thiết bị**.

### ⛔ ⓑ6 · **KHÔNG LÀM BÂY GIỜ**

```powershell
# ⛔⛔ ĐỪNG CHẠY — đây là lệnh phơi FLS ra mạng riêng.
# tailscale serve --bg https / http://127.0.0.1:8088
```

Ghi lại đây để bạn **nhận ra nó** nếu gặp trong hướng dẫn nào khác. Tôi sẽ nói khi đến lúc.

---

## §2 · Việc ⓐ — OAuth Client ID của Google *(làm SAU ⓑ)*

### ⓐ1 · Chọn project — 1 phút

1. Mở **`console.cloud.google.com`**, đăng nhập bằng tài khoản `@apero.vn` **có quyền quản trị**.
2. ⭐ **Dùng lại project đang chứa BigQuery** *(nơi `gcloud` của FLS đã lấy token)*, ⛔ đừng tạo project mới.
   **Vì sao:** màn hình xin quyền *(consent screen)* là **của project**. Hai project = hai màn hình phải nuôi. Và project cũ **chắc chắn** thuộc tổ chức `apero.vn` — điều kiện bắt buộc của bước sau.

### ⓐ2 · Màn hình xin quyền — 4 phút

1. Menu trái → **`APIs & Services`** → **`OAuth consent screen`**.
2. `User type` → chọn ⭐ **`Internal`** → `Create`.

   ⛔⛔ **Đây là ô quan trọng nhất của cả việc ⓐ.** `Internal` nghĩa là **chỉ tài khoản `@apero.vn` đăng nhập được** — Google chặn ở phía Google, **trước** khi chạm tới FLS. Nó cũng miễn cho ta vòng **thẩm định ứng dụng** *(mất vài tuần)* mà `External` đòi.
   ⚠ Nếu ⛔ **không chọn được** `Internal`: nghĩa là project ⛔ không thuộc tổ chức Workspace ⇒ **quay lại `ⓐ1`** và chọn đúng project.
3. Điền: `App name` = **`FLS`** · `User support email` = email bạn · `Developer contact` = email bạn.
4. `Save and Continue` qua hết các bước — ⛔ **không cần thêm scope nào** *(mặc định `email`+`profile` là đủ)*.

### ⓐ3 · Tạo Client ID — 4 phút

1. **`APIs & Services`** → **`Credentials`** → **`+ Create Credentials`** → **`OAuth client ID`**.
2. `Application type` → **`Web application`**.
3. `Name` → `FLS web`.
4. Mục **`Authorized redirect URIs`** → **`+ Add URI`** → dán **đúng** chuỗi này, thay phần trong ngoặc bằng tên lấy ở `ⓑ4`:

```
https://<ten-may>.<tailnet>.ts.net/dang-nhap/ve
```

   ⛔ **Ba chỗ sai một ly:** phải là `https` *(⛔ không `http`)* · ⛔ **không** dấu `/` ở cuối · đúng chữ `dang-nhap/ve` *(gạch ngang, ⛔ không gạch dưới)*.
   ⚠ Google có thể mất tới **5 phút** mới nhận một `redirect_uri` vừa thêm — sai thì sửa được, chỉ là **mỗi lần sửa lại chờ**.
5. `Create`. Google hiện **`Client ID`** và **`Client secret`**.

✅ **Xong khi:** bạn có hai chuỗi, `Client ID` kết thúc bằng `.apps.googleusercontent.com`.

---

## §3 · Cất bí mật — ⛔ không qua chat, ⛔ không vào git

Mở **PowerShell** trên máy này, chạy **hai** lệnh *(thay `<…>` bằng giá trị thật)*:

```powershell
[Environment]::SetEnvironmentVariable('FLS_GOOGLE_CLIENT_ID', '<Client ID>', 'User')
[Environment]::SetEnvironmentVariable('FLS_GOOGLE_CLIENT_SECRET', '<Client secret>', 'User')
```

⭐ `'User'` = lưu cho tài khoản Windows của bạn, **sống qua khởi động lại**. ⛔ Đừng dùng `'Machine'` *(mọi tài khoản trên máy đọc được)*.

Kiểm — lệnh này in ra **độ dài**, ⛔ không in nội dung:

```powershell
$env:FLS_GOOGLE_CLIENT_ID = [Environment]::GetEnvironmentVariable('FLS_GOOGLE_CLIENT_ID','User')
"ID dai $($env:FLS_GOOGLE_CLIENT_ID.Length) ky tu"
```

✅ **Xong khi:** in ra một con số khác `0`. ⛔ Phải **mở PowerShell mới** thì biến mới hiện.

⚠ `Client secret` ⛔ **không được** nằm trong bất kỳ tệp nào của kho `FLS` — kể cả tệp bị `gitignore`. Biến môi trường là chỗ duy nhất.

---

## §4 · Việc ⓒ — danh sách người được vào

Viết cho tôi **một dòng mỗi người**, gồm email `@apero.vn` và vai:

```
lanptn@apero.vn    — kế toán, người gõ chính
<...>@apero.vn     — kế toán
dungtt1@apero.vn   — COO-CFO (bạn)
```

⚠ Hôm nay **mọi người đăng nhập được đều làm được mọi thứ** *(`DEV-14 §6`)* — với **3 người** thì chấp nhận được. Người **thứ tư** thì ⛔ không, và lúc ấy phải mở `04_ROLE_PERMISSION_MATRIX` ra thi hành thật.

---

## §5 · Xong rồi thì đưa tôi **ba thứ**

| # | Thứ | Bí mật? |
|:-:|---|:--:|
| 1 | Tên đầy đủ `…ts.net` *(`ⓑ4`)* | ⛔ không |
| 2 | Câu *"đã đặt xong 2 biến môi trường"* | — |
| 3 | Danh sách email *(`§4`)* | ⛔ không |

⛔ **Đừng gửi `Client secret`.** Nếu nó lỡ đi qua chat: vào `Credentials` → `FLS web` → **`Reset secret`**, rồi đặt lại `§3`.

⇒ Có ba thứ đó, tôi làm hết `DEV-14 §4` *(7 việc + 6 cổng)*. **Trước khi có chúng** tôi vẫn làm được `1`·`1b`·`2`·`4`·`5`·`7` và **cả 6 cổng** — chúng tự đúc `id_token` giả nên ⛔ không cần Google thật.

---

## §6 · Changelog

- **v0.1** *(2026-09-11, owner hỏi *"hướng dẫn tôi cách làm từng việc một"*)*: bản đầu. ⭐ **Đổi thứ tự so với `DEV-14 §5` bản đầu**: ⓑ trước ⓐ, vì `redirect_uri` cần một tên có thật. ⛔⛔ **Và thêm `ⓑ6` — một lệnh CẤM CHẠY**: `tailscale serve` phơi FLS trong khi `phien.js` còn chở thẻ, mà cổng `kiem_phuc_vu_tep` **⛔ không thấy** *(nó canh địa chỉ nghe, còn proxy nối vào `127.0.0.1`)* ⇒ `DEV-14 §0b` + cổng `W6`.
