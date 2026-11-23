# PLAN TEST ＋ DEV — màn **Gán lệnh chi ↔ Giao dịch** *(`SCR-F01`, lằn MỐI NỐI)*

**Ngày:** 2026-09-21 · **Chủ sở hữu:** BA · **Căn cứ:** `QĐ-ITL-146` *(thiết kế về)* · `QĐ-ITL-147` *(nới trần)* · `QĐ-ITL-148` *(bốn quyết định `21/09`)* · `Audit-No-Thiet-Ke-Man-Ghep.md`

> ⭐⭐ **Plan này ⛔ KHÔNG bắt đầu bằng mã.** Bộ này chạy **spec-first ＋ TDD** *(`07_CHANGE_CONTROL §2`)*: đặc tả **trước**, bài thử **đỏ trước**, mã **sau**. `4` GAP hạng chặn của audit đều là **lỗ đặc tả** ⇒ ⛔ viết mã bây giờ là viết trên chỗ chưa có nền.

---

## §0 · Bốn quyết định nền — owner chốt `21/09`

| # | Câu | Chốt | Kéo theo |
|:-:|---|---|---|
| ① | Lằn nào trước | ⭐ **Lằn MỐI NỐI** *(`47` gật ＋ `738` chọn)* | ⛔ Lằn **GIÁ TRỊ** *(`4.424` gợi ý)* **⛔ KHÔNG mở** trong plan này — xem `§6` |
| ② | Tên người nhận trên màn | ✅ **Hiện nguyên** | Vẽ ranh giới *hồ sơ nhân sự* ／ *danh tính bên nhận tiền* — `BA-06 §4.5 ⓙ` |
| ③ | Bỏ gán ／ Đổi mapping | ✅ **Giữ cửa, MÀN nói ra thiệt hại** | ⛔ Bất biến `SIGMA_MOI_NOI` **⛔ không bị chạm**; việc nằm ở **một hộp thoại có số thật** |
| ④ | Nút `Xong` *(`QĐ-ITL-71`)* | ⚰ **KHAI TỬ** — ba đường ra là đủ | `GAP-SCR-19` **ĐÓNG**; cửa `done` giữ trong `BA-07` làm **bia**, màn ⛔ không vẽ nút |

⭐ **Lý do `④` được ghi ra chứ ⛔ không rút lặng:** lý do gốc của `QĐ-ITL-71` là *"chỗ đánh dấu việc đang làm dở"* — thiết kế mới **giải bài ấy bằng cách khác** *(gán xong **tự nhảy** sang lệnh kế tiếp)*, nên trạng thái *"đang làm dở"* ⛔ không còn tồn tại để mà đánh dấu.

---

## §1 · Ràng buộc thứ tự — ⛔ ⛔ không phải sở thích

```
B0  vá ĐẶC TẢ        ⛔ không chạm mã   ← 4 GAP chặn đều nằm ở đây
     ↓
B1  bài thử ĐỎ        ⛔ không chạm màn  ← INV-I20 đang có 0 bài gọi tên
     ↓
B2  CỬA               (API)
     ↓
B3  MÀN               (web)
```

⛔⛔ **⛔ Không được đảo `B1` xuống sau `B3`.** Đo `21/09`: cổng `G-a` **trượt** mà ⛔ **không cổng máy nào báo**, vì `INV-I20` — bất biến **trung tâm** của màn — có **`0`** tệp test gọi tên *(so `INV-I16`: **45**)*. Viết màn trước thì cổng vẫn mù đúng như hôm nay.

---

## §2 · `B0` — VÁ ĐẶC TẢ *(⛔ không chạm mã, ⛔ không chạm kho)*

