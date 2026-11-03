# 12 — BA LẠI MÀN GHÉP PM ↔ GIAO DỊCH

**Version:** v0.3 · **Ngày:** 2026-09-18 · **Chủ sở hữu:** BA
**Vì sao có tệp này:** owner xem màn `F01` lằn **LỆNH CHI** và nói *"chưa hài lòng về UIUX"*, nêu **bốn** điểm. Tệp này ⛔ không nhận bốn điểm ấy làm bốn việc — nó **đo trước**, và phép đo đổi cả **thứ tự** làm.

**Căn cứ:** `06_SCREEN_SPEC` · `QĐ-ITL-122` *(chiều đo: Trans map vào PM)* · `QĐ-ITL-63` *(dung sai)* · mã sống: `fls/web/tep/man_f01_lenh.js` · `fls/adapters/pm_join.py` · kho `fls` đo `2026-09-11`

> ⚰⚰⚰ **BIA — `CR#12`, `2026-09-18`. Tệp này ⛔ KHÔNG còn là đặc tả sống.**
> Nó tả màn `F01` **trước** lần thiết kế lại; bản sống nay là **`BA-14 §8`** *(vì sao)* ·
> **`BA-06 §4`** *(trông ra sao)* · **`BA-13 §A`** *(phản ứng thế nào)*.
>
> ⭐ **Giữ nguyên từng chữ, và nó ⛔ không phải phép lịch sự.** Ba phép đo của tệp này
> **vẫn đứng**, và `BA-14` dựng thẳng trên chúng — trong đó phép đo `§2ⓓ` chỉ mặt dòng
> `PM00576-1` ngày `11/09`, mà `18/09` nó **vẫn đứng đó**. ⇒ Tệp này là **bằng chứng**
> rằng *chỉ mặt* mà ⛔ không có người nhận việc thì **bằng ⛔ không** — lý do cửa
> `queue/loi-nguon` tồn tại *(`BA-13 §A4`)*.
>
> ⛔ **Chỗ tệp này ⛔ không thấy:** nó nhận *"bốn điểm UIUX"* làm khung, nên nó sửa **bốn chỗ**
> mà ⛔ không hỏi *"màn này hỏi câu gì"* — và đó đúng là câu `BA-14 Đ0` phải mở ra để hỏi.

---

## §0 · Bốn điểm owner nêu, và cái phép đo nói thêm

| # | Owner nói | Đo được | Phán quyết |
|:-:|---|---|---|
| ① | *"Mã tham chiếu là gì? Có một trường là **Reference number** ⇒ dùng tên chuẩn"* | Cột `25` của `PM_Unpivot` tên **`Reference number`**; cột sao kê ngân hàng **cũng** tên `Reference number`; màn hình đặt tên thứ **ba** là *"Mã tham chiếu"* | ✅ **ĐÚNG** — và nặng hơn owner nghĩ |
| ② | *"PM đã có số chứng từ rồi thì ⛔ không cần map; có tính năng sửa/map lại"* | **121** dòng lệnh có số chứng từ **khớp đúng** một dòng tiền trong sổ mà **⛔ chưa nối** · **514** dòng có số chứng từ ⛔ **không hề có tiền** trong sổ · nút **Bỏ ghép** ⛔ **KHÔNG tồn tại** trên lằn này | ✅ **ĐÚNG** — đây là **khuyết tật lớn nhất**, lớn hơn layout |
| ③ | *"Bảng PM cần đủ trường như trong GGSheet"* | FLS đọc **8** cột của `PM_Unpivot`; cột cuối nó chạm là số **25** ⇒ ⛔ **không đọc** phần lớn tờ. Và ảnh chụp `PM` lưu **0** dòng thô *(lằn `Bank` lưu 7.454.400)* | ✅ **ĐÚNG** — kèm một lỗ ⛔ chưa ai khai |
| ④ | *"Layout trang chưa đẹp"* | — | ✅ Đúng, **⛔ nhưng làm CUỐI**. `§5` nói vì sao |

---

## §1 · Điểm ① — ⛔ không phải chuyện đặt tên, là **ba cái tên cho một trường**

