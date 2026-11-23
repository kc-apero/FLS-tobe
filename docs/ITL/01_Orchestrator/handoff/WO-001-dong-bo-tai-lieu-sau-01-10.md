# WO-001 — Sửa thước đo mốc B + nhãn dấu sổ, rồi mới đồng bộ số sống sau 01/10

| | |
|---|---|
| **Trạng thái** | ✅ **`DONG`** *(`fls-ba` nghiệm thu PO 01/10 khuya — [`KQ-010`](KQ-010-kiem-bg-009.md) ĐẠT 9/9; mục **Nghiệm thu PO**)* · ~~`CHO_TEST`~~ *(`fls-dev` bàn giao [`BG-009`](BG-009-ban-giao-wo-001.md) @ `6e98796`, 01/10 tối)* · ~~`DANG_LAM`~~ *(nhận 01/10 tối @ `ee390cb`)* · ~~`MO`~~ · ⭐⭐ **LÀM NGAY** *(01/10 tối — `WO-003` đã `DONG` theo [`KQ-007`](KQ-007-kiem-bg-006.md); đây là việc kế tiếp của `fls-dev`)* · **SẴN SÀNG cho Dev** từ 01/10 *(owner đã trả Q1–Q4 — `QĐ-ITL-150`; ⛔ còn câu treo)* *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Vòng** | `1` · phát 01/10 · ⭐ cập nhật 01/10 *(điền lời owner, mở `T1b`·`T4`·`T5`)* · ⭐ rà lại 01/10 tối sau `c1fb250`…`5f4ae68` *(`WO-003` vòng 1, `BG-004`, `KQ-005`)* — phạm vi **đứng**; đính chính `AC-1b`/`AC-4` *(dấu `xfail`)* + Rủi ro 3 *(nền `kiem_so_song` nay **83**; làm **sau** `WO-003` vòng 2)* |
| **Phát bởi** | `fls-ba` · 2026-10-01 |
| **Nhận** | `fls-dev` |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B`** *(tác vụ ① mapping — cổng `B2`…`B5`)* + mọi số sống của mốc `A`/`B` mà owner đọc để quyết.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ **phiếu này ⛔ xoá trực tiếp mắt xích nào** — nói thẳng. Nó sửa **thước đo** của mắt xích *"SHQ1 / SHQ2 → chuẩn hoá & mapping"*: hôm nay thước báo mốc B **4/5 đạt** khi **0** kế toán đã bấm; sau cú đồng bộ kế tiếp nó sẽ báo **5/5**. Một thước nói sai thì mọi quyết định "mapping xong chưa" đứng trên cát.

## Căn cứ
- Owner 01/10: *"BA review lại tài liệu"* — kết quả: [`02_BA/Artifacts/Ra-soat-tai-lieu-2026-10-01.md`](../../02_BA/Artifacts/Ra-soat-tai-lieu-2026-10-01.md) **v1.0**, phát hiện `R-1`, `R-2`, `R-3`, `R-5`, `R-6`, `R-9`, `R-25`.
- `QĐ-ITL-143` *(18/09 — máy ghép xong thì GỢI Ý)*: chính đợt này ghi **2.219** sự kiện `match` actor `may@fls` và làm `_cong_moc_b` lật xanh *(commit `20e2910`)*.
- Lời khai sẵn trong mã — `tools/kiem_so_song.py::_cong_moc_b` docstring: *"LUAT NAY CO NGAY HET HAN … Giay phut con so ay len `1`, phep dem nay thanh qua tho … ⇒ Luc do phai siet lai"*. Ngày ấy đã đến **18/09**.
- `10_HOP_DONG_AGENT` §6: dòng ghi UAT mang `reason` bắt đầu `UAT <ngày>`.
- ⭐ **`QĐ-ITL-150`** *(owner 01/10: *"còn lại như đề xuất"*)* — trả lời Q1, Q2, Q4 bên dưới. Q3 trả riêng ở **`QĐ-ITL-149`** *(owner: *"Máy gợi ý"*)* — phần mã của nó ở **`WO-003`**, ⛔ ở phiếu này.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/Ra-soat-tai-lieu-2026-10-01.md` | §1, §2 `R-1`…`R-3`, `R-5`, `R-6`, `R-25` | v1.1 *(v1.0 + changelog 01/10 tối)* |
| `01_Orchestrator/09_MILESTONES_HAI_TAC_VU.md` | §2 *Cổng ra của mốc `B`* *(định nghĩa `B2`…`B5`)* | v1.12 |
| `01_Orchestrator/10_HOP_DONG_AGENT.md` | §1 *(bảng chủ tệp)* · §6 ngoại lệ UAT + `dong_bo_so_song --ghi` | ⭐ **v1.1** |
| `00_MASTER_INDEX.md` | `QĐ-ITL-150` | v0.30 |
| `02_BA/11_INVARIANTS.md` | `INV-I08` *(sổ chỉ-thêm — ⛔ sửa/xoá dòng UAT)* | ~~v0.14~~ ⇒ **v0.15** *(01/10 tối: chỉ thêm `INV-I22` cho `WO-003` vòng 2 — `INV-I08` ⛔ đổi)* |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| **`T1a`** — `tools/kiem_so_song.py`: `su_kien_cho_nguoi` loại sự kiện do **máy** ghi *(actor `may@fls` — dùng **chính hằng** `fls/repo/may_ghep.py::MAY`, ⛔ gõ lại chuỗi)*. ⭐ `fls-test` đã độc lập bắt cùng lỗi *(`KQ-002 · F-2`, bài `tests/nghiem_thu/test_kq002_moc_b_khong_dem_may_la_nguoi.py` — đọc câu SQL của cổng bằng `ast`)* ⇒ bài ấy là **thước nghiệm thu** của `T1a`; ⛔ sửa nó. ⭐ ⛔ Không chờ owner: chính docstring nói `match`/`unmatch` *"chỉ sinh từ một cú bấm có ý trong `F01`"* — tiền đề ấy vỡ 18/09 | ⛔ Chạy `tools/dong_bo_so_song.py --ghi` **trước** khi `T1a` + `T1b` + `T2` xanh *(Q2)* |
| **`T1b`** — loại dòng UAT *(`reason LIKE 'UAT %'`)* khỏi `su_kien_cho_nguoi` **và** khỏi `moi_noi_da_bo` *(cổng `B4`: `fls_pm_unlink` nối về `fls_queue_event` `unmatch` cùng `itl_id`/thời điểm)* — ⭐ **Q1 đã trả: UAT ⛔ tính người thật** *(`QĐ-ITL-150 ⓐ`)*. ⚠ Lọc theo **`reason` bắt đầu `UAT `**, ⛔ theo actor *(actor UAT là owner — một người thật có thể làm việc thật sau này)*. ⚠ ⛔ Đụng lý do mặc định `(may dien) …` của `WO-003` — đó là cú bấm **người thật**, phải đếm | ⛔ Sửa/xoá dòng UAT trong kho *(`INV-I08`)* |
| **`T2`** — dấu `dau_so` *(`kiem_so_song.py:310`–`312`, `:598`)*: dấu cạnh *"N dòng sổ"* phải là `started_at` của lượt nạp **SỔ** gần nhất *(lượt có dòng trong `fls_itl`)*, ⛔ lượt bất kỳ. Dấu ảnh PM `dau_anh` giữ nguyên | ⛔ Viết lại câu văn **ngoài** những câu cạnh số mà `T5` vừa đổi nghĩa — câu văn `09`, dashboard §1–§4, master §8/§10 thuộc `fls-ba` *(`QĐ-ITL-150 ⓒ`)*; danh sách câu đã biết sai ở báo cáo `R-8`, `R-9`, `R-10`, `R-11`, `R-16` ⇒ `fls-ba` sửa |
| **`T3`** — bài thử cho `T1a`/`T1b`/`T2` ở `tests/test_kiem_so_song.py`, **chứng minh ĐỎ trước** *(luật `Đ5`)* | ⛔ `GAP-CONG-01` *(đổi phép so giá trị ghim sang quan hệ)* — phiếu sau |
| **`T4`** ⭐ *(mở — Q4: `docs/ITL/_tools/**` thuộc `fls-dev`)* — `khop_owner.py`: `B5` neo lại về `BA-06` v4.7 *(tệp `12` là BIA — `R-5`)*; `C5` tách *"cột `fls_itl.memo`"* ↔ *"khung xem `fls_dien_giai`"* *(`R-6`)*; ghi lại `mong` kèm xuất xứ; chạy lại ⛔ `--kiem` để sinh lại khối `SINH-KHOP` trong `_AUDIT_ALIGNMENT_ROADMAP.md` | ⛔ Đổi mã cổng `B5`/`C5` sang tiền tố mới *(`R-7` — chờ owner, ⛔ thuộc phiếu này)* |
| **`T5`** ⭐ *(mở — Q2 + Q4)* — **SAU** khi `T1a`·`T1b`·`T2`·`T3` xanh: chạy `tools/dong_bo_so_song.py --ghi`; ⭐ **sửa luôn câu cạnh số** mà con số mới làm sai nghĩa *(owner Q2 — `10 §6` v1.1)*, **chỉ** những câu ấy; `BG` liệt kê từng câu `tệp:dòng · cũ → mới`. Câu biết trước sẽ đổi nghĩa: `09:147` · `dash:121` · bản vẽ `banve:1367` *(mốc B `4·1·0` ⇒ `1·1·3`: ⚠ ghi *"thước sửa, ⛔ việc lùi"* — Rủi ro 1)* | ⛔ Chạy `--ghi` **lần thứ hai** để dọn đỏ sinh ra bởi một `BG` khác *(`10 §6 ⓒ`)* |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 | Sau `T1a`, trên kho THẬT: `su_kien_cho_nguoi` = **`2`** *(chỉ hai sự kiện UAT)*, ⛔ `2.221`. **`2.219`** sự kiện actor `may@fls` đóng được **`0`** cổng | in khoá `su_kien_cho_nguoi` của `do_may()` *(tệp thử, ⛔ `python -c`)*; bài thử mở rộng `test_MAY_ghi_93k_su_kien_ma_KHONG_dong_duoc_cong_nao` với sự kiện `match` actor máy | Khuôn thử có **một** sự kiện `match` actor `may@fls` mà `moc_b_dat` đổi ⇒ bài phải **ĐỎ** |
| AC-2 | Sau `T1a`+`T1b` *(Q1 = "⛔ không tính UAT" — `QĐ-ITL-150 ⓐ`)*: kho THẬT ⇒ mốc B **`1` đạt · `1` một nửa · `3` chưa** — khớp bảng chi tiết `09:155`–`159` | `python tools/kiem_so_song.py` dòng *"dashboard · cổng mốc B"* in `MÁY đo 1 · 1 · 3` | Khuôn thử có **một** sự kiện `match` actor người, reason ⛔ bắt đầu `UAT` ⇒ `B5` phải lật **đạt** *(cổng ⛔ được mù với người thật)* |
| AC-3 | Dấu cạnh số dòng sổ = **`10/09 HH:MM`** *(giờ VN của lượt nạp sổ mới nhất trên `fls_itl`)*, ⛔ `01/10 16:21` | `kiem_so_song` nhóm *"kho · DẤU THỜI ĐIỂM bản sao sổ"* in giá trị máy | Khuôn thử có lượt `fls_run` PM mới hơn lượt sổ ⇒ dấu sổ ⛔ được đổi |
| AC-1b | Bài `KQ-002` `test_kq002_moc_b_khong_dem_may_la_nguoi.py` của `fls-test` **xanh** mà ⛔ một dòng của nó bị đổi | `pytest tests/nghiem_thu/test_kq002_moc_b_khong_dem_may_la_nguoi.py` + `git diff` tệp ấy = rỗng | Trả `_cong_moc_b` về câu SQL cũ ⇒ bài phải **ĐỎ** |
| AC-4 | `pytest` toàn bộ xanh · `lint-imports` **9 kept 0 broken** · số bài thử tăng đúng số bài mới | lệnh ở `CLAUDE.md` | — |
| AC-5 | `BG-NNN` ghi rõ: `kiem_so_song` còn đỏ bao nhiêu nhóm, **phân loại** theo bảng §1.1 báo cáo *(a/b/c)* — ⛔ "đỏ do số trôi" chung chung | đọc `BG` | — |
| AC-2b | `T1b` lọc **UAT** mà ⛔ lọc **lý do mặc định** `(may dien)` | bài thử: khuôn có **một** `match` actor người, `reason` = `"(may dien) ghep tren man - nguoi bam khong ghi ly do · ghep tay 1 dong lenh (X)"` ⇒ đếm **1** | đổi phép lọc thành `reason LIKE '(%'` hay lọc theo actor `khanhcq@%` ⇒ bài phải **ĐỎ** |
| AC-6 | `T4`: `khop_owner --kiem` — `B5` đo trên `BA-06` *(⛔ `12`)*, `C5` tách hai vế; mỗi `mong` mới kèm câu xuất xứ; cổng **ĐẠT** *(⛔ dòng `CONG NO`)* sau khi sinh lại khối `SINH-KHOP` | `python docs/ITL/_tools/khop_owner.py --kiem` in nguyên văn | đổi tên tệp neo của `B5` về `12_BA_MAN_GHEP_PM.md` ⇒ `B5` phải lật trạng thái ⇒ cổng **ĐỎ** *(khác `mong`)* |
| AC-7 | `T5`: sau `--ghi`, `python tools/kiem_so_song.py` **ĐẠT** *(0 lệch)* **và** mốc B ở cả `09`, dashboard §1, bản vẽ 13 = **`1 · 1 · 3`** kèm câu đúng nghĩa | lệnh cổng + `git diff` ba tệp + bảng câu trong `BG` | ⛔ chạy `T5` khi `T1a` chưa vá ⇒ ba nơi in `5·0·0` ⇒ `fls-test` phải bắt *(bài `test_kq002_moc_b_khong_dem_may_la_nguoi.py`)* |

