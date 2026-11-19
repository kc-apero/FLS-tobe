# BG-238 — bàn giao WO-234 · làm sạch số TK cá nhân ở BẢN HIỆN HÀNH

Nhánh `isp/PII` (nền `1882adb`) · commit ① `471f0ce` · cụm PG `5436` · review kế: `KQ-239` (R1) · `KQ-240` (R2).
⛔ Phiếu này KHÔNG chứa giá trị số TK — chỉ đếm · tệp · dòng.

## Máy quét `tools/quet_pii_repo.py` (+ `tests/kiem/test_quet_pii_repo.py`, 6 bài, có ca phá)
Quét `git ls-files` *(1.038 tệp — mẫu số Đ3, dưới 1.000 ⇒ ĐỎ)*, `mong` = 3 mẫu *(Đ5)*:
`khoa_R_CN` (`R | <số>_<NH> <TT>_CN`) · `tk_json_CN` (`"tk":"<số>"…"le":"CN"`) · `dien_giai_CK` (`<số>-<ddmmyy>-CK`).
**Trước → sau: 72 chỗ / 11 tệp → 0 / 0.** Nối vào cổng = bài `test_quet_repo_mau_so_khong_rong_va_dat_0` (tái phạm ⇒ ĐỎ ở pytest).
Ca phá đã đỏ trước che: bài ấy ĐỎ trên cây chưa che (11 tệp), xanh sau che.

## Bảng tệp (số chỗ MÃ CHE ghi vào; tổng 80 · 5 số khác nhau → `TK_CA_NHAN_1…5`)
| Tệp | chỗ che |
|---|---|
| `tests/fixture/cau_hinh/mapping_master_cfg.json` (ảnh DT3) | 5 |
| `docs/ITL/02_BA/Artifacts/man-gan-lenh-chi.html` | 27 |
| `docs/ITL/02_BA/Artifacts/man-gan-lenh-chi-v2.html` | 27 |
| `docs/ITL/02_BA/Artifacts/fls-gan-lenh-chi_9.html` · `_10.html` | 3 + 3 |
| `docs/ap-src/Man g#U00e1n…/ban-dung/fls-gan-lenh-chi_10.html` | 3 |
| `Brief-Thiet-Ke-Man-Ghep.md` · `Ket-qua-US-KT-037-…md` · `Prompt-Claude-Design.md` · `docs/ap-src/…/boi-canh/Prompt-Claude-Design.md` | 1 + 1 + 1 + 1 |
| `Ket-qua-Do-6-nhan-va-Xu-huong.md` | 2 |
Ghi chú đếm *(Đ4)*: máy thấy 72 khớp-mẫu; che 80 vì cùng số còn lặp ngoài mẫu *(thay mọi lần xuất hiện nguyên số, có biên chữ số)*.
AC-4: mỗi tệp tài liệu/HTML diff = đúng 1 dòng/chỗ che (`git diff --numstat`: 1/1 · 3/3 · 5/5), ⛔ dàn lại.

## Cách che
`TK_CA_NHAN_<n>` — n theo thứ tự gặp đầu tiên, cùng số ⇒ cùng mã; ⛔ đảo được (bảng số→mã chỉ sống trong bộ nhớ lúc chạy, ⛔ lưu). Giữ được mọi phép đo: số hàng · khoá duy nhất · ma_le `CN` ở cột B.

## Ảnh đổi CÓ CHỦ ĐÍCH (AC-1)
1 ảnh: `tests/fixture/cau_hinh/mapping_master_cfg.json` — `checksum_noi_dung` `a47878bf68499130 → 4f7605e5cff581ec` · sha256[:16] của tệp `3c1f61a28fd3d8ce → dc926c1b35b027ef`.
Ghim cập nhật cùng commit: `CHECKSUM_MM` *(test_anh_cau_hinh.py)* · `SHA_CAU_HINH` *(test_dap_an_406.py)* · `SHA_GIU` *(test_dap_an_cfa1.py)*. Ảnh khác: 0.

## Cổng
`--duong-nen --cong 5436` MỘT lần: **ĐẠT** — tập đỏ + XFAIL = đường nền `28 = 28` node id *(thêm 0 · bớt 0)* · chạy `4040` bài · `tests/web` `3 = 3`, `675` bài.
Q8: `MONG_PYTEST_TOAN_BO` `4034 → 4040` *(+6 bài của máy quét)* + bài ghim đổi cùng commit. `lint-imports` 11 kept · `kiem_tai_lieu` K1–K6 OK.

## ⚠ Rủi ro / ngoài phạm vi (AC-3)
1. **Lịch sử git cũ VẪN chứa giá trị số TK** (chủ chọn bản hiện hành, ⛔ viết lại lịch sử): ai clone/đọc commit cũ vẫn thấy. Xoá thật = đổi số TK ở ngân hàng hoặc viết lại lịch sử *(cần quyết riêng)*.
2. **TK pháp nhân** *(`_VGOH`, `_VGO9`, `_TPCI`…)*: ~155 chỗ ở ~51 tệp theo mẫu `R | <số>_…_<ĐV>` — NGOÀI phạm vi WO-234; `06_SCREEN_SPEC.md:615` khai rõ đây là TK công ty. Cần chủ quyết có che không.
3. Vài TK pháp nhân MSB 14 số trùng **8 chữ số đầu** với TK cá nhân *(cùng chi nhánh)* ở `05_DATA_DICTIONARY_ERD.md` · `FLS-Wireframe-Sau-Man.html` · `Checklist-G7…` · `Process-PM-den-ITL.md`: coi là mã chi nhánh của TK pháp nhân, ⛔ che. Nếu chủ coi là lộ ⇒ phiếu riêng.
4. Máy quét bắt 3 DẠNG đã thấy; dạng mới *(ví dụ số TK cá nhân trong ô tự do)* ⇒ ⛔ bắt — thêm mẫu khi gặp.
5. Biên bản cũ ở `KQ-109` · `BG-107` còn ghi checksum cũ `a47878bf…` — đúng lịch sử *(Đ2)*, ⛔ sửa.
6. Một lệnh dò cấu trúc của chính phiên này lỡ in **1 số TK pháp nhân** ra log phiên (không vào tệp/commit) — báo để orchestrator biết.

