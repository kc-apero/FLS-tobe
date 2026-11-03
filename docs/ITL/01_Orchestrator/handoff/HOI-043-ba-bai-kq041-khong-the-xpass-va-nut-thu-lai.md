# HOI-043 — Ba bài `xfail(strict)` của `KQ-041` ⛔ thể `XPASS` bằng mã đúng spec · và nút `Thử lại` của danh sách `②b` ⛔ có từ trước

| | |
|---|---|
| **Thuộc** | `WO-042` *(và `KQ-041` — chủ ba bài là `fls-test`)* |
| **Hỏi bởi** | `fls-dev` · 2026-10-05 |
| **Loại** | `MAU_THUAN` *(Q1 · Q2 · Q3 — bài nghiệm thu ⟷ spec / phiếu)* · `THIEU` *(Q4)* |
| **Trạng thái** | ✅ `DONG` *(`fls-ba` trả `TL-043` 05/10 — Q1–Q3 phương án **1** · Q4 phương án **3** ＋ đính chính `WO-042`; việc còn lại ⇒ `fls-test` viết lại ba bài trong lượt kiểm `BG-044`; `(d)` ⇒ `WO-045`)* |
| **Chặn** | `KHONG_CHAN` — mã `(a)` `(b)` `(c)` đã làm theo `BA-06` v4.18 `§4.5 ⓥ` + `BA-07` v3.11; chỉ **cách đếm cổng** `AC-1` · `AC-2` · `AC-8` · `AC-12` *(`--runxfail … ⇒ passed`, *"đúng 3 `XPASS(strict)`"*)* ⛔ đạt được nguyên văn |

## Bằng chứng

**Q1 — `test_F3_bam_lai_chip_DANG_CHON_*` đòi điều `ⓥ` ② cấm.**
- Chỗ 1: `tests/nghiem_thu/test_kq041_mot_luat_tien_te_va_ro_may.py:221` — *`assert r["goi"] >= 4, f"⛔ không đo được: màn ⛔ gọi cửa {r}"`* *(gác "đo được" dựng theo mã **cũ**: hai lượt × hai cửa)*.
- Chỗ 2: `BA-06` v4.18 `§4.5 ⓥ` ② *(dòng 715)* — *"bấm lại chip **đang chọn** khi đang tải ⇒ ⛔ mở lượt mới (**0** `GET` thêm)"*; `WO-042` `AC-2` — *"số lượt gọi cửa **= một lượt**"*.
- Phép đo *(mã mới, `pytest --runxfail`)*: ⇒ `AssertionError: ⛔ không đo được: màn ⛔ gọi cửa {'chip': 'chua_gan', 'n': 2, 'khac': 2, 'tt': ['chua_gan', 'chua_gan'], 'goi': 2}` — **hai** `assert` thực chất *(`n == khac == 2`)* **đúng**, chỉ cái gác đỏ. Mã nào thoả `ⓥ` ② thì bài này **⛔ bao giờ** `XPASS`.

**Q2 — `test_F3_doi_chip_KHI_DANG_TAI_*` gác `goi >= 3`.**
- Chỗ 1: cùng tệp `:210` — *`assert r["goi"] >= 3`*.
- Chỗ 2: `ⓥ` ① chỉ liệt kê điều lượt cũ ⛔ được làm *(⛔ ghi `ST.dong` · ⛔ tắt cờ tải · ⛔ hiện lỗi · ⛔ đặt con trỏ trang)*; ⛔ nói lượt cũ có phải **xin tiếp** trang / cửa kế ⛔. Mã mới chọn: lượt đã bị thay **dừng** ở lần `await` kế tiếp ⇒ ⛔ xin `ro=may` cho một kết quả sẽ bị bỏ *(mỗi cửa thật ~0,9 s/trang — `KQ-041`)*.
- Phép đo *(mã mới, `--runxfail`)*: ⇒ `{'chip': 'da_gan', 'n': 1, 'khac': 1, 'tt': ['da_gan'], 'goi': 2}` — `assert` thực chất *(`tt == ['da_gan']`)* **đúng**, gác `2 >= 3` đỏ.

