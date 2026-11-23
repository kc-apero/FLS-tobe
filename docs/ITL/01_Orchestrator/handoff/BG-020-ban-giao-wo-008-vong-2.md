# BG-020 — bàn giao `WO-008` *(vòng 2)*

| | |
|---|---|
| **Thuộc** | `WO-008` **vòng 2** — năm ca của nút `Bỏ gán` trên màn ghép *(`KQ-019` `F-1`…`F-4`; mục **Vòng 2** cuối phiếu)* · vòng 1 là [`BG-017`](BG-017-ban-giao-wo-008.md) |
| **Phát bởi** | `fls-dev` · 2026-10-02 tối |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ **`9dae3ac`** *(mã `man_f01_ghep.js` + bài vòng 1 viết lại + 17 bài mới + `WO` nhận)* → **`dd7c5bb`** *(+1 bài: chùm **và** `bo_qua`)* — **đã đẩy**. Phiếu này + changelog `03_Dev` + `WO` `CHO_TEST` + nhật ký + `README` ở commit kế tiếp *(⛔ chạm `fls/`, `tests/`)* |
| **Spec** | `BA-06` **v4.10** — `06_SCREEN_SPEC.md:3` *(dòng `Version`)* · `:860` mục ⓔ · `:883` đoạn ⭐⭐ *"NĂM ca của nút `Bỏ gán`"* *(bảng ①…⑤ + bảng 5 trạng thái + nợ `409`)* |

