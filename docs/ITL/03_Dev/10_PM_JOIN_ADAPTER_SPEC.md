# 10 — SPEC: Adapter ghép PM (bậc thang 6 tầng)

**Version:** v0.8 · **Ngày:** 2026-08-27 · **Chủ sở hữu:** Tech Lead
> ⛔⛔ **v0.2 ĐO TRÊN DỮ LIỆU THẬT VÀ BA TIỀN ĐỀ CỦA v0.1 BỊ LẬT.** Đọc §1a trước khi đọc phần còn lại — §2 và §3.1 của v0.1 dựng trên hai giả định sai.
**Loại:** spec thi công · **Thực thi:** `QĐ-ITL-44` bước ④ *(cải thiện ghép PM)*
**Căn cứ:** [`09_CR1_PM_JOIN_MODEL`](09_CR1_PM_JOIN_MODEL.md) v1.0 *(mô hình)* · `QĐ-ITL-48` *(mapping là việc của FLS)* · `QĐ-ITL-45` *(FLS chỉ đọc `fps_*`)* · `INV-I16` *(không mặc định im lặng)* · `FLS-Process` §3 chặng 2·7 + §7.6 *(số đo thật)*

> ⚠ **Bản tạm gồm gì:** thứ tự bậc thang, luật từng tầng, cổng tiền, và test. **Chưa gồm:** ngưỡng dung sai (`GAP-CR1-01`), luật 6 nhãn (`GAP-ITL-56`), pattern regex cụ thể (`GAP-ITL-57`). Ba chỗ đó chờ kế toán chốt — spec chừa cửa, không tự bịa.

---

## §1a ⛔ · BA TIỀN ĐỀ CỦA v0.1 BỊ SỐ LIỆU LẬT (đo 2026-08-27)

Nguồn đo: `[Importrange]PM_Unpivot` **3.703 dòng** × `Transaction Mapping L1` **10.100 dòng**, đọc live. Code + cổng: `fls/adapters/pm_join.py` · `tests/adapters/test_pm_join.py` (26 phép thử).

| # | v0.1 nói | Đo thật nói |
|:--:|---|---|
| ⓵ | *"`reference` sống ở **phiếu**; một phiếu N dòng dùng **chung một mã**"* | Sống ở **DÒNG**. Trong 1.468 phiếu có 579 phiếu nhiều dòng, và **526 phiếu mang 2–36 mã KHÁC NHAU**. Tiền ở cột *"Tổng số tiền thanh toán"* cũng **khác nhau từng dòng** (493/579). ⇒ Phép ghép là **bank ↔ DÒNG**. Và con số *"289 dòng dư bị bỏ im lặng"* **không tái lập được** từ nguồn này |
| ⓶ | Lo một mã → **N dòng PM** | Chiều **ngược lại** lớn hơn nhiều: một mã → **N DÒNG BANK**. 8.627 mã có 1 dòng · 297 có 2 · 58 có 3 … tới **32**. Đó là **trả nhiều lần** + **phí bank dùng chung mã** |
| ⓷ | `T-JOIN-03`: *"phiếu 3 dòng ⇒ **3 dòng ITL**"* | **KHÔNG làm.** Tách một dòng bank thành N dòng sổ làm **vỡ thế 1–1 giữa sổ và nguồn** — thứ mà mọi cổng đối soát đang dựa vào *(`vào = sổ + loại + rỗng + trùng`)*. Đổi lại được **27 dòng**. ⇒ Hình `A`+`C` = **2.650/2.677 = 99,0%** mối nối đậu thẳng; hình `B` cần bảng nối `fls_pm_link` ⇒ **`GAP-JOIN-03`** |

### §1a.1 ★★★ Con số phải nói thẳng: phép ghép ĐÚNG **nhỏ hơn** phép ghép đang dùng

