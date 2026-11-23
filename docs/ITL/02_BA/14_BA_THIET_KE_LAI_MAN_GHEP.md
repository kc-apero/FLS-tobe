# 14 — THIẾT KẾ LẠI MÀN GHÉP PM ↔ GIAO DỊCH: đo **NGƯỜI**, ⛔ không đo dữ liệu nữa

**Version:** v0.8 · **Ngày:** 2026-10-02 · **Chủ sở hữu:** BA
**Vì sao có tệp này:** owner xem màn `F01` sau đợt `G1…G5` và nói *"thiết kế hiện tại cho màn hình này bị **overdone** và ⛔ chưa user-friendly — cho tôi một lộ trình BA để **đánh giá và thiết kế lại**"*.

⛔⛔ **Tệp này ⛔ không nối tiếp `BA-12`. Nó nói `BA-12` đã đo thiếu một thứ, và thứ thiếu ấy là thứ quan trọng nhất.** `BA-12` đo **dữ liệu** rất kỹ và đo **cảm giác của owner về màn hình** rất kỹ. Nó ⛔ **chưa bao giờ** đo **một người thật làm công việc thật**. Thiếu phép đo ấy thì mọi cải tiến là **đoán** — và cách an toàn nhất khi đoán là *thêm vào cho chắc*. `§2` chứng minh đó đúng là điều đã xảy ra.

**Căn cứ:** `BA-12` v0.2 · `BA-13` v1.0 · `QĐ-ITL-135` *(owner gật `Đ0`+`Đ1` ngày 18/09)* · mã sống `fls/web/tep/man_f01_lenh.js` · **kho `fls` (THẬT), đo `2026-09-18`**, ảnh PM hiệu lực `NAP-2026-09-15-PM6552C5C7` *(3.772 dòng)*

---

## §1 · Ba phép đo, và cả ba đều đo thứ `BA-12` ⛔ không đo

### ⓐ Một nửa danh sách là việc ⛔ không ai làm được — và `G2` chỉ **dán nhãn** cho nó

Gọi **hàm thật** `lenh_cho.dem_theo_ro()` trên kho `fls`:

| Rổ | Dòng | % | Là việc của ai |
|---|--:|--:|---|
| `may` · tự chứng | **47** | 3,0% | **MÁY** — người chỉ bấm duyệt |
| `may` · khớp mã **lệch tiền** | **203** | 13,1% | người — phải **chia** |
| `nguoi` · ⛔ chưa có số chứng từ | **535** | 34,4% | người — **việc thật** |
| ⛔ **`khong`** · ⛔ **không bao giờ trả lời được** | **768** | **49,5%** | ⛔ **KHÔNG AI** |
| **Tổng** | **1.553** | 100% | |

⇒ Việc thật của kế toán là **738 dòng** *(47,5%)*. Phần còn lại — **815 dòng, 52,5%** — ⛔ **không phải việc của họ**, và vẫn đang nằm **trong cùng một danh sách**.

⛔⛔ **`G2` đã chia rổ và đã viết câu *vì sao* cho rổ `khong`. Nhưng nó ⛔ không BỎ chúng ra khỏi màn.** Dán nhãn cho rác ⛔ không phải là dọn rác — nó chỉ làm cái rác **có chú thích**, và làm danh sách **dài thêm một cột**.

### ⓑ ⭐⭐ **12 trong 20 dòng ĐẦU TIÊN màn hình đưa ra là ngõ cụt**

⛔ ⛔ Đây là con số đắt nhất tệp này, và nó ⛔ **không suy ra được** từ bảng `ⓐ`. Rổ `khong` chiếm `49,5%` **toàn danh sách**, nhưng thứ tự của màn là `(tiền tệ, tiền giảm dần)` — ⛔ **không phải** thứ tự ngẫu nhiên. Nên phải đo **đúng 20 dòng cửa trả về đầu tiên**, ⛔ không chọn tay:

| Rổ | Trong 20 dòng đầu | % |
|---|--:|--:|
| ⛔ `khong` — ngõ cụt | **12** | **60%** |
| `may` | 5 | 25% |
| `nguoi` — **việc thật** | **3** | **15%** |

⇒ Kế toán mở màn, nhìn **màn hình đầu tiên**, và **6 trên 10 dòng** trước mắt họ là thứ ngồi tra **mãi mãi ⛔ không ra**. Chỉ **3 dòng** là việc của họ.

⭐ **Và dòng số `1` — dòng đầu tiên một con người nhìn thấy trên hệ này** — là dòng này:

```
#1   tiền tệ = 20        số chứng từ = "Reject"        tiền = 20.00
```

Tiền tệ tên **`20`**; ô số chứng từ giữ chữ **`Reject`** *(một **trạng thái**, ⛔ không phải một mã)*. `BA-12 §2ⓓ` đã bắt được con tiền tệ ma này ngày `11/09` và xếp nó vào rổ *"sửa nguồn"* của `G2`. **Bảy ngày sau nó vẫn đứng đầu màn hình.** Trên ảnh hiệu lực: **1** dòng tiền tệ ma · **166** dòng có số chứng từ là chữ `Reject`.

⚠ Bản nháp đầu của tôi ghi **`3.486`** dòng `Reject` — tôi quét cả `fls_pm_line` mà quên bảng ấy giữ **9 bản sao ảnh chụp**. Đúng cái bẫy `BA-12` đã ghi và tôi vẫn đạp lại. Số đúng **166** là khi khoá `run_id` về ảnh **hiệu lực**.

### ⓒ ⛔⛔⛔ Màn này **chưa một lần** được người thật dùng

Đọc sổ vết thao tác trên kho `fls`:

| Đo | Kết quả |
|---|---|
| `fls_queue_event` | **108.128** sự kiện — **100%** `evt_type='reason'`, **100%** actor `dung-lai-so@apero.vn` *(công cụ)*, **100%** trong **một ngày** `10/09` |
| Ghép tay · bỏ ghép · gõ lý do · hoãn · đánh xong | **0** · **0** · **0** · **0** · **0** |
| `fls_pm_link` | **2.262** mối *(`A` 2.145 · `B` 65 · `C` 52)* — **tất cả** do **máy** tự ghép, **tất cả** ngày `10/09` |
| `fls_pm_unlink` | **0** |
| `fls_adjustment` | **0** |

