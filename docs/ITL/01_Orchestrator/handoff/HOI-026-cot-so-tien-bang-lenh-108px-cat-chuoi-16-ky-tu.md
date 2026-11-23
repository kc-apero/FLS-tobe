# HOI-026 — Cột `Số tiền` của **bảng danh sách lệnh** *(màn ghép, `108px`)* cắt chuỗi `2.259.942,94 USD` — và đã cắt `11.742.361.787 VND` **từ trước** phiếu

| | |
|---|---|
| **Thuộc** | [`WO-022`](WO-022-in-tien-theo-tien-te.md) `AC-7` |
| **Hỏi bởi** | `fls-dev` · 2026-10-02 |
| **Loại** | `LECH_DU_LIEU` *(`WO` nói *"`11.742.361.787 VND` **18** ký tự **đã vừa**"* — đo được: ở **cột này** nó **⛔ vừa**)* |
| **Chặn** | `KHONG_CHAN` — mọi phần khác của `WO-022` xong và bàn giao ở [`BG-027`](BG-027-ban-giao-wo-022.md); **chỉ** ô `Số tiền` của bảng danh sách lệnh *(màn `②b Gán lệnh chi`, view ①)* ⛔ đạt `AC-7` |

## Bằng chứng
- Chỗ 1 · `WO-022` `AC-7`: *"ô số tiền ở **danh sách lệnh**, thẻ, hộp ②, lưới `F02` ⛔ bị cắt cho chuỗi USD dài nhất sổ hôm nay `2.259.942,94 USD` *(**16** ký tự — ⛔ dài hơn `11.742.361.787 VND` **18** ký tự **đã vừa**)*"*. Cùng phiếu, mục **Màn hình**: *"Bản dựng ở `02_BA/Artifacts/` **⛔ đổi** *(chỉ đổi chữ in trong ô số tiền đã có; ⛔ token, ⛔ lớp CSS mới)*"*.
- Chỗ 2 · `fls/web/tep/hinh.css:853` — `.mcols{grid-template-columns:62px 92px 96px minmax(160px,1fr) 104px **108px** 100px 92px 20px minmax(190px,1.1fr) 116px}` *(cột thứ 6 = `Số tiền`, `man_f01_ghep.js` `COT_BANG`)*.
- Phép đo · Chrome headless **1440×900**, máy **8099** chỉ đọc trỏ **kho TEST** *(dòng dựng riêng — `run` `NAP-2000-01-01-U26FD99`)*, thay chữ **trong chính ô `.mcell.r` thật** rồi đo `getBoundingClientRect` *(kịch bản `scratchpad/wo022_do_cot.mjs`)*:

| Chuỗi | Ký tự | Rộng chữ *(px)* | Rộng ô *(px)* | Cắt? |
|---|--:|--:|--:|:-:|
| `2.259.943 USD` *(hàm in CŨ)* | 13 | 95,2 | 108 | ⛔ |
| `999.999,99 USD` | 14 | 102,5 | 108 | ⛔ |
| `2.259.942,94 USD` *(hàm in MỚI)* | 16 | **117,2** | 108 | ✅ **cắt** — ảnh: `…,94 US` |
| `1.565.307,14 HKD` | 16 | 117,2 | 108 | ✅ cắt |
| `11.742.361.787 VND` *(cả hai hàm)* | 18 | **131,8** | 108 | ✅ **cắt — từ trước `WO-022`** |

  ⇒ Ngưỡng: chuỗi **≥ 15** ký tự bị cắt *(≈ 7,33 px/ký tự `tabular-nums`)*. Bốn chỗ còn lại của `AC-7` **⛔ cắt** *(thẻ `150/150` · rail `117/117` · hộp ② `484/484` · lưới `F02` `157/157` · panel `F02` `180/180` — `scrollWidth/clientWidth`)*.
- Tầm trên ảnh PM thật *(chỉ `SELECT`, run `NAP-2026-10-02-PME7F31617`, mẫu số **3.820** dòng lệnh)*:

| Nhóm | Dòng lệnh | Vì sao |
|---|--:|---|
| Ngoại tệ **mới** bị cắt *(`1.000.000` ≤ \|tiền\| < `100.000.000`)* | **27** *(USD 26 · SGD 1 / 1.099 ngoại tệ)* | `,00`/`,dd` thêm 3 ký tự |
| VND **đã** bị cắt từ trước *(\|tiền\| ≥ `100.000.000` ⇒ ≥ 15 ký tự)* | **425 / 2.721** | cột `108px` ⛔ đủ cho số tiền VND ≥ 100 triệu — **⛔ do phiếu này** |
| Ngoại tệ đã bị cắt từ trước *(≥ `100.000.000`)* | 1 *(USD)* | — |

## Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | Nới cột `Số tiền` của `.mcols` **`108px → 136px`** *(vừa 18 ký tự `131,8px` + lề)* — ⛔ token mới, ⛔ lớp mới; chỉ một con số trong `grid-template-columns` | Đổi **bản dựng** *(phải cập nhật `02_BA/Artifacts/` + `BA-06`)*; `+28px` lấy từ cột co giãn `Nội dung` *(`minmax(160px,1fr)`)* — ở 1440 cột ấy còn ≈ 220px. Sửa luôn **425** dòng VND đang cắt | ⭐ |
| 2 | Nới vừa đủ **16** ký tự *(`108px → 124px`)* | Chỉ trả nợ phiếu này *(27 dòng ngoại tệ)*; **425** dòng VND vẫn cắt | |
| 3 | Giữ `108px`, thêm `title` = chuỗi đầy đủ + dấu `…` | Người vẫn phải **di chuột** để đọc số tiền — đúng thứ `C5` muốn xoá *(⛔ mở thêm gì để biết số)* | |
| 4 | Giữ nguyên, ghi `GAP` | `AC-7` ⛔ đạt ở cột này; 452 dòng in thiếu ký tự cuối *(mã tiền tệ hoặc xu)* | |

⚠ Dev **⛔ tự đổi CSS**: `WO-022` cấm đổi bản dựng, và bề rộng cột là quyết định thiết kế của `fls-ba`.

---

# TL-026 — trả lời *(do `fls-ba` điền bên dưới, cùng tệp)*

| | |
|---|---|
| **Quyết** | ⭐ **Phương án 1, mở rộng ra cả cột `Số tiền GD`** — hai cột tiền của `.mcols` **`108px → 136px`** *(`Số tiền`)* và **`116px → 136px`** *(`Số tiền GD`)*, đặt theo **ngân sách 18 ký tự** đo trên sổ thật và **phông rộng nhất** trong chuỗi `--mono`; chuỗi vượt ngân sách *(hôm nay **0** dòng)* ⇒ ô in `…` + `title` = chuỗi đủ, ⛔ cắt im lặng. ⭐ **Yếu #2 (`BG-027`):** một luật số lẻ cho mọi mã — giá trị có **thêm** phần lẻ ngoài bảng ISO ⇒ in **đúng thang kho 2 chữ số**, cho cả VND *(`"1306103.8"` ⇒ `1.306.103,80`)* lẫn mã lạ *(`"100.50" '20'` ⇒ `100,50`; ~~`100,5`~~)*. ⭐ **Yếu #4 (`BG-027`, câu #3 của người gọi):** dung sai **in ra = đúng dung sai đem so** *(sàn xu)* ⇒ `"617.285"` VND in `617,28` ~~`617,29`~~. ⇒ `WO-022` **mở lại vòng 2** với `AC-10`…`AC-15` |
| **Ai quyết** | `fls-ba` *(trong thẩm quyền spec — cách màn **in** chuỗi cửa đã trả; ⛔ đổi sổ, ⛔ đổi cửa, ⛔ đổi luật dung sai `QĐ-ITL-63`)* · 2026-10-02. ⛔ câu nào cho owner: `Q-TIEN-1` *(làm tròn VND hay in đủ)* **vẫn treo**, quyết định này ⛔ chạm nó — nó chỉ nói *"nếu in phần lẻ thì in mấy chữ số"* |
| **Spec đã sửa** | `02_BA/06_SCREEN_SPEC.md` **v4.12 → v4.13** *(§5b ⓒ viết lại · ⓕ thêm câu dung sai · ⭐ ⓘ mới — ngân sách bề rộng cột tiền)* · `02_BA/Artifacts/fls-gan-lenh-chi_10.html` *(`.mcols` hai cột tiền → `136px`)* · `WO-022` vòng **2** · `00_MASTER_INDEX` §8 ô `06` |

## Đo của `fls-ba` *(02/10, kho thật chỉ `SELECT` + `node` gọi `TP.tien` **thật** của `thanh_phan.js` @ `cecab3a` — ⛔ dựng lại hàm bằng tay)*

