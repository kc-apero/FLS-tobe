# Thiết kế màn “Gán lệnh chi với giao dịch” (SCR-F0x)

Bản dựng tham chiếu: `fls-gan-lenh-chi_10.html` (một tệp, tự chạy, không phụ thuộc ngoài Google Fonts).
Bản trước: `_9` (bảng + panel phải), `man-gan-lenh-chi-v2.html` (hai cột, chạy trên dữ liệu thật của kho).
Tài liệu này là **hợp đồng thiết kế** để Claude Code tiếp tục cài đặt — đọc trước khi sửa UI.

---

## 1. Việc màn này phục vụ

Kế toán trả lời **một câu, lặp lại nhiều lần**: *“Lệnh chi này đã đi bằng đồng tiền nào?”*
Trái = lệnh chi (PM, cái công ty **định** chi). Phải = giao dịch sao kê (cái **đã** chi). Việc = nối đúng một cặp.

- Người dùng: 2–3 kế toán, **hằng ngày, từng giao dịch một** (không phải dọn tồn theo đợt).
- Nghiệm thu: **số mối nối do NGƯỜI tạo đi từ 0 lên khác 0**, không phải “app chạy được”.
- Ràng buộc dữ liệu: giao dịch chỉ có **ngày · số tiền+chiều · số chứng từ · nguồn (chuỗi gộp) · diễn giải**.
  Không có: tên đối tác, pháp nhân riêng, số tài khoản riêng, mọi ô phân loại kế toán → **không vẽ chỗ cho chúng**.
- Diễn giải sao kê dài tới **189 ký tự** và với ~50% giao dịch (nước ngoài) là **bằng chứng duy nhất**.

## 2. Luật không được vi phạm

| Luật | Cài đặt trong bản này |
|---|---|
| Máy **đề xuất**, người **quyết** | Không bao giờ chọn sẵn ứng viên. Lệnh máy đề xuất chỉ được đánh dấu (viền đứt, nền warn) |
| Ngân sách trường = 9 ở màn làm | Thẻ PM đúng 9 trường; trường phụ nằm sau “Xem đủ trường” |
| Số của MÁY không lên màn của NGƯỜI | Không hiện thứ hạng, %, id nội bộ, cờ true/false, tên rổ kỹ thuật |
| Một sự thật, một chỗ hiện | Bậc chỉ nói ở **một** chỗ (ký hiệu ①–④ + vạch trái), không lặp thành nhãn chữ |
| Tiền | `tabular-nums`, giữ nguyên đơn vị gốc, **không** cộng gộp hai đơn vị |
| Hàng chờ rỗng = khoẻ mạnh | Trạng thái rỗng đọc như thành tựu (“Hàng chờ đã sạch.”) |

Ba cặp phải phân biệt bằng **hình**, không bằng chữ nhỏ: *chưa có dữ liệu ≠ chưa đọc được ≠ không có*; *máy đề xuất ≠ người đã chốt*; *danh sách đã cắt bớt ≠ không có ứng viên nào*.

## 3. Token

Kế thừa nguyên văn `fls/web/tep/tokens.css` (ink/muted/faint, surface/alt/page/line, accent, good/warn/crit/info, mono + sans IBM Plex). **Token thêm** (khai báo tập trung ở `:root`, không rải mã màu trong component):

| Token | Giá trị | Vì sao |
|---|---|---|
| `--hair` | `color-mix(in srgb, var(--line) 30%, var(--surface))` | Đường kẻ giữa các dòng của lưới dày đặc — `--line` quá đậm khi xếp 30–40 dòng |
| `--evi-bg` | `#0e757024` (dark `#4bb5ad33`) | Nền đánh dấu **bằng chứng** trong diễn giải/số CT/số tiền |
| `--rail` | `clamp(300px,26vw,380px)` | Bề rộng danh sách lệnh chi khi panel ghép đang mở |
| `--b` | đặt **inline theo dòng** | Màu bậc của dòng ứng viên (trỏ lại good/info/warn/line) |

Chạy được cả nền sáng/tối: `data-theme` + `prefers-color-scheme`, nút chuyển ở thanh trên.