⛔ **Đính chính 01/10 tối** *(`fls-ba`; chữ gốc ở trên giữ làm biên bản)*:
- **`AC-1b`** — bài `test_kq002_moc_b_khong_dem_may_la_nguoi.py::test_su_kien_cua_MAY_…` **vẫn mang** `@pytest.mark.xfail(strict=True)` *(`:72` — `KQ-005` giữ dấu vì nó thuộc phiếu này)*. Vá `T1a` xong, chạy thường nó ra **`XPASS(strict)` = FAILED** — ⛔ "xanh". Mong đúng: `pytest … --runxfail` ⇒ **passed**; chạy thường ⇒ **1** bài `XPASS(strict)`, `BG` ghi tên để `fls-test` gỡ dấu; `git diff` tệp ấy = **rỗng** *(như cũ)*.
- **`AC-4`** — *"`pytest` toàn bộ xanh"* ⇒ **chỉ** đỏ đúng **1** bài `XPASS(strict)` của `AC-1b`, ⛔ bài nào khác. Ba bài `xfail` của `KQ-005` *(`test_kq005_*`)* phải đã được `fls-test` gỡ dấu khi `WO-003` vòng 2 ĐẠT — nếu chưa thì `BG` ghi rõ.
- **Nền `kiem_so_song`** *(cho `AC-5`)*: `KQ-005` đo **83** nhóm lệch/⛔ đo được *(01/10 tối, @ `4b2b2e8`)* — ⛔ còn `47`/`55` như `Ra-soat` §1.1. `BG` tách theo nền **mới nhất** do `KQ` của `WO-003` vòng 2 ghi.