| | Số dòng | % | Nghĩa |
|---|--:|--:|---|
| AS-IS `VLOOKUP` *"đã ghép"* | 3.312 | 33,2% | tìm thấy mã — **không kiểm tiền** |
| … trong đó **không khớp tiền** | **968** | 29% của 3.312 | ghép rồi mà tiền không về |
| **FLS ghép được, không phải đoán** | **2.677** | **26,79%** | qua cổng Σ |
| FLS: có mã khớp mà tiền không khớp | **678** | | → **hàng chờ kèm lý do có tên** |

⛔ **Đây KHÔNG phải tụt lùi.** Đây là lần đầu con số có nghĩa: 968 dòng mà AS-IS báo *"đã ghép"* thực ra không đối soát được về tiền.

### §1a.2 · Sáu hình dạng — thay cho cổng Σ một-lần của v0.1

| Hình | Mô tả | Mã | Dòng bank | Xử |
|:--:|---|--:|--:|---|
| **A** | 1 bank × 1 PM · Σ khớp | 2.256 | 2.256 | ✅ ghép |
| **B** | 1 bank × N PM · Σ khớp | 27 | 27 | ✅ **ghép** — vào `fls_pm_link`, **69 mối nối** *(`GAP-JOIN-03` đóng 27/08)* |
| **C** | N bank × 1 PM · Σ khớp *(trả nhiều lần)* | 80 | 394 | ✅ ghép |
| **D** | N bank × M PM · Σ khớp | 5 | 27 | ⛔ **KHÔNG ĐOÁN** |
| **E** | tiền tệ **khác nhau** | 119 | 199 | → người *(cần tỷ giá)* |
| **F** | Σ lệch **quá dung sai** | 305 | 428 | → người *(dung sai **1.000 VND**, `QĐ-ITL-57`)* |

> ⭐ **Chạy thật trên nguồn live 27/08** *(10.100 dòng, ⛔ không phải hiện vật 9.992 dòng)*: `A` **2.272** · `B` **29** · `C` **400** · `D` 27 · `E` 199 · `F` **426** dòng · không có mã 105 · không thấy mã PM 6.579. Vào kho: **10.030 dòng sổ · 2.745 mối nối** *(`A` 2.272 · `B` **73** · `C` 400)* · **Σ lệch 0**. Bảng trên đo trên **hiện vật ghim**; số live lệch vài dòng vì mẫu số khác — ⛔ đừng đọc lẫn.
| — | không có mã · không thấy mã PM | | 105 · 6.522 | → hàng chờ |

⛔ **`D` bị từ chối DÙ Σ KHỚP.** N×M có nhiều cách chia tiền khác nhau mà **đều cộng đúng** — chọn một cách là máy quyết thay người (`INV-I16`).

⚠ **Thứ tự phép kiểm là có chủ ý:** tiền tệ kiểm **TRƯỚC** Σ. Cộng hai số khác đơn vị ra một con số **trông hình** nhưng vô nghĩa, và nếu nó tình cờ bằng nhau thì ta vừa ghép sai mà không cổng nào đỏ. **199 dòng** thuộc lớp này.

⭐ **Dung sai Σ = 1.000 VND** — owner chốt 27/08, `QĐ-ITL-57`, đóng `GAP-CR1-01`. Cứu **+24 dòng** *(2.677 → **2.701**, tỷ lệ **26,79% → 27,03%**)*.

⛔⛔ **Và nó là 1.000 VND, ⛔ không phải "1.000 đơn vị tiền tệ nào cũng được".** Đo **trước khi code**:

| Cách đọc | Cho qua | Ca xấu nhất |
|---|--:|---|
| 1.000 **đơn vị bất kỳ** | 105 mã · 171 dòng | lệch **660,04 USD** trên giao dịch **59,96 USD** = **1.100%** của chính nó |
| 1.000 **chỉ cho VND** | 20 mã · 24 dòng | lệch lớn nhất **2,00 đồng** *(làm tròn thuần)* |

