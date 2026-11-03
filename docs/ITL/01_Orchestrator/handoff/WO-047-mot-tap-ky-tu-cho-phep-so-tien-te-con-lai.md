# WO-047 — Một tập ký tự trắng cho **ba** phép so / gom tiền tệ còn sót: chiều ngược `ung_vien_pm` · tô số tiền `khoa_bang_chung` · đếm lệnh chưa có tiền theo tiền tệ

| | |
|---|---|
| **Trạng thái** | `MO` *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* · ưu tiên **THẤP** — nhận **sau** [`WO-045`](WO-045-luot-tai-moi-nhat-moi-man-va-xem-them-chi-doc.md) |
| **Phát bởi** | `fls-ba` · 2026-10-05 |
| **Nhận** | `fls-dev` |
| **Vòng** | `1` |
| **Thứ tự với phiếu khác** | **Sau** [`WO-042`](WO-042-doi-chip-khi-dang-tai-va-mot-tap-ky-tu-trang.md) *(✅ `DONG` 05/10 — phiếu này đứng trên hằng `TAP_TRANG_TIEN_TE` + `ma_tien_te` của nó, `fls/canon/tien_te.py`)* · **sau** `WO-045` *(CAO)* · **trước** [`WO-015`](WO-015-so-actor-phu-moi-bang-va-luat-uat-ascii.md) + [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) — lý do ở **Vì sao** |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B`** *(ghép PM ↔ tiền)* — chiều ngược `ung_vien_pm` là danh sách lệnh trong **hộp ghép của lằn *Theo dòng tiền*** `F01` *(`_drawer_ghep`)*: kế toán mở một dòng tiền, máy đưa lệnh nào cùng tiền tệ. `khoa_bang_chung` là chữ **tô sáng** trong hộp ấy và thẻ lệnh `F01G`.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ xoá thêm; phiếu này đóng nốt **một luật** của `WO-042 (c)` — hôm nay một lệnh `curr` = `' vnd '` **có** trong rổ, chiều thuận và cửa ghi nhận cặp ấy *(`KQ-046` `AC-10` ③ `POST /match` ⇒ `200`)*, nhưng **⛔ hiện** ở chiều ngược ⇒ máy nói hai điều khác nhau về cùng một cặp. `QĐ-ITL-27`: kiểm soát nằm trong máy ⇒ máy ⛔ được tự mâu thuẫn.
- ⭐ **Vì sao THẤP** *(PO)*: sổ thật **0** ca *(`fls_pm_line.curr` chữ thường / ký tự trắng ở mép / `U+00A0` / `U+FEFF` / `U+3000` / `U+0085` **0 / 276.028** · `fls_itl.curr` **0 / 8.387** — `fls-ba` chỉ `SELECT` 05/10)* ⇒ hôm nay ⛔ con số nào, ⛔ danh sách nào đổi; sửa vì **một luật**, ⛔ vì báo động.
- ⭐ **Vì sao trước `WO-015` / `WO-023`** *(cùng THẤP)*: ⓐ nhỏ nhất *(**3** chỗ, một hằng có sẵn)*; ⓑ cùng luật Dev vừa làm ở `WO-042` — làm ngay khi còn nóng rẻ hơn đọc lại; ⓒ gỡ **1** `xfail(strict)` đang treo trong `pytest` *(`kq046::test_F1_*`)*. ⛔ Chen trước `WO-045` — `WO-045` ① đứng sát một cú **GHI**.
- ⭐ **Vì sao ⛔ gom vào `WO-045`**: `WO-045` là **JS màn** *(lượt tải)*, phiếu này là **SQL + Python** cửa đọc — khác lớp, khác bài thử *(kho TEST ↔ DOM)*; gom là làm `WO-045` *(đã 13 AC)* phình thêm một lớp mà rủi ro #2 của nó đã cảnh báo.

## Căn cứ
- [`KQ-046`](KQ-046-kiem-bg-044.md) *(`fls-test` 05/10, ✅ ĐẠT `WO-042` 12/12)* — **`F-1` `NHE`**: `fls/repo/doc_bao_cao.py:309` · `:310` · `:317` *(`_SQL_UNG_VIEN`)* vế lệnh `upper(l.curr)` **trần**, vế dòng tiền `s.cur = ma_tien_te(so.curr)` *(`:377`)* ⇒ kho TEST, hàm thật: `' vnd '` · `U+00A0`＋`VND` · `U+FEFF`＋`VND` · `VND`＋`U+0085` · `U+3000`＋`VND` **5/5** ⛔ có mặt ở bậc nào. Có từ `0f6f054`. ⚠ Cùng lớp: `do_mau_so.py:297`. Bài `xfail(strict)` **`tests/nghiem_thu/test_kq046_chieu_nguoc_ung_vien_pm_mot_tap.py::test_F1_chieu_nguoc_ung_vien_pm_BANG_ma_tien_te`** ＋ mỏ neo `::test_CANH_chieu_nguoc_ca_thuong_vao_BAC_TIEN`.
- `fls-ba` kiểm kê lại 05/10 *(`Đ1` — grep `fls/` + `tools/`; bảng đủ ở `BA-07` v3.12 `§4g`)*: thêm **`man_ghep.py:631`** `khoa_bang_chung` *(`str(uv.get("curr")) == str(lenh.get("curr"))` — ⛔ chuẩn hoá gì; gọi từ `xu_ly.py:740` · `:903`)* — `KQ-046` ⛔ nêu.
- **`BA-07` v3.11** *(luật `TAP_TRANG_TIEN_TE` — "mọi phép so tiền tệ")* · **`QĐ-ITL-62`** *(một tiền tệ là **một** mã sau chuẩn hoá)* · **`QĐ-ITL-27`**.
- Quyết: **`fls-ba` trong thẩm quyền spec** *(danh sách chỗ áp một luật đã có — ⛔ đổi luật, ⛔ đổi sổ, ⛔ tuyến mới, ⛔ khoá cửa mới)*. ⛔ câu nghiệp vụ.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/07_API_CONTRACT.md` | ⭐ **§4g đoạn v3.12** *(bảng năm lớp ⓐ…ⓔ — chỗ nào áp, chỗ nào ngoài + lý do)* · đoạn v3.11 *(bảng luật `TAP_TRANG_TIEN_TE`)* | ⭐ **v3.12** |
| `01_Orchestrator/handoff/KQ-046-kiem-bg-044.md` | *Phát hiện* `F-1` + bảng *Bài thử mới* *(`kq046`)* | — |
| `fls/canon/tien_te.py` | `TAP_TRANG_TIEN_TE` · `ma_tien_te` *(chú thích đầu tệp — vì sao một chỗ)* | `db0adae` |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| ⭐ **(a) chiều ngược `ung_vien_pm`** — `doc_bao_cao.py` `_SQL_UNG_VIEN` `:309` · `:310` · `:317`: vế lệnh `upper(btrim(l.curr, %(tap)s))`, tham số `tap` **từ hằng** *(như `lenh_cho.py:225` · `:232`; ⛔ chuỗi gõ lại trong SQL)*. Ba chỗ trong một câu ⇒ **một** biểu thức *(vd. cột `cur_l` trong `q` hoặc CTE)* — cách viết là việc Dev | ⛔ đổi `DK_BAC_MA` · ⛔ đổi thứ tự bậc / `BAC` · ⛔ đổi `ung_vien_itl` *(chiều thuận — đã đúng ở `WO-042`)* |
| **(b) tô số tiền `khoa_bang_chung`** — `man_ghep.py:631`: điều kiện ⓑ *"cùng đơn vị"* = `ma_tien_te(uv) == ma_tien_te(lenh)` **và** mã ⛔ rỗng *(cùng luật màn `man_f01_ghep.js:227`)*. ⚠ Đổi **chủ ý**: hai vế cùng thiếu tiền tệ hôm nay `'None' == 'None'` ⇒ tô; sau phiếu ⇒ ⛔ tô | ⛔ đổi điều kiện ⓐ *(số chứng từ)* · ⛔ đổi tách tên `_TACH_TEN` / `TU_RAC` |
| **(c) đếm lệnh chưa có tiền theo tiền tệ** — `do_mau_so.py:297` `_SQL_PM_CHUA_THEO_TE`: `upper(btrim(COALESCE(l.curr, '?'), %(tap)s))` *(nhóm `'?'` giữ nghĩa: thiếu tiền tệ)*; `do_phu_pm` truyền tham số | ⛔ đổi khuôn trả `do_phu_pm` · ⛔ đổi `tools/do_mau_so.py` |
| **(d) cổng một chỗ** — mở rộng bài quét `AC-9` `WO-042` *(`tests/`)*: ngoài chú thích, trong `fls/`: `upper(` / `lower(` trên cột `curr` mà ⛔ bọc `btrim(…, %(tap)s)` ⇒ **0**; phép so `==` / `!=` trên `get("curr")` / `["curr"]` mà ⛔ qua `ma_tien_te` ⇒ **0**; danh sách cho phép **khai tên + lý do** *(lớp ⓒ ⓓ `BA-07` v3.12)* | ⛔ quét `tools/` *(lớp ⓔ — ngoài)* |
| **(e) Bài thử** `tests/api/**` / `tests/repo/**` — một bài mỗi AC, **chứng minh ĐỎ trước** trên `HEAD` khi nhận; hàm thật trên **kho TEST** *(`assert current_database() = 'fls_test'`)* | ⛔ sửa / gỡ dấu `tests/nghiem_thu/**` *(`fls-test` gỡ ở `KQ` — `kq046::test_F1_*` sẽ `XPASS(strict)` đúng ý)* |
| — | ⛔ **lớp ⓒ** xếp / gom / lọc hàng chờ *(`doc_bao_cao.py:507`…`:584` · `lenh_cho.py:111`…`:139` · `:309` — `PARTITION BY curr` `QĐ-ITL-58`, khứ hồi chip ⇄ lọc tự nhất quán; sổ thật 0 ca ⇒ nợ ghi ở `BA-07` v3.12)* · ⛔ lớp ⓓ `man_f01.js:60` · ⛔ lớp ⓔ `tools/demo_dong.py` · ⛔ chuẩn hoá `curr` lúc nạp *(ghi sổ)* · ⛔ đổi phép chữ hoa |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(a · chiều ngược)* | Kho TEST, **hàm thật** `ung_vien_pm`: dòng tiền `VND` số tiền `X` ＋ lệnh số tiền `X` ⛔ mã khớp, `curr` = `x`＋`vnd`＋`x` với **mỗi** `x` ∈ `TAP_TRANG_TIEN_TE` *(30)* ＋ ca `' vnd '` ⇒ lệnh có mặt, bậc **`tien`** — **31 / 31**; `x` = `U+200B` ⇒ lệnh ⛔ ở bậc `tien`/`gan_tien`/`cung_tien_te` *(giữ nguyên — ngoài tập)*. `pytest --runxfail tests/nghiem_thu/test_kq046_*::test_F1_*` ⇒ passed | bài `tests/` + `--runxfail` | giữ `upper(l.curr)` trần ⇒ **ĐỎ** *(`KQ-046`: 5/5)*; thêm `U+200B` vào tập ⇒ **ĐỎ** |
| AC-2 *(a · hai chiều cùng nói)* | Cùng 32 cặp *(lệnh, dòng tiền)* của AC-1: *"cùng tiền tệ"* theo chiều thuận `ung_vien_itl` **⇔** theo chiều ngược `ung_vien_pm` ⇔ cửa ghi `ghep_lenh` ⛔ trả `KhacTienTe` — **32 / 32** đồng ý | bài kho TEST *(cửa ghi: dựng ca, ghi kho **TEST**)* | một trong ba vế dùng tập khác ⇒ **ĐỎ** |
| AC-3 *(b · tô số tiền)* | `khoa_bang_chung(lenh, uv)` cùng số tiền: `(' vnd', 'VND')` ⇒ có số tiền · `(U+FEFF＋'VND', 'VND')` ⇒ có · `('VND', 'USD')` ⇒ ⛔ · `(None, None)` ⇒ ⛔ · `('', '')` ⇒ ⛔ · `('VND', None)` ⇒ ⛔ | bài đơn vị | mã khi nhận ⇒ **ĐỎ** ở `(' vnd', 'VND')` và `(None, None)` |
| AC-4 *(c · đếm theo tiền tệ)* | Kho TEST, **hàm thật** `do_phu_pm`: lệnh chưa có tiền `curr` = `'VND'` · `' VND'` · `U+00A0`＋`VND` · `NULL` ⇒ nhóm `VND` đếm **3**, nhóm `'?'` đếm **1**, ⛔ nhóm `' VND'` | bài kho TEST | giữ `upper(COALESCE(…))` ⇒ **ĐỎ** *(hai nhóm `VND`)* |
| AC-5 *(d · một chỗ)* | Bài quét: ba mẫu trong `BA-07` v3.12 ngoài danh sách cho phép ⇒ **0**; danh sách cho phép mỗi mục có **lý do**. Bài tự chứng: chèn `upper(l.curr) = s.cur` và `str(a.get("curr")) == str(b.get("curr"))` vào bản sao một tệp ⇒ bắt **2** | bài quét | quét chỉ `btrim(i.curr` *(như `AC-9` `WO-042`)* ⇒ bài tự chứng **ĐỎ** |
| AC-6 *(sổ thật ⛔ đổi)* | **Sổ thật CHỈ ĐỌC** *(`noi_chi_doc(dsn_that())`, cùng ảnh — in `run_id`)*: ⓘ `ung_vien_pm` mã khi nhận *(worktree)* = mã mới trên **200** `itl_id` đầu theo `itl_id` của dòng tiền chưa nối *(cùng danh sách `pm_line_id`, cùng `bac`, cùng thứ tự — in mẫu số)*; ⓘⓘ `do_phu_pm` nhóm tiền tệ trước = sau; ⓘⓘⓘ `dem_theo_ro` trước = sau *(6 khoá)* | phép đo chỉ đọc *(kịch bản trong `BG`)* | mẫu số `0` ⇒ **ĐỎ** |
| AC-7 *(Chrome — hộp ghép)* | **8099** `--cho-ghi` trỏ **kho TEST**, chuột thật 1440×900: lằn *Theo dòng tiền* ▸ mở dòng tiền ca AC-1 *(lệnh `' vnd '`)* ⇒ lệnh hiện trong hộp ở bậc tiền, số tiền **tô** *(`khoa_to`)*. **8088 sổ thật chỉ đọc**: mở **3** dòng tiền bất kỳ ⇒ danh sách = thân cửa `/queue/{itl_id}/pm-candidates` cùng lượt; **0** `POST`; console **0** lỗi | Chrome CDP | — |
| AC-8 | Cổng `CLAUDE.md`: `pytest` **0** đỏ ngoài `xfail(strict)` đã khai ＋ đúng **1 `XPASS(strict)`** `kq046::test_F1_*` *(đúng ý — `fls-test` gỡ dấu)*; 3 `kq021` vẫn `xfail` · `lint-imports` **9 / 0** · `soi_bang_tuyen` **40** *(⛔ tuyến mới)* · `kiem_thuyet_minh` khớp · `kiem_tai_lieu` · `khop_owner --kiem` · `kiem_so_song` tách **nền đầu phiếu** ⟷ đỏ mới loại (c), bảng **cộng ra đúng tổng**; ⛔ `dong_bo --ghi` | lệnh + `BG` | — |

