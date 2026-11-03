# 08 — NFR: yêu cầu phi chức năng đo được *(dự án ITL)*

**Version:** v1.4 | **Chủ sở hữu:** BA/PO + Tech Lead | **Mốc đo:** 2026-09-21 *(`NFR-I01`/`I04`: 2026-10-01 · `NFR-I29`: 2026-10-02 · `NFR-I30`: 2026-10-05)*

> ⭐⭐ **Mỗi dòng dưới đây có MỘT CON SỐ ĐO ĐƯỢC hay MỘT CƠ CHẾ ĐÃ CHẠY.** Chỗ
> nào chưa đo được thì ghi thẳng **⛔ chưa đo** — ⛔ không điền một con số mong
> muốn rồi để người sau tưởng nó đã được kiểm.

⛔⛔ **Bản v0.1 (17/07) là bản copy chương trình FIN-ERP**, và nó **tự khai**
điều đó ở dòng đầu. Trung thực — nhưng sau **bảy tuần**, một tệp tự nói *"đừng
dùng tôi"* vẫn là **một tệp không dùng được**. Bản này thay hẳn nó. Bản cũ
xem trong `git log`.

---

## §1 · Đúng đắn — thứ ⛔ KHÔNG được đánh đổi

| ID | Yêu cầu | Đích **đo được** | Cưỡng chế ở đâu |
|---|---|---|---|
| `NFR-I01` | **Sổ chỉ-thêm.** ⛔ Không đường code nào `UPDATE`/`DELETE` một dòng đã vào sổ | **0** câu `UPDATE`/`DELETE` trên `fls_itl` · `fls_adjustment` · `fls_journal` · `fls_pm_link` · `fls_pm_unlink` · `fls_queue_event` | ⛔⛔ **Sửa v1.2 *(`KQ-002 F-5`, đo 01/10)* — cưỡng chế KHÔNG đều hai vế:** ⓐ `fls_itl` — **DB**, **3** trigger *(`trg_fls_itl_inv_i03` · `trg_fls_itl_inv_i04a` · `trg_fls_itl_chan_truncate`)*, `INV-I03`; ⓑ năm bảng còn lại — ⛔ **CHỈ QUY ƯỚC MÃ**: `pg_trigger` **0** trigger, `pg_rules` **0**; `grep UPDATE/DELETE` trên chúng trong `fls/` = **0**, trong `tools/` = **2** tệp *(`don_ly_do_sai.py`, `verify_sua_duoc_gi.py` — công cụ dọn/kiểm, ⛔ đường ghi nghiệp vụ)*. ⇒ **`GAP-DB-06`** *(`BA-05:1756`, ghi vào dashboard §4 01/10)*. ⚠ Từ 01/10 các bảng ấy giữ **dòng người đầu tiên** *(UAT)* ⇒ lỗ này nay bảo vệ dữ liệu thật. ⛔ Câu cũ *"DB — trigger; ⛔ không phải quy ước"* chỉ đúng cho `fls_itl` |
| `NFR-I02` | **Máy chỉ ĐỌC nguồn.** FLS ⛔ không bao giờ ghi ngược Gsheet / `fps_*` / P100 | **0** đường ghi ngược | `QĐ-ITL-34` · `QĐ-ITL-45`; bảng tuyến khai từng bảng mỗi cửa chạm, có cổng `soi_bang_tuyen` **17/17 khớp SQL thật** |
| `NFR-I03` | **Cửa mặc định CHỈ ĐỌC.** Nhóm ghi phải **gõ tường minh** mới mở | `--cho-ghi` mặc định **TẮT** ⇒ mọi đường ghi trả `405` | `tools/chay_cua.py`; kết nối chỉ-đọc cưỡng chế ở tầng **PostgreSQL** |
| `NFR-I04` | **Ghi mà ⛔ không nói lý do là ⛔ không ghi được** — ⚠ **thu hẹp v1.2 *(`QĐ-ITL-149`, owner 01/10: *"bỏ yêu cầu lý do cho cú Ghép"*)*:** `match` · `unmatch` *(và `done`, `QĐ-ITL-72`)* nhận thiếu lý do; máy ghi **lý do mặc định có nhãn** `(may dien) …` ⇒ cột `reason` **⛔ bao giờ rỗng** *(`BA-07 §4h ⓼`)* | cửa **NO** — `FLS-UNMAPPED-HIDDEN` *(ở các cửa còn bắt buộc)*; ở `match`/`unmatch`: **0** dòng `fls_queue_event` mang `reason` rỗng | `INV-I16` *(phạm vi v0.14)* |
| `NFR-I05` | **⛔ Không mặc định im lặng.** Tra không được thì **khai `UNMAPPED`** | `#N/A` giữ nguyên trên màn, ⛔ không thay bằng một giá trị đẹp | `INV-I16`; đo: **6.691 dòng** `hd` rỗng vẫn hiện `#N/A` |
| `NFR-I06` ⭐ | **Bản khai rỗng = máy ⛔ KHÔNG BIẾT** — ⛔ không phải *"mọi giá trị đều sai"* | danh mục `0` dòng ⇒ cửa ⛔ không chặn, **và màn nói ra chỗ rỗng** | `INV-I17` *(04/09)* |