⭐ **Cập nhật 01/10 tối sau `KQ-007`** *(`fls-ba` — rà lại trước khi Dev nhận; chữ trên giữ)*:
- **Phạm vi `T1a`…`T5` đứng.** Đo lại sổ thật *(chỉ `SELECT`, @ `5d627c0`)*: sự kiện `match`/`unmatch` = `may@fls` **2.219** + `khanhcq@apero.vn` **2** · `fls_pm_unlink` **1** ⇒ số `AC-1` *(`2` · `2.221`)* **đứng**. Ba câu `T5` biết trước vẫn đúng chỗ, vẫn in `4 · 1 · 0` *(`09:147` · `dash:121` · `banve:1367`)*.
- **`AC-4` — điều kiện đã có:** ba bài `test_kq005_*` đã được `fls-test` **gỡ** dấu `xfail` *(`KQ-007`)*. `xfail` **duy nhất** còn lại trong cả bộ = `test_kq002_moc_b_khong_dem_may_la_nguoi.py::test_su_kien_cua_MAY_…` *(`:72`)* — chính bài của `AC-1b`.
- **Nền số phép thử:** `pytest` **`1948 passed, 1 xfailed`** = **1.949** phép thử *(`KQ-007`, @ `c785411`; `5d627c0` chỉ thêm giấy)*. `BG` báo số **tăng** so với nền này.
- **Nền `kiem_so_song` cho `AC-5`:** **83** nhóm lệch/⛔ đo được *(`KQ-007` @ `c785411`; đo lại **83** @ `5d627c0`)*. ⚠ Lượt `fls-ba` này bump `BA-06` v4.7 ⇒ **v4.8** *(`KQ-007 F-1`…`F-3`)* ⇒ nhóm *"master · §8 version BA-06"* **mới đỏ** *(loại b — version tài liệu; ⭐ `T5` `--ghi` dọn cùng `BA-05`/`BA-07`/`BA-10`/`BA-11` đã đỏ sẵn)* — nền **mới nhất** ghi ở dòng §5 dashboard của lượt này.
- **`T4`:** neo `B5` về `BA-06` — tệp nay **v4.8**, nội dung `B5` ⛔ đổi *(v4.8 chỉ thêm chữ màn sau bỏ ghép)*.
- `WO-008` *(chữ màn sau bỏ ghép, ưu tiên thấp)* xếp **SAU** phiếu này — đỏ số phép thử của nó là việc của chính nó, ⛔ của `T5`.