**Q3 — `test_F2_ca_bien_SQL_ve_so_BANG_ma_tien_te` so `ma_tien_te` với một câu SQL **của chính bài**.**
- Chỗ 1: cùng tệp `:50` — *`_SQL_VE_SO = "SELECT upper(btrim(%s::text, E' \\t\\r\\n'))"`*; `:75-80` gọi nó. Vế SQL là **chuỗi gõ trong bài**, ⛔ đọc `lenh_cho._SQL_ITL_UNG_VIEN` / `_SQL_DEM_CUNG_TE` ⇒ mã đổi gì bài cũng ⛔ thấy.
- Chỗ 2: `BA-07` v3.11 §4g bảng luật dòng *SQL* — *"vế sổ `upper(btrim(i.curr, %(tap)s))` — tập truyền **từ hằng** làm tham số; ⛔ chuỗi gõ lại trong SQL"*. Bài giữ đúng luật v3.10 mà v3.11 thay.
- Phép đo *(mã mới, `--runxfail`)*: ⇒ vẫn `[("'\\xa0VND'", '\xa0VND', 'VND'), … ("'VND\\x85'", 'VND\x85', 'VND')]` — **6 / 6** lệch như ngày `KQ-041`, vì SQL ấy ⛔ phải SQL của mã.

**Kiểm chứng ba bài viết lại đúng chỗ** *(bản sao ở scratchpad, ⛔ chạm `tests/nghiem_thu/`; chỉ đổi: `_ve_so` truyền `TAP_TRANG_TIEN_TE` làm tham số · hai gác thành `>= 2` · bỏ dấu `xfail`; mọi `assert` thực chất giữ)*:
- trên mã mới ⇒ `3 passed` *(`F2` · `F3` × 2)*;
- trên mã khi nhận *(`77737f7` ＋ chỉ tệp hằng)* ⇒ hai bài `F3` **ĐỎ đúng lý do `KQ-041`**: `tt ['chua_gan', 'da_gan', 'chua_gan'] == ['da_gan']` · `n 4 == 2`.

**Q4 — `Thử lại` của danh sách `②b`.**
- Chỗ 1: `WO-042` bảng *Màn hình* hàng *lỗi* / *mất kết nối* — *"câu lỗi của lượt **mới nhất** + `Thử lại`"*; `AC-3` — *"câu lỗi + `Thử lại` **như cũ**"*.
- Chỗ 2: `BA-06` v4.18 `§4.5 ⓥ` ③ — *"năm trạng thái **như cũ**"*. Mã: `man_f01_ghep.js` nhánh `ST.loi` *(trước `WO-042` và sau)* chỉ in `banner crit` *"⛔ Cửa lỗi: <câu>"* — **⛔ có** nút `Thử lại` *(`grep -n "Thử lại" fls/web/tep/man_f01_ghep.js` ⇒ **0**; nút ấy chỉ có ở `trang_thai.js:78` cho các khối `TT.chay` và `man_f02.js`)*. *"Như cũ"* và *"+ `Thử lại`"* ⛔ cùng đúng được.

## Phương án

| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | **`fls-test` viết lại ba bài, giữ lo gốc** *(như bản sao đã chạy ở trên)*: `F2` lấy vế SQL từ hằng `TAP_TRANG_TIEN_TE` *(hoặc gọi thẳng `lenh_cho` qua cửa `itl-candidates`)*; hai gác `F3` thành `>= 2` *(= số trang của **một** lượt `Chưa gán`)*. `AC-12` đọc lại: `pytest` **6 `xfailed`** cho tới khi `fls-test` gỡ dấu ở `KQ` | `fls-test` sửa bài của chính mình ở `KQ`; `AC-12` "đúng 3 `XPASS`" ⛔ đo được ở `BG-044` — thay bằng bằng chứng bản sao | ⭐ |
| 2 | Dev uốn mã cho khớp gác: lượt cũ **xin tiếp** cửa kế *(thoả Q2)*; **bỏ** luật ② *(thoả Q1)* | Q1: trái `ⓥ` ② + `AC-2` *(spec thua bài thử)*; Q2: thêm **một** `GET` thật ~0,9 s mỗi lần đổi chip lúc đang tải cho một kết quả bị vứt; **Q3 vẫn ⛔ thể** — bài ⛔ đọc mã | |
| 3 | *(Q4)* Giữ như cũ — **bấm lại chip đang chọn** khi ⛔ đang tải = tải lại *(đường thử lại hôm nay; bài `test_AC3_sau_loi_bam_lai_chip_THI_tai_lai` ghim)* | `WO` bảng *Màn hình* chữ *"+ `Thử lại`"* đọc là *"như cũ"* | ⭐ *(Q4)* |
| 4 | *(Q4)* Thêm nút `Thử lại` vào `banner crit` của `②b` | UI mới ⛔ có trong bản dựng `Artifacts/` *(`WO-042` cấm đổi)*; thuộc `WO-023` *(hộp/phím)* hoặc phiếu sau | |