| # | Việc | Đóng GAP | Nội dung phải có |
|:-:|---|---|---|
| `B0-1` | ⭐⭐ Khai **khuôn `ung_vien[]`** vào `BA-07` | `GAP-API-07 ⓐ` | **10** trường: `itl_id` · `doc_date` · `doc_no` · ⭐`dien_giai` · `amount` · ⭐`chieu` · `curr` · ⭐`nguon{tk,bank,curr,le}` · `bac` · `lech`. ⛔ **`nguon` là OBJECT, ⛔ không phải chuỗi** — bản dựng đang cắt chuỗi hiển thị |
| `B0-2` | ⭐⭐ Đặc tả **luật tách `source_sheet`** | `GAP-SPEC-04` | ⛔ Bóc tiền tố **`R \| `** *(có ở **`8.387/8.387`**)* ⇒ `<tk>_<bank> <curr>_<le>`. ⚠ **`6` tài khoản ⛔ không phải số** *(`PO1`·`PO2`·`PO3`·`PO5`·`PO6`·`PO9`)* ⇒ luật *4 số cuối* phải có **nhánh riêng** |
| `B0-3` | ⭐ Đặc tả **luật chiều `Nợ/Có`** | `BA-06 §4.5 ⓘ` | *"Bên nào ≠ `0` thì đó là chiều"* — `3.691` dòng mang **cả hai** ô, **`0`** dòng cả hai khác `0`. ⛔ **⛔ KHÔNG** lấy dấu từ `pay_type` *(đã sai một lần)* |
| `B0-4` | ⭐⭐ Đặc tả **phép đổi sê-ri → ngày** | `BA-06 §4.5 ⓗ ①` | ⛔ Kho có **`3.772/3.772` sê-ri**, `0` dòng có dấu ngày. Phải khai **gốc sê-ri** *(`1900` ／ `1904`)* — chọn sai lệch **4 năm 1 ngày** |
| `B0-5` | ⭐ Khai **cửa tra cứu TOÀN SỔ** | `GAP-API-07 ⓑ` | Nhận `pm_line_id` *(để **tính lại bậc**)* ＋ `q` *(tìm chữ)* ＋ phân trang. ⛔ **Bậc ① phải tính bằng `canon_ref` ở Python** — so chuỗi thô lệch **`17,9%`** |
| `B0-6` | Khai **`fls_dien_giai`** vào `BA-07` | `GAP-API-07 ⓒ` | Nối được **`8.358/8.387`**; ⭐ dòng ⛔ không có chữ thì **VẮNG** khỏi khung xem ⇒ cửa phải phân biệt *"⛔ không nối được"* *(`26`)* với *"nối được, ⛔ không có chữ"* *(`3`)* |
| `B0-7` | ⭐⭐ Đặc tả **hộp thoại BỎ GÁN có chùm** | `GAP-SCR-22` | Ở **`25/2.222` = 1,1%** ca, màn phải **liệt kê từng dòng lệnh sắp bị gỡ** trước khi hỏi. Chùm lớn nhất **`10`** |
| `B0-8` | ⭐⭐ Đặc tả **khối bung phải HIỆN trường vắng** | `GAP-SCR-23` | ⛔ `tho` có **`41` hình dạng**; ⭐ đo được **"có khoá" ≡ "có chữ"** cho cả `27` khoá ⇒ chỉ cần phân biệt **VẮNG** với **CÓ**, ⛔ không có ca *chuỗi rỗng* |
| `B0-9` | Bỏ trường **`Người lập`** khỏi thiết kế | `ND-09` | Quét `27` khoá `tho`: ⛔ **không** khoá nào là *người lập* ／ *email* ⇒ **⛔ không có nguồn**, ⛔ không vẽ |
| `B0-10` | ⭐ Gỡ trùng **`Người nhận` ↔ `Tên tài khoản`** | `BA-06 §4.5 ⓗ ②` | **Cùng một ô** hiện hai nhãn, hiện **cùng lúc** khi bung ⇒ `UI-F9`. Giữ trên thẻ, **bỏ** khỏi khối bung |
| `B0-11` | Thêm **chip lọc thứ tư** *(`⛔ Không gán được`)* | `GAP-SCR-20 ⓑ` | ⇒ Danh sách mặc định về **`738`**, cổng `G-a` **ĐẠT** |
| `B0-12` | Khai **nền tối ＋ bàn phím ＋ focus** thành yêu cầu | `ND-07` · `ND-08` | ⛔ Hôm nay **`0`** yêu cầu a11y trong cả bộ; thiết kế **làm tốt hơn** yêu cầu nhưng ⛔ không cổng nào giữ |

**Cổng ra `B0`:** `4` GAP hạng chặn ＋ `GAP-SPEC-04` đóng · `BA-07` bump · cổng tài liệu `6/6` · cổng số sống xanh.

---

## §3 · `B1` — BÀI THỬ ĐỎ TRƯỚC

### ⓐ Bất biến ⛔ chưa ai canh

| Bài | Canh gì | Đỏ trước vì |
|---|---|---|
| ⭐⭐⭐ `test_INV_I20_dich_cuoi_khong_tron_vao_viec` | Bộ lọc mặc định trả **`738`**, ⛔ **không** `1.553` | ⛔ Hôm nay **`0`** bài gọi tên `INV-I20` |
| ⭐⭐ `test_INV_I20_moi_dong_co_dung_BA_duong_ra` | ghép được ／ đích ⛔ không gán được ／ đích lỗi nguồn — ⛔ **không đường thứ tư** | ⚰ Chốt `Xong` khai tử *(`QĐ-ITL-148 ④`)* |
| ⭐⭐ `test_INV_I16_cua_KHONG_chon_san_ung_vien` | Phản hồi ⛔ **không** mang cờ *"đã chọn"* nào | Máy đề xuất, người quyết |
| ⭐⭐ `test_INV_I08_bo_gan_la_THEM_mot_dong` | Sau `unmatch`: số dòng sổ **tăng**, ⛔ **không** giảm | Cửa là `POST`, ⛔ không `DELETE` |

### ⓑ Bẫy đã đo — mỗi cái một bài ghim

