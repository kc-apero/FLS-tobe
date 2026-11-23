# BG-006 — bàn giao `WO-003` **vòng 2** *(bỏ ghép đảo mọi lớp gợi ý · `bo_qua` chỉ giá trị người)*

| | |
|---|---|
| **Thuộc** | `WO-003` — ⭐ **vòng 2 của `WO-003`** *(mở lại theo [`KQ-005`](KQ-005-kiem-bg-004.md) TRƯỢT `AC-7`; vòng 1 = [`BG-004`](BG-004-ban-giao-wo-003.md))* |
| **Phát bởi** | `fls-dev` · 2026-10-01 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ **`5fbc29c`** *(đã đẩy — mã + bài thử + changelog)*; phiếu này nằm ở commit kế tiếp |
| **Spec đã đọc** | `BA-10` **v0.7** `DT-I14` · `BA-11` **v0.15** `INV-I22` · `BA-09` **v0.6** `SM-I06` `F-10`/`F-11` · `BA-05` **v0.33** `DD-I15 ⓓd` · `BA-06` v4.7 `:1174` *(dòng `Version` từng tệp khớp `WO-003` mục Vòng 2)* |

> **Một câu cho owner:** bỏ ghép nay rút **hết** gợi ý của máy trên dòng, kể cả gợi ý cũ nằm dưới một gợi ý mới hơn — ⛔ còn gợi ý "mồ côi" nổi lên lại; và hộp *"Đã bỏ ghép"* chỉ nói *"người đã gõ tay"* khi **người** thật sự gõ. Hôm nay **0** dòng thật dính *(đo `KQ-005`)*, ⛔ chạm kho thật.

```mermaid
flowchart LR
  B["Bỏ ghép"] --> Q["Đọc BẢNG GỐC fls_adjustment<br/>bút toán gắn 'match'<br/>CHƯA có bản đảo — MỌI LỚP"]
  Q --> D["Đảo từng cái<br/>nguon + value_before của CHÍNH lớp ấy"]
  D --> G[("fls_may_goi_y của dòng = {}")]
  D --> BQ["bo_qua = đọc fls_sua_tay SAU khi đảo<br/>chỉ giá trị NGƯỜI, ≤ 1 mục/ô"]
  X["⛔ vòng 1: lọc qua khung xem<br/>= chỉ lớp trên cùng"] -. "lớp dưới nổi lên lại" .-> G
```

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/repo/ghi_tay.py` | ⓔ `bo_moi_noi`: tập cần đảo = bút toán `fls_adjustment` gắn sự kiện `evt_type='match'` + `reversal_of IS NULL` + **`NOT EXISTS` bản đảo** — **⛔ còn** phép lọc qua khung xem `fls_may_goi_y` ∪ `fls_sua_tay` *(`DT-I14` v0.7 *Luật một câu*; nhánh 6 + 8 mọi lớp; nhánh 7 = `NOT EXISTS`)*. Bản đảo mang `nguon` và `value_before` **của chính dòng bị đảo** *(Rủi ro 2)*. ⓕ `bo_qua` dựng **trong cùng giao dịch, SAU khi đảo**: dòng khung xem `fls_sua_tay` mà bút toán ⛔ gắn `match`, trên ô dòng **từng** có bút toán `match` *(mọi vòng, đã đảo hay chưa)*; mục mang `nguon='sua_tay'`. Bút toán máy ⛔ bao giờ vào `bo_qua`. Chú thích thiết kế `ⓑ` đầu khối ghi đính chính |
| `fls/api/bang_tuyen.py` | `unmatch`: **bỏ** `fls_may_goi_y` khỏi bảng đọc — mã ⛔ còn đọc khung xem ấy. Bảng chạm cũ → mới: `fls_itl, fls_moi_noi, fls_pm_unlink, fls_queue_event, fls_adjustment, fls_journal, fls_sua_tay, fls_may_goi_y` → **`… fls_sua_tay`** *(⛔ `fls_may_goi_y`)*. `BANG_CHO_PHEP` giữ `fls_may_goi_y` *(`match`/`match-lo` vẫn đọc)*. Chứng: trả bản khai cũ ⇒ `soi_bang_tuyen` ⛔ `1 vi pham: … unmatch: bang khai ['fls_may_goi_y'] ma SQL ⛔ khong cham` |
| `tests/repo/test_wo003_vong2_bo_ghep_moi_lop_pg.py` | **mới**, 6 bài — `AC-14` ⓐⓑⓒ *(ba lớp)* + Rủi ro 2 · `AC-14 ⓓ` *(⛔ đảo hai lần)* · nhánh 8 mọi lớp *(bút toán ghép `sua_tay` cũ dưới giá trị người)* · `bo_qua` ≤ 1 mục/ô, chỉ người · `bo_qua` ⛔ khai ô chưa từng có gợi ý · `AC-16` ca trộn |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` | dòng 2026-10-01 vòng 2 |

