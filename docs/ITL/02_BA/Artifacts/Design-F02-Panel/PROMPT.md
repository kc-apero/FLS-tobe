# PROMPT — dán nguyên văn vào một phiên Claude làm thiết kế

> ⭐ Kèm theo prompt này **ba tệp** trong cùng thư mục: `BRIEF.md` ·
> `DATA.json` · `tokens.SNAPSHOT.css`. Và kèm **ảnh chụp màn hình hiện tại**
> *(chụp panel bên phải, cả lúc cuộn xuống)* — ⛔ không có ảnh thì người thiết
> kế đang sửa một thứ họ chưa nhìn thấy.

---

Bạn là **design lead** cho một phần mềm kế toán nội bộ. Việc của bạn hôm nay là
**thiết kế lại panel đối soát** của màn `F02 · Sổ ITL`.

## Bối cảnh trong một đoạn

`F02` là màn **làm việc** của **2–3 kế toán** *(⛔ không phải màn đọc của sếp)*.
Bên trái là lưới **10.030 dòng** tiền ra/vào của công ty. Bấm một dòng thì bên
phải mở **panel đối soát** — nơi kế toán nhìn dòng đó thật kỹ và gõ vào **7 ô
phân loại**. Panel hiện chạy đúng, dữ liệu đúng, **nhưng kế toán nói nó rối và
khó nhìn**. Đó là việc của bạn.

## Vấn đề — đo được, ⛔ không phải cảm tính

| Đo | Số |
|---|---|
| Ký hiệu (`⛔ ⚠ ⭐ 🔒 · —`) trong chữ **hiện ra màn hình** | **235** |
| Riêng dấu **⛔** | **111** |
| Trong đó dấu ⛔ đứng ngay trước chữ *"không"/"chưa"* | **73 (66%)** |
| Chỗ có **hai dấu ⛔ liền nhau** | **5** |
| Dấu ⛔ nằm trong câu **báo tin TỐT** *(`✓ dòng này ⛔ không còn việc`)* | **2** |
| Câu tiếng Việt hiện ra màn hình | **260** |
| Dòng ở trạng thái `UNMAPPED` *(chưa ai phân loại)* | **7.682 / 10.030 = 76,6%** |
| Ô dữ liệu trên panel *(chưa kể 3 bảng con)* | **57** |

⭐⭐ **Hai con số cuối là chẩn đoán, ⛔ không phải hai con số nữa.**

Dấu **⛔** sinh ra để nói *"nguy hiểm, dừng lại"*. Nhưng 66% số lần nó chỉ đang
đứng trước chữ **"không"** — nó đã tụt xuống thành một **thói quen chính tả**,
⛔ không còn là tín hiệu. Và vì **76,6% dòng đều `UNMAPPED`**, trạng thái *"có
việc phải làm"* chính là trạng thái **BÌNH THƯỜNG** của cuốn sổ này — đánh dấu
báo động lên cái bình thường thì khi có chuyện thật, ⛔ **không còn gì để đánh
dấu**.

## Việc cần làm

1. **Một bộ luật ký hiệu & màu** — mỗi dấu mang **đúng một nghĩa**, và nói rõ
   *mỗi màn được dùng tối đa bao nhiêu lần*. Cắt mạnh tay.
2. **Xếp lại 7 khối của panel theo THỨ HẠNG**, ⛔ không để 7 khối cùng nặng như
   nhau. Kế toán mở panel ra là để **gõ 7 ô** — mọi thứ khác là để **tra**.
3. **Dùng màu để chở trạng thái** *(kế toán xin điều này)* — nhưng đọc kỹ §4
   `BRIEF.md`: màu ⛔ **không bao giờ được là thứ DUY NHẤT** chở một nghĩa.
4. **Viết lại chữ trên màn** — ngắn, và nói **việc phải làm**, ⛔ không giảng
   giải nội bộ hệ thống.

## Ràng buộc — ⛔ ĐỌC `BRIEF.md` §4 TRƯỚC KHI VẼ

Có **13 ràng buộc cứng**. Chúng ⛔ không phải sở thích: mỗi cái đến từ một lỗi
đã xảy ra thật hoặc một luật của cuốn sổ. Thiết kế đẹp mà phá một trong 13 cái
đó thì **⛔ không dùng được**.

Ba cái dễ vấp nhất:

- ⛔ **Một ô có BA nguồn** *(sổ gốc nói gì · máy đoán gì · người gõ gì)* và cả
  ba **phải phân biệt được bằng mắt**. ⛔ Đừng gộp thành một ô.
- ⛔ **`#N/A` phải hiện nguyên** khi máy tra không ra. Đó là **câu trả lời
  đúng**, ⛔ không phải lỗi — ⛔ đừng chữa cho đẹp.
- ⛔ **⛔ Không được bịa mã màu mới.** Toàn bộ màu lấy từ
  `tokens.SNAPSHOT.css` *(có sẵn 4 màu ngữ nghĩa)*. Thiếu thì **đề xuất thêm
  vào tệp đó**, ⛔ đừng gõ mã màu rời.

## Sản phẩm giao lại

1. **Một trang HTML chạy được** dựng lại panel đã thiết kế lại — vẽ trên **6
   dòng thật** trong `DATA.json` *(6 tình huống khác nhau: sạch · chưa phân
   loại · tiền vào · ngoại tệ · diễn giải dài · đã có người gõ đè)*. ⛔ Đừng
   dùng chữ giả.
2. **Bộ luật ký hiệu & màu** — dạng bảng: dấu · nghĩa · dùng ở đâu · tối đa
   mấy lần.
3. **Danh sách những gì bạn CẮT**, kèm lý do — phần này quan trọng ngang phần
   bạn thêm.
4. ⭐ **Chỗ nào bạn thấy ràng buộc §4 đang cản một thiết kế tốt hơn** — nói
   thẳng ra, ⛔ đừng lặng lẽ lách. Ràng buộc lật được, nhưng phải lật **công
   khai**.

## ⛔ Ngoài phạm vi

Lưới bên trái · cửa API · cách lưu · quyền. Chỉ **panel bên phải**.