## §2 · Tốc độ — số đo thật, ⛔ không phải số mong muốn

| ID | Yêu cầu | Đo được | Ghi chú |
|---|---|---|---|
| `NFR-I07` | Một trang sổ | **200 dòng**/trang · thân `canon` **393 B/dòng** ⇒ 500 dòng ≈ **584 KB / 0,04 s** | ⛔ Con số *"vài MB"* trong ghi chú cũ **chưa ai đo** — đã đo lại |
| `NFR-I08` | Lưu theo lô | **2,5 s** sau phím cuối · rút-rồi-mới-bắn · dừng ở lỗi đầu tiên | ⛔ **Không có nút Lưu** *(`06_SCREEN_SPEC` §1-8)* |
| `NFR-I09` ⚠ | `GET /gates` | **16,1 s** trong khi client chờ **10 s** ⇒ **5 bài ĐỎ mà ⛔ không phải lỗi code** | ⛔⛔ **`GAP-KHO-02`** — kho test phình **33.492 dòng**. ⛔ **Đừng nới `timeout`**: nới là giấu |
| `NFR-I10` | Vẽ màn trên máy kế toán | ⛔ **CHƯA ĐO** | `GAP-SCR-03` — thuộc **`B7 · UAT`**, máy ⛔ không đóng được |
| ⭐ `NFR-I30` *(v1.4)* | **Một trang danh sách việc ≤ `2 s`** — cửa `/queue` *(`F01` hàng chờ)* và `/lenh-cho` *(`F01L`)*, **mọi** tiền tệ, **mọi** trang *(trang đầu **và** mọi trang theo con trỏ)*, trên **sổ thật**. Đo bằng **đồng hồ** quanh **hàm thật** *(`doc_hang_cho` · `doc_lenh_cho`)* qua `noi_chi_doc` — ⛔ đếm lượt hỏi kho *(`11` §6: *"≤ N lượt"* xanh ở 3 lượt khi thật 126 lượt / 67,7 s)* | **Đo trước rồi khai** *(`fls-ba` 05/10, hàm thật, chỉ đọc, `limit=50`)*: `/queue` trang đầu `HKD` **0,12** · `SGD` **0,07** · `USD` **0,09** · `VND` **0,09 s**; trang 2 `SGD` **0,07** · `USD` **0,08 s** — ⛔ **trang 2 `VND` `104,33 s`** *(`KQ-050`: **95,1 / 81,1 s** qua cửa 8088)*. `/lenh-cho` trang 1–4 `VND` · `USD` · ⛔ lọc: **0,64–0,74 s** | Ngưỡng `2 s` ≈ **2,7 lần** trang lành chậm nhất đã đo *(`/lenh-cho` 0,74 s)* và ≈ **52 lần** nhỏ hơn trang `VND` hỏng — đủ rộng để ⛔ đỏ oan theo nhiễu máy, đủ hẹp để bắt lại đúng lớp lỗi này. ⚠ Số `fls-ba` chọn; owner muốn khác thì đổi **một** số. Lật hết `VND` *(4.242 dòng = **85** trang)* ở 104 s/trang *(84 trang sau trang đầu)* ≈ **2,4 giờ** ⇒ kế toán bỏ cuộc. Mã ⇒ `WO-051` |