## Dữ liệu
- Bảng/cột chạm *(chỉ ĐỌC)*: `fls_queue_event(evt_type, actor, reason)` · `fls_pm_unlink` · `fls_run(started_at)` · `fls_itl(run_id)`.
- Ghi kho THẬT: `KHONG`.
- Số dòng dự kiến chạm *(đã đếm 01/10)*: sự kiện ngoài `reason` **2.221** *(`may@fls` 2.219 · `khanhcq@apero.vn` 2)* · `fls_pm_unlink` **1** · `fls_run` lượt có dòng sổ: `NAP-2026-09-10-RTANG24037` *(6.617)* + `NAP-2026-09-10-BU1` *(1.770)*.
- ⚠ **Biên bản hồi tố cú UAT 01/10** *(`10 §6` đòi WO trước khi ghi kho thật; cú này chạy **trước** khi có phiếu nào)*: owner `khanhcq@apero.vn`, 01/10 16:06:19 → 16:06:40 giờ VN, `itl_id 27728`, dòng lệnh `PM00338-1`: `fls_pm_link` +1 *(hình `T`)* · `fls_pm_unlink` +1 · `fls_queue_event` +2 *(`evt 163561`, `163567`)* · `fls_adjustment` +4 *(`163563`, `163565`, đảo `163569`, `163571`)* · `fls_journal` +4. Ròng trên mapping: **0**.