| Bài | Ghim cái gì | Bằng chứng |
|---|---|---|
| ⭐⭐⭐ `test_bac_ma_dung_canon_ref_KHONG_dung_regexp` | Đổi sang `regexp` ⇒ bài **ĐỎ** | Đo: `regexp` **`560`** vs luật thật **`475`** ⇒ **`17,9%`** |
| ⭐⭐ `test_tach_source_sheet_boc_tien_to_R` | Chuỗi **`R \| PO2_OCBC USD_SGO2`** tách đúng `4` mảnh | **`8.387/8.387`** mang tiền tố |
| ⭐⭐ `test_tai_khoan_khong_phai_so_KHONG_bi_cat_4_so` | `PO2` ⛔ **không** ra `••PO2` | `6` tài khoản thẻ |
| ⭐⭐ `test_chieu_lay_tu_o_khac_0_KHONG_tu_pay_type` | `3.691` dòng hai ô vẫn ra **một** chiều | `0` dòng cả hai khác `0` |
| ⭐⭐ `test_se_ri_doi_ngay_dung_goc_1900` | Một dòng mẫu đã biết ra **đúng ngày** | `45726.759…` |
| ⭐⭐ `test_bo_gan_tren_CHUM_phai_liet_ke_truoc` | Dòng tiền có `n>1` mối nối ⇒ phản hồi **nêu tên** cả `n` | `25` dòng, lớn nhất **`10`** |
| ⭐ `test_khoi_bung_HIEN_truong_vang_KHONG_giau` | Dòng thiếu `Chi nhánh` ⇒ vẫn có hàng, ghi **"⛔ không có"** | `Chi nhánh` **11,7%** · `PE (Urgent)` **0,45%** |
| ⭐ `test_dien_giai_phan_biet_KHONG_NOI_DUOC_voi_RONG` | `26` ⛔ không nối ≠ `3` nối được mà ⛔ không chữ | `8.358/8.361/8.387` |

### ⓒ Bài ở tầng màn — `4` hành vi chống gật

`test_man_KHONG_chon_san` · `test_man_Enter_BI_KHOA_khi_lech_tien` · `test_man_lech_tien_phai_bam_HAI_lan` · `test_man_toan_so_BAT_SAN_khi_khong_ung_vien`.

⭐ Cả bốn là `INV-I16` **ở tầng ngón tay** — tầng ấy ⛔ **chưa từng có bài nào**.

**Cổng ra `B1`:** mọi bài trên **ĐỎ** và đỏ **đúng lý do** · `TEST-03` ma trận `INV` đi **`8 → 10`** *(thêm `I20`, và `I16` có bài ở tầng màn)*.

---

## §4 · `B2` — CỬA · §5 · `B3` — MÀN

| Chặng | Việc | Cổng ra |
|---|---|---|
| `B2` | Khuôn `ung_vien[]` **`10` trường** · cửa **toàn sổ** · `fls_dien_giai` · `unmatch` trả **danh sách chùm** · `reason` thành **tuỳ chọn** *(`QĐ-ITL-137` đã hoãn cột lý do)* | Bài `B1` nhóm `ⓐ`＋`ⓑ` **XANH** · `pg_verify` khớp · import-linter `9/9` |
| `B3` | `C1`–`C10` theo `BA-06 §4.5` · chip lọc **thứ tư** · hộp thoại **chùm** · khối bung **hiện trường vắng** · nền tối ＋ bàn phím | Bài nhóm `ⓒ` **XANH** · `G-a` **`738`** ✅ · `G-b` **`≤ 11`** ✅ · `G-c` **`0`／`0`** ✅ *(cần bỏ `6` mã nội bộ — `GAP-SCR-20 ⓒ'`)* |

⭐⭐ **`G-d` — mối nối do NGƯỜI tạo đi từ `0` lên khác `0` — ⛔ KHÔNG đo được ở `B3`.** Nó chỉ đo được **sau khi kế toán dùng thật**. ⇒ `B3` xong ⛔ **không** phải *"đã nghiệm thu"*, nó là *"đã đủ điều kiện để đo"*.

---

## §6 · ⛔ Cái plan này CỐ Ý ⛔ KHÔNG làm

| ⛔ Không làm | Vì sao |
|---|---|
| **Lằn GIÁ TRỊ** *(`4.424` gợi ý ⛔ không màn nào thấy)* | Owner chốt lằn MỐI NỐI trước. ⚠ **Lỗi vẫn đang sống** — ghi lại ở đây để ⛔ không rơi, ⛔ không phải để lặng cho qua |
| **Luật ghép `DT-I13`** *(VN ／ nước ngoài)* | Bốn bậc hiện nay **thay được mà ⛔ không đổi giao diện** — chỉ cần trả `bac` khác. ⚠ Chặn ở `GAP-LE-01`: **kế toán** phải nói `CNC` là gì |
| Chọn nhiều dòng · gán hàng loạt · ghi chú trên mối nối | Nhịp là **từng giao dịch một** *(`QĐ-ITL-144 ⓵`)* |
| Nới cửa `unmatch` cho bỏ lẻ | Owner chốt `③`: bất biến đứng nguyên, **màn nói ra thiệt hại** |
| Ảo hoá danh sách | ⛔ Chưa đo được là có cần ⛔ không — `3.772` dòng, và trần thật là **một ảnh PM** |

---

## §6b · ⭐ ĐÃ CHẠY — `2026-09-21`