⇒ Cách đọc thứ nhất cho qua **tiền không khớp thật**, ⛔ không phải phí bank. ⭐⭐ **`QĐ-ITL-62` (2026-08-28): ngoại tệ ⛔ KHÔNG có dung sai — máy ⛔ không được tự đóng một ca lệch dù chỉ vài xu** *(đóng `GAP-CR1-03`)*. ⛔ Số `0` ấy nay ⛔ **không còn nghĩa "chưa chốt"**; nó **là** quyết định, và có bài test khoá **cả bảng** `DUNG_SAI`.

⚠ **Chỗ hở có tên, ⛔ không ẩn:** dung sai **tuyệt đối** nên với giao dịch **nhỏ** nó có thể lớn hơn cả giao dịch. **39 dòng sổ** VND có số tiền ≤ 1.000 đồng. Lát đã đo ⛔ không có ca nào bị ghép sai vì thế, nhưng **luật vẫn hở** — đã khoá thành test `test_CHO_HO_da_biet__dung_sai_tuyet_doi_lon_hon_giao_dich_NHO`. ★ Nếu muốn bịt: một luật **theo tỷ lệ** khớp dáng phí bank tốt hơn hẳn *(đo được: ≤ 0,5% cứu **73 mã / 117 dòng**, và dáng thật của phí là **bank = lệnh + phí** với số trên lệnh **tròn**)* — nhưng đó là quyết định tiếp theo của kế toán trưởng. Trong `F` đã nhìn thấy rõ hai lớp sẽ được cứu nếu kế toán cho dung sai: **phí bank** *(`15.400 VND` · `68,53 USD` dùng chung mã với khoản chính)* và **trả thiếu/thừa lẻ**. ⛔ Nới ngưỡng là quyết định của kế toán trưởng.

### §1a.3 · Ba tầng CHƯA làm, và vì sao

| Tầng | Chặn bởi |
|:--:|---|
| ~~**T0** dán nhãn *"không cần lệnh chi"*~~ | ⛔ **RA KHỎI BẬC THANG 27/08.** `QĐ-ITL-56`: **không có quy định nào** nói khoản nào cần lệnh chi ⇒ ⛔ không có luật để mã hoá, và máy dán nhãn đó là **máy tự đặt ra quy định** *(`INV-I16`)*. Thay bằng **xếp hàng chờ theo TIỀN**: **799 dòng** *(10,4% hàng chờ)* phủ **90% tiền TRONG TỪNG tiền tệ** *(VND 310 · USD 444 · SGD 13 · HKD 32)* — cách này ⛔ không nói dòng nào *"không cần lệnh"*, nó chỉ nói **xem cái này trước**. `CR#3` **đã đóng 27/08: bỏ hẳn** *(`QĐ-ITL-58`)* |
| **T3** đọc mã lệnh trong diễn giải | `GAP-ITL-57` *(70 hay 158 dòng)* **và** luật ⛔ không đọc cột có thể chứa tên người — cần owner cho phép phạm vi đọc trước |
| **T4** người bấm Ghép ở `F01` | cần `fls/api` + `fls/web` (P4·P6). Đầu vào cho nó **đã có**: 678 dòng `D/E/F` kèm lý do có tên chính là hàng đợi của T4 |

⇒ `T-JOIN-06` và `T-JOIN-07` **chưa có phép thử** — vì chưa có gì để thử. Ghi ra đây để *"9 test T-JOIN"* không bị đọc thành *"9/9 xong"*.

---

## §1 · Đặt vấn đề — hai việc tay khác nhau, đừng gộp

| | Việc AS-IS | Code hoá được? |
|---|---|---|
| **`OP-02`** | Người gõ `Reference number` của giao dịch bank vào dòng PM — **người tuyên bố** "tiền này thuộc lệnh này" | ⛔ **Không thay được.** Không khoá nào tự nối. Chỉ làm **rẻ đi** |
| **Chặng 7** | `Transaction Mapping L1` **tra** khoá đó ra 15 cột PM bằng `VLOOKUP` một tầng | ✅ **Thay hoàn toàn**, và đúng hơn `VLOOKUP` |