## Câu còn treo

⭐ **Không còn câu nào treo** *(01/10)*. Bốn câu dưới giữ nguyên văn làm **biên bản**; lời owner ghi ngay dưới từng câu.

- **Q1 — Cú UAT 01/10 của owner có tính là "người thật" cho cổng mốc `B4`/`B5` *(và vế `C2`)* không?** `09:347` nói buổi `C1`+`B5` do *"kế toán (hoặc owner)"* ngồi sửa thật; `11:86` nói *"đừng tính cú UAT là B5 ĐẠT"*. Phương án: ⓐ **⛔ không tính** — reason `UAT…` là *thử đường ghi*, ⛔ việc thật; giá: mốc B ở `1·1·3` cho tới khi kế toán ngồi thật · ⓑ tính — giá: mốc B **5/5** dựa trên một cặp ghép-bỏ ghép ròng 0. **BA đề xuất ⓐ.** — Vì sao WO vẫn làm được: `T1a`, `T2`, `T3` độc lập với Q1; chỉ `T1b` và `AC-2` chờ.
  - ✅ **owner 01/10: "còn lại như đề xuất" ⇒ ⓐ — cú UAT 01/10 *(`itl_id 27728`, actor `khanhcq@apero.vn`, reason bắt đầu "UAT 01/10")* ⛔ KHÔNG tính là người thật** cho `B4`/`B5` hay **bất kỳ** cổng *"người đã làm"* nào *(`QĐ-ITL-150 ⓐ`)*. ⇒ `T1b` mở.