## §3 · An toàn & riêng tư

| ID | Yêu cầu | Đo được |
|---|---|---|
| `NFR-I11` | Thẻ phiên | `HS256`, khoá **≥ 32 ký tự** *(cửa **NO** nếu ngắn hơn)*; hạn mặc định **8 giờ** — ⛔ **không có chế độ "không hạn"** |
| `NFR-I12` | Cửa chỉ nghe **máy này** | mặc định `127.0.0.1`; ⛔ cửa **TỪ CHỐI** phục vụ màn hình nếu địa chỉ ⛔ không phải loopback |
| `NFR-I13` ⭐⭐ | ⭐ **MANG CÓ CÂN NHẮC — đã ĐO, và chặn bằng danh sách TRẮNG** *(owner phát biểu lại 17/09)* | Lời hứa gốc: **8 cột** `PM_COT` của `fls_pm_line` **cố ý ⛔ không lấy** Tên tài khoản · Số tài khoản · Ghi chú · Diễn giải. ⚠ **Cái giá đã đo:** xếp ứng viên ghép lệnh mất **hai trục** *(ngày · người nhận)* ⇒ trong **25 dòng** thử chỉ **1 dòng** có ứng viên đủ mạnh *(`GAP-JOIN-04`)*.<br>⛔ **Vòng ① — cột `tho`** *(migration `0021`/`0022`, 11/09)*: nó chở **cả hàng thô** của `PM_Unpivot` và **⛔ không đi qua lệnh cấm ấy**. Đo được: chuỗi dạng `%@%` ở `Ghi chú` **371** · `Số tài khoản` **147** · `Tên tài khoản` **119**; giá trị hay gặp của `Tên tài khoản` có ⛔ **`HA THU PHUONG` 896**. ⇒ **Tên người thật, số tài khoản thật**, trong một kho ⛔ không mã hoá cột và ⛔ không phân quyền — `GAP-DB-07`, xem `BA-05 §DD-I11 B1`.<br>⛔ **Vòng ② — `QĐ-ITL-128`** *(17/09)*: owner **mở lại** `QĐ-ITL-92` ⇒ `Description` *(diễn giải sao kê)* **ĐƯỢC ĐỌC**, `6/6` trường. Quyết định ấy **có đo trước**: `58/60` sheet `R \|`, `7.712` ô có chữ — tên NGƯỜI ~**4,3–4,8%** · số điện thoại **2,3%** · dạng số giấy tờ **9,5%**, cân với **23,0%** tín hiệu ghép.<br>⇒ ⭐⭐ **PHÁT BIỂU CHÍNH THỨC — owner chốt 17/09, thay câu cũ *“⛔ không mang dữ liệu cá nhân”*:**<br>**① Hệ CÓ mang** một phần dữ liệu có thể chứa thông tin cá nhân, và điều đó là **quyết định có chủ đích**, ⛔ không phải sơ suất — `QĐ-ITL-128` giữ nguyên.<br>**② Mỗi lần mở đều phải ĐO TRƯỚC, cả hai vế.** Tiền lệ: `58/60` sheet · `7.712` ô · rủi ro ~`4,3–4,8%` tên người **cân với** `23,0%` tín hiệu ghép. ⛔ Không mở vì *“chắc là ổn”*.<br>**③ Chặn bằng danh sách TRẮNG ở TỪ VỰNG, ⛔ không phải danh sách ĐEN ở dữ liệu** — `RE_TRUONG_CAM` + khối nhân sự `9`…`14` cấm *(`QĐ-ITL-107`)*, canh bởi `test_tu_vung_doc_duoc_KHONG_duoc_chua_truong_CAM`. Danh sách **ĐEN luôn thua** khi nguồn thêm cột, và **vòng ① là bằng chứng nó đã thua**.<br>**④ Hai chỗ chở dữ liệu ấy phải được NÊU TÊN**, ⛔ không giấu trong một câu tổng quát: cột `tho` của `fls_pm_line` · cột `memo` của `fls_itl`.<br>⚠ **Việc còn nợ, khai thẳng:** kho ⛔ **chưa** mã hoá cột và ⛔ **chưa** phân quyền theo hàng — `GAP-DB-07` **vẫn mở**. Phát biểu này nói *“mang có cân nhắc”*, ⛔ **không** nói *“đã bảo vệ đủ”*. |
| `NFR-I14` | Hai thư mục ⛔ không bao giờ vào git | `sao_luu/` · `hien_vat/` — chúng mang `Diễn giải`, có thể chứa tên người |