⛔ **Không** đổi schema · ⛔ **không** chạm `tests/nghiem_thu/**` · ⛔ **không** chạy `dong_bo_so_song --ghi` · ⛔ đổi `may_ghep.suy_hd_cdt1` *(phạm vi `(g)`)* · ⛔ đổi khung xem / `tools/goi_y_lai.py`. Bài cũ ghim luật cũ: grep `bi goi y moi hon` / `con_hieu_luc` / `dang_dung` trong `tests/` ngoài `nghiem_thu/` ⇒ **0** bài ghim chữ `vi_sao` cũ; các bài `bo_qua` cũ *(`test_bo_moi_noi_pg` ×2, `test_wo003…` ×1)* **xanh nguyên** ⇒ ⛔ phải viết lại bài nào.

## Cổng *(kết quả nguyên văn, `PYTHONUTF8=1`, `PG_DSN=postgresql://fls:fls@localhost:5433/fls`, cây làm việc = `5fbc29c`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `3 failed, 1941 passed, 1 xfailed in 266.50s (0:04:26)` — **đúng 3** bài đỏ, cả 3 là `[XPASS(strict)]` liệt kê dưới *(đỏ có chủ ý)*; `1 xfailed` = `test_kq002_moc_b_khong_dem_may_la_nguoi.py::test_su_kien_cua_MAY_tu_ghep_KHONG_lam_cong_moc_B_nhay` *(`WO-001`, **vẫn** `xfail`)* |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 83 lech/khong-do-duoc`. **Nền đo lại** trên chính `38a6b08` *(`git stash -u`, cùng giờ)*: **`83`** ⇒ **+0 nhóm mới**. Vòng 2 chỉ dời **giá trị máy đo** trong các nhóm đã lệch, toàn **loại (c)**: số phép thử `1939→1945`, `1736→1742`; dòng mã `24.961→24.982`; repo `522→528` tệp / `6.982→6.999` dòng; api `3.892→3.896` dòng *(diff nguyên văn hai bản in: 17 dòng, chỉ các số này)*. ⛔ Không chạy `dong_bo --ghi` *(`WO-001 T5`)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (94 file, 1166 bang, 631 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(đo trước khi thêm phiếu này)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 15/19 khop · 4 lech   (da do 19/19 phep)` · `✅ C8  ⭐ NGUOI da chot o nao chua` · `⛔ ⛔ CONG NO: · ⛔ khoi trong lo trinh LECH voi ban sinh lai` — **y nền** `KQ-005` |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ **CHƯA CHẠY bản ghi** — phiếu ⛔ chạm schema *(`git diff 38a6b08 -- fls/db` rỗng)*, và lệnh ấy áp lên kho thật. Thay: `--status` ⇒ mới nhất `da ap 0026_dien_giai_sao_ke` · `python -m fls.db.pg_verify` ⇒ `khop: 25 bang/view dung nhu khai bao` |

### ⭐ 3 bài `XPASS(strict)` — `fls-test` gỡ dấu `xfail`
1. `tests/nghiem_thu/test_kq005_bo_ghep_dao_ca_goi_y_chong.py::test_ghep_TAY_roi_goi_y_lai_CHONG__bo_ghep_KHONG_de_goi_y_mo_coi`
2. `tests/nghiem_thu/test_kq005_bo_ghep_dao_ca_goi_y_chong.py::test_dong_MAY_ghep_goi_y_CHONG_hai_lop__bo_ghep_ve_0`
3. `tests/nghiem_thu/test_kq005_bo_qua_chi_la_gia_tri_nguoi.py::test_ghep_BO_ghep_lai_BO__khong_ai_go_tay__bo_qua_RONG`

`pytest tests/nghiem_thu -rxX` ⇒ `3 failed, 9 passed, 1 xfailed` *(3 = ba tên trên, `XPASS(strict)`; xfail = bài `WO-001`)*.

## Bằng chứng từng AC
⭐ Đỏ **trước** khi vá *(mã `38a6b08`)*: `--runxfail` hai tệp `kq005` ⇒ `3 failed, 2 passed`; bài mới ⇒ `3 failed, 3 passed` *(đỏ đúng lý do: `_chua_dao == 2` sau bỏ ghép · bút toán ghép cũ lớp dưới ⛔ bị đảo `but_toan_dao == []` · `bo_qua` có `('cdt1','may_goi_y')`, `('hd','may_goi_y')`; 3 bài xanh trên mã cũ là bài **ghim** — `AC-14 ⓓ`, `AC-16`, ô chưa từng gợi ý)*. Chiều ĐỎ sau vá chứng bằng kịch bản phá-nguồn → chạy → trả nguyên *(`scratchpad/chung_minh_do_v2.py`, mỗi mẫu khớp **đúng 1** lần, kiểm byte sau khi trả)* — nguyên văn cột cuối.

