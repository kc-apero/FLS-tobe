# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `C11` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.2 · **Ngày:** 2026-11-18 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-182`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 25 · C11 · `WO-180` · `BG-181`

> Thang lớp *(A1 · A2 · B1 · B2)* và mức *(CHẶN · NÊN SỬA · GHI NHẬN)*: **y như** §1 sổ chung. Sổ **chỉ THÊM**. Lúc ghi R1, cả 3 hàng đều `mở`; R2 *(`KQ-183`)*: `-01` `-03` đóng thật *(hàng `C11-R2-01`)* — hàng R1 giữ nguyên *(sổ chỉ THÊM)*; `-02` ⇒ backlog.
> Đo độc lập *(không dùng hàm của tác giả)*: ảnh DT3 `mapping_master_cfg.json` có **73** dòng · **21** dòng có `method_cfa2` = By GI **8** + By NOEM **5** + H1000 Ledger **4** + GI/OMC/PS/SC Ledger **4** · **2** dòng `need` mà method rỗng · ⇒ **17** mã HD có luật, **17** mã khác nhau *(0 trùng)* ⇒ "17 = 4 + 8 + 5" **ĐÚNG**.

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `C11-R1-01` | C11 | R1 | B1 | **NÊN SỬA** | `fls/repo/cau_hinh_repo.py:540-554` *(`nap_ix_alr`)* · `fls/cau_hinh/luat_pb.py:94-105` *(`luat_cua`)* · `tests/cau_hinh/test_luat_pb_pg.py:71-77` | **Hiệu lực theo kỳ không tích luỹ qua các lần nạp.** `nap_ix_alr` gán MỘT `tu_ky` cho cả 17 dòng và `doc_alr` chỉ đọc phiên bản MỚI NHẤT. R1 chạy trên kho thử: nạp `tu_ky=202501` rồi `202507` ⇒ bản đọc ra có **17** dòng, `tu_ky` chỉ còn `{202507}`; `luat_cua("LC", 202503)` = **`None`** *(đáng ra By GI từ 202501)*. Hiệu lực nhiều mốc chỉ có được khi **một** lần nạp mang nhiều `tu_ky` — đường nạp thật ⛔ làm được. Đúng câu hỏi *"tháng trước HD này phân bổ thế nào"* mà `luat_pb.py:7-12` nói là lỗ cần lấp. Bài `…nap_lai_cung_anh…` chỉ so checksum, ⛔ hỏi `luat_cua` ở kỳ cũ. | Nạp mới phải GỘP dòng của phiên bản liền trước *(giữ `hd@tu_ky` cũ, thêm mốc mới)*, hoặc `doc_alr` hợp các phiên bản; thêm bài: nạp 202501 + 202507 ⇒ `luat_cua(LC, 202503)` = By GI. Nếu owner chốt "mỗi lần nạp là bản đầy đủ" thì ghi rõ vào docstring + WO. | Bài oracle về hiệu lực theo kỳ phải đi qua `nap` ≥ 2 lần, ⛔ chỉ dựng bảng tổng hợp một lần | `mở` |
| `C11-R1-02` | C11 | R1 | A2 | GHI NHẬN | `IncrementalStepPlan-FLS-Voi_v3.1.2.md:2395` *(Scope: "ghi chú ATL B2:C4")* | Scope Step 25 nêu *"`fls/cau_hinh/luat_pb.py` + ghi chú ATL B2:C4"*; `B2:C4` xuất hiện **0** lần ở `fls/` + `tools/` và BG-181 ⛔ nhắc. Mục 7/8 ⛔ đòi ⇒ không chặn. | Orchestrator ghi: hoặc bỏ khỏi Scope, hoặc giao bước sau. | Grep `fls/`+`tools/`+`docs/` cho mọi cụm Scope trước khi bàn giao | `mở` |
| `C11-R1-03` | C11 | R1 | B1 | GHI NHẬN | `fls/cau_hinh/luat_pb.py:100-104` *(`cdt1 is None`)* · `:158-161` *(`ngoai_le` hợp lệ trên mọi phương pháp)* | `luat_cua("OFR", ky, cdt1="")` ⇒ `""` ≠ `None` ⇒ ⛔ `CAN_CDT1`, trả By NOEM *(đoán — chính điều luật cấm)*. `kiem` cũng nhận `ngoai_le` cho HD `By GI`/`H1000` *(chỉ OFR có trong AP)*. Đọc từ code, ⛔ có bài. | `if not cdt1` thay `is None`; hoặc ghi giới hạn. | Lỗi có tên ⇒ thử giá trị rỗng/khoảng trắng | `mở` |
| `C11-R2-01` | C11 | R2 | B1 | GHI NHẬN | `fls/repo/cau_hinh_repo.py:557-566` *(`nap_ix_alr`)* | **Đóng `C11-R1-01`, `-03`** *(ghi vòng sửa `KQ-182` đóng thật)*. `-01`: bài `test_C11_R1_01_…` **ĐỎ** trên `a78e9b5` *(`tu_ky` chỉ còn `{202507}`)*, **XANH** trên `42492a9`: `luat_cua(LC,202503)` = By GI@202501, 34 dòng *(17×2 mốc)*, nạp lại 202507 ⇒ vẫn 34 *(⛔ nhân đôi)*; bản hỏng ⛔ chở theo *(đột biến `except` thu hẹp ⇒ bài cắn)*. `-03`: `cdt1` `""`/`"   "`/`"\t"` ⇒ `CAN_CDT1`; `ngoai_le` ở HD ngoài `{OFR}` ⇒ lỗi có tên *(4 ca)*. 8 bài mới ĐỎ trên `a78e9b5`, 0 đỏ trên ngọn. Không có lỗi mới. | — | Giữ: bài hiệu lực theo kỳ đi qua `nap` ≥ 2 lần | `đóng` |