## §4 · Giữ cho hệ ⛔ không già đi trong im lặng

| ID | Yêu cầu | Đo được |
|---|---|---|
| `NFR-I15` | Bộ phép thử | **1024 bài** · ⛔ **5 đỏ có sẵn** *(đều là `NFR-I09`)*. ⭐ Luật số một: *"cổng chưa từng thấy đỏ là cổng chưa biết có sống"* ⇒ mọi cổng mới phải **bị phá có chủ ý** và **đỏ thật** trước khi tin |
| `NFR-I16` | Ranh giới tầng | **9** hợp đồng `import-linter`, **0** vi phạm *(~~8~~ — đo lại 17/09: `9 kept · 0 broken`)*. Then chốt: `fls.api` ⛔ không được biết tầng kho · `fls.web` chỉ được gọi `fls.api` |
| `NFR-I17` ⭐ | **Tài liệu ⛔ không được già hơn máy** | **63 phép so SỐ SỐNG** *(`tools/kiem_so_song.py`)* — mỗi phép khớp **đúng một lần** và khớp **đúng con số máy đo**; nó **tự đếm cả chính nó** |
| `NFR-I18` | Một nguồn tên cột | tiêu đề lưới **sinh từ** `ledge_spec` + `canon/spec` ⇒ ⛔ **không một tên cột tiếng Việt nào gõ tay**; cổng đối chiếu **hai chiều** với cửa thật |
| `NFR-I19` | Một nguồn mã màu | **1** tệp được phép có mã màu *(`tokens.css`)*; bài quét NO nếu tệp khác có `#rrggbb` |

## §4b · ⭐⭐⭐ DÙNG ĐƯỢC — và cả bộ này trước `21/09` có **`0`** yêu cầu loại ấy *(`QĐ-ITL-148`, chặng `B0`)*

> ⛔⛔⛔ **Quét cả `BA-08` ngày `21/09`: ⛔ không một chữ `WCAG` · `tương phản` · `focus` · `aria` · `bàn phím`.** Và đó ⛔ không phải sơ suất nhỏ — nó là lý do **một thứ đã có thể mất mà ⛔ không ai thấy**.
>
> ⭐⭐ **Nghịch lý làm mục này cấp bách:** bản thiết kế `21/09` **làm TỐT HƠN** mọi yêu cầu chưa từng viết — `aria-current`, vòng focus, **`9`** phím tắt, nền sáng ／ tối đầy đủ. ⛔ Nhưng ⛔ **không cổng nào giữ** ⇒ lần sửa sau **rơi mất trong im lặng**, đúng hình `339 → 735`: thêm thì ai cũng thấy, **mất thì ⛔ không ai thấy**.