| AC | Bằng chứng của Dev | Chiều ĐỎ đã chứng |
|---|---|---|
| AC-13 *(e)* | `pytest tests/nghiem_thu/test_kq005_bo_ghep_dao_ca_goi_y_chong.py --runxfail` ⇒ **`3 passed in 1.28s`**; chạy thường ⇒ **2** `XPASS(strict)` *(tên 1, 2 trên)* | trả phép chọn về khung xem *(`se_dao ∩ {adj_id ∈ fls_sua_tay ∪ fls_may_goi_y}`)* ⇒ **`2 failed, 1 passed`** — đúng 2 bài-đỏ, đối chứng xanh |
| AC-14 *(e)* | `test_wo003_vong2…::test_BA_lop_goi_y_chong__bo_ghep_dao_CA_BON__moi_cai_DUNG_mot_ban_dao`: ⓐ trước bỏ `_chua_dao == 4` *(mẫu số ≠ 0; khung xem chỉ trả 2)* · ⓑ sau bỏ `== 0`, `fls_may_goi_y == {}`, `but_toan_dao` 4 · ⓒ mỗi gợi ý **đúng 1** bản đảo · Rủi ro 2: `value_before` các bản đảo = `["C-1","HD-A","HD-B","HD-C"]` · `bo_qua == []`. ⓓ `::test_ghep_BO_ghep_lai_BO__KHONG_bao_gio_dao_HAI_lan`: 4 gợi ý, **0** cái ≥ 2 bản đảo, mỗi cái đúng 1 | ⓑ chọn theo khung xem ⇒ **`1 failed`** · ⓓ bỏ `NOT EXISTS` *(giữ `reversal_of IS NULL` như vòng 1)* ⇒ **`1 failed`** *(bút toán vòng một bị đảo hai lần)* |
| AC-15 *(f)* | `pytest tests/nghiem_thu/test_kq005_bo_qua_chi_la_gia_tri_nguoi.py --runxfail` ⇒ **`2 passed in 1.26s`**; chạy thường ⇒ **1** `XPASS(strict)` *(tên 3)*. Thêm: `::test_bo_qua_moi_O_nhieu_nhat_MOT_muc_va_CHI_gia_tri_nguoi` *(2 vòng ghép + người gõ 2 lần ⇒ đúng `[("hd","sua_tay","HD-NGUOI-2")]`, ⛔ giao với `but_toan_dao`)* · `::test_bo_qua_KHONG_khai_o_ma_dong_CHUA_tung_co_goi_y` | dựng lại `bo_qua` từ *mọi bút toán `match` ngoài tập đảo* *(mã `48fb68f`)* ⇒ **`1 failed, 1 passed`** — đúng bài-đỏ, đối chứng xanh |
| AC-16 *(g)* | `::test_ca_TRON_dong_rong_hd_va_dong_co_hd__goi_y_gia_tri_co` — N = 2 *(X `hd=""`, Y `hd='HD-Y'`, cả hai `cdt1='C-1'`)* qua `ghep_lenh` thật ⇒ `fls_may_goi_y == {hd: HD-Y, cdt1: C-1}`, `hd ∉ khong_suy_duoc` | bỏ `gt.discard("")` ở `may_ghep.suy_hd_cdt1` ⇒ **`1 failed`** |
| AC-17 | bảng Cổng: **đúng 3** đỏ = 3 `XPASS(strict)` · bài `WO-001` **vẫn** `xfail` · lint `9 kept, 0 broken` · `soi_bang_tuyen` 40/40 *(bảng chạm `unmatch` cũ → mới ở mục Đã đổi)* · thuyết minh 31/31 | — |
| AC-18 | `kiem_so_song`: nền **83** *(đo lại trên `38a6b08`, = `KQ-005`)* ⟷ nay **83** ⇒ **0** nhóm mới; các giá trị dời đều loại (c) — liệt kê ở bảng Cổng. ⛔ chạy `dong_bo --ghi` | — |

⭐ Bài thêm ngoài AC: `::test_but_toan_ghep_CU_sua_tay_o_LOP_DUOI_gia_tri_nguoi__van_DAO__nguoi_NGUYEN` *(`DT-I14` nhánh 8 "bất kể lớp")* — đỏ trên `38a6b08` *(`but_toan_dao == []`, bút toán cũ còn nằm trong `bo_qua` với `vi_sao` "khong con hieu luc")*, xanh sau vá; giá trị người còn nguyên, bản đảo `nguon='sua_tay'`, `bo_qua == [("hd","sua_tay")]`.