## Màn hình *(chạm UI — gián tiếp, qua cửa đọc)*
- Thiết kế: ⛔ đổi — `02_BA/Artifacts/` ⛔ chạm, ⛔ token, ⛔ lớp CSS, ⛔ chữ. Màn chỉ **nhận** thêm lệnh / thêm tô ở ca biên.

| Trạng thái | `F01` hộp ghép lằn *Theo dòng tiền* *(`_drawer_ghep`)* |
|---|---|
| tải | ⛔ đổi |
| rỗng | ⛔ đổi — nhưng một dòng tiền có lệnh cùng tiền tệ mang ký tự trắng ở mép ⛔ còn rơi vào *"rỗng"* |
| lỗi | ⛔ đổi |
| mất kết nối | ⛔ đổi |
| có dữ liệu | lệnh có `curr` mang ký tự trong tập ở mép xếp **cùng** bậc với lệnh `VND` sạch; số tiền tô theo `ma_tien_te` |

## Dữ liệu
- Bảng/cột chạm: **⛔ bảng nào** — chỉ **đọc** `fls_pm_line.curr` / `fls_itl.curr` qua cửa có sẵn *(`/queue/{itl_id}/pm-candidates` · `itl-candidates` · `do_phu_pm`)*. ⛔ tuyến mới, ⛔ khoá mới.
- Ghi kho THẬT: **`KHONG`**. Máy **8088** **CHỈ ĐỌC** *(chỉ `GET` cho `AC-7`)*. Mọi cú ghi *(dựng ca `AC-1`/`AC-2`/`AC-4`/`AC-7`)* trên **kho TEST** qua **8099** / bài thử.
- Số dòng sổ thật đổi *(đã đếm — `fls-ba` 05/10, chỉ `SELECT`)*: **0** — `fls_pm_line.curr` lệch chuẩn ở mép / chữ thường **0 / 276.028** · `fls_itl.curr` **0 / 8.387** *(mẫu số ≠ 0 — `Đ3`)* ⇒ ⛔ danh sách nào, ⛔ con số nào đổi. ⇒ Báo động hiếm: ⛔ áp.