| Chặng | Trạng thái | Bằng chứng |
|---|---|---|
| ✅ `B0` **vá đặc tả** | **XONG** — `12/12` | `BA-07` **v3.0** `§4h` *(35 → 37 tuyến)* · `BA-06` **v4.0** `§4.6` · `BA-08` **v1.1** `§4b` *(`NFR-I24`…`I28`)* |
| ✅ `B1` **bài thử đỏ** | **XONG** — `29` bài, đỏ trước | `test_b1_luat_doc_man_ghep.py` · `test_b1_inv_i20_chip_loc.py` · `test_b1_chum_moi_noi_pg.py` |
| ✅ `B2` **cửa** | **XONG** — `35 → 39` tuyến | `man_ghep.py` · `so_theo_lenh` · `chum_moi_noi` · `ung_vien[]` **10 trường** |
| ⚠ `B3` **màn** | **PHẦN LỚN** — chạy được, ⛔ **chưa có CSS** | `man_f01_ghep.js` ＋ **2 cổng canh** · nối vào vỏ |

⚠ Dòng `B3` ở trên là trạng thái **`21/09`**. Xem `§6c` — `22/09` đã có CSS, và đã lộ ra một lỗi mà cả hai cổng ấy ⛔ không thấy.

#### ⛔ Ba chỗ `B3` **⛔ CHƯA** xong — nói thẳng

| ⛔ Chưa | Hệ quả |
|---|---|
| ⭐ **CSS** — `5/6` lớp *(`.cand` · `.mrow` · `.chip-loc` · `.fact` · `.rail`)* ⛔ **không có một dòng kiểu nào** | Màn **đúng cấu trúc** nhưng **⛔ chưa ra hình**: vạch trái `3px`, rail `clamp(300,26vw,380)`, dòng `36px`, nền `warn` của ca đề xuất — **⛔ chưa cái nào tồn tại** |
| `kiem_thuyet_minh` ⛔ chưa phủ màn mới | Bản đồ nút của nó ghim cứng `man_f01_lenh.js` ⇒ nút của màn mới **⛔ không ai canh** |
| ⛔ Chưa mở trên trình duyệt thật | Mọi phép đo ở đây là **DOM giả** ＋ quét mã. `NFR-I10` *(vẽ màn trên máy kế toán)* vẫn **⛔ CHƯA ĐO** |

#### ⭐⭐⭐ Hai cổng canh — và cái thứ hai vá một lỗ của cái thứ nhất

| Cổng | Đo gì | Vì sao cần |
|---|---|---|
| `test_b3_fe_bam_thiet_ke.py` | **14** phép: `4` chip · `4` bậc `①②③④` · **thứ tự hy sinh cột** · `Enter` khoá · ⛔ không chọn sẵn · `9` phím · trường vắng · ngân sách `11` | Một **lời nhắc** ⛔ không giữ được gì — đo được: `339 → 735` dòng, `0` lần co lại |
| ⭐⭐ `test_b3_man_ghep_chay_duoc.py` | **7** phép **CHẠY** màn trong DOM giả | ⛔⛔ **Bản đầu của màn gọi một API `TP` tôi TỰ BỊA** *(`el(tag, {attrs}, …con)` trong khi thật là `el(the_gi, lop, html)`)* — nó **⛔ không chạy nổi một dòng** và **qua cả 14 phép** của cổng trên ⇒ **một cổng đọc mã ⛔ KHÔNG thay được một cổng chạy mã** |

⭐ Cả hai đã **diễn tập phá** *(`NFR-I15`)*: đưa `dien_giai` vào `COT_BO_DUOC` ⇒ **ĐỎ**; phục hồi ⇒ **XANH**.

⭐⭐ **Gốc sê-ri được ĐO chứ ⛔ không chọn** *(thứ `B0-4` đòi)*: gốc `1900` cho dải `2025-03-10 … 2026-08-29` và lệch **trung vị `3` ngày** so với ngày **dòng tiền đã nối**; gốc `1904` cho `2029…2030`, lệch **`1.462`** ngày. ⛔ Phép kiểm dùng một **nguồn độc lập**, ⛔ không phải một dải ngày *"trông hợp lý"* — dải ngày một mình ⛔ không đủ.

### ⛔ Một bài thử của tôi ĐO SAI THỨ, và chính nó bắt được

`test_chieu_KHONG_duoc_suy_tu_pay_type` bản đầu quét `inspect.getsource()` ⇒ **ĐỎ ngay** — vì chính khối chú thích **giải thích vì sao ⛔ không dùng `pay_type`** có chứa chữ ấy. ⛔⛔ **Một phép đo bắt cả lời CẢNH BÁO về lỗi thì nó ⛔ không đo cái nó tưởng.** ⇒ Viết lại: quét **đối tượng mã** *(`co_names` ＋ `co_consts`, đệ quy)* — đo **thứ sẽ chạy**, và vẫn bắt được ca đọc `d["pay_type"]`.

⭐ **Và cổng ấy đã được DIỄN TẬP PHÁ** *(`NFR-I15`: "cổng chưa từng thấy đỏ là cổng chưa biết có sống")*: cho `chieu_tien` đọc `pay_type` ⇒ **ĐỎ**; phục hồi ⇒ **XANH**.

---

## §6c · ⭐ ĐÃ CHẠY — `2026-09-22` *(mở BE ＋ FE thật)*