⛔ **Sai lầm phải tránh:** hiểu code hoá = *"máy tự ghép hết"*. Máy làm hết phần **tra**; phần **quyết** co từ ~6.500 dòng xuống vài chục.

## §2 · Sai gốc của phép ghép AS-IS — grain lệch một tầng

`reference_number` sống ở **phiếu** (`fps_pm_slip`, `schema.py:653`), không ở **dòng** (`fps_pm_line`). Một phiếu N dòng dùng chung một mã ⇒ `VLOOKUP(reference)` lấy **dòng đầu**, **bỏ im lặng** phần còn lại — đo được **289 dòng dư bị bỏ**.

⇒ Phép ghép AS-IS *giả vờ* bank↔line, thực chất là bank↔slip. Luật `OP-03` *("1 PMLine ↔ 1 Reference = 1–1")* **bất khả về cấu trúc** — `CR#1` bỏ.

## §3 · Bậc thang — dừng ở bậc đầu tiên khớp

```
T0 dán nhãn "không cần lệnh"  ─┐
T1 ghép phiếu (reference)      ├─→ chia tiền theo fps_pm_line.amount ─→ CỔNG Σ ─→ ghép
T2 tách mã trùng (ref+ngày+tiền)│                                          │
T3 đọc mã trong diễn giải      ─┘                                     lệch │
T4 người bấm Ghép (F01) ────────────────────────────────────────────────────┤
T5 UNMAPPED tường minh ←────────────────────────────────────────────────────┘
```

| Tầng | Luật | Độ tin | Áp tự động? |
|:--:|---|---|---|
| **T0** | 6 nhãn *"không cần lệnh chi"* — thu tiền · phí/lãi bank · điều chuyển nội bộ · mua bán ngoại tệ · doanh thu nền tảng | — | ⏸ **chờ `GAP-ITL-56`** |
| **T1** | `canon(bank.reference)` = `canon(fps_pm_slip.reference_number)`, **hit duy nhất** | CAO | ✅ |
| **T2** | bộ ba `reference + ngày + số tiền`; **còn va ⇒ KHÔNG đoán**, đẩy T4 | CAO | ✅ khi tách được 1 |
| **T3** | regex mã lệnh nhúng trong diễn giải *(`US-KT-037`)* | TRUNG | ✅ **chỉ khi qua cổng Σ** |
| **T4** | `F01` drawer: máy **xếp hạng** phiếu ứng viên → người **chọn phiếu** | người quyết | ⛔ máy không tự chọn |
| **T5** | `work_status='UNMAPPED'`, `*_thyt IS NULL`, vào hàng chờ, **đếm được** | — | ⛔ cấm gán mặc định (`INV-I16`) |

### §3.1 · Cổng tiền — chung cho mọi tầng

```
Σ fps_pm_line.amount (theo pm_id)  ==  tiền bank  ⇒  cho ghép
                                   !=              ⇒  giữ UNMAPPED, vào hàng chờ
```

⛔ **Lệch ⇒ không chia bừa.** Ngưỡng dung sai cho chênh lẻ *(phí bank, tỷ giá)* = **`GAP-CR1-01`, chưa chốt** ⇒ tạm **dung sai = 0**, mọi lệch vào hàng chờ. Nới ngưỡng là quyết định của kế toán, không phải của code.

## §4 · Bốn điểm thi công

### 4.1 · `canon()` — chuẩn hoá khoá là BƯỚC ĐẦU TIÊN, không phải chi tiết phụ

`reference_number` là `STRING`, **không `UNIQUE`**. Phải chuẩn hoá **cả hai phía** trước khi so, nếu không mất dòng mà không ai biết.

```python
def canon_reference(raw: str | None) -> str | None:
    """Chuẩn hoá mã tham chiếu. Trả None nếu không còn ký tự có nghĩa."""
    if raw is None:
        return None
    s = unicodedata.normalize("NFKC", str(raw)).strip().upper()
    s = re.sub(r"[\s\-_.,/\\]+", "", s)      # bỏ khoảng trắng + dấu phân cách
    return s or None
```

