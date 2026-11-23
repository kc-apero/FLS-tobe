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
| AC-5 | `--duong-nen` ĐẠT; nâng sàn + bài ghim cùng commit | xem §Cổng | `MONG_PYTEST_TOAN_BO` 4822 → **4855** *(= số thu thập thật, web 690 không đổi)* + `tests/test_dung_moi_truong_isp.py` cùng commit |
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

## Cổng (CLAUDE.md) — dán thật
*(điền ở commit kế — xem cuối tệp)*