| Chặng | Trạng thái | Bằng chứng |
|---|---|---|
| ✅ `B3` **CSS** | **XONG** | `tokens.css` ＋ `5` token · `hinh.css` ＋ khối `SCR-F01` *(`531 → 752` dòng)* |
| ✅ `B3` **nạp danh sách** | **XONG** — và đây là một **lỗi mới phát hiện**, ⛔ không phải việc đã lên kế hoạch | `tai_danh_sach()` · `khuon_the_lenh()` · cửa trả `the` |
| ⚠ `B3` **trình duyệt thật** | **MỞ ĐƯỢC** — máy chạy, `4/4` tệp phục vụ `200` | ⛔ Vẫn **CHƯA có người nhìn**: `NFR-I10` chưa đo |

### ⛔⛔⛔ Mở máy thật lộ một lỗi mà **CẢ HAI** cổng `B3` bỏ qua

`man_f01_ghep.js` **⛔ KHÔNG hề có một dòng nào nạp danh sách.** Mở trên trình duyệt, màn **luôn** hiện *"Hàng chờ đã sạch."* — một câu **sai** trước `1.553` dòng đang chờ.

| Cổng | Vì sao nó **⛔ không thấy** |
|---|---|
| `test_b3_fe_bam_thiet_ke.py` *(quét mã)* | ⛔ Nó ⛔ không hỏi *"danh sách lấy từ đâu"* |
| `test_b3_man_ghep_chay_duoc.py` *(chạy mã)* | ⛔⛔ **Khuôn thử TỰ NHÉT `ST.dong` vào** trước khi gọi `ve()` |

⭐⭐ **Một khuôn thử cung cấp thứ mà bản thật phải tự đi lấy thì nó CHE MẤT chỗ thiếu ấy.** Cùng hạng lỗi với `TP.el` tự bịa, chỉ **cao hơn một tầng**: lần trước khuôn thử che một API **sai**, lần này nó che một API **⛔ chưa bao giờ được gọi**.

⇒ Cổng thứ **ba**: `test_b3_man_ghep_tu_nap_danh_sach.py` — **8** phép, và nó **⛔ KHÔNG gán `ST.dong`** một lần nào.

⭐ **Diễn tập phá** *(`NFR-I15`)*: gỡ lời gọi nạp ⇒ **`3` bài mới ĐỎ**, còn **cả hai cổng cũ vẫn XANH** — đúng bằng chứng chúng ⛔ không bao giờ nhìn thấy lỗi này. Phục hồi ⇒ **XANH**.

### ⭐⭐ Bốn chip, và chỉ **HAI** có cửa

Đo `22/09` bằng cách **gọi cửa thật**, ⛔ không đọc đặc tả:

| Chip | Cửa | Đếm thật |
|---|---|---|
| `Chưa gán` | `?ro=nguoi` ＋ `?ro=may&tu_chung=0` | **`738`** ✅ đúng `G-a` |
| `Không gán được` | `?ro=khong` | **`768`** ✅ `INV-I20` |
| `Đã gán` | ⛔ **KHÔNG cửa nào** | — |
| `Tất cả` | ⛔ cửa chỉ trả dòng **chưa nối** *(`1.553`)* | — |

`/queue/lenh-cho` lọc cứng `NOT EXISTS (fls_moi_noi)` ⇒ ⛔ **không** đường nào hỏi *"lệnh chi nào ĐÃ có tiền"* — `GAP-API-08`.

⛔ Màn **NÓI RA** điều đó thay vì vẽ một danh sách rỗng: một danh sách rỗng đọc **y hệt** *"đã xong hết"*, và đó là máy trả lời thay người (`INV-I16`).

### ⭐⭐⭐ Thẻ `11` trường — `6/11` ⛔ KHÔNG cửa nào gọi tên

Đo `22/09`: `nguoi_nhan` · `phap_nhan` · `ngan_hang` · `tai_khoan` · `noi_dung` · `loai_phieu` **chỉ** sống trong túi `tho`, khoá theo **TÊN CỘT CỦA GOOGLE SHEETS**.

⇒ Nếu JS tự móc `tho["Tên tài khoản"]` thì **màn hình đọc thẳng tên cột của sheet**. Tên ấy **đã đổi một lần rồi**, và lần sau chỗ hỏng là **một ô trống trong im lặng** — ⛔ không bài thử nào bắt được, vì bài thử sẽ gõ **y hệt tên ấy**.

⇒ Phép ánh xạ ở **tầng đọc**: `fls/repo/man_ghep.py::khuon_the_lenh` *(`14` bài thử)*, cửa trả thêm khoá `the`.

### ⛔⛔ Và số sê-ri **VẪN CÒN** trên màn

`BA-06 §4.5 ⓕ` từng khai *"đã hết timestamp sê-ri"*. Đo lại `22/09` **trên cửa thật**: `Timestamp` ra **`46091.42265217593`** ở **`3.772/3.772`** dòng, trong khối *"Xem đủ trường"*.

⭐ Đây là **lần thứ hai** cùng một sai lầm: lần đầu tôi đo **bản dựng** *(người thiết kế gõ tay `18/09/2026 09:14`)* rồi tưởng đã đo kho; lần này tôi sửa lời khai nhưng **⛔ không kiểm lại đường đi thật của giá trị**. ⇒ Đổi ở tầng đọc *(`KHOA_NGAY_SE_RI`, dùng lại `ngay_tu_seri` đã đo)*, có bài thử canh.