⚠ **Chưa gồm** việc cắt tiền tố bank *(`FT<yy><ddd>`…)* — phải đo trên dữ liệu thật trước khi thêm, vì cắt sai là **gộp hai lệnh khác nhau**. Xem `GAP-JOIN-01`.

### 4.2 · Định danh dòng = `fps_pm_line.line_id`

⛔ **KHÔNG** dùng cột `ID PMLine` gõ tay trong sheet *(vốn `#N/A` đầy)*. `line_id` là khoá 1–1 mức dòng duy nhất bền.

### 4.3 · Ghép của người là sự kiện DÍNH, không phải giá trị bị tính lại

FLS chỉ đọc `fps_*` (`QĐ-ITL-45`) ⇒ khi kế toán bấm Ghép ở `F01`, mối nối **lưu trong `fls_*`**, **không ghi ngược** vào PM.

⚠ **Hai hệ quả phải nhận:**
1. Cột `Reference number` bên PM sẽ **mãi không đầy** — **FLS thành nơi giữ mối nối**.
2. ⛔ Adapter chạy lại **phải tôn trọng match người đã làm** — cấm suy lại từ reference rồi đè. *(Test `T-JOIN-07`.)*

### 4.4 · Bù lại chỗ AS-IS đánh mất

Chặng 8 hiện **vứt 12 cột** PM/PE/PI. Adapter mới mang vào `canon`:

| Trường | Nguồn | Vì sao |
|---|---|---|
| `pm_line_id` | `fps_pm_line.line_id` | lineage bền, thay `PMLine` gõ tay |
| `le_payer` | `fps_pm_slip.payer_id` *(`schema.py:641`)* | bắt giao dịch nội bộ; nguồn code không phải cột Sheet dễ vỡ |

⚠ Cả hai đang chờ **`QĐ-ITL-20`** — hiện là ghi chú thiết kế trong `INV-I05`/`DD-I05`, **chưa nâng thành QĐ**.

## §5 · Test — mỗi tầng một cổng

| ID | Tầng | Given → Then |
|---|:--:|---|
| `T-JOIN-01` | canon | `"ft25 123-456"` và `"FT25123456"` ⇒ **cùng** khoá |
| `T-JOIN-02` | canon | mã chỉ có dấu/khoảng trắng ⇒ `None`, **không** ghép với `None` phía kia |
| `T-JOIN-03` | T1 | phiếu 3 dòng, `Σ amount` = tiền bank ⇒ **3 dòng** ITL, mỗi dòng một `line_id` *(chống lỗi 289 dòng dư)* |
| `T-JOIN-04` | cổng Σ | `Σ amount` ≠ tiền bank ⇒ `work_status='UNMAPPED'`, **0 dòng** được gán, có trong hàng chờ |
| `T-JOIN-05` | T2 | 1 reference → 2 phiếu, khác ngày+tiền ⇒ tách đúng 1; **cùng** ngày+tiền ⇒ **không đoán**, đẩy T4 |
| `T-JOIN-06` | T3 | diễn giải chứa mã lệnh ⇒ ghép **chỉ khi** qua cổng Σ; không qua ⇒ `UNMAPPED` |
| `T-JOIN-07` | dính | người ghép tay → chạy adapter lại ⇒ match **giữ nguyên**, không bị đè |
| `T-JOIN-08` | `INV-I16` | không ghép được ⇒ `hd_thyt IS NULL`; ⛔ **cấm** xuất hiện giá trị mặc định nào |
| `T-JOIN-09` | parity | tổng dòng vào = tổng dòng ra *(ghép + UNMAPPED + nhãn T0)*; **0 dòng rơi im lặng** |

## §6 · Nói thật về mức cải thiện