⭐⭐ **⛔ Không một kế toán nào đã bấm một nút nào trên màn này. ⛔ Không phải "ít" — là KHÔNG.**

⇒ Câu *"⛔ chưa user-friendly"* hôm nay ⛔ **không thể** là kết luận từ việc dùng. Nó là kết luận từ việc **nhìn**. Và đó là toàn bộ chỗ đứng của `Đ1`: **⛔ không ai được phép thiết kế lại một màn hình mà ⛔ chưa ai từng nhìn thấy nó bị dùng thế nào.**

---

## §2 · Chẩn đoán — *overdone* là khuyết tật của **CÁCH LÀM**, ⛔ không phải của gu thẩm mỹ

`git log` của **một** tệp, `fls/web/tep/man_f01_lenh.js`:

| Ngày | Commit | Dòng | Thêm gì |
|---|---|--:|---|
| 09/09 | `4282242` | **339** | *(hỏi từ phía lệnh chi)* |
| 11/09 | `c98b710` | 418 | `G1` một tên + `G2` ba rổ |
| 11/09 | `528c8ba` | 521 | băng *"Việc của bạn hôm nay"* |
| 11/09 | `e617582` | 579 | cửa *"nhìn đủ 28 cột"* |
| 11/09 | `774700c` | 639 | cột GGSheet ra thẳng bảng |
| 11/09 | `d810090` | 669 | `G3` duyệt lô |
| 11/09 | `ac2ef67` | **735** | `G5` layout |

⭐⭐ **`339 → 735` — gấp `2,17` lần trong `2` ngày. Bảy lần sửa, ⛔ KHÔNG một lần nào tổng đi xuống.**

⛔⛔ Mỗi lời chê sinh thêm **một thứ**: một băng, ba nút băng, một khối gấp, một huy hiệu `còn chờ/tổng`, một nút bật `28` cột, hai cột ghim trái, một cột ghim phải, bốn nhãn nút khác nhau theo rổ. Mỗi thứ **riêng lẻ** đều có một phép đo chống lưng và đều **đúng**. Cộng lại chúng thành cái owner gọi là *overdone*.

★ **Và cổng tài liệu đang ĐẨY theo chiều ấy.** `tools/kiem_thuyet_minh.py` bắt *mọi nhãn nút phải có dòng thuyết minh*. Nó làm việc thêm nút **đắt hơn**, nhưng nó ⛔ **không hề** làm việc **bỏ** nút **rẻ hơn** — và ⛔ không phép đo nào trong bộ cổng hỏi câu *"màn này có to lên ⛔ không"*. ⇒ `Đ5`.

---

## §3 · `Đ0` — câu màn hình hỏi *(owner gật 18/09)*

> ### **«Lệnh chi nào chưa tìm được tiền, và ai trả lời được?»**

⭐ **Vế sau — *"ai trả lời được"* — là vế quyết định layout**, và nó là thứ `BA-12` tìm ra mà `G5` ⛔ không vẽ tới nơi: màn hình ⛔ **không** trả lời *một* câu, nó **phân loại người trả lời** trước, rồi mới đưa việc. Một màn hình trả lời đúng câu này thì **⛔ không được phép** đặt `768` dòng ⛔-không-ai-trả-lời-được cạnh `535` dòng việc thật.

---

## §4 · `Đ1` — bộ đo, dựng sẵn để buổi quan sát đẻ ra **SỐ**, ⛔ không đẻ ra ý kiến

⛔ **Một buổi quan sát ⛔ không có dụng cụ sẽ trả về *"em thấy hơi rối"*** — đúng thứ chúng ta đã có, và đúng thứ ⛔ không dùng được để thiết kế.

### ⓐ Khuôn buổi

| Mục | Chốt |
|---|---|
| Người | **2** kế toán đang làm việc ghép. ⛔ **Không** phải người mới |
| Việc | **20 dòng đầu** màn hình đưa ra — ⛔ **không chọn tay**, ⛔ không bỏ dòng khó |
| Thời lượng | ~45 phút/người |
| ⛔ Cấm | ⛔ **Không** hướng dẫn trước · ⛔ **không** giải thích màn khi họ khựng · ⛔ **không** trả lời câu hỏi của họ *(ghi lại câu hỏi ấy — nó **chính là** dữ liệu)* |
| Ghi | Bấm giờ **từng dòng**. Có thể quay màn hình |

### ⓑ Phiếu ghi — **5 ô mỗi dòng**, ⛔ không hơn

| Ô | Ghi gì | Vì sao ô này |
|---|---|---|
| **1** `giây` | Từ lúc mắt chạm dòng tới lúc rời dòng | Thước gốc của `Đ4` |
| **2** `kết cục` | `ghép` · `bỏ qua` · ⛔ `không biết` | ⛔ `không biết` là **thất bại của màn**, ⛔ không phải của người |
| **3** `cuộn ngang mấy lần` | Đếm | Đo trực tiếp cái giá của lưới `28` cột |
| **4** `có mở ngăn kéo ⛔ không` | Có/⛔ không | Ngăn kéo ⛔ không ai mở = một khối chết |
| **5** `có phải hỏi người khác ⛔ không` | Có/⛔ không | Màn ⛔ không tự đứng được |

### ⓒ Ba con số nền `Đ1` phải trả về

| # | Con số | Dùng để |
|:-:|---|---|
| **N1** | **Trung vị giây/dòng** | `Đ4` so `≥ 40%` nhanh hơn |
| **N2** | **% dòng kết thúc bằng ⛔ *không biết*** | Đo màn, ⛔ không đo người |
| ⭐ **N3** | **% THỜI GIAN tiêu vào rổ `khong`** | ⭐⭐ **Đây là giá tiền mặt của việc ⛔ chưa CẮT.** Đã biết trước `60%` số **dòng** trong 20 dòng đầu là ngõ cụt — `N3` nói `60%` ấy ăn mất bao nhiêu **phút** |