- **Q2 — Có chạy `tools/dong_bo_so_song.py --ghi` không, và khi nào?** Chạy **hôm nay** ⇒ máy ghi *"mốc B 5 đạt · 0 · 0"* vào `09`, dashboard, bản vẽ — **sai**. **BA đề xuất:** chỉ chạy **sau** `T1a`+`T1b`, và người chạy phải sửa **câu** cạnh số *(công cụ chỉ sửa số — chính docstring của nó nói vậy)*. — Vì sao WO vẫn làm được: phiếu ⛔ cần `--ghi`.
  - ✅ **owner 01/10: như đề xuất** — chỉ chạy `--ghi` **SAU** khi bộ đếm mốc B đã loại sự kiện máy + loại UAT; **người chạy sửa cả câu cạnh số** *(`QĐ-ITL-150 ⓑ`)*. ⇒ thêm `T5`.
- **Q3 — Giá trị `hd`/`cdt1` máy suy ra từ một cú ghép TAY ghi là `sua_tay` *(`ghi_tay.py:686`–`697`)*. Đó là "người chốt" hay "máy gợi ý"?** Hệ quả: cổng `C8` *(`khop_owner`)* sẽ báo *"người đã chốt"* ở cú ghép thật đầu tiên dù người ⛔ gõ ô nào. Đây là câu nghiệp vụ *"con số trên màn đến từ đâu"* ⇒ owner. — Vì sao WO vẫn làm được: phiếu ⛔ chạm `ghi_tay.py`.
  - ✅ **owner 01/10: "Máy gợi ý"** *(`QĐ-ITL-149`)*. Spec: `BA-05` v0.32 `DD-I15 ⓓd` · `BA-10` v0.6 `DT-I14` · `BA-07` v3.4. Phần mã ⇒ **`WO-003`**, ⛔ phiếu này.
- **Q4 — Ai sở hữu** dashboard §1–§4, `09_MILESTONES`, `00_MASTER_INDEX` §8/§10, `_AUDIT_ALIGNMENT_ROADMAP.md`, `docs/ITL/_tools/**`, và **ai được chạy** `dong_bo_so_song --ghi` *(nó ghi vào `02_BA/Artifacts/` của BA)*? `10 §1` ⛔ giao ai. **BA đề xuất:** số **máy sinh** + `_tools/` ⇒ Dev; **câu văn** quanh số ⇒ BA; `10` lên v1.1 ghi rõ. — Vì sao WO vẫn làm được: `T4` là phần duy nhất chờ Q4.
  - ✅ **owner 01/10: như đề xuất** — `fls-ba` giữ câu văn dashboard §1–§4, `09_MILESTONES`, master §8/§10, `_AUDIT_ALIGNMENT_ROADMAP.md`, `_DOC_REWRITE_ROADMAP.md`; `fls-dev` giữ `tools/**` + `docs/ITL/_tools/**` và là **người chạy** `dong_bo_so_song --ghi`, kể cả khi nó ghi vào tệp của BA *(ngoại lệ có chủ đích — `10` v1.1 §6; `QĐ-ITL-150 ⓒ`)*. ⇒ `T4` mở.