> ⭐⭐ **BỐN tỷ lệ ghép đang cùng lưu hành. Nối chúng lại đây một lần, ⛔ đừng đọc lẫn.**
>
> | Con số | Mẫu số | Đo trên | Nghĩa |
> |--:|--:|---|---|
> | **33,8%** *(3.301)* | 9.767 | bản **.xlsx offline** *(đo trước 26/08)* | AS-IS *"tìm thấy mã"*, ⛔ **không kiểm tiền** |
> | **33,2%** *(3.312)* | 9.992 | sổ **live** *(đo 27/08)* | cùng phép đếm, mẫu số khác ⇒ hai con số này **không lệch nhau về bản chất** |
> | **26,79%** *(2.677)* | 9.992 | FLS, **qua cổng Σ** | **DÒNG SỔ** ghép được mà ⛔ không phải đoán |
> | **2.719** | — | FLS | **MỐI NỐI** *(≠ dòng sổ)* — hình `B` 27 dòng mang **69** mối nối |
>
> ⛔ **968 dòng** mà AS-IS báo *"đã ghép"* thì **không khớp tiền** ⇒ đó là toàn bộ khoảng cách giữa **33,2%** và **26,79%**. ⇒ Mọi chỗ công bố tỷ lệ ghép phải **đưa kèm cả hai**, vì con số **đúng nhỏ hơn** con số **đang dùng** và một mình nó **trông như một bước lùi**.
>
> ⚠ Bảng §6 dưới đây tính trên nền **33,8% / 9.767** *(bản offline)* — giữ nguyên làm lịch sử; ⛔ đừng cộng nó vào các con số live.

Nền: **9.767 dòng tiền**, hiện ghép **33,8%** *(3.301)*, không ghép **66,2%** *(6.466)*.

| Nguồn cải thiện | Thu hồi |
|---|--:|
| T2 — mã trùng đang bị bỏ im lặng | ≤ **289 dòng** |
| T3 — mã trong diễn giải | **70 hoặc 158** *(`GAP-ITL-57`, **19,57 tỷ** phụ thuộc)* |
| **Cộng dồn code, một mình** | **33,8% → ~37–38%** |

⛔ **Code một mình KHÔNG cứu được 66,2%.** Bước nhảy thật nằm ở **hai câu trả lời của kế toán**:

- **`GAP-ITL-56`** luật 6 nhãn — nếu phần lớn dòng thật sự *không cần* lệnh thì mẫu số co lại. Con số cũ *3.480 dòng / 92% tiền* **chưa tái lập được** ⇒ spec **không hứa**.
- **`GAP-ITL-29`** — **4.940 dòng chi tiền (~237 tỷ)** không truy được về lệnh nào. **Máy không phát minh ra lệnh không tồn tại.** Đây là câu hỏi nghiệp vụ, không phải bug.

## §7 · Việc mở

| ID | Việc | Ai |
|---|---|---|
| `GAP-JOIN-01` | `canon()` có được cắt tiền tố bank không — đo trên dữ liệu thật; cắt sai = **gộp hai lệnh khác nhau** | Tech Lead |
| `GAP-JOIN-02` | Luật xếp hạng ứng viên ở `F01` *(trọng số reference/tiền/ngày/payee)* — chưa đặc tả | Tech Lead + `AC-B` |
| `GAP-CR1-01` | Ngưỡng dung sai cổng Σ | Kế toán trưởng |
| `GAP-CR1-02` | `reference + ngày + tiền` có đủ tách 75 mã trùng | đo dữ liệu thật |
| `GAP-ITL-56` | Luật 6 nhãn *(chặn T0)* | kế toán |
| `GAP-ITL-57` | 70 hay 158 dòng *(chặn T3)* | kế toán |

## Changelog

