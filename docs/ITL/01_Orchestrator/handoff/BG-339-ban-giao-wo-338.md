# BG-339 — bàn giao `WO-338` · bể GIỮ RIÊNG cho A2.04 (bể A dữ liệu CŨ ↔ bể B dữ liệu THẬT hiện tại)

| | |
|---|---|
| **Thuộc** | `WO-338` |
| **Phát bởi** | `fls-dev` làn DATA · 2026-11-23 |
| **Nhận** | `fls-test` (R1 → `KQ-340`) |
| **Nhánh** | `claude/bold-galileo-zukpaf-isp/HELD` (nền = ngọn `isp/AG`) · SHA ghi ở cuối §Cổng |
| **Kho thật** | `KHONG_CHAM` · ⛔ gọi API thật · ⛔ bật agent · SA chỉ-đọc · ⛔ sửa `fls/agent/` |

⚠ **Report đo ĐƯỜNG ỐNG + CỔNG, ⛔ chất lượng mô hình.** Agent = mô hình GIẢ tất định (`luat_v0`, `luat_gia_v1`), ⛔ gọi API thật.

## Tóm tắt (đọc 1 phút)
- Hai bể dựng xong từ lượt đọc SA chỉ-đọc 23/11 trên `ITL RAW`: **A 65/65 ca · B 70/70 ca** *(= `mong` từng tầng; 0 ca thiếu)*; **0 trùng** ca dựng WO-329 và **0 trùng** prompt/ví dụ agent *(mẫu số: 65 và 70 ca; 20 tệp prompt/ví dụ đã quét)*. Bể nằm ngoài repo (`FLS_HELDOUT_NOI_DUNG`, dir 700, tệp 600); repo chỉ có `docs/ITL/05_FleetEval/be/DEM_BE.json` (đếm + vân tay muối).
- ⛔ **Một mục ĐỎ có tên:** đối chiếu "kỳ đã chốt Ledge **sống** ↔ ảnh đóng băng DT12" **⛔ đo được** — đọc cột ngày `ITL Ledge` hết giờ liên tục (lát 1000–1500 hàng; lượt 1 hỏng ở lát `A4010:A8009`, lượt chạy lại hỏng 2/4 lát đầu rồi dừng). Mẫu số = **0** ô ngày ⇒ ĐỎ, ⛔ coi là KHỚP (Đ3/Đ5). Có **phép thay thế** *(khác vật đo)* ở §A↔B.
- **Vòng GIẢ bắt được đúng thứ nó phải bắt:** luật giả `luat_gia_v1` nối **2/25** ca phải-để-người ở bể A và **1/25** ở bể B ⇒ bar thẻ `a3-1-ref` (0 ca phải-để-người bị nối) = **CHẶN** ở cả hai bể, cả TẮT · BẬT-đã-che · KHÔNG CHE. Đây là kết quả của đường ống + cổng, ⛔ của mô hình thật.