```
GGSheet PM_Unpivot  cột 25   →  "Reference number"
Sao kê ngân hàng    cột khai →  "Reference number"
fls_pm_line         cột      →  ref_tho / ref_canon
Màn hình F01 lằn PM →          "Mã tham chiếu"
Màn hình F02 Sổ ITL →          "Số chứng từ"   (doc_no)
```

⛔⛔ **Một trường, NĂM cách gọi, và hai trong số đó nằm trên HAI màn hình kế toán nhìn cùng một buổi.** Kế toán mở `F01` thấy *"Mã tham chiếu"*, mở `F02` thấy *"Số chứng từ"*, mở GGSheet thấy `Reference number` — và **cả ba là một thứ**. Đó ⛔ không phải bất tiện, đó là chỗ người ta **kết luận sai rằng chúng khác nhau**.

★ **Quyết:** tên hiển thị tiếng Việt **duy nhất** là **`Số chứng từ`**, có chú `(Reference number)` ở tiêu đề cột lần đầu. `ref_tho`/`ref_canon` giữ nguyên trong kho *(chúng là **hai trạng thái** của cùng trường — thô và đã chuẩn hoá — chứ ⛔ không phải hai trường)*, nhưng **⛔ không bao giờ** lộ chữ `ref` ra màn hình.

⚠ Và ⛔ **đừng** sửa bằng find-replace: chữ *"Mã tham chiếu"* nằm ở `man_f01_lenh.js:174` cho **tiêu đề cột**, ở `:145` và `:237` cho **giá trị** — chỗ thứ ba là câu trong ngăn kéo, sửa máy móc sẽ ra câu tiếng Việt sai ngữ pháp.

---

## §2 · Điểm ② — **màn hình đang hỏi sai người, ba lần**

⛔⛔⛔ **Đây là phần đắt nhất của tệp này.** Đo `3.772` dòng lệnh của ảnh PM hiệu lực:

| Nhóm | Dòng | % | Màn hình hôm nay làm gì | Nên làm gì |
|---|--:|--:|---|---|
| ⭐ **Đã nối rồi** | **1.477** | 39,2% | ẩn *(đúng)* | ẩn, nhưng **mở được để sửa** |
| ⭐⭐ **MÁY TRẢ LỜI ĐƯỢC** — số chứng từ khớp đúng một dòng tiền | **121** | 3,2% | ⛔ **hỏi kế toán** | ⛔ **đừng hỏi** — máy ghép, người **duyệt theo lô** |
| ⛔ **⛔ KHÔNG BAO GIỜ trả lời được** — có số chứng từ nhưng ⛔ **không có tiền** trong sổ | **514** | 13,6% | ⛔ **hỏi kế toán** | tách ra rổ riêng, nói **vì sao** |
| ⚠ **Số chứng từ là MỘT SỐ TIỀN** | **354** | 9,4% | hiện như một mã | rổ **sửa nguồn** — ⛔ không phải việc ghép |
| **Trống** | **535** | 14,2% | hiện `—` | rổ **cần người tra** |
| Hình dạng khác | **771** | 20,4% | hiện bình thường | cần người |

★ **Ba câu hỏi khác nhau đang bị trộn vào MỘT danh sách**, và kế toán ⛔ không có cách nào biết mình đang ở câu nào:

  ⓐ *"Ghép cái này với cái nào?"* — **việc thật**
  ⓑ *"Máy biết rồi, bấm duyệt thôi"* — **121 dòng**, ⛔ không đáng một giây suy nghĩ
  ⓒ *"Cái này ⛔ không bao giờ ghép được"* — **514 dòng**, và ngồi nghĩ về nó là **phí công tuyệt đối**

⇒ **`635/1.553` dòng đang chờ ⛔ KHÔNG phải việc của kế toán** — **40,9%**. Chia rổ **xoá gần 41% danh sách** trước khi ai chạm vào layout.