- **v0.8** (2026-08-28): ⭐⭐ **`QĐ-ITL-63` — thêm `dung_sai_ghep_tay(cur, tien_bank) = min(dung_sai_cua(cur), 0,5% × tien_bank)`.** Một **chỗ duy nhất** quyết định dung sai vẫn là `pm_join.py`; cửa ghép tay *(`repo/ghi_tay.py`)* và danh sách ứng viên *(`repo/doc_bao_cao.py`)* **đều gọi hàm này** — ⛔ không ai tự tính lại. ⛔ Cửa ghép **TỰ ĐỘNG** vẫn dùng `dung_sai_cua` *(1.000 phẳng, `QĐ-ITL-57`)*: con số ấy **được đo tại chỗ đó**. ⭐ Diễn tập ĐỎ **hai chiều**: bỏ tỷ lệ ⇒ đỏ 2 bài · bỏ số tuyệt đối ⇒ đỏ với `18.455.849 ≠ 1.000`.
- **v0.7** (2026-08-28): ⭐⭐ **`QĐ-ITL-62` — ngoại tệ ⛔ KHÔNG có dung sai**, đóng `GAP-CR1-03` *(câu hỏi kế toán cuối cùng treo từ 27/08)*. Máy ⛔ không được tự đóng một ca lệch dù chỉ vài xu ⇒ dòng nằm lại hàng chờ. **Căn cứ đo trên 2.701 dòng đã ghép:** 2.283 khớp tuyệt đối · 418 có lệch nhưng **400 là trả từng phần** · **lệch thật 18 dòng, toàn bộ 0,40–2,00 đồng** ⇒ ⛔ không ca lệch ngoại tệ nào là làm tròn ⇒ dung sai ngoại tệ mở thêm **0** dòng, chỉ mở thêm rủi ro. ★ Code ⛔ không đổi *(đã là `0`)*; thứ đổi là **nghĩa**: từ *"chưa chốt"* thành **đã chốt**, khoá bằng `test_KHOA_bang_DUNG_SAI_chi_duoc_co_VND` *(khoá cả bảng, diễn tập đỏ)*.
- **v0.6** (2026-08-27): ⭐⭐ **Bộ nạp nay LƯU LẠI dòng lệnh nó đã đọc** — bảng `fls_pm_line` *(migration `0011`, `QĐ-ITL-61`)*. Trước đó nó đọc **3.703 dòng lệnh từ Sheets rồi bỏ đi**, nên thao tác **ghép tay** ⛔ không thể có danh sách ứng viên *(`GAP-API-04`)*. ⛔ Ảnh chụp là **của một lần nạp**, ⛔ không phải danh mục — nạp lại là **thêm ảnh mới**. ⭐ `DongPM` thêm trường `ref_tho` để ảnh chụp giữ **cả** mã nguyên văn lẫn mã đã chuẩn hoá *(chỉ giữ bản chuẩn hoá thì bẻ `canon_ref` đi mà cổng vẫn xanh)*. ⭐ Thêm **hình `T`** vào `fls_pm_link.hinh` — mối nối do **người** ghép ở màn `F01`, đứng cạnh `A`/`B`/`C` do máy ghép; cổng quét mã nguồn nay khai **hai chỗ** được ghi vào `fls_pm_link` *(bộ nạp = máy · cửa ghi = người)* kèm bài chứng minh **cả hai** thật sự có ghi. ⚠ Và ghi lại một con số đo được trên **sổ thật**: trong **25 dòng** hàng chờ thử qua HTTP, chỉ **1 dòng** có ứng viên bậc `ma` *(reference khớp)* — tức phần lớn việc ghép tay sẽ dựa vào **tiền**, đúng chỗ `GAP-JOIN-04` nói là còn thiếu hai trục.

- **v0.5** (2026-08-27): ⭐⭐ **Hai câu trả lời của owner.** ⓵ `QĐ-ITL-57`: **dung sai Σ = 1.000 VND** *(đóng `GAP-CR1-01`)* ⇒ ghép **2.677 → 2.701**, **26,79% → 27,03%**; hình `F` **452 → 428** dòng. ⛔ Đo trước khi code cho thấy *"1.000 đơn vị bất kỳ"* sẽ cho qua ca lệch **1.100% của chính giao dịch** ⇒ **chỉ áp VND**, tiền tệ khác giữ **0** *(`GAP-CR1-03`)*; kèm **chỗ hở có tên**: 39 dòng sổ có tiền ≤ 1.000 đồng, đã khoá thành test. ⓶ `QĐ-ITL-56`: **KHÔNG CÓ quy định** nào nói khoản nào cần lệnh chi ⇒ tầng **`T0` RA KHỎI bậc thang** *(⛔ không có luật để mã hoá)*, `US-KT-036` khai tử, và **mở `CR#3`** vì tiền đề của `QĐ-ITL-28` bị lật. ⭐ Lối ra ⛔ không cần luật nào: **xếp hàng chờ theo TIỀN**.

