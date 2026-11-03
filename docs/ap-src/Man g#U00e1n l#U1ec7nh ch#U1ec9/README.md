# Bàn giao thiết kế — màn “Gán lệnh chi với giao dịch”

Toàn bộ những gì cần để tiếp nhận và cài đặt. Đọc theo thứ tự dưới đây.

```
handoff-gan-lenh-chi/
├─ README.md                      ← bạn đang đọc
├─ thiet-ke-man-gan-lenh-chi.md   ← HỢP ĐỒNG THIẾT KẾ, đọc trước khi sửa UI
├─ ban-dung/
│  ├─ fls-gan-lenh-chi_10.html    ← BẢN CHÍNH, mở thẳng bằng trình duyệt
│  ├─ man-gan-lenh-chi-v2.html    ← bản chạy trên DỮ LIỆU THẬT (40 lệnh chi, kho 18/09/2026)
│  └─ fls-gan-lenh-chi_9.html     ← bản trước, giữ để đối chiếu vì sao đổi
├─ asset/
│  └─ tokens.css                  ← bộ token (kế thừa tokens.css của FLS + 4 token thêm)
└─ boi-canh/
   └─ Prompt-Claude-Design.md     ← brief gốc: dữ liệu thật, luật thiết kế, ĐÃ THỬ VÀ BỊ BÁC
```

## Bắt đầu từ đâu

1. `boi-canh/Prompt-Claude-Design.md` — **mục ⑦ “ĐÃ THỬ VÀ BỊ BÁC”** trước tiên: nó tiết kiệm một vòng làm lại.
2. `thiet-ke-man-gan-lenh-chi.md` — luật, token, bố cục, C1–C10, bốn quyết định khó, bàn phím, việc còn lại.
3. Mở `ban-dung/fls-gan-lenh-chi_10.html` (nhấn `→` để vào vùng ghép) rồi đối chiếu với tài liệu.

## Ba điều dễ làm sai nhất

- **Máy không được chọn sẵn ứng viên.** Máy đề xuất, người quyết. Ca lệch số tiền phải xác nhận hai bước và `Enter` bị khoá.
- **Bậc chỉ được nói một lần** (ký hiệu ①–④ + vạch trái 3px). Thêm nhãn chữ cho từng dòng là quay lại đúng lỗi cũ; bậc ④ chiếm 149/226 ứng viên nên không được có màu.
- **Diễn giải sao kê là bằng chứng, không phải chữ trang trí.** Không bao giờ để nó là cột bị hy sinh khi màn hẹp (thứ tự hy sinh: Nguồn → Số CT → không bao giờ Diễn giải).

## Trạng thái

Bản dựng, **chưa nối kho**: bấm “Gán” không ghi gì. Dữ liệu trong `_10` là mẫu giống thật; dữ liệu trong `v2` là thật (đã che tên cá nhân). Danh sách việc còn lại nằm ở §9 của tài liệu thiết kế.
