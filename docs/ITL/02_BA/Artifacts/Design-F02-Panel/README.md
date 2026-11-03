# Bộ asset thiết kế — panel đối soát `F02 · Sổ ITL`

**Dựng:** 2026-09-04 · **Vì:** kế toán nói *"vùng panel quá nhiều note, ký
hiệu → khó nhìn; UIUX, layout chưa bắt mắt"*

---

## Dùng thế nào

1. Mở một phiên Claude mới, **đính kèm cả 4 tệp** trong thư mục này
2. Chụp **ảnh màn hình panel hiện tại** *(cả lúc cuộn xuống)* và đính kèm luôn
   — ⛔ không có ảnh thì người thiết kế đang sửa một thứ họ **chưa nhìn thấy**
3. Dán nguyên văn `PROMPT.md`

## ✅ Đợt này **ĐÃ XONG** — đọc [`DA-DUNG.md`](DA-DUNG.md) trước

> ⭐ Bộ giao thiết kế đã về *(04/09)* và **đã code hoá** — `QĐ-ITL-88`/`89`.
> ⚠ Bộ giao nằm ở `FLS/hien_vat/`, thư mục **gitignore** ⇒ nó ⛔ **không vào
> git**. `DA-DUNG.md` là **cầu nối duy nhất** giữa nó và mã: đã dựng gì, **sửa
> luật** gì *(và con số nào là lý do)*, ⛔ **chưa** dựng gì, và **bốn chỗ tôi tự
> vấp**.

Bốn tệp dưới đây giữ lại để **dùng lại cho đợt sau** *(và làm biên bản của đợt
này)*.

## Bốn tệp

| Tệp | Là gì |
|---|---|
| `PROMPT.md` | ⭐ **Dán cái này.** Đề bài + việc cần làm + sản phẩm giao lại |
| `BRIEF.md` | Kiểm kê panel · **13 ràng buộc cứng** · số đo · hình dạng giá trị thật |
| `DATA.json` | **6 dòng THẬT**, 6 tình huống khác nhau — để vẽ trên chữ thật, ⛔ không phải chữ giả |
| `tokens.SNAPSHOT.css` | ⚠ **bản CHỤP** bộ màu. SSOT là `fls/web/tep/tokens.css` |

## ⛔ Hai điều dễ làm hỏng bộ này

### ⓐ ⛔ Đừng sửa tay `DATA.json`

Nó **sinh ra bằng máy**:

```
python tools/lam_bo_asset_thiet_ke.py
```

⛔⛔ Văn xuôi trong đó là **chữ TỔNG HỢP**, ⛔ không phải chữ thật. `Diễn giải`
có thể mang **tên người** — đó là lý do `sao_luu/` và `hien_vat/` bị gitignore.
Tệp này thì **vào git** và **được đưa ra ngoài**, nên nó phải sạch.

⚠ Chỗ dễ vấp: văn xuôi ⛔ **không chỉ nằm ở `memo`**. Mảng `canon` chở lại
chính câu ấy ở vị trí **2**, cộng *Nội dung PE/PI* **8·9·10** và *Ghi chú*
**31**. Scrub `memo` xong mà quên `canon` là để chữ ấy đi ra qua **cửa sau** —
đúng việc này đã xảy ra khi dựng bộ asset, và bắt được vì **đọc lại tệp**, ⛔
không phải vì một phép thử nào đo.

⇒ Nay có cổng, và nó **đã được chứng minh đỏ trên cả 4 kiểu phá**:

```
python tools/kiem_du_lieu_thiet_ke.py
```

### ⓑ ⛔ Đừng sửa `tokens.SNAPSHOT.css`

Nó là **bản sao**. Đổi màu thì đổi ở **SSOT** `fls/web/tep/tokens.css`, rồi
chụp lại. Có cổng canh:

```
python tools/kiem_ban_chup_mau.py
```

⭐ Chính tệp SSOT đã ghi bài học này: trước `B2` bộ màu tồn tại ở **ba chỗ**, và
câu *"màu nhãn là màu gì"* có ba câu trả lời đúng — chúng đã lệch.

## Nhận lại rồi làm gì

Sản phẩm giao về là **một trang HTML + một bộ luật ký hiệu/màu + danh sách
những gì bị cắt**. ⛔ Đó ⛔ chưa phải mã chạy được.

⇒ Bước sau: đối chiếu với **13 ràng buộc** ở `BRIEF.md` §4 **trước khi** dựng.
Cái nào người thiết kế đề nghị **lật**, thì lật **công khai** bằng một quyết
định `QĐ-ITL-*`, ⛔ không lặng lẽ áp vào mã.