Dev đã làm theo **⭐ 1 + ⭐ 3** trong `WO-042` *(⛔ chạm `tests/nghiem_thu/**`)*.

---

# TL-043 — trả lời *(do `fls-ba` điền bên dưới, cùng tệp)*

| | |
|---|---|
| **Quyết** | ⭐ **Q1 · Q2 · Q3 — phương án 1** *(lỗi ở **gác của bài**, ⛔ ở mã)*: `fls-test` **được phép và phải** viết lại ba bài trong **chính lượt kiểm `BG-044`**, giữ nguyên **lo gốc** của `KQ-041` *(`F-3`: rổ trộn · nhân đôi; `F-2`: SQL ⟷ Python lệch ở ký tự biên)*, kèm **chứng ĐỎ đúng lý do trên `77737f7`** *(mã khi nhận)* và **xanh trên `db0adae`**. ⛔ Phương án 2 *(uốn mã theo gác)*. ⭐ **Q4 — phương án 3 + đính chính `WO-042`**: hôm nay `②b` thử lại = **bấm lại chip đang chọn khi ⛔ đang tải** *(`man_f01_ghep.js:991`)*; chữ *"+ `Thử lại`"* ở bảng *Màn hình* + `AC-3` là **lỗi viết phiếu** của `fls-ba`, đọc là *"như cũ"*. Nút `Thử lại` **nhìn thấy được** cho `②b` ⇒ spec `BA-06` v4.19 `§4.5 ⓥ ⑤` + mã ở **`WO-045` `(e)`** *(⛔ trong `WO-042`)* |
| **Ai quyết** | `fls-ba` trong thẩm quyền spec — Q1–Q3 là **cách đo** một luật spec đã chốt *(`BA-06` v4.18 `§4.5 ⓥ` · `BA-07` v3.11 §4g)*, Q4 là chữ của **phiếu** + hành vi trạng thái màn. ⛔ câu nghiệp vụ *(con số trên màn ⛔ đổi nguồn)* ⇒ ⛔ hỏi owner |
| **Spec đã sửa** | `02_BA/06_SCREEN_SPEC.md` **v4.18 → v4.19** — `§4.5 ⓥ` đoạn v4.19 *(① lượt bị thay **được dừng ngay**, ⛔ bắt buộc xin tiếp — đóng chỗ mập mờ của Q2; ⑤ nút `Thử lại` của `②b`)* ＋ ⭐ `§4.5 ⓦ` mới *(luật `ⓥ` áp cho **mọi** lượt tải ghi trạng thái chung của màn · chế độ **chỉ đọc** khoá **chỉ** thao tác GHI)*. `BA-07` ⛔ đổi *(v3.11 đã nói đúng — tập truyền **từ hằng** làm tham số)*. Phiếu: `WO-042` thêm mục **Đính chính `TL-043`** *(⛔ viết lại dòng cũ)* · phát **`WO-045`** |

### Q1 · Q2 · Q3 — ba bài viết lại thế nào *(việc của `fls-test`, trong `KQ` kiểm `BG-044`)*

`fls-ba` đọc lại cả ba gác **đối chiếu nguyên văn** *(`Đ1` — ⛔ tin lời `HOI`)*: `tests/nghiem_thu/test_kq041_mot_luat_tien_te_va_ro_may.py:50` `_SQL_VE_SO = "SELECT upper(btrim(%s::text, E' \\t\\r\\n'))"` · `:210` `assert r["goi"] >= 3` · `:221` `assert r["goi"] >= 4`; `BA-06` v4.18 `§4.5 ⓥ` ② *"⛔ mở lượt mới (**0** `GET` thêm)"*; `man_f01_ghep.js:991` `if (c === ST.chip && ST.dang_tai) return;`. Khớp `HOI`.