⭐ `N3` là lý do `Đ1` phải chạy **TRƯỚC** `Đ2`. Cắt rồi mới đo thì `N3` **⛔ không còn tồn tại** để đo, và chúng ta mất vĩnh viễn con số chứng minh việc cắt là đúng.

### ⓓ 20 dòng của buổi — chốt sẵn, tái lập được

Lấy bằng `lenh_cho.doc_lenh_cho(limit=20)` trên ảnh `NAP-2026-09-15-PM6552C5C7`, thứ tự **y nguyên của cửa**:

| # | Rổ | Tiền tệ | Tiền | Số chứng từ |
|:-:|---|---|--:|---|
| 1 | ⛔ `khong` | ⚠ `20` | 20,00 | ⚠ `Reject` |
| 2 | `nguoi` | EUR | 40,00 | *(trống)* |
| 3–11 | ⛔ `khong` ×9 | HKD | 173.553,92 … 54.866,41 | 813508758 … `PC00085CNTT` |
| 12 | `may` | HKD | 14.800,00 | `CT0036484556M001139` |
| 13 | ⛔ `khong` | SGD | 1.516.560,00 | ⚠ `Reject` |
| 14 | `may` ⭐tự chứng | SGD | 21.587,28 | 202607131017 |
| 15 | `nguoi` | SGD | 5.100,00 | *(trống)* |
| 16 | `may` | SGD | 4.040,00 | 202604161535 |
| 17 | `may` ⭐tự chứng | SGD | 3.618,27 | `CT0036073009M001` |
| 18 | `nguoi` | SGD | 3.600,00 | *(trống)* |
| 19 | `may` ⭐tự chứng | SGD | 3.570,30 | `CT0039376526M001` |
| 20 | ⛔ `khong` | SGD | 2.735,90 | `SGTT250104903071` |

⚠ Ảnh PM sau sẽ **đổi** danh sách này. ⇒ `Đ1` chạy trên ảnh nào thì **ghi run_id ấy vào biên bản**, và `Đ4` phải chạy trên **cùng** ảnh — nếu ⛔ không, `Đ4` so hai tập việc **khác nhau** và kết luận vô nghĩa.

---

## §5 · Lộ trình — sáu chặng, và **thứ tự là một ràng buộc đo được**, ⛔ không phải sở thích

| # | Chặng | Làm gì | Cổng ra **đo được** | Ai quyết |
|:-:|---|---|---|:-:|
| ✅ **Đ0** | **Câu màn hình hỏi** | `§3` | ✅ **XONG 18/09** — owner gật | Owner |
| ⭐ **Đ1** | **Xem người thật làm** | `§4` | `N1` · `N2` · `N3` có mặt, kèm `run_id` ảnh | **Owner** — cần người |
| ⭐⭐ **Đ2** | **CẮT, ⛔ không dán nhãn** | `768` rổ `khong` **ra khỏi** danh sách mặc định, sang trang riêng · `47` tự chứng **máy ghép**, ⛔ không hỏi ai · `166` dòng `Reject` + `1` tiền tệ ma sang rổ **sửa nguồn** | Danh sách mặc định `1.553 → 738` *(**−52,5%**)*; và `20` dòng đầu còn **≤2** dòng rổ `khong` | Tôi |
| **Đ3** | **Dựng lại theo VIỆC, ⛔ không theo BẢNG** | Mỗi lần **một** dòng, **một** câu hỏi, **hai** lựa chọn — thay lưới `28` cột | **Trần** số thứ trên màn cùng lúc, khai thành hằng và có bài thử | Tôi |
| **Đ4** | **Đo lại bằng ĐÚNG thước `Đ1`** | Cùng 2 người, cùng 20 dòng, **cùng ảnh** | `N1` nhanh hơn **≥40%** · `N2` giảm · ⛔ nếu ⛔ không đạt thì **bản vẽ sai**, ⛔ không phải người chưa quen | — |
| **Đ5** | **Cổng chống phình** | Cổng NO bản sửa làm màn **to thêm** mà ⛔ không bỏ thứ gì | Cổng chứng minh **ĐỎ** được | Tôi |

### ⚠⚠ Ràng buộc thứ tự — và nó **chặn** `Đ2`

⛔⛔ **`Đ1` phải đo màn hình HÔM NAY.** Hai lý do, cả hai ⛔ không lách được:

- `N3` *(% thời gian tiêu vào rổ `khong`)* ⛔ **không còn đo được** sau khi `Đ2` cắt. Đo sau thì mất vĩnh viễn.
- `Đ1` phải quan sát **cách người ta xoay xở** với `768` dòng ngõ cụt. Cắt trước là xoá mất **hành vi** cần quan sát.

⇒ ⛔ **Tôi giữ `Đ2` lại, ⛔ không chạy trước `Đ1`** — dù `Đ2` là chặng tôi tự đi được và là chặng gỡ được nhiều nhất.

★ **Lối thoát nếu buổi `Đ1` chậm:** tôi đóng băng màn hôm nay sau một cờ *(`?man=g5`)* để `Đ2` chạy trước mà `Đ1` vẫn đo được bản cũ sau. ⚠ Nó **⛔ không miễn phí**: hai bản màn cùng sống là đúng thứ `Đ5` sinh ra để chặn. ⇒ Chỉ dùng nếu buổi `Đ1` ⛔ **không** xếp được trong **2 tuần**.

---

## §6 · Ba thứ tệp này ⛔ KHÔNG giải