## Rủi ro
1. Siết `_cong_moc_b` làm **ba** nơi ghim *(dashboard · `09` · bản vẽ 13)* đổi từ `4·1·0`/`5·0·0` sang `1·1·3` cùng lúc — đúng, nhưng ai đọc lướt sẽ tưởng **tụt**. `BG` phải nói rõ: *"thước sửa, ⛔ việc lùi"*.
2. Lọc theo **actor** là luật mới dễ vỡ lần thứ ba *(lần 1: `reason` 10/09; lần 2: `may@fls` 18/09)* — một tiến trình máy mới mang actor khác sẽ lại lọt. Khai hằng actor máy **một chỗ**, có bài ghim.
3. ⚠ **Thứ tự với `WO-003`:** `WO-003` thêm bài thử ⇒ số phép thử ghim trôi *(loại c)*. ⭐ **Làm `WO-003` TRƯỚC**, rồi phiếu này *(để `T5` chụp số **sau** cùng; `10 §6 ⓒ` cấm chạy `--ghi` lần hai để dọn đỏ của phiếu khác)*. Cũ: trong lúc chờ Q2, cổng `kiem_so_song` đỏ **mãi** ⇒ mọi `BG` của phiếu khác cũng mang đỏ. `BG` phải tách *"đỏ của WO này"* khỏi *"đỏ nền 38a/8b/1c"*.
   - ⭐ **01/10 tối:** `WO-003` vòng 1 trượt *(`KQ-005`)* ⇒ **mở lại vòng 2** *(`F-1`/`F-2`/`F-3` — thêm bài thử, cùng `ghi_tay.py`)*. Thứ tự: **`WO-003` vòng 2 → `KQ` ĐẠT → phiếu này** *(`T1a`…`T4` rồi `T5` sau cùng)*. Đo lại 01/10 tối trên kho thật: sự kiện `match`/`unmatch` = `may@fls` **2.219** + `khanhcq@apero.vn` **2** · `fls_pm_unlink` **1** ⇒ số `AC-1` *(`2` · `2.221`)* **đứng**; ba câu `T5` biết trước *(`09:147` · `dash:121` · `banve:1367`)* vẫn ở đúng dòng, vẫn in `4 · 1 · 0`.

## Nghiệm thu PO *(`fls-ba` · 2026-10-01 khuya)*

✅ **ĐÓNG.** `KQ-010` ĐẠT trọn *(**9/9** AC: `AC-1`…`AC-7`, `AC-1b`, `AC-2b`; ba lăng kính ⛔ `CHAN`/`NANG`)*. Đối chiếu lại với **ý owner**, ⛔ chỉ với chữ AC — và **đếm lại sổ thật một lần nữa** *(chỉ `SELECT`, 01/10 khuya)* chứ ⛔ tin số trong `KQ`:

| Ý owner *(nguyên văn)* | Đo lại *(sổ thật)* | Kết luận PO |
|---|---|---|
| `QĐ-ITL-150 ⓐ` — *"cú UAT 01/10 ⛔ KHÔNG tính là người thật"* cho mốc `B` hay **bất kỳ** cổng *"người đã làm"* | sự kiện `evt_type <> 'reason'` = **2.221** *(mẫu số ≠ 0)* = `match/may@fls` **2.219** + `match`/`unmatch` `khanhcq@apero.vn` **2** — cả 2 lý do bắt đầu `UAT 01/10` ⇒ **người thật = `0`**; `fls_pm_unlink` **1** = chính cú UAT ⇒ `B4` việc thật **0** | ✅ mốc `B` **`1 · 1 · 3`** nói đúng câu owner cần: ***chưa một kế toán nào bấm thật***. ⚠ Vế *"bất kỳ cổng"* **chưa trọn** — `C8` và `G-d` chưa loại UAT *(`KQ-010 F-2 ⓓ`)* ⇒ [`WO-011`](WO-011-thuoc-nguoi-ban-trang-va-anh-hieu-luc.md); ⛔ chặn đóng vì hôm nay cả hai đều **0** *(`fls_sua_tay` 0 · `hinh='T'` 1 = UAT, `G-d` vẫn là cổng đo tay)* |
| `QĐ-ITL-150 ⓑ` — `--ghi` chỉ **sau** khi bộ đếm đã loại máy + UAT; **người chạy sửa luôn câu cạnh số** | `BG-009` chạy `--ghi` sau `T1a`+`T1b`; `KQ-010` đọc **16** câu cạnh số ✅ | ✅ — ⚠ **một câu lọt**: chân trang bản vẽ 13 — `--ghi` đổi **dấu ngày** sang `01/10` mà câu *"10.030 dòng sổ … nhật ký vẫn 0 dòng"* đứng yên ⇒ thành khai *hôm nay* *(`F-4 ⓐ`)*. `fls-ba` đã sửa *(câu nay **trỏ** về thẻ có phép so)*; ⛔ mở lại phiếu |
| `QĐ-ITL-150 ⓒ` — câu văn ⇒ `fls-ba`, số máy sinh + `_tools/` ⇒ `fls-dev` | `KQ-010 F-4 ⓔ`: khối đính chính mốc 2 *(bản vẽ 13)* mang nhãn `fls-ba` mà chứa câu `fls-dev` thêm | ✅ — đã ghi lại nhãn đúng người viết |
| Rủi ro 1 — *"thước sửa, ⛔ việc lùi"* phải nói ra | `09:149` · `dash:121` · `banve:1367`–`1374` đều nói | ✅ |