| Bài | Vì sao gác cũ sai | Viết lại *(giữ lo gốc)* | Chứng ĐỎ bắt buộc trên `77737f7` *(đúng lý do — ⛔ `ImportError`, ⛔ gác)* |
|---|---|---|---|
| `test_F3_bam_lai_chip_DANG_CHON_*` | `goi >= 4` = **hai** lượt × hai cửa ⇒ chính điều `ⓥ` ② cấm. Mã nào đúng spec ⛔ bao giờ qua | gác *"đo được"* = màn **có** gọi cửa *(`goi >= 1`)*; ⭐ thêm assert **thực chất** của `AC-2`: `goi ==` số `GET` của **một** lượt `Chưa gán` — đo bằng **mỏ neo** cùng khuôn *(một cú `doi_chip('chua_gan')` đơn, hôm nay **2** = hai cửa của chip)*, ⛔ gõ số 2 cứng; giữ `n == khac ==` số hàng một lượt | `n 4 == 2` *(mỗi lệnh hai lần)* **và** `goi 4 == 2` |
| `test_F3_doi_chip_KHI_DANG_TAI_*` | `goi >= 3` đòi lượt **bị thay** xin tiếp cửa thứ hai — `ⓥ` ① ⛔ đòi *(v4.19 nói rõ: **được** dừng ngay)*; mỗi `GET` thừa ~0,9 s cửa thật cho một kết quả bị vứt | gác = **cả hai lượt đã bay**: ≥ 1 `GET` đường của `Chưa gán` **và** ≥ 1 `GET` `lenh-da-gan` *(đếm theo **đường**, ⛔ đếm tổng)*; giữ `chip == 'da_gan'` · `tt == ['da_gan']` | `tt ['chua_gan','da_gan','chua_gan'] == ['da_gan']` |
| `test_F2_ca_bien_SQL_ve_so_BANG_ma_tien_te` | vế SQL là **chuỗi của bài** ⇒ mã đổi gì bài ⛔ thấy *(`11` §6: "đo một quan hệ thì gọi hàm thật")*. ⚠ Bản sao của Dev *(truyền `TAP_TRANG_TIEN_TE` làm tham số)* **chưa đủ**: nó đo `btrim` của PG với hằng, vẫn ⛔ đọc SQL của `lenh_cho` — và trên `77737f7` đỏ vì **`ImportError`** *(hằng chưa có)*, ⛔ vì lệch | đi qua **hàm thật** `lenh_cho.ung_vien_itl` *(có ở **cả** `77737f7` lẫn `db0adae` — đã grep)* hoặc cửa HTTP `itl-candidates`, **kho TEST** *(`assert current_database() = 'fls_test'`)*: với mỗi chuỗi `CA_BIEN`, dòng tiền `curr = x` cùng số tiền với lệnh `VND` ⇒ có mặt trong ứng viên **cùng tiền tệ** ⟺ `ma_tien_te(x) == 'VND'`. Giữ 6 chuỗi `CA_BIEN` + mỏ neo `CA_THUONG` | ≥ 1 / 6 chuỗi biên lệch *(`KQ-041` đo **6 / 6** với SQL cũ)* |