⚠ `1.553` là **số đo từ cửa**, ⛔ không phải số tôi cộng tay. Bản nháp đầu của tệp này ghi `1.541` — tôi cộng ba dòng của một bản tóm tắt **bị cắt** và đánh rơi `HKD` · `EUR` · và một đơn vị tiền tệ tên **`20`**. Đúng lớp lỗi *"đọc số từ màn hình thay vì gọi phép đo"*.

### ⓐ Vì sao `514` dòng ⛔ không bao giờ ghép được — và phải nói thẳng

Số chứng từ của chúng ⛔ không khớp **dòng tiền nào** trong sổ. Nguyên nhân **đã biết** *(⛔ không phải giả thuyết)*: **272** dòng lệnh có bạn đời nằm trên **8 sheet đã bị xoá khỏi workbook sống**, và owner đã chốt bỏ `1.919` dòng lịch sử ấy ngày `10/09`. Phần còn lại là sheet `CHẶN` ⛔ chưa khai `thu_tu` + tiền chưa về.

⛔ Màn hình hôm nay để chúng nằm lẫn, ⛔ không một chữ giải thích. Kế toán sẽ tìm **mãi mãi**.

### ⓓ Và cửa vừa khai ra một đơn vị tiền tệ tên **`20`**

Gọi `GET /queue/lenh-cho/summary` để lấy tổng thật, nó trả **sáu** đơn vị tiền tệ:
`USD` · `VND` · `SGD` · `HKD` · `EUR` · và **`20`**.

Đo thẳng kho: đúng **1** dòng, `curr = '20'`, `amount = 20.00`. Tức ô **tiền tệ**
của dòng ấy đang giữ một **con số**, y hệt lớp lỗi *"số chứng từ là số tiền"*
ở trên — cùng một bệnh, ở một cột khác.

⛔ Nó **nhỏ** *(1/3.772)* nhưng nó ⛔ **không vô hại**: luật `QĐ-ITL-58` xếp hàng
chờ **trong từng tiền tệ**, nên một tiền tệ ma tạo ra một **nhóm riêng** mà
⛔ không ai ghép được, và nó sẽ nằm đó mãi. ⇒ Vào rổ **sửa nguồn** của `G2`.

### ⓑ `60` vs `61` — một chỗ ⛔ đừng gộp

Trong `121` dòng máy trả lời được: **60** khớp **cả số chứng từ lẫn số tiền** *(tự chứng hoàn toàn)*; **61** khớp số chứng từ nhưng **tiền lệch** *(trả nhiều đợt, hay một giao dịch gánh nhiều lệnh)*.

⛔⛔ **Hai nhóm này ⛔ KHÔNG được gộp vào một nút.** Nhóm `60` máy ghép được và người chỉ **duyệt**. Nhóm `61` là chỗ máy **phải** hỏi *"lệnh này ăn bao nhiêu của giao dịch kia"* — gộp lại là để máy **quyết thay người** *(`INV-I16`)*.

### ⓒ Sửa / map lại — **⛔ KHÔNG CÓ trên lằn này**

`POST /queue/{itl_id}/unmatch` **có tồn tại** ở cửa, và nút **Bỏ ghép** có ở `man_f01.js` *(lằn TIỀN)*. Lằn **LỆNH CHI** — lằn **mặc định**, lằn owner đang nhìn — ⛔ **không có nút ấy**. ⇒ Một dòng ghép sai trên lằn mặc định thì kế toán phải **đổi lằn** mới sửa được, mà ⛔ không gì trên màn nói thế.

---

## §3 · Điểm ③ — FLS đọc **8 cột**, và ⛔ không giữ lại gì để bù

`fls/adapters/pm_join.PM_COT` khai đúng **8** cột:

| Cột | Tên trong GGSheet |
|:--:|---|
| 8 · 9 | `Đơn vị tiền tệ (Currency)` · `Tổng số tiền thanh toán (Transaction Amount)` |
| 15 · 16 | `ID PMSlip` · `ID PMLine` |
| 21 · 22 | `Budget Code (HDCode)` · `Chủ dự toán (CDT1)` |
| 24 · 25 | `Status_Final` · **`Reference number`** |