## Bảng AC → bằng chứng
| AC | Mong | Kết | Bằng chứng |
|---|---|---|---|
| AC-1 | công cụ dựng bể; mong từng tầng; ghi ngoài repo chmod 600; repo chỉ đếm | **ĐẠT** | `tools/dung_be_giu_rieng.py` · `tests/agent/test_be_giu_rieng.py` (nguồn GIẢ: mong A 65 · B 70, thiếu ⇒ ĐỎ cả hai chiều, chmod 700/600, ghi trong repo ⇒ exit 2) · chạy thật chỉ-đọc: A 65/65 · B 70/70 · `DEM_BE.json` |
| AC-2 | 0 trùng ca dựng WO-329 · 0 trùng prompt | **ĐẠT** | bài `test_doc_lap_*` + 2 bài CẤY ca trùng ⇒ phép đo cắn (=1) · thật: **0 · 0** ở cả A, B |
| AC-3 | `fleet_eval_voi.py --be-giu-rieng` GIẢ/phát lại ⇒ recall · nối sai · phải-để-người bị nối, TẮT vs BẬT-đã-che | **ĐẠT** *(chạy được, in số; exit 1 vì bar CHẶN — xem trên)* | `docs/ITL/05_FleetEval/vong/BE_GIU_RIENG.md` + `.json` · bảng dưới |
| AC-4 | bộ che trên bể thật: 0 lọt; `quet_pii_repo` 0; ⛔ commit bể | **KHÔNG ĐẠT phần "0 lọt"** (bộ che là TUỲ CHỌN theo chủ 06:00 ⇒ ⛔ chặn) · `quet_pii_repo` **0** ĐẠT · bể ⛔ commit ĐẠT | `tools/do_ro_ri_che.py` · bài `test_BE_THAT_phep_do_ro_ri_ghim_dung_so_da_do` (xanh) + `test_BE_THAT_che_0_lot_MONG_AC4` (**XFAIL** có lý do) |
| AC-5 | `--duong-nen` ĐẠT; nâng sàn + bài ghim cùng commit | **ĐẠT** | `MONG_PYTEST_TOAN_BO` 4822 → **4854** *(= số thu thập thật, web 690 không đổi)* + `tests/test_dung_moi_truong_isp.py` cùng commit |
| AC-6 | bể A: chuỗi 4 agent phát lại/GIẢ + fleet eval ⇒ mẫu số · khớp · lệch + recall/nối sai | **ĐẠT** | chuỗi **627/627 ô khớp · lệch 0 · ⛔ đo được 0** (TẮT và BẬT-đã-che) + G0 A2.04 ở bảng dưới |
| AC-7 | bể B: kỳ mở nhãn `chua_chot` ⛔ vào recall chính; report hai cột A ↔ B; kỳ chốt B = A | **ĐẠT một phần** | `chua_chot` 5 ca, `agent nối 0/5`, loại khỏi mẫu số recall (bài `test_chay_be_chi_so_va_chua_chot_khong_vao_recall`). Tập kỳ chốt A = B: **25 = 25**. Đối chiếu Ledge sống: **⛔ đo được (ĐỎ có tên)** |

## Bảng bể A ↔ bể B *(chỉ số; ⛔ nội dung)*
| | bể A · dữ liệu CŨ | bể B · dữ liệu THẬT hiện tại |
|---|---|---|
| kỳ đã chốt · kỳ mở | 25 · 0 | 25 · 1 (`2026-11`) |
| ca / mong | 65 / 65 | 70 / 70 |
| tầng *(số MÃ; L3·chuyển·chưa chốt = số DÒNG bank)* A · B · C · D · E · F | 10 · 5 · 10 · 5 · 10 · 10 | 10 · 5 · 10 · 5 · 10 · 10 |
| L3 không-Ref · L3 mã-khác · chuyển · chưa chốt | 5 · 5 · 5 · — | 5 · 5 · 5 · 5 |
| nhóm theo đáp án `phai_noi` · `phai_nguoi` · `l3` · `chua_chot` | 29 · 25 · 11 · 0 | 30 · 25 · 10 · 5 |

Vòng GIẢ — mẫu số chính **65** ca (⛔ tính `chua_chot`):
| phiên bản · cờ nội dung | nối A / B | nối sai A / B | recall phải-nối A / B *(mẫu số 29 / 30)* | **ca phải-để-người bị nối** A / B | L3 bị nối A / B |
|---|---|---|---|---|---|
| `v0-ma-tat-dinh` · TẮT | 0 / 0 | 0 / 0 | 0,0 / 0,0 | **0 / 0** | 0 / 0 |
| `v1-gia-tat-noi-dung` · TẮT | 2 / 2 | 2 / 1 | 0,0 / 0,0333 | **2 / 1** | 0 / 0 |
| `v1-gia-bat-noi-dung` · BẬT-đã-che | 2 / 2 | 2 / 1 | 0,0 / 0,0333 | **2 / 1** | 0 / 0 |
| `v1-gia-khong-che` · KHÔNG CHE *(chủ 06:00: chế độ chính)* | 2 / 2 | 2 / 1 | 0,0 / 0,0333 | **2 / 1** | 0 / 0 |