## 4. Bố cục

Khung ứng dụng cao bằng màn hình, **trang không cuộn**; mỗi vùng tự cuộn.

```
┌ thanh trên 44px ─────────────────────────────────────────────┐
├ dải lọc + số việc 36px (thay 4 ô thống kê cũ) ───────────────┤
│ ┌ rail lệnh chi ─┐ ┌ vùng làm việc ───────────────────────┐ │
│ │ (chỉ khi đã mở)│ │ đầu: thẻ PM (đứng yên)               │ │
│ │                │ │ thanh tra cứu (đứng yên)             │ │
│ │                │ │ BẢNG GIAO DỊCH — vùng duy nhất cuộn  │ │
│ │                │ │ thanh hành động (đứng yên)           │ │
└─┴────────────────┴─┴──────────────────────────────────────┴─┘
```

- **Chưa mở lệnh nào**: một bảng sổ đầy đủ chiếm toàn bộ bề ngang.
- **Đã mở**: bảng thu về rail `clamp(300px,26vw,380px)`, phần còn lại là bàn làm việc.
- Bảng ứng viên đo theo **`@container` của `.work`**, không theo viewport (rail chiếm chỗ trước).
  Thứ tự hy sinh cột khi hẹp: **Nguồn → Số CT → không bao giờ là Diễn giải** (`minmax(200px,1fr)`).

## 5. Component

| # | Component | Trạng thái |
|:-:|---|---|
| C1 | Dòng sổ (`.mrow`) | chưa gán · đề xuất · đã gán · không gán được · hover · con trỏ bàn phím (`aria-current`) — trạng thái đọc bằng **vạch trái 3px** ＋ chip |
| C2 | Thẻ lệnh chi (`.wh`) | dòng 1: mã · trạng thái · loại · **nội dung** · số tiền · ↑↓✕; dòng 2: lưới fact đều (Người nhận · Số CT · Pháp nhân · Ngân hàng · Tài khoản · CDT); dòng 3: **Xem đủ trường** |
| C3 | Dòng ứng viên (`.cand`) | cột: ○ · **bậc ①–④** · Số CT · Diễn giải · Ngày · Nguồn · Số tiền. Cao **36px cố định**, mở rộng mới cao thêm |
| C4 | Khối đang gán (`.mblock`) | đầy đủ: bậc · diễn giải nguyên văn · ngày · nguồn · số CT · số tiền · lệch · nút bỏ gán |
| C5 | Bộ lọc | Chưa gán / Đã gán / Tất cả, mỗi cái mang số đếm |
| C6 | Dải số việc | gộp một dòng: `x/y đã gán · 47 đề xuất gán · 768 không gán được` |
| C7 | Dải cảnh báo (`.banner`) | crit = máy không tìm được ứng viên · warn = không ứng viên nào đúng tiền · info = danh sách đã cắt bớt |
| C8 | Thanh hành động | Gán / Đổi sang giao dịch đã chọn · bật/tắt · **hai bước** khi lệch tiền · câu gợi ý |
| C9 | Rail | ngày · mã PM · loại + trạng thái / nội dung + số tiền / CDT |
| C10 | Trạng thái khung | rỗng (“Hàng chờ đã sạch.”) · không có ứng viên · không khớp bộ lọc |

## 6. Bốn quyết định khó — và lý do

1. **Bốn bậc**: phân bằng **thứ tự + một ký hiệu ①②③④ tô màu** (good/info/warn/—) ＋ vạch trái 3px, **không** nhóm có tiêu đề (tốn dòng) và **không** bốn chip cùng cỡ (bậc ④ chiếm 149/226 ứng viên sẽ nhuộm hết màn). Nghĩa của ký hiệu nói **một lần** ở chú giải trong thanh tra cứu ＋ tooltip.
2. **Diễn giải dài**: cắt **một dòng** trong bảng ＋ liên kết `đủ ↓` **chỉ hiện khi thật sự bị cắt** (đo `scrollHeight` sau khi dàn trang, không đoán theo số ký tự) ＋ `title` để hover đọc nguyên văn. Không dùng tooltip làm lối duy nhất.
3. **Đề xuất ≠ đã gán**: đề xuất = viền **đứt** + nền warn + **không chọn sẵn**; đã gán = khối xanh `.mblock` **trên** bảng, đồng thời dòng tương ứng vẫn nằm trong bảng để đổi.
4. **Chống gật phản xạ**: khi **không** ứng viên nào đúng số tiền → dải warn riêng, thanh hành động đổi nền, nút chính **bỏ nền đặc**, **`Enter` bị khoá**, phải bấm **hai lần** (“Xác nhận gán lệch …”). Độ lệch hiện dạng viên `Δ −12.40` nền warn nhạt.