### ⛔⛔ Một lỗi CÓ SẴN, sống câm lặng ba chỗ

`--accent-soft` được **dùng 3 chỗ** trong `hinh.css` và **⛔ CHƯA BAO GIỜ được khai**:

| Dòng | Hệ quả thật |
|---|---|
| `247` `@keyframes soi` | hiệu ứng soi dòng chạy *trong suốt* → *trong suốt* = **⛔ không thấy gì** |
| `251` `@media (prefers-reduced-motion)` | người **tắt chuyển động** đáng lẽ nhận nền tĩnh — họ nhận **⛔ không gì cả** |
| `297` `.gapfold:hover` | hover **⛔ không đổi nền** |

⭐ Cổng màu canh *"có hex ngoài `tokens.css` ⛔ không"* — **một chiều**. Chiều kia *"tên token có thật ⛔ không"* thì **⛔ không ai hỏi**, và CSS **⛔ không bao giờ báo lỗi**: `var(--khong-co)` chỉ lặng lẽ ⛔ không áp gì.

⇒ `tests/web/test_moi_token_deu_duoc_khai.py`. **Diễn tập phá**: gỡ khai báo ⇒ cổng chỉ thẳng **cả ba dòng** `247/251/297`.

### ⭐ Cổng mới của tôi BÁO OAN — lần thứ **tư** cùng một hình dạng

| Lần | Phép đo | Báo oan vì |
|---|---|---|
| ① | `inspect.getsource()` | khối chú thích **cảnh báo về lỗi** chứa `pay_type` |
| ② | quét mã màu riêng | `#f01-ghep` — một `id`, `f01` là hex hợp lệ |
| ③ | quét `var(--x)` | câu văn **tả chính cổng ấy** trong `tokens.css` |
| ④ | quét tên cột sheet | `'Ngân hàng'` trong JS là **nhãn hiển thị**, ⛔ không phải phép móc khoá |

⭐⭐ **Cùng một gốc cả bốn: đo CHỮ thay vì đo THỨ SẼ CHẠY.** ⇒ ③ dùng lại `_bo_ghi_chu` của cổng màu *(⛔ không viết bản thứ hai)*; ④ đổi sang đo **phép truy cập** `\.tho\b` — cái bị cấm là *đọc túi `tho`*, và nó có đúng một hình dạng cú pháp.

### ⛔ Ba chỗ `B3` **vẫn CHƯA** xong

| ⛔ Chưa | Hệ quả |
|---|---|
| `kiem_thuyet_minh` ⛔ chưa phủ màn mới | Bản đồ nút ghim cứng `man_f01_lenh.js` ⇒ nút màn mới **⛔ không ai canh** |
| ⛔ Chưa có **người** nhìn màn | Máy chạy `200` ở `4/4` tệp, nhưng `NFR-I10` *(vẽ trên máy kế toán)* vẫn **⛔ CHƯA ĐO** — một cổng ⛔ không thay được một đôi mắt |
| ⛔ **Khung cao bằng màn hình** *(hợp đồng `§4`)* | Vỏ `index.html` là một trang **CUỘN** và **4 màn khác** đang sống trong nó ⇒ đổi kiểu cuộn là đổi cả 4 màn trong một cú. Dùng khuôn `F02` đã chứng minh *(rail `sticky` tự cuộn)*. Khoảng nợ: `GAP-SCR-24` |

---

## §6d · ⭐ ĐÃ CHẠY — `2026-09-22` *(kiểm ĐỘC LẬP ＋ vá bốn lỗi CHẶN)*

Một agent **độc lập** đối chiếu mã ↔ hợp đồng thiết kế ↔ bản dựng. Nó tìm **`4`** lỗi hạng CHẶN, `14` ĐÁNG SỬA, `4` NHẸ. Tôi **tự kiểm lại** cả bốn CHẶN trước khi nhận: **cả bốn đều đúng**.

### ⛔⛔⛔ Bốn lỗi, một hình dạng

| # | Lỗi | Vì sao **ba** cổng đều xanh |
|:-:|---|---|
| ① | `ST.dong` — ⛔ không ai gọi cửa | khuôn thử **tự nhét** `ST.dong` |
| ② | `phim()` đủ `9` phím, ⛔ không ai đăng ký `keydown` ⇒ **`0/9`** dùng được | khuôn thử **gọi thẳng** `F01G.phim(…)` |
| ③ | `#ghep-tim` ⛔ không ai nghe ⇒ cửa `?q=` **⛔ chưa từng nhận một chữ** | ⛔ không cổng nào hỏi *"ai đọc ô này"* |
| ④ | `bo_gan` đọc `itl_id_da_gan` — khoá **⛔ không ai sinh ra** | nhánh *"đã gán"* **⛔ chưa bao giờ bật** |

⭐⭐⭐ **Gốc chung: bài thử với tay VÀO gọi thứ mà sản phẩm phải với tay RA nối.**

### Năm chặng — mỗi chặng đều **diễn tập phá** trước khi commit