Đọc bảng: TẮT = BẬT = KHÔNG CHE ở **mọi** chỉ số trên bể này ⇒ luật giả ⛔ dùng nội dung để quyết (nối 2 ca bằng "ứng viên DUY NHẤT khớp tiền+tiền tệ+ngày"). Nên **bể này CHƯA đo được lợi ích của nội dung** — việc đó cần mô hình thật (`WO` sau, ⛔ trong WO-338). Recall ≈ 0 vì ID PM ở ứng viên là bí danh, mã PM hiếm khi nằm trong Diễn giải thật (đo: **1/12.710** dòng bank có Diễn giải chứa mã PM thật).

### Đối chiếu kỳ đã chốt A ↔ B
- tập kỳ chốt A = B: **25 = 25** ✔.
- Ledge sống ↔ ảnh DT12: **⛔ đo được** (0 ô ngày giải mã) ⇒ **ĐỎ**. Cách gỡ: đọc `ITL Ledge!A` bằng lát nhỏ hơn / giờ ít tải, hoặc chủ cấp bản xuất CSV cột A.
- **Phép thay thế** *(khác vật đo — Đ4: đây là dòng bank sống ở `Mapping L1` theo kỳ, ⛔ dòng Ledge sống)*: so với dòng Ledge đóng băng, **26 kỳ** · **8 kỳ lệch**: `2025-11` 475 vs 477 · `2026-02` 438 vs 439 · `2026-03` 582 vs 584 · `2026-04` 599 vs 600 · `2026-05` 536 vs 537 · `2026-06` 611 vs 613 · `2026-07` 683 vs 686 *(7 kỳ chốt, bank ít hơn Ledge 1–3 dòng; ⛔ giải thích nguyên nhân — chưa đo)* · `2026-11` 748 vs 659 *(kỳ MỞ, tăng 89 dòng từ 20/11 — đúng kỳ vọng)*. Ngược lại **18 kỳ khớp tuyệt đối** *(vd `2026-10` 1038 = 1038)*. ⚠ Đây là bằng chứng GIÁN TIẾP, ⛔ thay cho đo Ledge sống.

### Vũ trụ (đếm, lượt đọc 23/11)
Mapping L1 **12.710** dòng bank dùng được *(bỏ 1.544 dòng ⛔ có ngày · 12 dòng ⛔ có tiền tệ)* · PM **3.909** dòng lệnh chi · số **mã** theo hình A **2.437** · B **30** · C **78** · D **5** *(đúng số thẻ)* · E **120** · F **327** · dòng bank ⛔ ghép được: Số chứng từ rỗng **100** · mã ⛔ có ở PM **9.051** (trong đó **8.877** ⛔ vào tầng nào, phần còn lại là L3 mã-khác) · loại do đáp án mâu thuẫn Mapping L1 ↔ `pm_join`: **6** mã hình A.

### Riêng tư — số đo của bộ che *(TUỲ CHỌN theo chủ 06:00; ⛔ in mẫu)*
Bộ dò độc lập `tools/do_ro_ri_che.py`, mẫu số = số nội dung **65 / 70**, tập khác rỗng (trước che dò thấy **34 / 40**):
| | trước che A / B | sau che A / B |
|---|---|---|
| email | 0 / 0 | 0 / 0 |
| số TK (dãy ≥ 8 số, kể cả xen dấu) | 28 / 35 | **1 / 3** |
| Số chứng từ nguyên văn | 0 / 0 | 0 / 0 |
| tên người *(ỨNG VIÊN: họ Việt + 1–3 từ viết hoa — có thể dương giả)* | 6 / 5 | **5 / 2** |
Lớp 2 (`che.kiem_den`) chặn **0** ca. ⇒ bộ che `che_noi_dung` **bỏ sót** số TK xen dấu cách và tên **có dấu / chữ thường**. ⛔ Không sửa `fls/agent/` (luật phiếu). Khuyến nghị nếu chủ muốn giữ che: WO riêng nới `MAU_TEN`/`MAU_SO_DAI`.