## Nền khi nhận *(`fls-ba` chép 05/10 — Dev đo lại ở cổng vào, ⛔ tin)*
| Cổng | Nền | Nguồn |
|---|---|---|
| git | `origin/feat/p2-oracle-parity` — commit giấy `fls-ba` phát phiếu này *(sau `47e9fa4` `KQ-046`)*; mã `fls/**` cuối = `db0adae` *(`WO-042`)* ⇒ ⚠ **sau `WO-045`** nền đổi — đo lại khi nhận | `git log` |
| `pytest` | **`2302 passed, 4 xfailed`** *(`KQ-046`; 4 = 3 `kq021` ＋ `kq046::test_F1_*`)* ⇒ sau phiếu: `kq046::test_F1_*` thành `XPASS(strict)` | `KQ-046` |
| `kiem_so_song` | **55** *(`KQ-046`)*; sau `WO-045` — đo lại | `KQ-046` |
| version spec | `BA-07` **v3.12** | header tệp |
| sổ thật | `/ro` *(`KQ-046` `AC-11`, ảnh `NAP-2026-10-02-PMA07ED283`)*: `may` **184** · `nguoi` **616** · `khong` **801** · `tu_chung` **64** · `tong` **1.601** · `nguoi_khac_tien_te` **84** | `KQ-046` |