## Vòng sửa sau R1 (KQ-239)
⛔ Mục này KHÔNG chứa giá trị số TK — chỉ đếm · tệp · dòng. Chỉ THÊM; các mục trên giữ nguyên.
Quyết của chủ 19/11 08:30: TK pháp nhân ⛔ che; chỉ TK cá nhân *(đã duyệt 02:30)* — che CHỈ khi CHẮC.

| Mã | Kết | Đo |
|---|---|---|
| `PII-R1-01` CHẶN | **ĐÃ SỬA** | Che BÊN TRONG zip: 37 chỗ · 4 số · 4/7 tệp ruột; nhãn dùng lại `TK_CA_NHAN_1…4` *(học số→nhãn bằng so ruột zip với bản đã che trong cây; mâu thuẫn nhãn 0)*. Nén lại cùng cấu trúc *(tên · thứ tự · ngày · kiểu nén)*; so từng tệp: dòng đổi 3+3+1+1, số dòng bằng nhau, **0 lệch ngoài chỗ che**. Máy quét đọc ruột zip |
| `PII-R1-04` | **ĐÃ SỬA** | `KetQua.so_doc` đếm mục ĐÃ ĐỌC: **1.049** *(1.042 tệp văn bản + 7 ruột zip)*; mong ≥ 1.000 và ≥ 95 % mục. Không đọc được: **0** *(nhị phân khai theo đuôi 0 · đuôi lạ 0)*. Nhị phân khai theo `DUOI_NHI_PHAN` ⇒ liệt kê có tên; đuôi lạ ⇒ ĐỎ. Đỏ trước: đột biến `_doc → None` (M2) ⇒ 5 bài đỏ *(trước: 0)* |
| `PII-R1-05` | **ĐÃ SỬA** | Bài `…bien_chu_so_o_buoc_che` + ca số ⊂ chuỗi dài hơn; đột biến M9 *(bỏ biên)* ⇒ 1 bài đỏ *(trước: 0)* |
| `PII-R1-02` | **GIỮ + ĐẾM** | 1 số vừa gắn `CN` vừa gắn `_VGO1` *(khoá pháp nhân ở dữ liệu gốc — ảnh DT3)* ⇒ ⛔ CHẮC ⇒ **GIỮ 3 chỗ / 2 tệp** *(`05_DATA_DICTIONARY_ERD.md` 1 · `FLS-Wireframe-Sau-Man.html` 2)*. Máy quét đếm `số_vừa_CN_vừa_pháp_nhân`, ⛔ che. Đã che sẵn từ vòng đầu: 1 hàng `VGO1` ở ảnh DT3 + chỗ ở diễn giải `-CK` — giữ nguyên, ⛔ gỡ che *(chủ quyết nếu muốn gỡ)* |
| `PII-R1-03` | **GIỮ + ĐẾM** | 3 dạng chữ tự do đo ở máy mới, trên 1.049 mục *(kể cả ruột zip)*: `cho <số>-…` **46** · `<số>-Ref…-CK` **26** · `tài khoản <số>` **1**. Ngữ cảnh đi kèm: `APERO HQ…` · `CONG TY` *(pháp nhân)* hoặc không nhãn ⇒ **0 chắc cá nhân ⇒ che 0**. Máy quét thêm mẫu `so_da_biet_CN`: số ĐÃ CHẮC cá nhân *(có khoá `CN`)* lặp ở BẤT KỲ dạng nào *(kể cả ba dạng chữ)* ⇒ bắt + che; ca phá đủ ba dạng *(số giả)* |

Máy quét: **trước** *(cây `isp/PII` @ `d1ce388`, máy mới)* **69 khớp / 4 tệp ruột zip** → **sau 0 / 0**; mẫu 3 = 3 *(Đ5)*; 1.043 tệp theo dõi.
Phụ: `che_repo` xử cả tệp chỉ mang SỐ ĐÃ BIẾT *(không có mẫu)*; `so_cn` trả danh sách theo thứ tự gặp *(⛔ `set` — băm ngẫu nhiên làm nhãn lệch giữa lần chạy; lộ qua 1 bài đỏ ở đường nền lần 1, đã sửa + bài ghim)*.
`.gitattributes` thêm `*.zip binary` — trước đó `* text eol=lf` coi zip là văn bản *(cảnh báo CRLF→LF ở `git add`)* ⇒ có thể làm hỏng zip trong kho; đã kiểm blob trong index = tệp làm việc *(`testzip` None)*.
Q8: `MONG_PYTEST_TOAN_BO` `4040 → 4051` *(+11 bài của `test_quet_pii_repo.py`)* + bài ghim cùng commit.