`AC-1`…`AC-12` ⛔ đo lại *(WO: chỉ đo lại khi vòng 2 làm chúng đổi)*. Vòng 2 chạm `bo_moi_noi` ⇒ các bài `AC-7` vòng 1 *(`test_wo003…::test_bo_ghep_*` ×3, `test_bo_moi_noi_pg` 12 bài)* chạy lại trong lượt pytest toàn bộ: **xanh**.

## Kho thật
- `KHONG_CHAM`. Mọi bài chạy trên kho TEST `fls_test` *(`dsn_test()`, `run_id` `NAP-2000-…`)*. ⛔ Không khởi động máy nào *(8088 vẫn chỉ đọc, ⛔ dựng 8099 — vòng 2 ⛔ chạm màn)*; ⛔ `--cho-ghi`.

## Cách chạy để xem
- ⛔ Vòng 2 ⛔ chạm màn *(`fls/web/` ⛔ đổi)*. Hộp *"Đã bỏ ghép"* của `F01` *(`man_f01.js::_bao_bo_ghep`)* đọc `bo_qua` ⇒ câu *"người đã gõ tay"* nay chỉ hiện khi có giá trị người.

## Dev tự thấy còn yếu
1. **`bo_qua` nay đọc SAU khi đảo** *(trong cùng giao dịch)* — khác vòng 1 *(đọc trước)*. Lý do: nếu một bút toán ghép `sua_tay` **cũ** nằm **trên** giá trị người thì trước khi đảo khung xem `fls_sua_tay` trả bút toán cũ ấy *(bị loại vì gắn `match`)* ⇒ giá trị người bên dưới **lọt khỏi** `bo_qua`; đọc sau khi đảo thì nó hiện. Định nghĩa `DT-I14` ⛔ nói *"khung xem đọc lúc nào"* — tôi chọn đọc sau vì đúng nghĩa *"cái máy ⛔ rút"*. Ca này kho thật **0** *(`sua_tay` gắn `match` chưa đảo = 0 — `WO-003` Dữ liệu vòng 2)*; ⛔ có bài riêng cho đúng ca *"bút toán cũ ở TRÊN người"* *(bài nhánh 8 dựng ca ở DƯỚI)*.
2. **Bỏ ghép nay đảo cả bút toán ghép `sua_tay` cũ ở LỚP DƯỚI giá trị người** *(nhánh 8 "bất kể lớp")*. Final ⛔ đổi *(khung xem vẫn trả lớp người — bài chứng)*, nhưng nhật ký nhận thêm một dòng `value_after NULL`, `value_source='sua_tay'`, actor người bấm bỏ ghép — ai đọc nhật ký theo ô có thể tưởng *"ô bị xoá"*. Đúng spec; ⛔ chạm ai hôm nay *(0 dòng)*.
3. `bo_qua` của vòng 1 có khoá `vi_sao` hai kiểu; nay **chỉ còn** kiểu *"gia tri NGUOI…"* *(chữ cuối đổi "goi y cua phep ghep (moi lop) thi da dao")*. Màn chỉ đọc `field`/độ dài *(grep `bo_qua` trong `fls/web/`: **2** dòng, `man_f01.js:421`–`:425`)* — ⛔ dò hết người đọc ngoài repo *(tài liệu `BA-07` ví dụ thân trả về có thể còn chữ cũ — ⛔ grep `02_BA` vì ⛔ phải tệp của tôi)*.
4. Ba bài mới **xanh ngay trên mã cũ** *(`AC-14 ⓓ`, `AC-16`, ô chưa từng gợi ý)* — chúng là bài **ghim**: đỏ chỉ chứng được bằng phá mã **mới** *(bỏ `NOT EXISTS`, bỏ `discard`)*, ⛔ bằng mã cũ. Đã chứng cả ba hướng phá ở bảng AC *(trừ bài "ô chưa từng gợi ý" — ⛔ chứng đỏ riêng)*.
5. ⚠ Lệch nhỏ **giấy** *(⛔ chặn, ⛔ mở `HOI`)*: `BA-10` v0.7 `:82` ghi bài ghim ca trộn là *"`WO-003` vòng 2 `AC-15`"*, nhưng `WO-003` khai ca trộn là **`AC-16`** *(`AC-15` = `bo_qua`)*. Tôi theo `WO` — BA xem lại.
6. `INV-I22 ⓑ` *(toàn sổ: 0 gợi ý chưa đảo trên dòng ⛔ còn mối nối)* — vẫn ⛔ có cổng sổ chạy định kỳ *(spec tự khai "chỉ bài thử ⇒ đứng bằng mã")*; vòng 2 ⛔ thêm *(ngoài bảng TRONG)*.