## Cổng vào
| Kiểm | Đo | |
|---|---|---|
| git thật | `HEAD` = `origin/feat/p2-oracle-parity` = `124a067` *(`git rev-parse` cả hai, sau `git fetch`)* | ✅ |
| version hợp đồng | `06_SCREEN_SPEC.md:3` **v4.10** = `WO` mục **Vòng 2 › Spec phải đọc** | ✅ |
| run id | `WO` ⛔ nói "đã chạy" | — |
| `WO` vòng 2 đủ trường `10` §3.1 | Căn cứ · Spec · Phạm vi TRONG/NGOÀI · AC đo được + chiều ĐỎ · Màn hình 5 trạng thái · Dữ liệu · Câu treo *(⛔ chặn)* · Rủi ro | ✅ ⇒ ⛔ `HOI` |
| nền `kiem_so_song` đầu vòng 2 *(trên `124a067`, **trước** commit mã đầu tiên)* | `⛔ CONG SO SONG KHONG DAT — 34 lech/khong-do-duoc` — tách ở mục **Cổng** dưới | ✅ đã chụp |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/web/tep/man_f01_ghep.js` | `bo_gan` viết lại theo năm ca *(`F-1`…`F-4`)*, **⛔ bao giờ ném**: ① `itl_da_gan` ≥ 2 ⇒ `HT.mo('Lệnh này đang gắn N giao dịch', …, [['Đã hiểu']])`, `return` trước mọi cửa · ② `/chum` `can_hoi` ⇒ `HT.mo('Bỏ gán sẽ gỡ CẢ N lệnh chi', …, [['Thôi', null], ['Gỡ cả N', fn, {danger}]])`, `fn` gọi `/unmatch`, lỗi ⇒ `HT.loi_trong_hop(e); return false`, xong ⇒ `setTimeout(_sau_bo_gan, 0)` *(chạy **sau** khi hộp hỏi đóng — hộp *"Đã bỏ ghép"* dùng chung `#scrim`)* · ③ hàm mới `_sau_bo_gan`: đổi thẻ **tại chỗ** cho mọi lệnh trong `ST.dong` có `ma_lenh ∈ da_bo[].pm_line_id` *(lọc `itl_da_gan`, `gd_ds`, `gd`; hết ⇒ `Object.assign(d, BO_BA_CHUA_GAN)`)* → `ve()` → `F01._bao_bo_ghep` nếu `bo_qua` ⛔ rỗng → **rồi** `mo_lenh` *(④: lỗi ⇒ `ST.tin_bo_gan.loi_doc`)* · ⑤ hàm mới `_loi_bo_gan` *(`/chum` hoặc `/unmatch` ném ngoài hộp)* ⇒ `ST.loi_bo_gan = {ma, cau, lam_gi, chi_tiet}`. Hàm mới `ve_dong_bo_gan` vẽ hai dòng chữ **trong** `.act` *(lớp `note ok` / `note warn` / `note crit` đã có, `flex:1 1 100%` inline — ⛔ token/màu mới)*. `ST` thêm `dang_bo_gan` *(khoá: cú thứ hai `return`; hai nút `bỏ gán`/`Bỏ gán` vẽ `disabled`)* · `tin_bo_gan` · `loi_bo_gan`; hằng `BO_BA_CHUA_GAN` *(bản thứ hai của `khuon_the_lenh` — bài so quan hệ)*. `mo_lenh`: đổi sang lệnh **khác** ⇒ xoá hai dòng chữ. `grep -rn "HT\.hoi" fls/web/tep` = **0** *(cả chú thích — viết lại chữ cho mẫu `AC-8 ⓒ` khỏi khớp)*. `hop_thoai.js` **⛔ đổi** |
| `tests/web/test_wo008_chu_man_sau_bo_ghep.py` | ⓐ `BAY_HOP` *(dòng 181 cũ)*: **⛔ thay** `HT.mo`, **⛔ định nghĩa** hàm hỏi trên `HT` — nay **bọc đếm** rồi gọi **xuyên** `HT.mo` thật; giữ lo gốc *(đếm hộp, đọc tiêu đề/thân/nút)*; chú thích ghi lý do *(`KQ-019 F-1`, `11` §6)*. ⓑ `test_AC4_cua_unmatch_LOI__KHONG_mo_hop_da_bo_ghep` viết lại **giữ hai lo gốc** *(⛔ hộp "Đã bỏ ghép" khi cửa lỗi · lỗi ⛔ được biến mất)*: tiền đề *"lỗi đi như nay (ném lên người gọi)"* **sai** *(`KQ-019 F-3`; `BA-06` v4.10 ca ⑤ đính chính)* ⇒ *"⛔ biến mất"* nay đo bằng **chữ trên màn** + promise **resolve**. ⓒ `_bo_gan` mở lệnh trước khi bấm *(nút `Bỏ gán` chỉ sống ở view ②)* và trả thêm `man` |
| `tests/web/test_wo008_v2_nam_ca_bo_gan.py` *(mới)* | **18** bài, nạp `hop_thoai.js` **THẬT**, nút trong hộp bấm bằng **chính `onclick`** của phần tử `#dlg-f`: `AC-7` ×6 · `AC-8` ×2 *(1 DOM + 1 quét mã)* · `AC-9` ×4 · `AC-10` ×1 · `AC-11` ×4 *(`unmatch`/`chum` × `FLS-MAT-KET-NOI`/`FLS-INTERNAL`)* · `AC-12` ×1. Bộ ba trạng thái lấy từ **hàm thật** `fls.repo.man_ghep.khuon_the_lenh` *(⛔ chép hằng)* |
| `docs/ITL/03_Dev/08_CHANGELOG_RELEASE.md` | dòng `WO-008` vòng 2 |

## Chứng minh ĐỎ *(`Đ5`)*
- **18/18** bài mới **ĐỎ** trên mã `124a067` *(chép `git show 124a067:fls/web/tep/man_f01_ghep.js` đè tạm, chạy, chép trả — `sha256` trùng `9dae3ac`)*: `18 failed in 4.03s`. Lý do đỏ đúng chỗ: nhánh hộp ⇒ `TypeError: HT.hoi is not a function`; ca ③ ⇒ màn còn *"✓ Đang gán với giao dịch"*, bộ ba vẫn `da_gan · Đã gán · ok`, ⛔ dòng tín hiệu; `AC-10` ⇒ nút `[False, False]` *(⛔ khoá)*; `AC-11` ⇒ promise **reject** `Không nối được tới máy chủ FLS.` / `Máy gặp lỗi bên trong.`; `AC-8 ⓒ` ⇒ `{'fls\web\tep\man_f01_ghep.js': 2}`.
- **17/17** đột biến trên mã mới bị bắt *(`scratchpad/dot_bien_v2.py` + `dot_bien_m17.py`, sửa tệp thật → chạy → trả; `sha256` trả nguyên **2/2**)*:

| # | Đột biến | Bài đỏ |
|---|---|---|
| M1 | hộp chùm gọi lại hàm hỏi ⛔ có trên `HT` | `test_AC7_chum__HOP_HOI_that_mo…` · `1 failed` |
| M2 | nút `Thôi` mang hàm ghi `/unmatch` | `test_AC7_chum__bam_THOI…` · `1 failed` |
| M3 | lỗi trong hộp ⛔ `return false` | `test_AC7_chum__GO_CA_2_cua_LOI…` · `2 failed` |
| M4 | ca ① vẫn hỏi `/chum` | `test_AC8_lenh_HAI_giao_dich…` · `1 failed` |
| M5 | đổi thẻ theo lệnh đang mở thay vì `da_bo[]` | `test_AC7_chum__bam_GO_CA_2…CA_HAI…` · `1 failed` |
| M6 | bỏ bước cập nhật thẻ | `test_AC9_bo_gan_200…` + `kq019::test_F2_*` · `2 failed` |
| M7 | nhãn JS `Chưa ghép` ≠ `khuon_the_lenh` | `test_AC9_bo_ba…TRUNG_khuon_the_lenh_THAT` · `1 failed` |
| M8 | bỏ dòng tín hiệu | `test_AC9_bo_gan_200…` · `1 failed` |
| M9 | tải lại `lenh-da-gan` sau bỏ gán | `test_AC9_bo_gan_200…` · `1 failed` |
| M10 | bỏ khoá chờ | `test_AC10_hai_cu_bam…` · `1 failed` |
| M11 | bỏ `try/catch` quanh `/unmatch` | `test_AC11_*[unmatch-…]` + `kq019::test_F3_*` · `3 failed, 2 passed` *(2 xanh = ca `/chum` — đúng: đột biến chỉ chạm `/unmatch`)* |
| M12 | lỗi chỉ ra `console` | `test_AC11_*` · `4 failed` |
| M13 | `await mo_lenh` **trước** hộp + thẻ *(như vòng 1)* | `test_AC12_*` + `kq019::test_F4_*` · `2 failed` |
| M14 | báo *"chưa xảy ra"* khi sổ đã ghi | `test_AC12_*` · `1 failed` |
| M15 | bẫy hàm hỏi quay lại `BAY_HOP` | `test_AC8_KHONG_con_HT_hoi…` · `1 failed` |
| M16 | dòng tín hiệu ⛔ mất khi đổi lệnh | `test_AC9_dong_tin_hieu_MAT_khi_mo_lenh_KHAC` · `1 failed` |
| M17 | ca ② gọi `_sau_bo_gan` trực tiếp *(⛔ `setTimeout`)* | `test_AC7_chum_bo_qua_CO__hop_hoi_DONG…` · `1 failed` |

