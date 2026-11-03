# 08 — NFR: yêu cầu phi chức năng đo được *(dự án ITL)*

**Version:** v1.0 | **Chủ sở hữu:** BA/PO + Tech Lead | **Mốc đo:** 2026-09-04

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
| `NFR-I01` | **Sổ chỉ-thêm.** ⛔ Không đường code nào `UPDATE`/`DELETE` một dòng đã vào sổ | **0** câu `UPDATE`/`DELETE` trên `fls_itl` · `fls_adjustment` · `fls_journal` · `fls_pm_unlink` | **DB** — trigger `trg_fls_itl_inv_i03`; ⛔ không phải quy ước *(`INV-I03`/`INV-I08`)* |
| `NFR-I02` | **Máy chỉ ĐỌC nguồn.** FLS ⛔ không bao giờ ghi ngược Gsheet / `fps_*` / P100 | **0** đường ghi ngược | `QĐ-ITL-34` · `QĐ-ITL-45`; bảng tuyến khai từng bảng mỗi cửa chạm, có cổng `soi_bang_tuyen` **17/17 khớp SQL thật** |
| `NFR-I03` | **Cửa mặc định CHỈ ĐỌC.** Nhóm ghi phải **gõ tường minh** mới mở | `--cho-ghi` mặc định **TẮT** ⇒ mọi đường ghi trả `405` | `tools/chay_cua.py`; kết nối chỉ-đọc cưỡng chế ở tầng **PostgreSQL** |
| `NFR-I04` | **Ghi mà ⛔ không nói lý do là ⛔ không ghi được** | cửa **NO** — `FLS-UNMAPPED-HIDDEN` | `INV-I16` |
| `NFR-I05` | **⛔ Không mặc định im lặng.** Tra không được thì **khai `UNMAPPED`** | `#N/A` giữ nguyên trên màn, ⛔ không thay bằng một giá trị đẹp | `INV-I16`; đo: **6.691 dòng** `hd` rỗng vẫn hiện `#N/A` |
| `NFR-I06` ⭐ | **Bản khai rỗng = máy ⛔ KHÔNG BIẾT** — ⛔ không phải *"mọi giá trị đều sai"* | danh mục `0` dòng ⇒ cửa ⛔ không chặn, **và màn nói ra chỗ rỗng** | `INV-I17` *(04/09)* |

## §2 · Tốc độ — số đo thật, ⛔ không phải số mong muốn

| ID | Yêu cầu | Đo được | Ghi chú |
|---|---|---|---|
| `NFR-I07` | Một trang sổ | **200 dòng**/trang · thân `canon` **393 B/dòng** ⇒ 500 dòng ≈ **584 KB / 0,04 s** | ⛔ Con số *"vài MB"* trong ghi chú cũ **chưa ai đo** — đã đo lại |
| `NFR-I08` | Lưu theo lô | **2,5 s** sau phím cuối · rút-rồi-mới-bắn · dừng ở lỗi đầu tiên | ⛔ **Không có nút Lưu** *(`06_SCREEN_SPEC` §1-8)* |
| `NFR-I09` ⚠ | `GET /gates` | **16,1 s** trong khi client chờ **10 s** ⇒ **5 bài ĐỎ mà ⛔ không phải lỗi code** | ⛔⛔ **`GAP-KHO-02`** — kho test phình **33.492 dòng**. ⛔ **Đừng nới `timeout`**: nới là giấu |
| `NFR-I10` | Vẽ màn trên máy kế toán | ⛔ **CHƯA ĐO** | `GAP-SCR-03` — thuộc **`B7 · UAT`**, máy ⛔ không đóng được |

## §3 · An toàn & riêng tư