| ⛔ Không giải | Vẫn là gì |
|---|---|
| **768 dòng ⛔ không bao giờ ghép được** | `Đ2` làm chúng **rời khỏi tầm mắt**, ⛔ không làm chúng ghép được. Bạn đời của `272` dòng nằm ở **8 sheet đã xoá** *(owner chốt bỏ 10/09)* |
| **166 số chứng từ là chữ `Reject` · 1 tiền tệ tên `20`** | Khuyết tật **của nguồn**, sửa ở GGSheet. FLS **chỉ mặt**, ⛔ không tự chữa *(`INV-I16`)*. ⚠ `BA-12` đã chỉ mặt con tiền tệ ma từ `11/09` và **7 ngày sau nó vẫn đứng dòng `1`** ⇒ *chỉ mặt* mà ⛔ không có **người nhận việc** thì ⛔ bằng ⛔ không |
| **`GAP-CHUP-01` — lằn PM ⛔ không lưu dòng thô** | Đã vá từ `11/09` *(migration `0021`)* cho ảnh **mới**. Dòng của ảnh **cũ** ⛔ vẫn ⛔ không bù ngược được |

---

---

## §8 · ⭐⭐⭐ THIẾT KẾ TỔNG THỂ — `CR#12` *(thêm 18/09, owner: *"mới chỉ có component, cần tổng thể hơn"*)*

⛔⛔ **Owner đúng, và chỗ thiếu ⛔ không phải thiếu bản vẽ — là thiếu một câu trả lời cho *"việc này là việc GÌ"*.** `§1`–`§7` và hai hiện vật bản vẽ đều dừng ở mức **thành phần**: bỏ cột nào, giữ trường nào, nút nào đổi chữ. Ba phép đo dưới đây nằm **trên** mức ấy, và cả ba đổi **hình dạng** của việc, ⛔ không đổi hình dạng của một màn.

### §8.0 · ⚰⚰ OWNER SỬA TRỤC — đọc trước `§8.1`…`§8.3` *(18/09 chiều, `QĐ-ITL-136`)*

⛔⛔ **`§8.1`–`§8.3` bên dưới chia việc theo một trục SAI, và owner sửa trục ấy ngay trong ngày.**

| Owner nói | Hệ quả |
|---|---|
| *"FLS ⛔ không cần trả lời câu hỏi này"* *(«tiền đã rời tài khoản — có ai duyệt ⛔ không»)* | ⚰ **`SCR-F07` khai tử**; `§8.1` và cột ⓷ của `§8.3` **⛔ không còn hiệu lực** |
| *"Duyệt lô và Ghép từng việc đều là **mapping**, chia theo **người ghép** và **máy ghép**"* | Trục đúng: **`Tự động`** / **`Thủ công`**. ⓵ và ⓶ của `§8.3` là **MỘT việc, HAI chế độ** |

⭐ **Phép đo ⛔ không sai — cái KHUNG thì sai.** `6.165` dòng tiền ⛔ không có lệnh chi **vẫn là `6.165`**; nó chỉ ⛔ **không phải một việc của FLS**. Và điều đó nhất quán với `QĐ-ITL-56` *(owner 27/08: **⛔ không có quy định nào** nói khoản nào cần lệnh chi)* — ⛔ không luật thì ⛔ không có vi phạm để soát.

⛔⛔⛔ **Bài học đắt nhất của cả `BA-14`, và nó về TÔI:** tôi đo được `6.165` dòng, thấy nó to gấp `8,4` lần việc ghép, rồi **tự đặt cho nó một ý nghĩa nghiệp vụ** *(«việc kiểm soát»)* mà ⛔ **không một quyết định nào của owner** nói thế. Đó **đúng là** `INV-I16` — *máy ⛔ không được tự trả lời thay người* — chỉ khác là lần này **người vi phạm là tôi**, và ⛔ không cổng nào bắt được vì cổng canh **số**, ⛔ không canh **cái khung đặt quanh số**.

⭐ **Cấu trúc đúng, sau khi sửa trục:**

```
                     MỘT việc: MAPPING
                            │
          ┌─────────────────┴─────────────────┐
     ⭐ TỰ ĐỘNG                          ⭐ THỦ CÔNG
     máy ghép · người DUYỆT              người ghép từng dòng
          47                                   738
          └─────────────────┬─────────────────┘
                            ▼
              HAI ĐÍCH CUỐI ⛔ (không phải việc của ai)
        ⛔ ghép không được 768   ·   ⚠ lỗi nguồn 167
```

---

### §8.1 · ⭐⭐⭐ Hai lằn là **HAI VIỆC**, ⛔ không phải hai cách xem một việc

| | lằn **LỆNH CHI** → `SCR-F01` | lằn **TIỀN** → ⭐ `SCR-F07` *(tách mới)* |
|---|---|---|
| Câu hỏi | *"Khoản chi này đã ra tiền chưa?"* | *"Đồng tiền này có ai duyệt không?"* |
| Loại việc | **KHỚP** — có đáp án đúng/sai | **KIỂM SOÁT** — có thể ⛔ không có đáp án nào |
| Quy mô `18/09` | **738** việc thật | ⭐ **6.165** dòng tiền ⛔ **không có một lệnh chi nào** |
| Kết thúc bằng | một **mối nối** | một **câu trả lời của người** |

⭐⭐ **`6.165` ⛔ không phải hàng chờ ghép còn sót.** Tiền đã ra khỏi tài khoản mà ⛔ không có lệnh chi nào đứng sau — đó là câu hỏi **kiểm soát**, và nó to gấp **8,4 lần** việc ghép. Đặt nó làm **một nút gạt bên trong màn ghép** khiến nó trông như *"cách xem thứ hai của cùng một danh sách"*, và vì thế **⛔ chưa ai từng xử nó**.

⛔ Và đặc tả ⛔ không hề biết: chữ **`lằn`** xuất hiện **`0`** lần trong cả `BA-06` suốt **9 ngày** kể từ `GAP-SCR-14`.

### §8.2 · ⭐⭐⭐ Hàng chờ ⛔ KHÔNG CÓ LỐI RA

```
fls_itl          8.387 dòng  ·  work_status = UNMAPPED :  8.387  =  100%
fls_queue_event  108.128 sự kiện  ·  evt_type = 'done' :      0
```