| Chặng | Làm gì | Bài thử | Commit |
|---|---|:-:|---|
| `1` | **Bàn phím** nối trên `document`, tự chặn khi màn ⛔ không bật | `+4` | `fe403ce` |
| `2` | **Ô tìm** — gõ ⇒ bật Toàn sổ ＋ chờ `250ms` | `+4` | `3037441` |
| `3` | **Diễn giải** — `khoa_bang_chung()` ở tầng đọc ＋ `<mark>` ＋ `đủ ↓` | `+17` | `309a8da` |
| `4` | **Tuyến `40`** `lenh-da-gan` ＋ `itl_da_gan[]` | `+8` | `a09e5a1` |
| `5` | Cổng **tổng quát** ＋ đồng bộ tài liệu | `+5` | — |

### ⭐⭐ Sáu lỗi của **chính tôi**, lộ ra khi chạy

| | Lỗi | Bài học |
|:-:|---|---|
| ⓐ | Diễn tập phá đầu của Chặng `2` **⛔ không hợp lệ** *(`TRE_TIM=0` vẫn xanh vì sáu cú `_ban` chạy **đồng bộ**)* | **Một phép phá ⛔ không làm đỏ được thì ⛔ chưa chứng minh gì** |
| ⓑ | **Nút lồng nút** — `<button>` trong `<button class="cand">` | Lớp lỗi một **bài chạy ⛔ KHÔNG THỂ** bắt: DOM giả ⛔ không phân tích HTML |
| ⓒ | **Đụng tên lớp** — `.mo` đã nghĩa là *"dòng sổ đang mở"* | `querySelectorAll` trả **cả hai**, bài thử lặng lẽ đo **nhầm phần tử** |
| ⓓ | Cổng "nút lồng nút" **báo oan HAI lần** | Lần thứ **năm**: **đo CHỮ thay vì đo THỨ SẼ CHẠY** ⇒ đo **phép tạo thẻ** |
| ⓔ | Câu con `fls_moi_noi` **⛔ không lọc phạm vi** ⇒ `[2, 3, 23, 24]` | `pm_line_id` là khoá **nghiệp vụ** *(lặp mọi lần nạp)*; `itl_id` là khoá **của một ảnh chụp** |
| ⓕ | Ngưỡng `>= 2` ô nhập tôi **tự đặt** ⇒ đỏ vì vỏ chỉ có **`1`** | Một ngưỡng ⛔ không đo được sẽ đỏ vì **một lý do ⛔ không liên quan** |

### ⭐⭐⭐ `itl_da_gan` phải là một **DANH SÁCH** — đo mới biết

| Đếm trên kho thật `22/09` | |
|---|---|
| lệnh chi **đã gán** | **`2.219`** |
| lệnh chi **chưa gán** | **`1.553`** ✔ khép về `3.772` |
| ⭐ lệnh gắn **nhiều hơn một** dòng tiền | **`23`** = **`1,0%`** |

Một khoá số ít **im lặng bỏ mất** mối nối thứ hai — đúng ở chỗ người ta bấm `Bỏ gán`. ⭐ `1,0%` gần đúng **`1,1%`** ca có chùm: **cùng một sự thật** *(tiền ↔ lệnh là **nhiều ↔ nhiều**)* nhìn từ **hai phía**.

### ⛔ Còn nợ — nói thẳng

| Còn | Vì sao ⛔ chưa làm |
|---|---|
| ~~`C4` khối `.mblock`~~ ✅ **LÀM `23/09`** | Owner mở màn thật và hỏi đúng nó. Kèm **dòng TỔNG** cho chùm — xem `§6e` |
| ~~Bảng sổ `12` cột~~ ✅ **LÀM `22/09`** ⇒ ⚠ **`11` từ `23/09`** | Owner bỏ cột `Bậc`: lúc **quét**, câu hỏi là *"dòng nào chưa xong"* |
| Nền tối | Chạm **cả 5 màn**; `GAP-NFR-01` đòi **đo tương phản** trước |
| Chip `Tất cả` | `GAP-SCR-26` — **hợp** của hai rổ, cần một **quyết định** về *"con số đến từ đâu"*. ⚠ **Vẫn chờ owner** |
| Số đếm trên chip · rail `6` mục | *"Thêm trường"*, ⛔ không phải *"sửa lỗi"* |
| ~~⛔ **Chưa có NGƯỜI nhìn màn**~~ ✅ **ĐO `23/09`** | Owner mở màn thật ⇒ **`13`** điều trong `4` vòng, và ⛔ **không cổng nào** trong `8` cổng chạm tới được — xem `§6e` |

---

## §6e · ⭐⭐⭐ ĐÃ CHẠY — `2026-09-23` *(owner nhìn màn THẬT: `4` vòng, `13` điều)*

⭐⭐⭐ **`NFR-I10` lần đầu được đo bằng MẮT NGƯỜI.** `8` cổng đang chạy ⛔ **không cổng nào** chạm tới được `13` điều ấy — chúng đo *"có đúng ⛔ không"*, ⛔ không đo *"đọc có mệt ⛔ không"*.