## Đo R1 *(mỗi số nói nó đếm gì)*
- Bài C11 **54** *(40 đơn vị + 6 pg + 8 tuyến… cùng `test_kho_cau_hinh_pg.py` 18 = **72 xanh** ở cụm 5444)*; `--duong-nen --cong 5444` MỘT lần: ĐẠT, tập đỏ + XFAIL = **28** *(thêm 0 · bớt 0)*, chạy **3520** bài.
- Đột biến trên bản `git archive`: **17** chỗ, **17** bị bài cắn *(tu_ky `<=`→`<` · max→min · `bat` · `khong_qua_allocate` · driver PE · `CAN_CDT1` · đếm thừa · `nap` bỏ kiểm trước ghi · `?run_id=` · ngoại lệ đảo · sổ nền tảng · tháng ≤13 · khoá `hd@tu_ky` · bẫy VLOOKUP `0` · `BanHong` · 500 thay 4xx lỗi có tên · `khong_doi` so bản ĐẦU)*. Bản sao đầu tiên sống = 0.
- `lint-imports` 11 kept/0 broken · `soi_bang_tuyen` KHỚP **45** tuyến · `kiem_tai_lieu` ĐẠT · chỉ-thêm: `UPDATE`/`DELETE` trên `fls_cau_hinh_*` bị `INV-I08` chặn.

## Đo R2 *(mỗi số nói nó đếm gì)*
- Đỏ→xanh: **8** bài vòng sửa ĐỎ trên `a78e9b5` *(1 `pg` + 7 ca tham số `test_luat_pb.py`)*; `tests/cau_hinh` **272** bài xanh trên cây gộp thử.
- Đột biến trên bản `git archive` `isp/C11`: **7** chỗ *(bỏ tích luỹ · bản hỏng chở theo · `cdt1` rỗng hợp lệ · `ngoai_le` mọi HD · bỏ mốc mới · bản cũ thắng · không `strip`)*, **7** bị cắn.
- Cây gộp thử `thu/C11` = `claude/bold-galileo-zukpaf` + `isp/C11`: xung đột **2** tệp *(`tools/dung_moi_truong_isp.sh`, `tests/test_dung_moi_truong_isp.py` — ô sàn `MONG_PYTEST_TOAN_BO`; loại: hằng số, hai bên cùng nâng)* ⇒ gộp tay, sàn = thu thập **3557** *(web **675**)*.
- `--duong-nen --cong 5434` MỘT lần: toàn bộ tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **3557**; web **3 = 3**, chạy **675**. `lint-imports` 11/0 · `kiem_tai_lieu` ĐẠT · `soi_bang_tuyen` KHỚP **45** tuyến.

## Changelog
- **v0.1** *(2026-11-18, `fls-test` R1 của `C11`, `KQ-182`)*: khởi tạo — **3** phát hiện `C11-R1-01…03` *(0 CHẶN · **1** NÊN SỬA · 2 GHI NHẬN)*.
- **v0.2** *(2026-11-18, `fls-test` R2 của `C11`, `KQ-183`)*: THÊM hàng `C11-R2-01` *(đóng `-01` `-03`)* + mục *Đo R2* — **0 CHẶN · 0 NÊN SỬA** mới.