## Cổng *(`PG_DSN=postgresql://fls:fls@localhost:5433/fls`, `PYTHONUTF8=1`, `.venv`)*
| Lệnh | Kết quả nguyên văn |
|---|---|
| `python -m pytest` | `5 failed, 2116 passed in 296.08s (0:04:56)` — **5** `failed` = **đúng 5** `[XPASS(strict)]` liệt kê dưới *(đếm `grep -c "XPASS(strict)"` = **5**)*. Trước vòng 2 *(`KQ-019`)*: `2098 passed, 5 xfailed` ⇒ **+18** bài mới = `2121` phép thử |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 34 lech/khong-do-duoc` — **y số chỗ nền** *(34 ⇒ 34; **0** chỗ lệch mới)*, tách ở bảng dưới |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (110 file, 1297 bang, 652 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(+1 file = phiếu này)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech   (da do 20/20 phep)` · `⛔ ⛔ CONG NO: · ⛔ khoi trong lo trinh LECH voi ban sinh lai ⇒ chay lai ⛔ khong co --kiem` — ⚠ **y nền, ⛔ do vòng 2**: đo bằng `scratchpad/khoi_diff.py` *(chỉ đọc, gọi `khop_owner.chay()` + `bang_md()` thật rồi `difflib` với khối trong lộ trình)* ⇒ **đúng 1 ô lệch**: `B5` *"`06_SCREEN_SPEC.md` nhac co che de xuat **49** lan"* ⟶ máy đếm **50** — vì `BA-06` **v4.10** *(`124a067`, `fls-ba`)* thêm một chữ *"gợi ý"/"đề xuất"*; `git diff 124a067 HEAD -- docs/ITL/02_BA` **rỗng**. `B5` vẫn ✅ *(`n > 0`)*. ⛔ Tôi sinh lại khối *(ngoài phạm vi `WO`)* — `fls-ba` hoặc lượt `--ghi` kế tiếp |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` *(⛔ đỏ vì nút hộp ⇒ ⛔ `HOI`)* |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ **CHƯA CHẠY** — ⛔ chạm schema *(`git diff 124a067 dd7c5bb -- fls/db` rỗng)* |
| `pytest --runxfail tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py` | `8 passed` |

### ⭐ Năm bài `XPASS(strict)` — **đỏ ĐÚNG MONG** *(`AC-13`; `fls-test` gỡ dấu, Dev ⛔ chạm `tests/nghiem_thu/**`)*
1. `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py::test_F1_bo_gan_chum__HOI_TRUOC_that_su_hien[chum]`
2. `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py::test_F1_bo_gan_chum__HOI_TRUOC_that_su_hien[da_giao_dich]`
3. `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py::test_F2_sau_bo_gan_THANH_CONG__man_khong_con_noi_DANG_GAN`
4. `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py::test_F3_bo_gan_cua_LOI__nguoi_THAY_loi`
5. `tests/nghiem_thu/test_kq019_bo_gan_man_ghep_va_nhat_ky.py::test_F4_ve_lai_lenh_LOI_sau_bo_gan__hop_bo_qua_VAN_mo`

⇒ `pytest` **⛔ còn đỏ nào khác** ngoài đúng 5 tên này *(đếm trong `short test summary info`: **5** dòng `FAILED`, cả 5 thuộc tệp `kq019`, cả 5 mang nhãn `[XPASS(strict)]`)*.

### `kiem_so_song` — tách nền ⟷ vòng 2 *(`AC-14`; ⛔ chạy `dong_bo --ghi`)*
Nền đo trên `124a067` *(trước commit mã)*: `34 lech` · cuối *(sau `dd7c5bb` + phiếu này)*: `34 lech`. Mỗi chỗ = một cặp `tài liệu ghi → MÁY đo` của công cụ.

| Nhóm | Phép so *(tên công cụ in)* | Tài liệu ghi | Máy đo ở nền `124a067` | Máy đo cuối | Số chỗ | Vòng 2 có làm trôi? |
|---|---|---|---|---|--:|---|
| **(b)** nhịp chụp | dấu giờ ảnh | `02/10 10:09` | `02/10 12:09` | `02/10 12:09` | 3 | ⛔ |
| **(b)** | ảnh nhịp *(dashboard · bản vẽ 13)* | `135` | `137` | `137` | 2 | ⛔ |
| **(b)** | tổng ảnh *(dashboard · bản vẽ 13)* | `147` | `149` | `149` | 2 | ⛔ |
| **(b)** | bản vẽ · ảnh chụp lệnh chi *(nhóm 2)* | `256.928` | `260.748` | `260.748` | 4 | ⛔ |
| **(b)** | ảnh lệnh chi khác nhau | `68` | `69` | `69` | 2 | ⛔ |
| **(c)** có từ trước *(vòng 1 `BG-017` + bài `KQ-019`)* | số phép thử *(test · tổng · roadmap · master · bản vẽ · chân trang)* | `2084` | `2103` | `2121` | 6 | ✅ **+18** bài vòng 2 |
| **(c)** | phép thử trong module *(test nhóm 2 · bảng tiến độ dòng TỔNG nhóm 2)* | `1782` | `1793` | `1811` | 2 | ✅ **+18** |
| **(c)** | số **dòng** mã thử *("phép thử + dòng" nhóm 2 ở roadmap · master · bản vẽ · test nhóm 5 · dòng TỔNG nhóm 1)* | `25.133` | `25.213` | `25.373` | 5 | ✅ **+160** *(cùng mức trôi với ô `web` dưới)* |
| **(c)** | bảng tiến độ · web *(nhóm 2)* / caption khối 9 | `448` | `459` | `477` | 2 | ✅ **+18** bài web |
| **(c)** | bảng tiến độ · web *(nhóm 1)* / caption khối 9 | `8.547` | `8.627` | `8.787` | 2 | ✅ **+160** |
| **(c)** | nhánh · commit / bản vẽ · chân trang *(lần sửa `fls/` gần nhất)* | `88ab178` | `69f03f6` | `9dae3ac` | 2 | ✅ commit mã vòng 2 |
| **(c)** | master · §8 số file | `105` | `109` | `110` | 1 | ✅ **+1** = `BG-020` |
| **(c)** | test · ngoài module *(nhóm 4 — bài `nghiem_thu`)* | `302` | `310` | `310` | 1 | ⛔ *(bài `KQ-019`)* |
| | **Cộng** | | | | **34** | |

Kiểm cộng: **(b)** `3+2+2+4+2` = **13** · **(c)** trôi thêm vì vòng 2 `6+2+5+2+2+2+1` = **20** · **(c)** ⛔ đổi `1` = **1** ⇒ `13 + 20 + 1` = **34** = dòng tổng của công cụ ✓ *(bài học `F-5`)*. Chỗ lệch **mới** do vòng 2 *(cặp chưa có ở nền)*: **0**. ⛔ `dong_bo_so_song --ghi` *(`AC-14`)*.

## Bằng chứng từng AC
| AC | Bằng chứng của Dev |
|---|---|
| **AC-7** *(ca ② chùm)* | ⓐ `pytest --runxfail "…kq019…::test_F1_…[chum]"` **xanh** *(trong `8 passed`)*. ⓑ `test_wo008_v2_nam_ca_bo_gan.py::test_AC7_chum__HOP_HOI_that_mo__Thoi_Go_ca_2__chua_ghi_truoc_khi_bam` *(`/chum` 1 · hộp thật `#scrim.on` **1** · tiêu đề `Bỏ gán sẽ gỡ CẢ 2 lệnh chi` · thân có `PWB-1` + `PWB-2` · nút `["Thôi", "Gỡ cả 2"]`, `danger` chỉ ở nút 2 · `/unmatch` **0**)* · `::test_AC7_chum__bam_THOI__khong_ghi_hop_dong` *(`onclick` thật của `Thôi` ⇒ `/unmatch` **0**, hộp đóng, 3 thẻ vẫn `da_gan`; mẫu số: hộp **mở** trước khi bấm)* · `::test_AC7_chum__bam_GO_CA_2__mot_luot_ghi__CA_HAI_the_ve_Chua_gan` *(`/unmatch` **1**; `PWB-1` + `PWB-2` ⇒ bộ ba `khuon_the_lenh([])`, `itl_da_gan []`; đối chứng `PWB-3` *(ngoài `da_bo`)* giữ `da_gan [5000]`; dòng *"gỡ cả 2 lệnh chi"*)* · `::test_AC7_chum_bo_qua_CO__hop_hoi_DONG_roi_hop_Da_bo_ghep_MO` *(chùm **và** `bo_qua`: thứ tự hộp `["Bỏ gán sẽ gỡ CẢ 2 lệnh chi", "Đã bỏ ghép"]`, hộp cuối **mở**)* · `::test_AC7_chum__GO_CA_2_cua_LOI__hop_O_NGUYEN__loi_TRONG_hop[…]` ×2 *(`FLS.LoiCua` thật — hộp **ở nguyên**, câu lỗi trong `#dlg-b`, `/unmatch` 1)*. ⓒ **Bấm thật** `8099` dòng **D** *(chùm 2 lệnh, `itl 111`)*: `Bỏ gán` ⇒ `GET /chum 200` ⇒ hộp `Bỏ gán sẽ gỡ CẢ 2 lệnh chi`, nút `["Thôi", "Gỡ cả 2 [danger]"]` · `Thôi` ⇒ hộp đóng, `POST` **0** · bấm lại ⇒ hộp lại · `Gỡ cả 2` ⇒ `POST /unmatch` **1** → `RES 200` → `GET itl-candidates`; thẻ `Chưa gán`, cả `PVE3FF8-1` lẫn `PVFA226-1` ⇒ `chua_gan`; `.act` = *"Gán Chọn một giao dịch bên trên. ↩ Đã bỏ gán khỏi giao dịch #111 — lệnh về Chưa gán · gỡ cả 2 lệnh chi. Sổ giữ lịch sử."*; lỗi console **0** |
| **AC-8** *(ca ①)* | ⓐ `--runxfail …[da_giao_dich]` **xanh**. ⓑ `::test_AC8_lenh_HAI_giao_dich__hop_BAO_mot_nut__khong_chum_khong_unmatch` *(hộp **1**, `2 giao dịch` + `Sổ ITL`, nút `["Đã hiểu"]`, `/chum` **0**, `/unmatch` **0**)*. ⓒ `::test_AC8_KHONG_con_HT_hoi__ca_cho_goi_lan_cho_dinh_nghia_bay`: quét `fls/web/tep/*.js` mẫu gọi ⇒ `{}` · quét `tests/web/**/*.py` mẫu định nghĩa ⇒ `{}`; mẫu số: cùng phép quét thấy `HT.mo` ở **cả hai** nơi. `grep -rn "HT\.hoi" fls/web/tep` ⇒ **0** dòng *(hôm qua **2**)*. ⓓ **Bấm thật** `8099` dòng **F** *(`PVBAEA2-1` ↔ `itl 119, 120`)*: hộp `Lệnh này đang gắn 2 giao dịch` · thân *"FLS không tự chọn hộ bỏ giao dịch nào. Hãy bỏ gán từ màn Sổ ITL…"* · nút `["Đã hiểu"]`; mạng: **0** `/chum`, **0** `POST`; `HT` xuất `mo,dong,loi_trong_hop` |
| **AC-9** *(ca ③)* | ⓐ `--runxfail …::test_F2_*` **xanh**. ⓑ `::test_AC9_bo_gan_200_bo_qua_RONG__the_ve_Chua_gan__dong_tin_hieu__0_hop` *(mẫu số: *"Đang gán với giao dịch"* **có** trước cú bấm; sau: **⛔ có**; có *"↩ Đã bỏ gán khỏi giao dịch #4242 — lệnh về Chưa gán"* + *"Sổ giữ lịch sử."*; ⛔ *"gỡ cả"*; hộp **0**; nút `Gán` **1**, `Bỏ gán`/`bỏ gán` **0**; `ST.mo = PWB-1`, thứ tự `ST.dong` giữ, chip `da_gan`; lượt `lenh-da-gan`/`lenh-cho` sau cú bấm **0**)* · `::test_AC9_bo_ba_trang_thai_sau_bo_gan__TRUNG_khuon_the_lenh_THAT` *(**quan hệ**: bộ ba trước ≡ `khuon_the_lenh(itl_da_gan=[4242])`, sau ≡ `khuon_the_lenh(itl_da_gan=[])`, hai bộ **khác nhau**; chip `.wh1` in `trang_thai_nhan` ấy)* · `::test_AC9_bo_qua_CO__them_hop_Da_bo_ghep_MOT_lan` *(`bo_qua=[hd]` ⇒ hộp `Đã bỏ ghép` **1** lần, `HD-NGUOI-B2`, nút `["Đã hiểu"]` + dòng tín hiệu — `AC-4` giữ)* · `::test_AC9_dong_tin_hieu_MAT_khi_mo_lenh_KHAC`. ⓒ **Bấm thật** `8099`: **C** *(`bo_qua` rỗng, `itl 75`)* ⇒ hộp **0**, thẻ `Chưa gán`, nút `["Gán [khoa]"]` *(khoá vì chưa chọn giao dịch — như mọi lệnh chưa gán)*, `.act` có dòng tín hiệu `#75`, ⛔ lượt `lenh-da-gan`/`lenh-cho` sau cú bấm · **B2** *(`bo_qua=[hd = HD-NGUOI-B2]`, `itl 61`)* ⇒ hộp `Đã bỏ ghép` **1** *(*"…⚠ ⛔ KHÔNG đảo 1 ô — người đã gõ tay lên đó sau khi ghép: hd = HD-NGUOI-B2"*, nút `["Đã hiểu"]`)* + thẻ `Chưa gán` + dòng tín hiệu `#61` |
| **AC-10** *(tải)* | `::test_AC10_hai_cu_bam_khi_cua_CHUA_tra__mot_luot_unmatch__nut_khoa` — cửa `/unmatch` **treo** *(Promise chưa resolve)*; bấm **nút thật** `Bỏ gán` *(trình nghe `click` của phần tử)*, đọc lại hai nút ⇒ `disabled` `[true, true]`, bấm lại cả hai + gọi `bo_gan` lần nữa ⇒ `/unmatch` **1** lượt khi treo và **1** sau khi trả. **Bấm thật** `8099` dòng **H** *(`itl 99`)*: hai `click()` liền trong cùng một lượt JS ⇒ nút sau cú 1 `[true, true]`, `POST /unmatch` **1** |
| **AC-11** *(ca ⑤)* | ⓐ `--runxfail …::test_F3_*` **xanh**. ⓑ `::test_AC11_cua_LOI__Bo_gan_chua_xay_ra__the_giu_Da_gan__promise_RESOLVE[…]` ×4 *(`unmatch`/`chum` × `FLS-MAT-KET-NOI`/`FLS-INTERNAL`, `FLS.LoiCua` **thật** ⇒ `.catch` **⛔ gọi**; màn có *"Bỏ gán chưa xảy ra — Cửa lỗi: <câu>"* + `chi_tiet` + `lam_gi` *(khi mã có)*; `trang_thai` `da_gan`, khối *"Đang gán"* còn; hộp **0**; ca `/chum` lỗi ⇒ `/unmatch` **0**)*. ⓒ **Bấm thật** `8099` dòng **E** *(`itl 87`, `Fetch.failRequest` đúng lượt `/unmatch`)*: `.act` = *"… Bỏ gán chưa xảy ra — Cửa lỗi: Không nối được tới máy chủ FLS. Kiểm tra máy chủ còn chạy không, rồi tải lại trang. Failed to fetch"*; thẻ `Đã gán`, khối *"Đang gán"* còn, nút `bỏ gán`/`Bỏ gán` **mở** lại; `Runtime.exceptionThrown` **0** *(⛔ `Uncaught`)*; ảnh `scratchpad/man/v2_E_mat_mang_1.png` |
| **AC-12** *(ca ④)* | ⓐ `--runxfail …::test_F4_*` **xanh**. ⓑ `::test_AC12_doc_lai_ung_vien_LOI__hop_bo_qua_VAN_mo__tin_hieu_va_dong_loi_doc` *(`itl-candidates` ném `FLS-INTERNAL` ⇒ promise resolve; hộp **mở**, `HD-NGUOI-B2`; màn có *"Đã bỏ gán khỏi giao dịch #4242"* **và** *"Chưa tải lại được giao dịch gợi ý: Máy gặp lỗi bên trong."*; ⛔ *"Bỏ gán chưa xảy ra"*; thẻ `chua_gan`)* |
| **AC-13** | mục **Cổng** trên: `pytest` đỏ **đúng 5** `XPASS(strict)` liệt kê tên · `--runxfail` `kq019` **8/8** · lint **9 kept 0 broken** · `soi_bang_tuyen` 40/40 *(⛔ tuyến đổi)* · `kiem_thuyet_minh` 31/31 *(⛔ đỏ ⇒ ⛔ `HOI`)* · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh trong lượt `pytest` *(chữ mới chỉ dùng `↩` + `—`; ⛔ `⛔ ⚠ ⭐ 🔒`)* |
| **AC-14** | mục **`kiem_so_song`** trên — bảng tách **cộng đúng tổng** *(dòng kiểm cộng cuối bảng)*; `dong_bo_so_song --ghi` **⛔ chạy** |