⛔ Cột cuối FLS chạm là **25**, nên tờ có **ít nhất 25 cột** và FLS bỏ qua **≥17**. Kế toán muốn thấy *nhà cung cấp · nội dung · ngày đề nghị · người duyệt* — ⛔ **không cột nào trong số đó có trong kho**.

⛔⛔ **Và đây là lỗ ⛔ chưa ai khai — `GAP-CHUP-01`:**

```
lằn Bank : 14 ảnh · 65 nguồn · 7.454.400 dòng thô  ⇒ thêm cột = ĐỌC LẠI TỪ KHO
lằn PM   : 14 ảnh ·  1 nguồn ·         0 dòng thô  ⇒ thêm cột = PHẢI CHỤP LẠI SHEET
```

Lằn `PM` **⛔ không lưu một dòng thô nào**. ⇒ Mọi trường muốn thêm **⛔ không thể bù ngược** cho `3.772` dòng đang có — phải **đợi cú chụp sau**. Đây là bất đối xứng thật giữa hai lằn, và nó ⛔ không phải quyết định của ai, nó là chỗ ⛔ không ai để ý.

⚠ `PM_TIEU_DE_MONG_DOI` so **từng vị trí** và **NỔ TO** khi lệch ⇒ thêm cột **phải** bump `PM_KHAI_VERSION`, ⛔ không sửa lặng.

---

## §4 · Điểm ④ — layout, và **vì sao nó đi CUỐI**

⛔⛔⛔ **Làm layout trước là vẽ HAI LẦN, và bản vẽ đầu sẽ vẽ cho nội dung SAI.**

| Sau chặng | Danh sách đổi thế nào |
|---|---|
| `G2` chia rổ | `1.553` → còn **~918** dòng là việc thật *(−40,9%)*, và **3 rổ** thay 1 bảng |
| `G2` thêm trường | bảng PM mọc thêm **≥4** cột |
| `G3` sửa/map lại | mỗi dòng mọc thêm **một** hành động |

⇒ Vẽ lưới 8 cột cho `1.553` dòng hôm nay là vẽ cho một màn hình **sắp ⛔ không còn tồn tại**.

★ Những gì `G4` sẽ phải giải, ghi sẵn ⛔ **không bàn bây giờ**: cột `Mã HĐ · CĐT` đang là **một chuỗi nối dài 4 phần** *(`NB | Lưu chuyển nội bộ · SHQ2 | Headquarters2`)* ⇒ tách hay cắt · nút **Tìm tiền** lặp trên **mọi** dòng · ⛔ không thấy được **các dòng khác của cùng phiếu** *(một `PMSlip` mang tới 36 `reference` khác nhau)* · cột `Luỹ kế %` nằm giữa các cột tiền.

---

## §5 · LỘ TRÌNH — năm chặng, và thứ tự là **kết luận**, ⛔ không phải sở thích

| # | Chặng | Đóng điểm nào | Cổng ra **đo được** |
|:--:|---|:--:|---|
| ⭐ **G1** | **MỘT TÊN** — `Số chứng từ (Reference number)` ở mọi màn, mọi câu | ① | Quét **cả `fls/web/tep/`**: **0** lần xuất hiện chữ *"Mã tham chiếu"*; `F01` và `F02` gọi cùng một tên. Có cổng duyệt **mã màn hình**, ⛔ không gõ tay danh sách |
| ⭐⭐ **G2** | **CHIA BA RỔ** — *máy trả lời được* · *cần người* · *⛔ không bao giờ* | ② | `GET /queue/lenh-cho` trả thêm `ro`; đếm được **`60` + `61` + `514`**; rổ ⛔-không-bao-giờ mang **câu vì sao**, ⛔ không để trống |
| **G3** | **DUYỆT LÔ + SỬA/MAP LẠI** trên lằn LỆNH CHI | ② | Nút **Bỏ ghép** có mặt trên lằn LỆNH CHI *(bài duyệt DOM)*; `match-lo` duyệt được **60** dòng tự chứng; **61** dòng lệch tiền ⇒ **⛔ KHÔNG** vào nút lô |
| **G4** | **BẢNG PM ĐỦ TRƯỜNG** — mở `PM_COT`, bump `PM_KHAI_VERSION`, khai `GAP-CHUP-01` | ③ | Số cột đọc `8 → N`; `kiem_tieu_de_pm` xanh; ⭐ và một **quyết định** về việc lằn `PM` có lưu dòng thô như lằn `Bank` không |
| ✅ **G5** | **LAYOUT** — vẽ cho nội dung **sau** `G1…G4` | ④ | **XONG 11/09.** Bốn khuyết tật `§4`, mỗi cái một phép đo: cột `55` ký tự → `4` *(song ánh **31↔31** · **9↔9**)* · nút đổi chữ **theo rổ** · phiếu nhiều dòng hiện ra *(**70,1%** danh sách)* · `Luỹ kế %` rời khỏi khối tiền. **8** bài `tests/web/test_man_f01_lenh_g5_dom.py`, cả bốn cổng chứng minh **ĐỎ** được |