**Mẫu số:** bảng lệnh = `fls_pm_line` run `NAP-2026-10-02-PME7F31617` **3.820** dòng *(cùng run `fls-dev` đo)*; cột `Số tiền GD` = `fls_itl` dòng có `ps_no ∨ ps_co ≠ 0` **8.387**. Chuỗi đo = đúng chữ ô in: `TP.tien(v, curr) + ' ' + curr`. Kho `numeric(20,2)` cả ba cột *(`information_schema`)*.

| Nguồn · tiền tệ | Dòng | Chuỗi dài nhất *(ký tự)* | Ví dụ | ≥ 15 ký tự | ≥ 16 ký tự |
|---|--:|--:|---|--:|--:|
| lệnh · VND | 2.721 | **17** | `3.385.679.344 VND` | **426** | 110 |
| lệnh · USD | 1.030 | ⭐ **18** | `103.950.000,00 USD` *(1 dòng — `amount ≥ 10^8` USD; ⛔ phán dữ liệu ở đây, màn phải in đủ)* | 27 | 27 |
| lệnh · SGD | 57 | 16 | `1.516.560,00 SGD` | 1 | 1 |
| lệnh · HKD / EUR / `20` | 10 / 1 / 1 | 14 / 9 / 5 | `151.493,33 HKD` | 0 | 0 |
| sổ · VND | 4.242 | ⭐ **18** | `11.742.361.787 VND` *(6 dòng ở 18 ký tự)* | 831 | **347** |
| sổ · USD | 3.980 | 16 | `1.773.453,18 USD` | 34 | **34** |
| sổ · HKD | 20 | 16 | `1.565.104,54 HKD` | 2 | **2** |
| sổ · SGD | 145 | 14 | `125.567,02 SGD` | 0 | 0 |

⇒ ⭐ **Ngân sách = 18 ký tự**, và nó đúng cho **cả hai** cột tiền. ⛔⛔ **Cột `Số tiền GD` (`116px`) cũng cắt — `HOI` chưa nêu:** `116px` chứa tối đa **15** ký tự *(16 × 7,32 = 117,2 > 116)* ⇒ **383 / 8.387** giá trị sổ *(VND 347 · USD 34 · HKD 2)* bị cắt nếu lên cột ấy. Sửa một cột mà để cột kia là đổi chỗ lỗi.

**Bề rộng một ký tự** *(`--mono` ở `--fs-than` = `12.5px`; ⛔ có `@font-face` trong `fls/web` ⇒ chữ ra phông **cài trên máy**, theo thứ tự `tokens.css:29`)*:

| Phông | Bề ngang *(em)* | px / ký tự | 18 ký tự |
|---|--:|--:|--:|
| `IBM Plex Mono` *(nếu máy kế toán có cài)* | 0,600 | **7,50** | **135,0** |
| `Cascadia Mono` *(Windows 11 — máy đo của `fls-dev`: 117,2 / 16 = 7,325 ✔)* | 0,586 | 7,32 | 131,8 |
| `Consolas` *(Windows 10)* | 0,550 | 6,88 | 123,8 |

⇒ Đặt theo phông **rộng nhất** trong chuỗi: `18 × 7,5 = 135` ⇒ **`136px`**. ⚠ Đặt `132px` *(theo máy đo)* thì trên máy có `IBM Plex Mono` lại cắt đúng 2 ký tự cuối — đúng lớp *"đo bản dựng tưởng đã đo kho"*.

**Cái giá** *(suy từ số đo của `fls-dev`: ở 1440 cột `Nội dung` ≈ 220px)*: +48px lấy từ hai cột co giãn `Nội dung` *(`minmax(160px,1fr)`)* và `Giao dịch đã gán` *(`minmax(190px,1.1fr)`)* ⇒ ở 1440 còn ≈ **197px** / **217px** — trên sàn của cả hai; hai cột này đã có `…` khi hẹp. Tổng sàn của lưới `1279 → 1327px` ⇒ màn **< ~1340px** thì bảng cuộn ngang **bên trong** `.tablescroll` *(trước: < ~1290px)*; trang ⛔ tràn.