`QĐ-ITL-71` chốt nút **`Xong`** là *"cách **DUY NHẤT** một dòng rời hàng chờ"*. Nút ấy **⛔ chưa được bấm một lần nào**. ⇒ Hàng chờ chỉ vào ⛔ không ra — **nó ⛔ không phải hàng chờ, nó là một cái kho**, và ⛔ không ai đọc một cái kho.

⭐ Đây là lý do thật khiến mọi bản vẽ trước **⛔ không thể** cứu màn hình: vẽ lại một danh sách ⛔ **không** làm nó ngắn đi nếu ⛔ không gì rời khỏi nó được. ⇒ `INV-I20` *(`BA-11` v0.10)* — và nó là bất biến **đầu tiên** của bộ này canh **thứ ĐI RA**, thay vì canh thứ đi vào.

### §8.3 · ⭐⭐ Thứ tự việc trong một ngày, ⛔ không phải thứ tự cột trên một màn

```
    ┌── máy chạy đêm ──────────────────────────────────────────┐
    │  nhịp CHỤP  →  NẠP  →  tự ghép những gì tự chứng được    │
    └──────────────────────────────┬───────────────────────────┘
                                   ▼
   ⓵ DUYỆT LÔ        ⓶ GHÉP TỪNG VIỆC       ⓷ SOÁT CHI KHÔNG LỆNH
      47 dòng            738 việc                6.165 dòng
      1 cú bấm           F01, một việc/lúc       F07, theo KỲ
      ~1 phút            việc hằng ngày          việc của kỳ, ⛔ không của ngày
                                   │
                                   ▼
                        ⓸ GỬI LỖI NGUỒN  →  người sửa bảng tính
                           166 + 1 dòng      ⛔ KHÔNG phải việc ghép
```

⭐⭐ **Bốn việc ấy khác nhau về NHỊP, ⛔ không chỉ khác nội dung** — ⓵ một phút mỗi sáng · ⓶ hằng ngày · ⓷ theo kỳ · ⓸ gửi đi cho người khác. Trộn cả bốn vào **một danh sách** là lý do gốc khiến `1.553` dòng trông như `1.553` việc, trong khi việc thật chỉ là `738`.

### §8.4 · Cổng của `CR#12` — và vì sao thước cũ chết

⚠ Owner **bỏ yêu cầu bấm giờ thao tác** *(18/09)* ⇒ cổng *"nhanh hơn ≥40%"* của `Đ4` **⛔ không còn đo được**. Thay bằng **ba phép đếm**, ⛔ không cần đồng hồ:

| # | Cổng | Ngưỡng |
|:-:|---|---|
| `G-a` | Danh sách mặc định | `1.553` → **`738`** *(−52,5%)* |
| `G-b` | Trường trên thẻ việc | ⭐ **`≤ 11`** *(`UI-F7` — owner nới `9 → 11` ngày `21/09`, `QĐ-ITL-147`)* |
| `G-c` | Bản sao + số của máy | **`0`** và **`0`** *(`UI-F8`·`UI-F9`)* |
| ⭐ `G-d` | **Mối nối do NGƯỜI tạo** / 28 ngày *(`fls_pm_link.hinh='T'`)* | **`> 0`** *(`INV-I20`)* — hôm nay **`0`**. ⚠ Thước đổi `18/09` tối *(`QĐ-ITL-137`)*: bản đầu đếm *sự kiện gõ lý do*, mà cột ấy vừa bị **hoãn** ⇒ ⛔ một cổng ⛔ không được dựa vào một **ô nhập liệu**; `hinh='T'` là **vết của chính hành động ghép**. ⭐ **v0.7 *(01/10, `QĐ-ITL-150 ⓐ` — `KQ-010 F-2 ⓓ`)*: chỉ đếm mối nối của NGƯỜI THẬT** — sự kiện `match` cùng `itl_id` + cùng thời điểm giao dịch *(`fls_pm_link.created_at` = `fls_queue_event.at`; đo 01/10: khớp **1/1**)* phải có ~~`actor` ∈ danh mục người~~ ⏸ *(v0.8, 02/10 — danh mục người hoãn)* `actor` ⛔ thuộc `ACTOR_MAY` và lý do ⛔ UAT *(luật `09` **v1.14** ⓑ+ⓓ)*. Sổ thật 01/10: `hinh='T'` = **`1`** — chính cú UAT `itl_id 27728` ⇒ người **`0`** |

⭐ `G-d` là cổng duy nhất trong bốn cái **⛔ không phụ thuộc bản vẽ**: nó đo việc màn hình có **được dùng** hay không, và đó là phép đo mà cả `BA-12` lẫn `BA-14 §1`–`§7` đều thiếu.

### §8.5 · ⭐⭐⭐ ĐO BẢN THIẾT KẾ ĐÃ VỀ VÀO BỐN CỔNG — `2` trượt, `1` đạt, `1` chưa đo được *(21/09, `QĐ-ITL-146`)*

> ⭐⭐ **Đây là lần đầu bốn cổng của `§8.4` có một thứ để đo.** Chúng được dựng `18/09` cho một bản vẽ **chưa tồn tại**; nay có `Artifacts/fls-gan-lenh-chi_10.html` ⇒ soi thẳng vào mã của nó, ⛔ không đọc hợp đồng thiết kế rồi nhận xét.

| # | Cổng | Ngưỡng | Bản dựng `21/09` | Kết |
|:-:|---|---|---|---|
| `G-a` | Danh sách mặc định | `738` | ⛔ **`1.553`** — bộ lọc `Chưa gán` = *mọi dòng ⛔ không phải đã gán* ⇒ **gộp cả `768` đích cuối** | ⛔ **TRƯỢT** |
| `G-b` | Trường trên thẻ việc | ⭐ `≤ 11` *(nới `21/09`)* | **`11`** — thêm mã lệnh ＋ trạng thái ＋ `CDT`, bỏ *câu vì sao* | ✅ **ĐẠT** *(sau `QĐ-ITL-147`)* |
| `G-c` | Bản sao ＋ số của máy | `0` và `0` | ⚠ **`0` bản sao**, nhưng **`6` mã nội bộ** *(`ID PMSlip`…)* hiện sau *«Xem đủ trường»* | ⚠ **MỘT NỬA** |
| ⭐ `G-d` | Mối nối do **NGƯỜI** tạo | `> 0` | **`0`** — bản dựng ⛔ **chưa nối kho**, bấm `Gán` ⛔ không ghi gì | ⬜ **⛔ chưa đo được** |