⭐ **`G1` + `G2` đáng làm trước tất cả**, và lý do là một con số: chúng ⛔ không cần ai quyết gì, và chúng **xoá 41,2% danh sách** — tức phần lớn cảm giác *"trang rối"* của owner **⛔ không phải lỗi layout**, nó là **635 dòng ⛔ không nên có mặt**.

⚠ **Chỉ `G4` cần owner quyết** *(có chụp thô lằn PM không — nó làm kho to lên)*. `G1`·`G2`·`G3`·`G5` tôi tự đi được.

---

## §6 · Ba thứ tệp này ⛔ KHÔNG giải

| ⛔ Không giải | Vẫn là gì |
|---|---|
| **272 dòng lệnh ⛔ không bao giờ ghép được** | Bạn đời của chúng ở 8 sheet đã xoá. `G2` làm chúng **hiện ra có lý do**, ⛔ không làm chúng ghép được |
| **354 số chứng từ là số tiền** | Khuyết tật **của nguồn**, sửa ở GGSheet. FLS chỉ **chỉ mặt**, ⛔ không tự chữa *(`INV-I16`)* |
| **Cột lý do hàng chờ còn câu sai** | `108.128` sự kiện cũ trong kho — vá `065cb1c` chỉ áp lượt nạp sau. ⭐ Công cụ dọn đã dựng: `tools/don_ly_do_sai.py` *(tự **chứng minh** trước khi xoá, và **TỪ CHỐI** nếu chứng minh ⛔ không đủ)*. Còn đợi một lượt chạy có `FLS_CHO_GHI_THAT=1` |

---

## §7 · Changelog