**Bốn phát hiện `NHE` của `KQ-010`:** `F-1` *(lỗ bài thử, đã lấp bằng bài `kq010`)* — ghi nhận · `F-2` + `F-3` ⇒ [`WO-011`](WO-011-thuoc-nguoi-ban-trang-va-anh-hieu-luc.md) *(spec `09` v1.13 · `BA-14` v0.7)* · `F-4` — `fls-ba` sửa câu lượt này *(bản vẽ 13 ×4 chỗ · `09` `B1` + §7 dòng `B` · `FLS-Luong-va-Nut.html:317` · dashboard `6.-3`)*.

## Changelog
- 2026-10-01 · `fls-ba` · phát `WO-001` *(4 câu treo)*.
- 2026-10-01 · `fls-ba` · owner trả Q1–Q4 *(`QĐ-ITL-149`, `QĐ-ITL-150`)* ⇒ điền lời owner; mở `T1b`, `T4`; thêm `T5` *(`--ghi` + sửa câu cạnh số)*, `AC-2b`, `AC-6`, `AC-7`; spec `10` ⇒ v1.1. **Sẵn sàng cho Dev** — làm **sau** `WO-003`.
- 2026-10-01 tối · `fls-ba` · rà lại sau `c1fb250`…`5f4ae68`: phạm vi `T1a`…`T5` **đứng** *(số kho `AC-1` đo lại khớp)*; đính chính `AC-1b`/`AC-4` *(bài `KQ-002` vẫn `xfail strict` ⇒ mong `XPASS(strict)`, ⛔ "xanh")*; nền `kiem_so_song` **83** *(`KQ-005`)*; `BA-11` ⇒ v0.15 *(`INV-I08` ⛔ đổi)*; thứ tự: sau `WO-003` **vòng 2**.
- 2026-10-01 tối · `fls-ba` · sau `KQ-007` *(`WO-003` `DONG`)* ⇒ **làm NGAY**; phạm vi đứng; nền **1.949** phép thử · `kiem_so_song` **83** *(+1 nhóm version `BA-06` do lượt BA bump v4.8)*; `AC-4` đủ điều kiện *(3 bài `kq005` đã gỡ dấu)*.
- 2026-10-01 khuya · `fls-ba` · ✅ **nghiệm thu PO — `DONG`** theo `KQ-010` ĐẠT *(mục **Nghiệm thu PO**; đếm lại sổ thật: người thật **0**)*; `F-2`/`F-3` ⇒ `WO-011`; `F-4` sửa câu.
- 2026-10-01 tối · `fls-dev` · nhận @ `ee390cb` → làm `T1a`…`T5` → **`CHO_TEST`**, [`BG-009`](BG-009-ban-giao-wo-001.md) @ `6e98796` *(mốc B máy đếm `1 · 1 · 3`; `kiem_so_song` 84 ⇒ 0; bài `KQ-002` `XPASS(strict)` chờ `fls-test` gỡ dấu)*.