#### ⓐ ⛔⛔ Hai cổng trượt, và **cả hai đều là VA CHẠM giữa hai yêu cầu của cùng một phía**

⛔⛔⛔ **⛔ Không cái nào là người thiết kế vượt rào — và đó mới là chỗ đáng học.**

- ✅ ~~**`G-b`** *(`11 > 9`)*~~ ⇒ **ĐÓNG `21/09`, `QĐ-ITL-147`**: ba ô thêm là **mã lệnh ở đầu thẻ** *(owner nêu `18/09` khi xem bản dựng)*, **trạng thái**, và **`CDT`** *(kế toán đòi — `QĐ-ITL-144 ⓑ`)*. ⇒ **Owner và kế toán đòi thêm trường; `CR#12` của chính owner đặt trần `9`.** Hai câu ấy ⛔ không thể cùng đúng, và cả tôi lẫn họ đều ⛔ không thấy lúc phát biểu — vì chúng cách nhau **vài giờ** và nằm ở **hai tệp khác nhau**. ⭐ **Owner xử bằng cách GIỮ yêu cầu và NỚI TRẦN lên `11`**, ⛔ không bỏ ô — tức chọn *"phát biểu sau đúng"*, và ký nó thành quyết định thay vì để trần trôi. ⚠⚠ **Điều đó ⛔ KHÔNG làm `UI-F7` yếu đi, nếu `11` được coi là trần THẬT:** thêm trường thứ `12` vẫn phải **bỏ một** hoặc **xin một quyết định nữa**. ⛔ Một trần nới được **⛔ không cần ai ký** thì nó ⛔ không phải trần — và đó đúng là đường mà `339 → 735` đã đi.
- ⛔ **`G-a`** *(`1.553` vs `738`)* — **VẪN TRƯỢT**: thiết kế cho **ba** chip lọc *(`Chưa gán` ／ `Đã gán` ／ `Tất cả`)*. ⛔ Nhưng `INV-I20` nói một dòng rời hàng chờ bằng **ba** đường, trong đó **`768` dòng ⛔ không gán được** là **ĐÍCH CUỐI**, ⛔ không phải việc. ⇒ Thiếu **chip thứ tư**; đây là **thiếu một khái niệm**, ⛔ không phải thiếu một cú bấm. ⭐ **BA sửa được**, ⛔ không cần hỏi owner.

⭐⭐ **Bài học chung cho cả hai:** một ràng buộc chỉ **sống** nếu nó đi cùng cái được thiết kế. `Prompt-Claude-Design.md` chở sang `UI-F7`, `UI-F8`, `UI-F9`, `INV-I16` — nhưng ⛔ **không chở `INV-I20`**, ⛔ **không chở bốn cổng `§8.4`**, và ⛔ **không chở lệnh bỏ bấm giờ**. ⇒ Cả ba chỗ lệch nằm **đúng** ở ba thứ tôi quên gói.

⇒ ⭐ **Sửa GỐC, ⛔ không sửa từng chỗ:** brief bàn giao thiết kế phải chở **cổng nghiệm thu** sang, ⛔ không chỉ chở **luật hình dạng**. Luật nói *"đừng làm gì"*; cổng nói *"đo bằng gì thì gọi là xong"* — và người thiết kế ⛔ không đoán được vế thứ hai.

#### ⓑ ⭐ Thứ cổng ⛔ KHÔNG đo được, mà bản thiết kế vẫn đóng

⛔ Bốn cổng đều đo **bề mặt**. Chúng ⛔ không hỏi *"màn này có dạy người ta gật bừa ⛔ không"* — và đó là câu `§1 ⓑ` đặt ra rồi **bỏ dở**:

| Câu ⛔ không cổng nào hỏi | Bản dựng trả lời thế nào |
|---|---|
| ⭐⭐ `45%` ca ⛔ không có ứng viên đúng tiền — màn có **trông khác** ⛔ không | ✅ dải `warn` riêng · nút bỏ nền đặc · ⭐ **`Enter` BỊ KHOÁ** · phải bấm **hai lần** |
| Máy có **chọn sẵn** đáp án ⛔ không *(`INV-I16`)* | ✅ ⛔ **⛔ không ca nào**, kể cả ca máy đề xuất |
| Lệnh máy ⛔ không tìm được ứng viên — người làm gì tiếp | ✅ chế độ **Toàn sổ** **bật sẵn** ⇒ ⛔ không ngõ cụt |

⚠ ⇒ **Cân nhắc thêm cổng `G-e`** cho vòng sau: *tỷ lệ ca lệch tiền được xác nhận* — ⛔ **không** đo bằng đồng hồ *(owner đã bỏ bấm giờ)* mà bằng **đếm**: bao nhiêu mối nối do người tạo rơi vào ca `lệch`, so với bao nhiêu ca lệch được đưa ra. Tỷ lệ ấy **gần `100%`** nghĩa là bước hai bước ⛔ không cản được gì.

## §7 · Changelog

- **v0.8** *(2026-10-02, `fls-ba`)*: `G-d` *(§8.4)* đổi thước *"người thật"* theo `09` **v1.14** ⓑ — `actor` ⛔ thuộc `ACTOR_MAY` ∧ ⛔ UAT *(danh mục người **hoãn**, owner 02/10: *"defer phần tài khoản, làm xong công cụ đã"*)*. Sổ thật ⛔ đổi: `hinh='T'` **1** = cú UAT ⇒ **0**.
- **v0.7** *(2026-10-01 khuya, `fls-ba`, `KQ-010 F-2 ⓓ`)*: `G-d` *(§8.4)* chỉ đếm mối nối `hinh='T'` của **người thật** — loại máy + UAT theo `QĐ-ITL-150 ⓐ` *("bất kỳ cổng")* và luật bản trắng `09` v1.13. Đo sổ thật: `hinh='T'` **1** = cú UAT ⇒ **0**. `G-d` vẫn là cổng **đo tay** *(phép đo máy ⇒ phiếu sau, ⛔ `WO-011`)*.