| Vòng | Owner nói | Điều đo được đằng sau |
|---|---|---|
| ⓐ | cỡ chữ *"chưa đều, rối mắt"* | **`10`** cỡ chữ trên một màn ＋ `--mono` dùng **`14`** chỗ, gồm **câu văn xuôi** |
| ⓐ | bỏ cột `Bậc` · bỏ dải nhắc `GAP-SPEC-01` | lúc **quét**, câu hỏi là *"dòng nào chưa xong"*; dải nhắc nói về **dự án**, ⛔ không về việc kế toán đang làm |
| ⓐ | *«Xem đủ trường»* theo wireframe · màu · kéo rộng · tên cột | bốn chỗ màn **nói khó hơn mức cần thiết** |
| ⓑ | đủ trường **chiếm hết màn** | nó phục vụ **niềm tin vào dữ liệu** *(`QĐ-ITL-144 ⓐ`)*, ⛔ không phục vụ việc ghép ⇒ **LỚP PHỦ** |
| ⓑ | thẻ PM phải **đứng yên** khi cuộn | rail đã làm đúng từ trước; bàn làm việc thì ⛔ chưa |
| ⓑ | cột **⛔ không thẳng hàng** | ⛔ **không phải lỗi căn lề** — vệt `auto` ＋ **mỗi dòng là một lưới riêng** |
| ⓒ | *"kế toán cần nhìn rõ cột Nguồn"* | tôi cố định bề rộng **để cột thẳng hàng** và ⛔ **không đo thứ phải nằm vừa trong đó** |
| ⓓ | bấm chọn ⇒ danh sách **nhảy về đầu** | lỗi do **chính phép sửa ⓑ** đẻ ra |
| ⓓ | PM đã gán phải hiện Transaction đã map | **`C4`** — hợp đồng khai từ đầu, ⛔ **chưa bao giờ** làm |

### ⛔⛔⛔ Một lỗi CHẶN lộ ra giữa chừng — ⛔ KHÔNG nằm trong câu hỏi nào

Đi đo cột `Số tiền` để căn thẳng thì thấy **⛔ không có gì trong đó**: `/itl-candidates` *(đường chính, ứng viên do MÁY đề xuất)* trả **HÀNG THÔ**, ⛔ không qua `khuon_ung_vien`.

⇒ Hai cột rỗng, và `khop_dung_tien` so `Number(undefined)` ⇒ **MỌI ứng viên đều thành *"lệch"*** ⇒ nút `Gán` **luôn** đi đường cảnh báo. ⭐⭐ **Một phép khớp ĐÚNG được trình bày như một phép khớp SAI** — tệ hơn ⛔ không hiện gì, vì nó dạy kế toán rằng cảnh báo là chuyện thường.

⛔⛔ **Vì sao nó sống sót:** bài thử cũ hỏi `bac` và `itl_id` — **đúng hai khoá mà hàng thô TÌNH CỜ cũng có**. Một bài thử hỏi **vài khoá giao nhau** thì ⛔ **không bao giờ** thấy **hai khuôn là HAI**. ⇒ `GAP-API-09` vá; `GAP-API-10` mở — ⛔ **không cổng nào** hỏi *"cửa có trả đúng khuôn đã khai ⛔ không"*.

### ⭐⭐ Ba phép đo **lật cách hiểu vấn đề**

| Đo | Con số | Nó lật điều gì |
|---|---|---|
| Vệt `auto` ＋ lưới riêng từng dòng | **một** bản khai, **`14`** kết quả | *"cột ⛔ không thẳng"* ⛔ **không phải** lỗi căn lề |
| `Δ` ↔ bậc | `1.664`↔④ · `51`↔① · `46`↔② — **`97,1%`** có `Δ` | `Δ` là một **hàm của bậc** ⇒ ⛔ không tin gì mới *(`UI-F9`)*, và **⛔ không còn là một dấu hiệu** |
| Chùm `PM00001-1` | `29.211.750` ＋ `40.513.971` = **`69.725.721`** ≡ số tiền lệnh | chùm khớp **chính xác ở TỔNG** mà bậc từng dòng nói `④` — sửa ⛔ **không ở `_bac`** |

### ⛔⛔ Và một lỗi do **chính phép sửa của tôi** đẻ ra

Cho `.cands` cuộn riêng *(vòng ⓑ)* ⇒ `ve()` dựng lại cây ⇒ `scrollTop` về `0`. Trước `23/09` nó ⛔ **không tồn tại**: cả trang cuộn, và trình duyệt tự giữ vị trí.

⭐ ***Một phép sửa mở ra một lỗi mới thì phải có một bài thử ĐI KÈM, ⛔ không phải một lần nhìn lại.***

⭐ **Cổng sau đợt:** `1.903` bài thử · tuyến `40/40` · tài liệu `6/6` · số sống `109/109` · thuyết minh `31/31` · bản đồ `4/4` · khớp owner `19/19`. `4` commit `b1e8dd8`→`f7aa151`.

---

## §7 · Hai điều plan này tự khai

1. ⛔⛔ **`B0` chiếm quá nửa số việc, và ⛔ không dòng mã nào.** Đó ⛔ không phải chậm — đó là chỗ `4` GAP chặn đang nằm. Bắt đầu bằng mã thì `B0` vẫn phải làm, chỉ là làm **sau khi đã dựng sai**.
2. ⚠ **Plan này ⛔ chưa có ước lượng thời gian.** Tôi ⛔ **không** đưa con số tôi ⛔ không đo được — `§2` có `12` việc, `§3` có `16` bài, và đó là phép đo duy nhất tôi đang cầm.