## Kho thật
- **`KHONG_CHAM`**. Máy `8088` *(kho thật, chỉ đọc)* ⛔ đụng tới. Mọi cú bấm thật trên `8099` *(`chay_cua.py --cho-web --cho-ghi --cong 8099`, `PG_DSN=…/fls_test`)*; dòng dựng bằng `scratchpad/v2_dung_8099.py` *(`dsn_test()` nổ nếu trỏ kho thật; `run_id` `NAP-2000-01-01-V8A734E`)*. Đã tắt: `Get-NetTCPConnection -LocalPort 8099 -State Listen` ⇒ **0**. ⚠ Lượt `pytest` sau đó **dựng lại** kho TEST *(`GAP-KHO-02`)* ⇒ các dòng ấy đã mất — bằng chứng giữ ở `scratchpad/man/v2_*.json|png` *(⛔ lên git)*.

## Cách chạy để xem
- `PG_DSN=postgresql://fls:fls@localhost:5433/fls_test python tools/chay_cua.py --cho-web --cho-ghi --cong 8099` *(kho TEST, **ghi**)* · dựng dòng: chép `v2_dung_8099.py` *(sáu ca B2/C/D/F/E/H — xem chú thích đầu tệp)* · màn `②b Gán lệnh chi` › chip `Đã gán` › mở lệnh › `Bỏ gán`. Kịch bản Chrome headless: `node scratchpad/v2_soi.mjs <S> 8099 '{"ma":"…","nhan":"…","mat_mang":true|"hai_lan":true|"thoi_truoc":true}'`.
- `8088` *(kho thật)* chỉ đọc — ⛔ dùng để bấm.