| ID | Yêu cầu | Đo được |
|---|---|---|
| `NFR-I11` | Thẻ phiên | `HS256`, khoá **≥ 32 ký tự** *(cửa **NO** nếu ngắn hơn)*; hạn mặc định **8 giờ** — ⛔ **không có chế độ "không hạn"** |
| `NFR-I12` | Cửa chỉ nghe **máy này** | mặc định `127.0.0.1`; ⛔ cửa **TỪ CHỐI** phục vụ màn hình nếu địa chỉ ⛔ không phải loopback |
| `NFR-I13` ⭐ | **⛔ Không mang dữ liệu cá nhân** | ảnh chụp `fls_pm_line` **cố ý ⛔ không lấy** Tên tài khoản · Số tài khoản · Ghi chú · Diễn giải. ⚠ **Cái giá đã đo:** xếp ứng viên ghép lệnh mất **hai trục** *(ngày · người nhận)* ⇒ trong **25 dòng** thử, chỉ **1 dòng** có ứng viên đủ mạnh *(`GAP-JOIN-04`)* |
| `NFR-I14` | Hai thư mục ⛔ không bao giờ vào git | `sao_luu/` · `hien_vat/` — chúng mang `Diễn giải`, có thể chứa tên người |

## §4 · Giữ cho hệ ⛔ không già đi trong im lặng

| ID | Yêu cầu | Đo được |
|---|---|---|
| `NFR-I15` | Bộ phép thử | **1024 bài** · ⛔ **5 đỏ có sẵn** *(đều là `NFR-I09`)*. ⭐ Luật số một: *"cổng chưa từng thấy đỏ là cổng chưa biết có sống"* ⇒ mọi cổng mới phải **bị phá có chủ ý** và **đỏ thật** trước khi tin |
| `NFR-I16` | Ranh giới tầng | **8** hợp đồng `import-linter`, **0** vi phạm. Then chốt: `fls.api` ⛔ không được biết tầng kho · `fls.web` chỉ được gọi `fls.api` |
| `NFR-I17` ⭐ | **Tài liệu ⛔ không được già hơn máy** | **63 phép so SỐ SỐNG** *(`tools/kiem_so_song.py`)* — mỗi phép khớp **đúng một lần** và khớp **đúng con số máy đo**; nó **tự đếm cả chính nó** |
| `NFR-I18` | Một nguồn tên cột | tiêu đề lưới **sinh từ** `ledge_spec` + `canon/spec` ⇒ ⛔ **không một tên cột tiếng Việt nào gõ tay**; cổng đối chiếu **hai chiều** với cửa thật |
| `NFR-I19` | Một nguồn mã màu | **1** tệp được phép có mã màu *(`tokens.css`)*; bài quét NO nếu tệp khác có `#rrggbb` |

## §5 · Việc còn mở — ⛔ chưa đo được, và nói thẳng

| ID | Còn thiếu gì |
|---|---|
| `NFR-I10` | Cảm giác khi gõ · thời gian vẽ · `346px` cột khoá có đủ · `430px` panel có đủ ⇒ **`B7 · UAT`** |
| `NFR-I20` | **Nhịp chốt kỳ** *(flash T+? · final T+?)* — ⛔ chưa ai chốt; `GAP-PLAN-04` |
| `NFR-I21` | **Sao lưu / khôi phục** — `RPO`/`RTO` ⛔ chưa ai chốt cho FLS |
| `NFR-I22` | **Nhiều hơn một máy** — hôm nay `actor` là *"ai khởi động máy này"*; chạy cho nhiều người thì chỗ ấy phải thành **đường đăng nhập thật** *(`GAP-WEB-01`)* |
| `NFR-I23` | **Hai người sửa một ô** — cửa ghi ⛔ không thấy *(`GAP-SCR-09`)*; màn lách bằng một phép **kiểm**, ⛔ không phải một **bảo đảm** |

## Changelog
- **v1.0** (2026-09-04): ⭐⭐ **Viết lại HẲN — dẫn xuất cho ITL, thay bản copy chương trình.** 23 NFR, mỗi dòng có **một con số đo được** hay **một cơ chế đã chạy**; 5 dòng ⛔ **chưa đo được** thì ghi thẳng là chưa đo *(`§5`)*, ⛔ không điền số mong muốn. ⛔ Bản v0.1 tự khai *"đừng dùng làm căn cứ build ITL"* và đứng yên **bảy tuần** — một tệp tự nói *"đừng dùng tôi"* vẫn là một tệp **không dùng được**.
- v0.1 (2026-07-17): Khởi tạo 14 NFR của **chương trình FIN-ERP** *(⛔ không phải ITL)*; 2 ô `???` chờ chốt. Xem `git log`.