- **v0.6** *(2026-09-21, `QĐ-ITL-147` — owner nới trần)*: ⭐⭐ **`G-b` đổi ngưỡng `≤ 9` → `≤ 11` ⇒ ĐẠT.** Owner chọn **giữ yêu cầu và ký con số mới** thay vì bỏ `2` ô. ⚠⚠ **Ghi kèm điều kiện, vì ⛔ không có nó thì cổng này chết cùng ngày nó được sửa:** `11` phải là trần **THẬT** — trường thứ `12` vẫn phải **bỏ một** hoặc **xin một quyết định nữa**. ⛔ Một cổng mà **ngưỡng nới được mỗi khi bị chạm** thì nó ⛔ không đo gì cả, nó chỉ **ghi lại hiện trạng** — và đó là cách `339 → 735` xảy ra mà ⛔ không ai thấy. ⛔ **`G-a` VẪN TRƯỢT** *(`1.553` thay vì `738`)*, và `GAP-TEST-04` chỉ ra vì sao nó trượt **trong im lặng**: `INV-I20` — bất biến **trung tâm** của màn — có ⛔ **`0`** bài test gọi tên *(so `INV-I16`: **45**)*, nên ⛔ **không cổng máy nào** hỏi câu ấy. ⇒ ⭐ Cổng `§8.4` ⛔ **không tự chạy**; chúng là **danh sách phải đo tay** cho tới khi có bài.
- **v0.5** *(2026-09-21, `QĐ-ITL-146` — bàn giao thiết kế về)*: ⭐⭐⭐ **Thêm `§8.5` — bốn cổng của `§8.4` lần đầu có một thứ để đo, và `2/4` TRƯỢT.** Chúng được dựng `18/09` cho một bản vẽ **chưa tồn tại**; nay soi thẳng vào mã bản dựng: `G-a` **`1.553`** *(đòi `738`)* ⛔ trượt · `G-b` **`11` trường** *(đòi `≤ 9`)* ⛔ trượt · `G-c` **`0` bản sao** nhưng **`6` mã nội bộ** lộ sau *«Xem đủ trường»* ⚠ một nửa · `G-d` ⬜ **⛔ chưa đo được** *(bản dựng chưa nối kho)*. ⛔⛔⛔ **Và ⛔ KHÔNG cái nào là người thiết kế vượt rào — đó mới là chỗ đáng học.** `G-b` trượt vì **owner ＋ kế toán đòi thêm `3` trường** *(`QĐ-ITL-144`)* trong khi **`CR#12` của chính owner** đặt trần `9`; hai câu ấy cách nhau **vài giờ** và nằm ở **hai tệp khác nhau**, nên ⛔ không ai thấy lúc phát biểu. `G-a` trượt vì bộ lọc chỉ có **ba** chip và gộp **`768` đích cuối** vào việc hằng ngày ⇒ **thiếu một KHÁI NIỆM** *(`INV-I20`)*, ⛔ không thiếu một cú bấm. ⭐⭐ **Bài học chung, và nó là lỗi của tôi:** `Prompt-Claude-Design.md` chở sang `UI-F7`·`UI-F8`·`UI-F9`·`INV-I16` nhưng ⛔ **không chở `INV-I20`**, ⛔ **không chở bốn cổng `§8.4`**, ⛔ **không chở lệnh bỏ bấm giờ** — và **cả ba chỗ lệch rơi đúng vào ba thứ tôi quên gói**. ⇒ Sửa **GỐC**: brief bàn giao phải chở **cổng nghiệm thu**, ⛔ không chỉ chở **luật hình dạng** — luật nói *"đừng làm gì"*, cổng nói *"đo bằng gì thì gọi là xong"*, và người thiết kế ⛔ không đoán được vế thứ hai. ⭐ `ⓑ` ghi ba thứ **⛔ không cổng nào đo mà bản thiết kế vẫn đóng** *(`Enter` khoá ở ca lệch · máy ⛔ không chọn sẵn · Toàn sổ bật sẵn khi bí)*, và đề nghị cổng **`G-e`** cho vòng sau — đếm **tỷ lệ ca lệch được xác nhận**, ⛔ **không** bằng đồng hồ.
- **v0.4** *(2026-09-18 tối, `QĐ-ITL-137` — owner: *"bỏ lý do, chưa cần"*)*: cổng **`G-d` đổi thước**. ⛔⛔ Bản trưa đặt `G-d` = *"sự kiện **rời** hàng chờ / 28 ngày"*, mà đường rời chính của nó là **người gõ lý do** — đúng cột owner vừa hoãn ⇒ **cổng rỗng ngay khi ra đời**. ⭐⭐ **Bài học, và nó lớn hơn cổng này:** một cổng ⛔ **KHÔNG được** dựa vào một **ô nhập liệu** — ô nhập liệu có thể bị gỡ khỏi màn bất cứ lúc nào, và khi ấy cổng chết **lặng**. ⭐ Thước mới là **vết của chính hành động**: `fls_pm_link.hinh='T'` — mối nối do **NGƯỜI** tạo, sinh ra **vì** có người ghép chứ ⛔ không vì có người nhớ điền. Đo `18/09`: **`0`**. ⚠ Kèm: `US-039` thu hẹp · `US-045` **hoãn** *(mất dụng cụ đo)* · câu `vi_sao` do **MÁY** sinh thì ⭐ **GIỮ** — ⛔ không lẫn với cột lý do người gõ.