## Câu còn treo
- ⛔ câu mới cho owner. `Q-FX-1` *(84 lệnh trả bằng tiền tệ khác)* vẫn treo — ⛔ chặn: phiếu này ⛔ đổi luật *"khác tiền tệ"*, chỉ đổi **cách đọc mã** cho ba chỗ còn sót.
- Lớp ⓒ *(xếp / lọc hàng chờ theo `curr` thô)* là **nợ ghi** — mở phiếu khi sổ thật có ca đầu tiên *(hôm nay 0)*; ⛔ chặn.

## Rủi ro
1. **Ba chỗ trong một câu SQL** *(`:309` · `:310` · `:317`)* — sửa hai bỏ một là hai tập trong một câu *(đúng lỗi `F-1`)*; `AC-1` đo qua **hàm thật** cả `WHERE` lẫn `CASE` *(lệnh phải **có mặt** và **đúng bậc**)*.
2. **`khoa_bang_chung` đổi chủ ý ca `(None, None)`** — bài cũ có thể ghim *"tô"* cho ca ấy ⇒ đổi bài theo `BA-07` v3.12 *(`tests/` — Dev sở hữu)*, ⛔ sửa `tests/nghiem_thu/**`.
3. **`do_phu_pm` nuôi `kiem_so_song`** *(`tools/do_mau_so.py --json`)* — sổ thật 0 ca ⇒ số ⛔ đổi; nếu `kiem_so_song` đổi thì đó là **lỗi**, ⛔ chạy `dong_bo --ghi` để che.

## Changelog
- 2026-10-05 · `fls-ba` · phát **`WO-047`** `MO` từ nghiệm thu PO `WO-042` + xếp `KQ-046 F-1`; kiểm kê lại ⇒ thêm `man_ghep.py:631` *(`KQ-046` ⛔ nêu)*; spec `BA-07` **v3.12** *(`§4g` bảng năm lớp)*. Ưu tiên **THẤP**, thứ tự `WO-045` → `WO-047` → `WO-015` → `WO-023`.