| ID | Yêu cầu | Đo được |
|---|---|---|
| ⭐⭐ `NFR-I24` | **Màn LÀM đi được bằng bàn phím, ⛔ không cần chuột** | `SCR-F01`: mở lệnh · di con trỏ · chọn ứng viên · gán · quay lại — **đủ `9` phím** *(`↑` `↓` `←` `→` `Enter` `Esc` `/` `k` `j`)*. ⛔ Bài thử đi hết **một vòng ghép** ⛔ không dùng một sự kiện chuột nào |
| ⭐⭐ `NFR-I25` | ⛔ **`Enter` ⛔ KHÔNG được gán ở ca lệch tiền** | `INV-I16` ở tầng ngón tay. ⛔ **`45%`** ca ⛔ không có ứng viên khớp đúng tiền ⇒ nếu `Enter` vẫn gán được thì màn **dạy người ta gật bừa**. Đo: bài thử bấm `Enter` trên ca lệch ⇒ **`0`** mối nối mới |
| ⭐ `NFR-I26` | **Chỗ đang đứng phải nhìn thấy được** | Mọi phần tử nhận bàn phím có **vòng focus** *(`--focus-ring`)*; dòng đang trỏ mang `aria-current`. ⛔ Bỏ `outline` mà ⛔ không thay bằng gì ⇒ bài **NO** |
| ⭐ `NFR-I27` | **Hai nền — sáng ／ tối** | Trang theo cài đặt người xem *(`prefers-color-scheme`)* ＋ công tắc *(`data-theme`)*. ⛔ Mọi màu khai ở `:root`; một màu **chỉ** sống trong khối `@media` hay `[data-theme]` ⇒ nền kia mất chữ. ⭐ Đo: **`2`** khối × **`17`** token — **một nửa** hệ token là cho nền tối |
| ⭐⭐ `NFR-I28` | ⛔ **Trạng thái "⛔ không có" phải ĐỌC ĐƯỢC, ⛔ không phải một ô trống** | Ba câu **⛔ không được lẫn**: *"⛔ chưa có dữ liệu"* ≠ *"⛔ chưa đọc được"* ≠ *"⛔ không có"*. ⭐ Ca thật đang chờ: `dien_giai` `null` mang **hai** nghĩa *(`3` rỗng · `26` ⛔ chưa nối được)*; khối *«Xem đủ trường»* có **`41`** hình dạng `tho` |
| ⭐ `NFR-I29` *(v1.3)* | **Chữ mang nghĩa phải đọc được — tương phản ≥ `4,5 : 1` với nền thật của nó** *(mức WCAG AA cho chữ thường; mọi cỡ chữ FLS đang dùng < `18px`)*. Ký hiệu **một ký tự** mang nghĩa mà **cùng màn** có chú giải bằng chữ *(ô `.tg` `①②③④≠`)* ≥ **`3 : 1`**. ⛔ Áp cho: nút **khoá** *(`disabled`)* · dấu trang trí *(`::marker`, mũi tên)* | Đo 02/10 *(`fls-ba`, công thức WCAG trên `fls/web/tep/tokens.css`, **9** nền: `surface` · `page` · `alt` · `label-bg` · `crit-bg` · `warn-bg` · `good-bg` · `info-bg` · `edit-h-bg`)*: `--ink` **14,39–16,73** · `--muted` **4,81–5,59** · `--accent` **4,76–5,53** · `--good` **4,52–5,26** · `--info` **4,44–5,17** · `--crit` **4,41–5,13** · `--warn` **3,14–3,65** · `--faint` **2,12–2,47** ⇒ `--faint` đạt `3 : 1` trên **0 / 9** nền, `--warn` đạt `4,5 : 1` trên **0 / 9**. Ca đo bằng máy trên màn thật: chữ nghĩa chú giải bậc **2,17 : 1** *(`KQ-036 F-4`)* ⇒ `WO-037`. ⛔ **Chưa phân loại** *(chữ nghĩa hay khoá / trang trí)*: **22** chỗ `color:var(--faint)` trong `hinh.css` *(2 chỗ vào `WO-037`)* · **15** chỗ `color:var(--warn)` ⇒ phần còn mở của `GAP-NFR-01` |