- **v0.3** *(2026-09-18 chiều, `QĐ-ITL-136` — owner sửa TRỤC của bản trưa)*: thêm **`§8.0`**, và nó **hạ hiệu lực `§8.1`–`§8.3`** vừa viết vài giờ trước. ⛔⛔⛔ **Bài học đắt nhất của cả tệp, và nó về TÔI:** tôi đo được `6.165` dòng tiền ⛔ không có lệnh chi, thấy nó to gấp `8,4` lần việc ghép, rồi **tự đặt cho nó một ý nghĩa nghiệp vụ** — *"việc KIỂM SOÁT"* — mà ⛔ **không một quyết định nào của owner** nói thế; rồi dựng cho nó `SCR-F07`. Owner: *"FLS ⛔ không cần trả lời câu hỏi này"*. ⭐ **Phép đo ⛔ không sai; cái KHUNG đặt quanh phép đo thì sai** — và đó **đúng là** `INV-I16` *(máy ⛔ không được tự trả lời thay người)*, chỉ khác là người vi phạm là **tôi**, còn cổng thì canh **số** chứ ⛔ không canh **cái khung**. ⚠ Nó cũng mâu thuẫn với `QĐ-ITL-56` mà tôi ⛔ không nhận ra: ⛔ **không có quy định nào** nói khoản nào cần lệnh chi ⇒ ⛔ không luật thì ⛔ không vi phạm để soát. ⭐⭐ Trục đúng owner đặt: **`Tự động`** *(máy ghép, người duyệt — `47`)* vs **`Thủ công`** *(người ghép — `738`)* ⇒ **MỘT việc, HAI chế độ**, cộng **hai đích cuối** *(`768` ghép ⛔ không được · `167` lỗi nguồn)* ⛔ không phải việc của ai.

- **v0.2** *(2026-09-18, `CR#12` — owner: *"áp dụng quy trình CR, review lại toàn bộ tài liệu BA"* + *"mới chỉ có component, cần thiết kế tổng thể hơn"*)*: thêm **`§8` THIẾT KẾ TỔNG THỂ**, và nó lật chính `§5` của bản `v0.1`. ⭐⭐⭐ **Chỗ thiếu ⛔ không phải thiếu bản vẽ — là thiếu câu trả lời cho *"việc này là việc GÌ"*.** Ba phép đo mới: ⓐ **hai lằn là HAI VIỆC** *(`738` việc KHỚP vs **`6.165`** dòng tiền ⛔ không có lệnh chi nào — việc **KIỂM SOÁT**, to gấp **8,4 lần**)* ⇒ tách `SCR-F07`; ⓑ ⛔⛔ **hàng chờ ⛔ KHÔNG CÓ LỐI RA** — `8.387/8.387` dòng `UNMAPPED` và nút `Xong` có **`0`** lần bấm ⇒ vẽ lại một danh sách ⛔ **không** làm nó ngắn đi nếu ⛔ không gì rời khỏi nó được ⇒ `INV-I20`; ⓒ bốn việc khác nhau về **NHỊP** *(một phút mỗi sáng · hằng ngày · theo kỳ · gửi cho người khác)* đang bị trộn vào **một danh sách**. ⚠ Owner bỏ bấm giờ ⇒ cổng `Đ4` *"nhanh hơn ≥40%"* **chết**, thay bằng `G-a`…`G-d` — trong đó ⭐ **`G-d`** *(sự kiện rời hàng chờ / 28 ngày)* là cổng duy nhất ⛔ **không** phụ thuộc bản vẽ. ⭐ Kèm: khai `US-KT-052`…`056` ở `BA-03` — năm story `BA-13` đã **trích làm căn cứ** từ `14/09` mà `BA-03` ⛔ **chưa bao giờ khai**.

- **v0.1** *(2026-09-18, owner: *"overdone và ⛔ chưa user-friendly — cho tôi lộ trình đánh giá và thiết kế lại"*)*: bản đầu.

  ⭐⭐⭐ **Phép đo lật chẩn đoán của chính owner — theo hướng nặng hơn.** *"Overdone"* ⛔ **không phải** chuyện gu: `git log` cho thấy màn đi `339 → 735` dòng qua **7** lần sửa trong **2** ngày, và ⛔ **KHÔNG** lần nào tổng đi xuống. Mỗi thứ thêm vào đều có một phép đo chống lưng và đều **đúng riêng lẻ**. ⇒ Đây là khuyết tật của **quy trình**, và nó sẽ **tái diễn** sau mọi lần vẽ lại nếu ⛔ không có `Đ5`.

  ⭐⭐⭐ **Và một phép đo ⛔ chưa ai từng lấy, nó đổi cả chỗ đứng của lộ trình:** sổ vết nói **⛔ KHÔNG một kế toán nào đã bấm một nút nào** trên màn này — `0` ghép tay · `0` bỏ ghép · `0` lý do · `0` bút toán; `108.128` sự kiện và `2.262` mối nối đều do **máy**, đều trong **một ngày** `10/09`. ⇒ Cả `BA-12` lẫn lời chê hôm nay đều là kết luận từ việc **NHÌN** màn, ⛔ chưa phải từ việc **DÙNG** màn. Đó là lý do `Đ1` đứng trước mọi bản vẽ, và là lý do `Đ2` **bị giữ lại**.

  ⭐ **`12/20` dòng ĐẦU màn hình là ngõ cụt** *(60%)*, trong khi rổ `khong` chỉ chiếm `49,5%` toàn danh sách — vì thứ tự màn là `(tiền tệ, tiền giảm dần)`, ⛔ **không** ngẫu nhiên. ⇒ ⛔ **Đừng suy trải nghiệm màn hình từ tỷ lệ toàn tập**; phải đo **đúng trang đầu**.

  ⚠ **Một lỗi tôi mắc lại dù `BA-12` đã ghi:** quét `Reject` trên cả `fls_pm_line` ra **3.486**, vì bảng giữ **9 bản sao ảnh chụp**. Số đúng **166** khi khoá về ảnh **hiệu lực**. Cùng lớp lỗi `GAP-NAP-03`, lần thứ hai, và lần này ⛔ không có cổng nào chặn — chỉ có việc tôi tự nhớ ra.