## Dev tự thấy còn yếu
1. **Bộ ba trạng thái có hai bản** *(`khuon_the_lenh` Python ↔ `BO_BA_CHUA_GAN` JS)* — `WO` Rủi ro ①. Bài quan hệ chỉ canh nhánh **⛔ gán**; nhánh `Đã gán` của JS ⛔ có *(màn ⛔ bao giờ tự đặt `Đã gán` — luôn do cửa trả)*.
2. **Thẻ đổi tại chỗ ≠ thẻ cửa sẽ trả nếu tải lại**: sau bỏ gán tôi đặt `gd = null` *(hoặc dòng còn lại của `gd_ds`)*; cửa `lenh-da-gan`/`lenh-cho` khi tải lại sẽ trả `gd` = **ứng viên máy đầu** *(`da_gan=false`)*. Hệ quả: bảng sổ view ① cột *"Giao dịch đã gán"* của lệnh vừa bỏ in `— chưa có` thay vì gợi ý máy cho tới lần tải chip kế. Spec ③ⓐ ⛔ nói gì về `gd` ⇒ ⛔ mở `HOI` *(trình bày, ⛔ số)*; Test soi xem có coi là lệch.
3. **Chỗ đặt đuôi chùm**: spec *"(chùm: thêm · gỡ cả N lệnh chi)"* ⛔ nói chèn ở đâu; tôi in *"— lệnh về Chưa gán · gỡ cả 2 lệnh chi. Sổ giữ lịch sử."*. `N` = số phần tử `da_bo[]` của **thân trả** *(⛔ `chum.so_dong`)* — hai số ⛔ được lệch nếu cửa đúng, nhưng tôi ⛔ có bài nào ép chúng bằng nhau.
4. **Dòng tín hiệu mất cả khi về bảng sổ rồi mở lại CÙNG lệnh** *(`ArrowLeft` đặt `ST.mo = null` ⇒ lượt `mo_lenh` sau thấy `ST.mo !== ma`)* — spec chỉ nói *"mất khi mở lệnh khác"*. Tôi coi *"về bảng"* là rời lệnh; Test có thể đọc khác.
5. **Ca ② → ③ nối bằng `setTimeout(…, 0)`** để hộp *"Đã bỏ ghép"* ⛔ bị `dong()` của hộp hỏi đóng mất *(bài + đột biến `M17` canh)*. Trên trình duyệt thật tôi **chỉ** bấm chùm với `bo_qua` **rỗng** *(dòng D)*; chùm **có** `bo_qua` mới đo bằng DOM giả.
6. **Cờ khoá `ST.dang_bo_gan` sống trong một mô-đun**: nếu một ngoại lệ **ngoài dự tính** bật ra giữa lúc đặt cờ và lúc trả cờ *(⛔ từ cửa — mọi lỗi cửa đã bắt)*, nút ở trạng thái khoá tới khi tải lại trang. Tôi ⛔ có bài cho ca ấy.
7. **Nợ `409` ⛔ trong phạm vi** *(`BA-06` v4.10)*: hai người bỏ gán cùng lúc ⇒ người thứ hai thấy *"Bỏ gán chưa xảy ra — Cửa lỗi: Giá trị bạn gõ khác với giá trị nguồn đang có."* — đúng là **với họ** chưa xảy ra, nhưng câu sai nghĩa và thẻ của họ vẫn nói `Đã gán` trong khi sổ đã gỡ *(người khác gỡ)*. Chờ phiếu đổi mã lỗi.
8. Bài DOM giả ⛔ đo được **bố cục** *(dòng chữ `flex:1 1 100%` xuống hàng riêng trong `.act`)* — chỉ ảnh Chrome `8099` *(1440×900; `scrollWidth 1409 ≤ innerWidth 1424`)* cho thấy dòng nằm dưới hàng nút, ⛔ tràn.