⭐ **Vì sao mấy cái này là `NFR` chứ ⛔ không phải đặc tả màn:** chúng đúng cho **mọi** màn LÀM, và chúng là thứ **⛔ không ai nhớ kiểm** khi sửa một nút. ⇒ Đặt ở đây để có **mã** mà bài thử gọi tên.

⚠ *(v1.3 — đính chính: ngưỡng **đã khai** ở `NFR-I29` sau khi đo **9** token chữ × **9** nền 02/10; câu dưới giữ làm biên bản. Nền tối: `fls/web/` có **0** khối `prefers-color-scheme`/`data-theme` ⇒ ⛔ có gì để đo — `NFR-I27` hôm nay chỉ sống ở bản dựng `Artifacts/`)* ⛔ **Cố ý ⛔ CHƯA khai:** ngưỡng tương phản `WCAG` bằng số. Hệ token đang có **⛔ chưa ai đo** tỷ lệ tương phản, và khai một ngưỡng **⛔ chưa đo** là khai một cổng sẽ đỏ ngay hoặc ⛔ không bao giờ chạy. ⇒ `GAP-NFR-01` — đo trước, khai sau.

## §5 · Việc còn mở — ⛔ chưa đo được, và nói thẳng

| ID | Còn thiếu gì |
|---|---|
| `NFR-I10` | Cảm giác khi gõ · thời gian vẽ · `346px` cột khoá có đủ · `430px` panel có đủ ⇒ **`B7 · UAT`** |
| `NFR-I20` | **Nhịp chốt kỳ** *(flash T+? · final T+?)* — ⛔ chưa ai chốt; `GAP-PLAN-04` |
| `NFR-I21` | **Sao lưu / khôi phục** — `RPO`/`RTO` ⛔ chưa ai chốt cho FLS |
| `NFR-I22` | **Nhiều hơn một máy** — hôm nay `actor` là *"ai khởi động máy này"*; chạy cho nhiều người thì chỗ ấy phải thành **đường đăng nhập thật** *(`GAP-WEB-01`)* |
| `NFR-I23` | **Hai người sửa một ô** — cửa ghi ⛔ không thấy *(`GAP-SCR-09`)*; màn lách bằng một phép **kiểm**, ⛔ không phải một **bảo đảm** |