## Câu chủ — hai chỗ TỰ ĐỊNH NGHĨA (theo lời orchestrator 06:00) + khuyến nghị
| # | Chỗ tự định nghĩa | Vì sao | Khuyến nghị |
|---|---|---|---|
| **Q1** | **Nguồn bank = `ITL RAW`** (`Transaction Mapping L1`, cột A–G + N; PM = `[Importrange]PM_Unpivot`) | sheet `Bank Transactions` gốc (`1zJA0M…`) trả **403** cho SA | **Chấp nhận.** `Mapping L1` mirror đúng cột `Transaction Original` (đối chiếu tiêu đề 7/7 vị trí) |
| **Q2** | **Kỳ "đang mở" = tháng của ngày chạy** (`2026-11`); kỳ chốt A = kỳ ảnh DT12 trừ kỳ mới nhất (25 kỳ `2024-10…2026-10`) | ⛔ có cờ "kỳ đã chốt" ở sheet | **Chủ xác nhận** (nếu `2026-10` còn mở thì đổi `ky_mo` ⇒ `chua_chot` tăng) |
| **Q3** | **Đáp án phải-nối = `ID PMLine` ở `Mapping L1`** (VLOOKUP theo Reference No của AS-IS, ⛔ gồm lần người đè `_adjust`), nhận chỉ khi = dòng `pm_join` chọn; D·E·F → `DE_NGUOI`; **L3 → `DE_NGUOI`** | không có cột "mối nối người chốt" ở mức dòng-lệnh-chi | **Chấp nhận cho vòng đầu**; L3 chấm NGHIÊM (nối = sai) vì ⛔ có đáp án Final — nên có `human-verified` cho L3 trước khi tin recall L3 |
| **Q4** | **L3 "mã khác" theo HÌNH mã** (`FT…`·`IBDN…`·`PC…` ≠ Số chứng từ) thay vì "mã trùng một dòng PM" | định nghĩa gốc chỉ cho **1** dòng/12.710 ⇒ ⛔ đủ 5 ca | **Chấp nhận**; thẻ ghi 136 (đo ảnh 26/08, định nghĩa khác) |
| **Q5** | Bí danh mã PM trong ca = `PM-<10 chữ cái>` | hex bị lớp 2 nhầm số TK (lỗi đo 23/11, ghim bài) | giữ |

## Trung thực về giới hạn
1. Chỉ đo **đường ống + cổng**. Chưa có lời gọi API thật; recall ≈ 0 là của LUẬT GIẢ.
2. Vòng 3 "BẬT-đã-che" ≡ TẮT trên bể này ⇒ **C4 chưa có số liệu để quyết bằng chất lượng**; chủ đã chọn "cho đọc toàn bộ" (06:00) nên ⛔ chặn.
3. Đối chiếu Ledge sống **ĐỎ (⛔ đo được)** — chưa kết luận "nguồn đã sửa sau chốt" hay không.
4. Tên người trong phép đo rò rỉ là **ứng viên** (dò theo họ), ⛔ khẳng định.

## Cổng (CLAUDE.md) — dán thật *(cụm PG cổng 5437, 23/11)*
```
python -m pytest tests/agent/test_be_giu_rieng.py     → 32 passed (có và không có FLS_HELDOUT_NOI_DUNG), 0 skipped
python tools/quet_pii_repo.py                         → [ĐẠT] 0 chỗ số TK cá nhân · 0 tệp
python docs/ITL/_tools/kiem_tai_lieu.py               → cong tai lieu DAT (493 file, 2982 bang, 968 o ngay, 104 ma QD)
python tools/soi_bang_tuyen.py                        → ban khai KHOP SQL that o ca 49 tuyen
python tools/kiem_thuyet_minh.py                      → CONG THUYET MINH DAT — 35/35 nut
lint-imports                                          → Contracts: 11 kept, 0 broken.
python -m fls.db.pg_migrate                           → khong co gi de ap · pg_verify: khop
bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5437:
[ĐẠT] đường nền toàn bộ tập đỏ + XFAIL = đường nền: 28 = 28 node id (trong đó XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 4854 bài (mong ≥ 4854) · skipped 0 · deselected 0
  [ĐẠT] đường nền tests/web  tập đỏ + XFAIL = đường nền: 3 = 3 node id (trong đó XFAIL 0 = 0 · thêm 0 · bớt 0) · chạy 690 bài (mong ≥ 690) · skipped 0 · deselected 0
  toàn bộ: 12 failed, 4826 passed, 2 xfailed, 14 errors · tests/web: 3 failed, 687 passed · KẾT: ĐẠT — mọi phép kiểm khớp mong
```
**Hai cổng ĐỎ có sẵn từ nền — ⛔ do WO-338** *(đã chạy lại ở `9840f27`, ra y hệt)*:
- `docs/ITL/_tools/khop_owner.py --kiem` → exit 1 (`B1`, `C6` đổi trạng thái; khối lộ trình lệch bản sinh lại).
- `tools/kiem_so_song.py` · `tools/dong_bo_so_song.py --ghi` → `FileNotFoundError: .venv/Scripts/lint-imports.exe` — đường dẫn Windows cứng, ⛔ chạy được trên Linux cloud. *(⛔ đo được ở máy này; chưa chạy ở máy chủ)*