- **v0.3** *(2026-09-18 tối muộn, `CR#12` — đặt BIA)*: ⚰ **Tệp này KHAI TỬ làm đặc tả sống.** Bản sống nay chia ba: `BA-14 §8` *(vì sao)* · `BA-06 §4` *(trông ra sao)* · ⭐ `BA-13 §A` *(phản ứng thế nào — tầng mà cả hai tệp kia đều ⛔ không tả)*. ⛔⛔ **Giữ nguyên từng chữ**, vì ba phép đo của tệp này **vẫn đứng** và `BA-14` dựng thẳng trên chúng. ⭐ Đắt nhất: `§2ⓓ` chỉ mặt dòng `PM00576-1` ngày `11/09`, và `18/09` nó **vẫn đứng đó** ⇒ tệp này là **bằng chứng** cho luật *chỉ mặt mà ⛔ không có người nhận việc thì bằng ⛔ không*, tức lý do cửa `queue/loi-nguon` tồn tại. ⛔ Chỗ tệp này ⛔ không thấy: nó nhận *"bốn điểm UIUX"* làm khung nên sửa **bốn chỗ** mà ⛔ không hỏi *"màn này hỏi câu gì"* — đúng câu `BA-14 Đ0` mở ra để hỏi.
- **v0.1** *(2026-09-11, owner: *"chưa hài lòng về UIUX… cho tôi một lộ trình"*)*: bản đầu. ⭐⭐ **Phép đo đổi thứ tự bốn điểm owner nêu**: layout *(điểm ④)* xuống **cuối**, vì `635/1.541` dòng trong danh sách ⛔ **không phải việc của kế toán** *(121 máy trả lời được · 514 ⛔ không bao giờ trả lời được)* ⇒ **41,2%** cảm giác *"trang rối"* tan sau `G2` mà ⛔ không cần vẽ lại gì. ⭐ Điểm ① nặng hơn owner nghĩ: **một trường, NĂM tên**, trong đó `F01` và `F02` gọi khác nhau trên cùng một buổi làm việc. ⭐ Mở **`GAP-CHUP-01`**: lằn `PM` lưu **0** dòng thô *(lằn `Bank` lưu 7.454.400)* ⇒ mọi trường thêm ở `G4` **⛔ không bù ngược được**, phải đợi cú chụp sau.
- **v0.2** *(2026-09-11, owner: *"dọn và tiếp tục làm layout"*)*: **`G5` xong** — và bốn khuyết tật `§4` đều được **đo trước khi vẽ**, vì *"trang chưa đẹp"* ⛔ không tự nó nói phải sửa cái gì.

  | Khuyết tật | Phép đo | Đã làm |
  |---|---|---|
  | `Mã HĐ · CĐT` là chuỗi nối 4 phần | **55** ký tự; mã ≤ **4**; `hd` **31 mã ↔ 31 tên**, `cdt1` **9 ↔ 9** ⇒ **song ánh** | Chỉ hiện mã; tên đầy đủ sang `title` ⇒ ⛔ **không mất một thông tin nào**. **9** dòng `cdt1` ⛔ không có dấu `\|` giữ **nguyên văn** |
  | Nút **Tìm tiền** lặp mọi dòng | **1.553** nút giống hệt ⇒ **0** thông tin | Chữ đổi **theo rổ**: *Duyệt* · *Mở để chia* · *Tra tiền* · *Xem vì sao*. Cùng **một** ngăn kéo, ⛔ không đường ghi thứ hai |
  | ⛔ Không thấy dòng khác cùng phiếu | ⭐ **1.088/1.553 = 70,1%** dòng chờ nằm trong phiếu nhiều dòng; phiếu to nhất **44** dòng | Huy hiệu `còn chờ/tổng` trên cột `Phiếu`. ⛔ Phiếu **một dòng** ⛔ không đeo — một dấu hiệu có mặt trên **mọi** dòng thì ⛔ không còn là dấu hiệu |
  | `Luỹ kế %` giữa các cột tiền | Nó là **vị trí trong danh sách**, ⛔ không phải tiền của dòng | Gộp vào `#` ⇒ **mất hẳn một cột** |

  ⭐ Thêm: hai cột đầu **ghim tại chỗ** (`f1`/`f2`) và cột **Việc** ghim **bên phải** — với 28 cột bật lên, cuộn ngang làm mất **danh tính của dòng** ở một đầu và **nút bấm** ở đầu kia.

  ⚠⚠ **Một lỗi tôi suýt mắc, ghi lại vì nó là loại ⛔ không ai thấy:** lớp ghim phải nằm trên **cả `th` lẫn `td`**. Thiếu ở `th` thì thân bảng đứng yên còn dòng tiêu đề **trôi ngang** ⇒ mọi cột đọc **sai tên**, và ⛔ không có thông báo lỗi nào. `TP.bang` trước hôm nay ⛔ không nhận `lop` trên tiêu đề.

  ⛔ **Phép đo đầu tiên của tôi SAI 15 lần** — `23.295` thay vì `1.553`, vì tôi dựng SQL tay trên `fls_pm_line` mà ⛔ không biết bảng ấy giữ **9 bản sao** *(mỗi cú chụp giờ một bản, `pm_line_id` ⛔ không duy nhất)*. Con số đúng đến từ **gọi hàm thật** `dem_theo_ro()`, thứ đi qua `anh_pm_hieu_luc()`. ⇒ `GAP-NAP-03` giờ có một triệu chứng đo được, ⛔ không còn là một lo ngại.