## Changelog
- **v1.4** *(2026-10-05, `fls-ba` — `KQ-050 F-1`)*: ⭐ **Thêm `NFR-I30` — một trang danh sách việc ≤ `2 s`** *(`/queue` · `/lenh-cho`, mọi tiền tệ, mọi trang, sổ thật, đồng hồ quanh hàm thật)*. Trước v1.4 `§2` chỉ có `NFR-I07` *(trang **sổ** `/ledger`)* — ⛔ ngưỡng nào cho trang hàng chờ, nên trang 2 `VND` **104,33 s** ⛔ phạm luật nào. **Đo trước rồi khai**: **18** trang lành *(6 `/queue` · 12 `/lenh-cho`)* **0,07–0,74 s**, 1 trang hỏng.
- **v1.3** *(2026-10-02, `fls-ba` — `KQ-036 F-4`, `GAP-NFR-01` một phần)*: ⭐ **Thêm `NFR-I29` — ngưỡng tương phản** *(chữ nghĩa ≥ `4,5 : 1`, ký hiệu một ký tự có chú giải ≥ `3 : 1`)*, **đo trước rồi khai**: 9 token chữ × 9 nền của `tokens.css` *(bảng ở dòng `NFR-I29`)*; `--faint` ⛔ đạt `3 : 1` trên nền nào, `--warn` ⛔ đạt `4,5`. Ca màn thật `2,17 : 1` *(chú giải bậc)* ⇒ `WO-037`. Còn mở: phân loại **22** chỗ `--faint` + **15** chỗ `--warn`, và nền tối *(app **0** khối)*.
- **v1.2** *(2026-10-01, `fls-ba` — `KQ-002 F-5` + `QĐ-ITL-149`)*: ⛔⛔ **`NFR-I01` khai một trigger ⛔ có thật** — câu cũ nói *"DB — trigger"* cho `fls_adjustment`·`fls_journal`·`fls_pm_unlink`; đo `pg_trigger` 01/10: **3** trigger, **cả 3 trên `fls_itl`**. Nay tách hai vế: `fls_itl` = DB · năm bảng sổ vết = **chỉ quy ước mã** ⇒ trỏ `GAP-DB-06`. ⚠ **`NFR-I04` thu hẹp**: `match`/`unmatch` nhận thiếu lý do, máy điền lý do mặc định có nhãn ⇒ vết ⛔ rỗng.
- **v1.1** *(2026-09-21, `QĐ-ITL-148` — chặng `B0` của plan màn ghép)*: ⭐⭐⭐ **Thêm `§4b` DÙNG ĐƯỢC — `NFR-I24`…`I28`. Trước hôm nay cả tệp này có `0` yêu cầu loại ấy:** quét sạch, ⛔ không một chữ `WCAG` · `tương phản` · `focus` · `aria` · `bàn phím`. ⭐⭐ **Và nghịch lý mới là thứ làm nó cấp bách:** bản thiết kế `21/09` **làm TỐT HƠN** mọi yêu cầu chưa từng viết — `aria-current`, vòng focus, `9` phím tắt, hai nền đầy đủ. ⛔ Nhưng ⛔ **không cổng nào giữ** ⇒ lần sửa sau **rơi mất trong im lặng**, đúng hình `339 → 735`: **thêm thì ai cũng thấy, MẤT thì ⛔ không ai thấy**. ⭐ Nặng nhất là `NFR-I25` — **`Enter` ⛔ KHÔNG được gán ở ca lệch tiền**: `45%` ca ⛔ không có ứng viên khớp đúng tiền, nên một phím `Enter` dễ dãi **dạy người ta gật bừa**; đây là `INV-I16` ở **tầng ngón tay**, và tầng ấy ⛔ chưa từng có bài nào. ⭐ `NFR-I28` gom ba câu ⛔ **không được lẫn** *(«⛔ chưa có dữ liệu» ≠ «⛔ chưa đọc được» ≠ «⛔ không có»)* và nêu **hai ca thật đang chờ**: `dien_giai` `null` mang **hai** nghĩa *(`3` rỗng · `26` ⛔ chưa nối được)*, và khối *«Xem đủ trường»* có **`41`** hình dạng `tho`. ⚠ **Cố ý ⛔ CHƯA khai ngưỡng tương phản bằng số** — hệ token ⛔ chưa ai đo, và khai một ngưỡng **⛔ chưa đo** là dựng một cổng sẽ đỏ ngay hoặc ⛔ không bao giờ chạy ⇒ `GAP-NFR-01`, đo trước khai sau. ⭐ `§4b` **⛔ không** đụng `NFR-I13` *(phát biểu dữ liệu cá nhân, owner `17/09`)*: quyết định `21/09` *(hiện nguyên tên người nhận)* là **một ca cụ thể** của `NFR-I13 ①`, ⛔ không phải một luật thứ hai.
- **v1.0** (2026-09-04): ⭐⭐ **Viết lại HẲN — dẫn xuất cho ITL, thay bản copy chương trình.** 23 NFR, mỗi dòng có **một con số đo được** hay **một cơ chế đã chạy**; 5 dòng ⛔ **chưa đo được** thì ghi thẳng là chưa đo *(`§5`)*, ⛔ không điền số mong muốn. ⛔ Bản v0.1 tự khai *"đừng dùng làm căn cứ build ITL"* và đứng yên **bảy tuần** — một tệp tự nói *"đừng dùng tôi"* vẫn là một tệp **không dùng được**.
- v0.1 (2026-07-17): Khởi tạo 14 NFR của **chương trình FIN-ERP** *(⛔ không phải ITL)*; 2 ô `???` chờ chốt. Xem `git log`.