Lượt đầu của `--duong-nen` ĐỎ vì 7 bài của WO-338 bị SKIP khi vắng bể thật (cổng đòi skipped = 0) → sửa: bài chạy trên bể giả khi vắng bể + `test_DEM_BE_nhat_quan` luôn chạy; lượt hai ĐẠT.

---

## Vòng sửa sau R1 (KQ-340) — `fls-dev` làn DATA · 2026-11-23 *(chỉ THÊM; các mục trên giữ nguyên là biên bản R0)*

⚠ Mọi con số ở mục này là của **lượt dựng lại 23/11 (lần 2)** trên bể ngoài repo; nhãn = cái nó đếm (Đ4). Agent vẫn là mô hình **GIẢ** (0 lượt API thật · 0 ghi sheet · 0 ghi kho thật). Mục "Cổng" của R0 ở trên thuộc nền `9840f27` — bản **hiện hành** ở mục §Cổng sau vòng sửa cuối trang.

### Việc đã sửa *(mỗi mục sửa có bài ĐỎ đúng lý do trước)*
| Mã | Mức | Đã làm | Bằng chứng |
|---|---|---|---|
| `HELD-R1-01` | CHẶN | **Gộp `origin/…/AG` (ngọn `2db1f22`, R2 cuối ĐẠT) vào HELD** (`git merge --no-ff`, 3 xung đột). `tools/fleet_eval_voi.py`: chuyển `VONG`/`chay_vong`/`chay_chuoi_be`/`chay_be` sang `che_do` *(`mo` · `che_noi_dung` · `che_het`)*, chuỗi gọi `cav.chay("gia", che_do, ncc=…)` + `cav.sinh_report(…)` của AG. Sàn: script + bài ghim = **4.967** (= `pytest --collect-only` cây gộp, ⛔ cộng tay) · web **690**. **⛔ sửa `fls/` của AG: 0 tệp** *(`git diff 2db1f22 -- fls/` rỗng)* | 28 → mục tiêu **28 = 28** (xem §Cổng) · `tests/test_dung_moi_truong_isp.py` 60 passed |
| `HELD-R1-02` | CHẶN | Ca bể mang `tk` = cột G `Tài khoản` của `Mapping L1` *(`dung_be_giu_rieng.DongNguon.tk`, ép số nguyên khi Sheets trả float)*. **Bể dựng lại: A 65/65 · B 70/70 ca có `tk` khác rỗng.** `o_ca` của AG chạy hết, ⛔ `KeyError`. | bài `test_o_ca_doc_tk_va_moi_ca_cua_be_co_tk` — **ĐỎ** khi gỡ `"tk"` khỏi ca: `KeyError: 'tk'` ở `chay_agent_voi.py:137` *(đột biến của reviewer)* · `test_tk_doc_tu_cot_G_va_ep_so_nguyen` |
| `HELD-R1-03` | NÊN SỬA | Bài ghim **số đã đo** cho khoảng trống bộ che: `test_che_hien_tai_so_tk_xen_cach_het_lot_ma_ten_co_dau_van_lot_DA_DO` *(sau `che_noi_dung`: số TK xen cách ⇒ 0 lọt; tên CÓ DẤU ⇒ 1 lọt)*. Hai tên bài cũ trong AC-4 *(`…che_0_lot_MONG_AC4`, `…phep_do_ro_ri_ghim_dung_so_da_do`)* **đã đổi** — tên hiện hành: `test_BE_che_ro_ri_phep_do_hop_le_va_ghim_so_da_do` + bài mới trên | grep hai tên cũ trong `tests/` = **0** |
| `HELD-R1-04` | NÊN SỬA | `do_ro_ri_che.do` thêm `do_duoc_theo_loai` *(loại có `truoc_che = 0` ⇒ `False`)*. Trên bể thật: **`email` · `so_chung_tu` = `False`** — "0 lọt" của hai loại ấy là tập RỖNG, ⛔ số đo; `so_tk` · `ten_ung_vien` = `True`. | `test_ro_ri_hop_le_THEO_LOAI_…` · `test_DEM_BE_nhat_quan` đòi `do_duoc_theo_loai == {loại: truoc_che > 0}` |
| `HELD-R1-05` | NÊN SỬA | Muối vân tay **dẫn xuất** `HMAC-SHA256(bí mật ngoài repo, "fls-be-giu-rieng/<a/b>")[:16]`: bí mật = `FLS_MUOI_BE` hoặc khoá SA chỉ-đọc của môi trường *(đã có ở mọi container của phiên)*; ⛔ bí mật nào ⇒ ngẫu nhiên. Dựng lại lần 2 ⇒ `test_BE_van_tay_khop_tep_dem_repo` **ĐẠT trên bể thật** *(có `FLS_HELDOUT_NOI_DUNG`)*, trước đó ĐỎ. | `test_muoi_on_dinh_theo_bi_mat_va_khac_giua_hai_be` *(ổn định · khác giữa a/b · đổi bí mật ⇒ đổi muối · không bí mật ⇒ ngẫu nhiên)* |
| `HELD-R1-06` | NÊN SỬA | Bỏ nhánh `khong_che` (đọc thẳng `luat(o_ca)`). **Chế độ chính của chủ = `che_do="mo"` đi QUA `chay_skill`** *(cổng skill + chốt)*; bài kiểm `cong_skill.dat` ở mọi vòng. | `test_chay_be_chi_so_…` |
| `HELD-R1-07…10` | GHI NHẬN | **Backlog, giữ nguyên, có lý do:** `-07` đáp án = cột N `Mapping L1` *(công thức)* — đổi đáp án cần chủ chốt Q3/Q4, ⛔ việc của vòng sửa · `-08` A∩B **9** ca — bể là hai mẫu từ CÙNG vũ trụ, loại trùng làm lệch `mong` từng tầng · `-09` **đã tự gỡ**: lượt dựng lần 2 đọc Ledge **hết 12.675 ô ngày · 0 lát hỏng** ⇒ đối chiếu kỳ ĐỎ cũ ⇒ **KHỚP** (xem dưới) · `-10` sàn đặt ở `-01` | — |