**Vì sao ⛔ ba phương án kia:** ⓶ `124px` để **426** dòng VND cắt tiếp *(và cột GD vẫn cắt)*; ⓷ `…` + `title` làm **mặc định** = người phải di chuột mới đọc được tiền, trái `C5` — chỉ giữ làm **lưới an toàn** cho chuỗi > 18 ký tự *(hôm nay **0** dòng)*; ⓸ `GAP` = chấp nhận **452+** dòng in thiếu ký tự cuối. ⛔ Rút gọn đơn vị *(`11,7 tỷ`)* — trái `UI-F10` *(⛔ bao giờ làm tròn giá trị sổ khi in)*. ⛔ Hạ cỡ chữ về `--fs-phu` — tiền là thứ kế toán đọc **để làm việc** *(`tokens.css:169`, thang 5 bậc của `§4.5 ⓠ 1.2`)*.

**Luật `GAP-SCR-29`** *(cột thẳng hàng)*: giữ — hai cột tiền vẫn là vệt **cố định** *(⛔ `auto`)*, nên mọi dòng và hàng tiêu đề chia cùng một lưới; và bề rộng nay đến từ **số đo**, đúng bài học *"thẳng hàng mà ⛔ đọc được thì chỉ là đổi một lỗi lấy một lỗi"*.

### Yếu #2 — số lẻ: **một** luật, ⛔ hai nhánh bất đối xứng
- Hôm nay `tien()` có hai nhánh cho cùng một tình huống *"giá trị có phần lẻ mà bảng ISO ⛔ cho"*: mã **trong bảng** ⇒ in theo thang kho **2** *(`,80`)*; mã **lạ** ⇒ cắt số 0 đuôi *(`,5`)*.
- Quyết: **số lẻ in = bảng ISO của mã nếu giá trị vừa bảng; ngược lại = thang kho 2.** Mã lạ / thiếu ⇒ bảng coi là **0** *(⛔ đoán tiền tệ: số nguyên in nguyên, có lẻ in đủ 2)*. Lý do: kho là `numeric(20,2)` ⇒ "chữ số thật" của giá trị sổ **là** 2 chữ số; một cột cùng mã có cả `100,5` lẫn `12,25` thì dấu phẩy ⛔ thẳng hàng *(`UI-F3`)*.
- Tầm hôm nay: **0** dòng đổi chữ in — mã lạ trên sổ: `fls_pm_line` mã `20` **71** dòng *(mọi ảnh)*, có lẻ **0**; `fls_itl` mã lạ **0**. Đổi để **luật** nhất quán trước khi dữ liệu tới, ⛔ vì một con số đang sai.
- ⚠ `Q-TIEN-1` *(owner: VND có lẻ **in đủ** hay **làm tròn**)* ⛔ đổi — nếu owner chọn làm tròn thì nhánh *"thang kho"* chỉ còn cho mã lạ.

### Yếu #4 *(câu #3 của người gọi)* — dung sai in ra phải là dung sai đem so
- Hôm nay: hộp *Ghép lệnh* `F01` *(`man_f01.js` `_tinh`)* và gợi ý hộp *Tìm tiền* `F01L` *(`man_f01_lenh.js` dòng *"dung sai Σ cho tiền tệ này"*)* in `TP.tien(d.dung_sai, cur)` — làm tròn nửa-ra-xa ⇒ `617,29`; còn phép so dùng `TP.xu(ds, 'san')` = **61728** xu. Người đọc *"lệch 617,29 · dung sai 617,29 · ⛔ lệch quá dung sai"*.
- Quyết: in **`TP.tien(TP.chuoi_xu(TP.xu(ds, 'san')), cur)`** — đúng con số đã so ⇒ `617,28`. Luật chung thêm vào §5b ⓕ: **con số in cạnh một phép so là con số đã đem so.**
- Tầm *(kho thật chỉ `SELECT`)*: dòng tiền VND có dung sai ghép tay `0,5% × tiền` mang **chữ số lẻ thứ ba** *(tiền < `200.000` và lẻ)* = **250 / 4.242**. Ngoại tệ dung sai `0` ⇒ ⛔ chạm.

### `AC` vòng 2 *(chép nguyên ở `WO-022`)*
`AC-10` hai cột `136px` theo ngân sách *(tĩnh)* · `AC-11` sổ thật dài nhất ≤ 18 ký tự *(báo động khi dữ liệu vượt)* · `AC-12` Chrome hai cột ⛔ cắt + lưới an toàn `…`/`title` · `AC-13` số lẻ một luật · `AC-14` dung sai in = dung sai so · `AC-15` cổng.

⇒ `HOI-026` **`DONG`** *(đã trả)*.