- **v0.4** (2026-08-27): Thêm bảng **nối BỐN tỷ lệ ghép đang cùng lưu hành** vào đầu §6 *(33,8% offline · 33,2% live · **26,79%** qua cổng Σ · **2.719** mối nối)* — ba con số đầu là **cùng một phép đếm trên ba mẫu số/nguồn khác nhau**, con số thứ tư đếm **thứ khác hẳn**. ⛔ Ghi rõ bảng §6 tính trên nền **offline**, đừng cộng vào số live.

- **v0.3** (2026-08-27): ⭐⭐ **`GAP-JOIN-03` ĐÓNG — hình `B` đậu được.** Bảng nối `fls_pm_link(itl_id, pm_line_id, amount, hinh, run_id)`, khoá **hai cột**; cột `fls_itl.pm_line_id` **BỎ** *(mối nối chỉ còn MỘT chỗ)*. ⛔ Kèm **cổng Σ chặn TRƯỚC khi ghi**: Σ tiền mối nối của một dòng sổ phải bằng tiền dòng bank — lệch thì NỔ, ⛔ không ghi dòng nào. ⭐⭐ **Phân biệt hai con số**: **DÒNG SỔ ghép được 2.677** *(tỷ lệ ghép 26,79% tính theo đây — vẫn đúng)* vs **MỐI NỐI 2.719** *(`B` 27 dòng mang **69** mối nối, một dòng chia cho 10 dòng lệnh)*; lệch **42** — cả hai đã khoá trong test. ⚠ Vẫn ⛔ **không** làm `T-JOIN-03` *(tách 1 dòng bank thành N dòng sổ)*: bảng nối giải đúng vấn đề đó mà ⛔ không động đến thế 1–1. Còn `T-JOIN-06`/`07` **chưa có test** — `T0`/`T3`/`T4` vẫn bị chặn.

- **v0.2** (2026-08-27): ⛔ **Đo trên dữ liệu thật và ba tiền đề của v0.1 bị lật** — thêm **§1a**. `reference` sống ở **dòng** không ở phiếu *(526/1.468 phiếu mang 2–36 mã khác nhau)*; chiều lo sai *(một mã → **N dòng bank**, tới 32)*; và ⛔ **không tách một dòng bank thành N dòng ITL** *(vỡ thế 1–1 mà mọi cổng đối soát dựa vào, đổi lại 27 dòng)*. Cổng Σ một-lần → **sáu hình dạng** `A…F`, mỗi hình một con số. ★★★ Và con số phải nói thẳng: ghép **đúng** *(26,79%)* **nhỏ hơn** ghép **đang dùng** *(33,2%)* vì 968 dòng AS-IS báo đã ghép thì **không khớp tiền**. Code `fls/adapters/pm_join.py` · 26 phép thử · **2.650 mối nối đã vào kho** *(`fls_itl.pm_line_id`, migration 0006)*. Mở `GAP-JOIN-03` *(bảng nối cho hình `B`)*. ⛔ Rút *"289 dòng dư"* khỏi §2 — không tái lập được.
- **v0.1** (2026-08-26): **Bản tạm.** Dựng bậc thang 6 tầng từ `CR#1` §3, cổng Σ dung sai 0, `canon()` phác thảo, 9 test, và mức cải thiện đo được *(33,8% → ~37–38% nếu chỉ code)*. Chừa cửa cho 3 GAP chờ kế toán, mở `GAP-JOIN-01/02`.