### Đo thêm trong vòng sửa — **điều R1 chưa thấy**
1. **Đối chiếu kỳ "đã chốt" ĐỎ vì lý do SAI** *(bản R0 cho cả kỳ ĐANG MỞ vào `ket`)*. Ledge đọc được lần này: **25/25 kỳ chốt khớp ảnh DT12 · mẫu số 12.675 ô ngày**; chỉ kỳ mở `2026-11` lệch *(ảnh 659 dòng · sống 701 — kỳ mở nhận thêm dòng sau ảnh: lớn lên là đúng)*. Sửa `doi_chieu_ky`: `ky_lech_ky_chot` (vào `ket`) tách khỏi `ky_lech_ky_mo` (chỉ in); bài `test_doi_chieu_ky_mo_lon_len_KO_do_nhung_ky_chot_lech_DO` **cả hai chiều** (Đ5). `ket` = **KHỚP**.
2. **Bộ che `che_noi_dung` (AG, `AG-R1-03`) trên bể thật: lọt nhiều hơn bản cũ.** Nhãn: bộ dò độc lập `do_ro_ri_che`, mẫu số **65 / 70** nội dung — số TK *(dãy ≥ 8 số)* trước che **28 / 35** ⇒ sau che **17 / 24** *(R0 đo ở nền cũ: 1 / 3)*; ca bị lớp 2 `CamGui` chặn **9 / 11**. Nguyên nhân đo được: dãy số **DÍNH CHỮ** *(dạng mã `FT…` + 9–14 số)* — `MAU_CUM_SO` đòi `(?<![\w.\-])` nên ⛔ bắt dãy dính chữ, còn `\d{6,}` cũ thì bắt. Hệ quả ở vòng eval: `v1-gia-che-noi-dung` bị `CamGui` **từ chối gửi** *(10 / 14 chỗ)* — **cổng chạy đúng**, và nay được ghi là KẾT QUẢ có tên `bi_cam_gui` *(⛔ làm dừng cả vòng)*. **⛔ sửa `fls/agent/`** (che là TUỲ CHỌN theo chủ 06:00; chế độ chính `mo` ⛔ qua che) ⇒ **GHI NHẬN cho orchestrator**: nếu chủ muốn giữ `che_noi_dung`, cần WO cho AG nới `MAU_CUM_SO` bắt dãy dính chữ.