- Ba bài **bỏ dấu `xfail`** khi viết lại *(chúng thành bài thường — phải **xanh** trên `db0adae`)*. ⛔ Giữ `xfail(strict)` cho một bài đã biết là ⛔ thể `XPASS`.
- Chứng đỏ: `git worktree add <thư mục> 77737f7`, chép **ba bài mới** vào đó, chạy ⇒ dán đầu ra nguyên văn vào `KQ` *(`Đ5`)*. Bài nào đỏ vì gác / vì nhập ⇒ bài ấy **⛔ đạt** yêu cầu viết lại.
- ⭐ **`AC-12` đọc lại** *(⛔ viết lại dòng `WO`)*: *"đúng 3 `XPASS(strict)` `kq041`"* ⇒ *"ba bài `kq041` viết lại: đỏ đúng lý do trên `77737f7`, xanh trên `db0adae`"*. Cổng ở `BG-044` *(6 `xfailed`)* là **đúng nền** cho tới khi `fls-test` viết lại. `AC-1` · `AC-2` · `AC-8` cùng đọc: *"`--runxfail … ⇒ passed`"* ⇒ *"bài viết lại tương ứng ⇒ passed"*. 3 bài `kq021` *(`WO-023`)* **vẫn** `xfail`.
- Q2 — lựa chọn *"lượt bị thay dừng ngay"* của Dev **đúng ý spec** *(`BG-044` yếu #2)*: ⛔ đòi Dev đổi.

### Q4 — `Thử lại` của `②b`
- Đo *(`Đ1`, grep 05/10)*: `"Thử lại"` trong `fls/web/tep/man_f01_ghep.js` **0** chỗ; nhánh lỗi chỉ in `banner crit` *"⛔ Cửa lỗi: <câu>"* *(`:1473`)*; nút `Thử lại` có ở `trang_thai.js:78` *(khung `TT.chay`)* · `man_f02.js:1050` · `:1463`. ⇒ `WO-042` viết *"+ `Thử lại`"* là **sai sự thật về mã**, ⛔ phải yêu cầu mới.
- Quyết: `WO-042` **⛔ đòi** nút *(`AC-3` nghiệm thu theo "như cũ" + đường bấm lại chip — bài `test_AC3_sau_loi_bam_lai_chip_THI_tai_lai` của Dev ghim)*. Nhưng đường thử lại hôm nay **vô hình** *(câu lỗi ⛔ nói "bấm lại chip")* — trái luật năm trạng thái *(lỗi phải có lối ra)* ⇒ `BA-06` v4.19 `ⓥ ⑤` + `WO-045 (e)`.

### `(d)` + `Xem thêm` bị khoá *(từ `BG-044`)* ⇒ **`WO-045`**
Một phiếu **mới**, ưu tiên **CAO**, làm **sau khi `WO-042` `DONG`** *(cùng hai tệp `man_f01_ghep.js` · `man_f01_lenh.js`, dựng trên `_luot` của `WO-042`)* và **trước** `WO-015` · `WO-023`. Thứ tự bên trong theo **tầm** — chi tiết + lý do ở [`WO-045`](WO-045-luot-tai-moi-nhat-moi-man-va-xem-them-chi-doc.md). Tóm: ① `F01G` `mo_lenh` / `tai_toan_so` *(#2 #3 — ứng viên của lệnh **khác** hiện dưới lệnh đang mở, và `gan` gửi `itl_id` lấy từ chính danh sách ấy kèm `ma_lenh` đang mở — chỗ **duy nhất** trong 21 chạm sát một cú GHI)* · ② `F01L` lưới #6 #7 ＋ `Xem thêm` / `Tìm tiền` bị khoá ở máy chỉ đọc · ③ `F01` #10 #11 · ④ `F04` #17 #18 · `(e)` nút `Thử lại` `②b`.

⭐ **"Xem thêm" bị khoá ảnh hưởng ai?** Chế độ **chỉ đọc là MẶC ĐỊNH** *(`BA-08` `NFR-I03`: `--cho-ghi` mặc định **TẮT**)* ⇒ **mọi** người mở sổ thật mà ⛔ định ghi: CFO/COO xem *(`11` §1: owner là lớp **xem & quyết**; `BA-06` `UI-F6` cùng tinh thần ở `F05`)*, kế toán tra cứu trước khi bật ghi, và **mọi phép đo của `fls-test` / `fls-ba` trên 8088** *(chính `WO-042 AC-7` chỉ đo được trang đầu — `BG-044` yếu #5)*. Lưới `F01L` trang **50** *(`man_f01_lenh.js:554` `limit=50`)* ⇒ mỗi rổ chỉ thấy 50 dòng đầu: `may` chưa nhận theo lô **50 / 120** · `nguoi` **50 / 616** · `khong` **50 / 801** *(số `/ro` sổ thật, `BG-044` `AC-7`, 8097 chỉ đọc 05/10)*, và màn **⛔ nói** là còn — nút xám kèm câu *"Mọi thao tác ghi bị trả 405"* cho một thao tác **đọc**. Kế toán ghép thật chạy `--cho-ghi` ⇒ ⛔ bị. ⇒ Hại là **đọc thiếu im lặng** ở vai xem & quyết, ⛔ ghi sai.