**Bằng chứng được đánh dấu** (`<mark>`, nền `--evi-bg`): số chứng từ **chỉ khi trùng đúng** số của lệnh chi, số tiền khi khớp tuyệt đối, và tên vendor trong diễn giải. Bộ **từ rác** loại các từ pháp lý (TNHH, JSC, JOINT, STOCK, COMPANY, INC, LTD, PTE, CP, VIỆT NAM…) để không tô nhiễu; quét **một lượt** bằng regex hợp nhất nên không lồng `<mark>`.

## 7. Bàn phím

| Ở màn sổ | |
|---|---|
| `↑` `↓` | di chuyển con trỏ chọn dòng PM (tự cuộn theo) |
| `→` hoặc `Enter` | mở vùng ghép của dòng đang chọn |

| Ở vùng ghép | |
|---|---|
| `↑` `↓` (`k` `j`) | đổi sang lệnh chi trước/sau |
| `←` | quay lại màn sổ (giữ nguyên dòng đang chọn) |
| `Enter` | gán — **chỉ khi ứng viên đúng số tiền**; ca lệch phải xác nhận bằng chuột |
| `/` | nhảy vào ô tìm giao dịch |
| `Esc` | thoát ô tìm, hoặc đóng vùng ghép |

Sau khi gán xong, màn **tự nhảy sang lệnh chưa gán kế tiếp** (nhịp làm việc liên tục).

## 8. Tra cứu toàn sổ

Chip **“Toàn sổ”** đổi nguồn danh sách từ *ứng viên máy đề xuất* sang *toàn bộ giao dịch trong sổ*, bậc được **tính lại theo lệnh đang mở** (khớp số CT → ①, đúng số tiền → ②, còn lại → ④). Với lệnh máy không tìm được ứng viên nào, chế độ này **bật sẵn** — màn không bao giờ là ngõ cụt.
Trong bản dựng, “sổ” là gộp mọi giao dịch mẫu; khi cài thật thì trỏ vào API tra cứu sổ ITL có phân trang.

## 9. Việc còn lại cho bước cài đặt

- Nối API thật: danh sách PM (lọc/đếm), ứng viên theo PM, ghi mối nối, bỏ gán (sổ giữ lịch sử — bỏ gán là **thêm một dòng**, không xoá).
- “Sang màn Sổ” phải mở **SCR-F02** đã lọc sẵn đúng các dòng đang xem (kế toán cần nó để *yên tâm về dữ liệu*, không phải để ghép).
- Luật ghép thật `DT-I13` (Việt Nam: mã PM + số tiền + pháp nhân · nước ngoài: từ khoá diễn giải + vendor + số tiền) chưa được cài — bốn bậc hiện tại chỉ là thứ tự suy từ dữ liệu, **thay được mà không đổi giao diện**: chỉ cần trả `tier` khác.
- Ảo hoá danh sách khi số dòng thật (3.772 / 8.387) thay cho dữ liệu mẫu.
- Chưa làm: chọn nhiều dòng, gán hàng loạt, ghi chú trên mối nối — **cố ý**, vì nhịp làm việc là từng giao dịch một.

## 10. Chỗ cần đo sau khi lên thật

1. Số mối nối do người tạo (mục tiêu: > 0, rồi tăng đều).
2. Thời gian từ lúc mở một lệnh tới lúc bấm Gán.
3. Tỷ lệ ca lệch tiền bị bấm xác nhận ngay dưới 2 giây — dấu hiệu vẫn đang gật phản xạ.