### Bảng A ↔ B mới *(chỉ số; ⛔ nội dung · mẫu số chính **65** ca mỗi bể, `chua_chot` tách)*
| | bể A · dữ liệu CŨ | bể B · dữ liệu THẬT hiện tại |
|---|---|---|
| ca / mong · ca có `tk` | 65 / 65 · **65** | 70 / 70 · **70** |
| kỳ chốt · kỳ mở · đối chiếu kỳ chốt ↔ ảnh DT12 | 25 · 0 · **KHỚP** | 25 · 1 · **KHỚP** |
| độc lập: trùng ca WO-329 · trùng prompt | 0 · 0 | 0 · 0 |
| `v0-ma-tat-dinh` (`che_het`) nối · sai · người-bị-nối | 0 · 0 · 0 | 0 · 0 · 0 |
| `v1-gia-mo` **(`mo` — CHÍNH)** nối · sai · recall phải-nối *(mẫu số 29 / 30)* · **ca phải-để-người bị nối** · L3 bị nối | 2 · 2 · 0,0 · **2** · 0 | 2 · 1 · 0,0333 · **1** · 0 |
| `v1-gia-che-het` nối · sai · recall · người-bị-nối | 2 · 2 · 0,0 · 2 | 2 · 1 · 0,0333 · 1 |
| `v1-gia-che-noi-dung` | ⛔ `CamGui` 10 chỗ | ⛔ `CamGui` 14 chỗ |
| `chua_chot`: ca · agent nối *(⛔ recall)* — vòng `mo` | 0 · 0 | 5 · **0** |
| điểm TB 0–2 — `mo` | 1,4923 | 1,5231 |
| chuỗi 4 agent `mo`: ô khớp / mẫu số · lệch · ⛔ đo được | 631/631 · 0 · 0 | 631/631 · 0 · 0 |
| chuỗi `che_het` · `che_noi_dung` ô khớp | 631/631 · 195/631 *(dừng ở A2)* | 631/631 · 195/631 |
| G0 A2.04 chuỗi `mo`: nối · sai · recall · người-bị-nối | 2 · 2 · 0,0 · 2 | 2 · 1 · 0,0333 · 1 |

Đọc bảng: bar thẻ `a3-1-ref` *(0 ca phải-để-người bị nối)* vẫn **CHẶN** ở cả hai bể ở **mọi** chế độ có chạy — luật giả `luat_gia_v1` nối 2 / 1 ca bằng "ứng viên DUY NHẤT khớp tiền+tiền tệ+ngày", ⛔ dùng nội dung ⇒ `mo` ≡ `che_het` ở mọi chỉ số; bể **chưa** đo được lợi ích của việc cho agent đọc nội dung + số TK *(cần mô hình thật — ngoài WO-338)*. `fleet_eval_voi.py --be-giu-rieng` exit **1** vì CHẶN, đúng mong.

**Giả định** *(Q6 — hẹp nhất, chủ xác nhận)*: `tk` = cột `Tài khoản` của `Mapping L1` *(số TK của dòng sao kê)*; cột `Số tài khoản` của `PM_Unpivot` *(người nhận)* ⛔ đưa vào ca *(ca mang MỘT dòng bank; người nhận đã nằm ở ứng viên PM, mà ứng viên chỉ mang `pm · tiền · cur · ngày`)*. Khuyến nghị: giữ.
