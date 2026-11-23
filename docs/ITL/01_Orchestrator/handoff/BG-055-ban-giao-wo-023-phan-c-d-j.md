# BG-055 — bàn giao `WO-023` **phần `(c)(d)(j)`** *(vòng 1)*: hạn chờ cửa ghi `30 s` ⇒ `FLS-HET-GIO` · ba mã `409` mới · bài `AC7_doi_MUC_PHU` tự đủ

| | |
|---|---|
| **Thuộc** | `WO-023` *(vòng 1)* — phần `(c)` *(`AC-3`)* · `(d)` *(`AC-4`)* · `(j)` *(`AC-15`)*. Spec `BA-06` **v4.11** `ⓕ3` · `ⓕ4` · `BA-07` **v3.5** §5 *(hiện hành **v3.12** — §5 ⛔ đổi từ v3.5)* · `KQ-050 F-4` |
| **Phát bởi** | `fls-dev` · 2026-10-05 |
| **Nhận** | `fls-test` |
| **Commit** | `feat/p2-oracle-parity` @ `7ec2dc0` *(mã `(c)(d)` + bài + `HOI-056`)* · `7b2b901` *(`(j)` — chỉ bài)* · `82522e1` *(tài liệu Dev)* — **đã đẩy**; tờ này ở commit kế tiếp |
| **Nền** | `BG-052` `(i)` · `BG-053` `(h)` · `BG-054` `(a)(b)` |
| **Vì sao `(j)` đi cùng `BG` này** *(⛔ cuối phiếu)* | `pytest` toàn bộ @ `7ec2dc0` **đỏ** `tests/web/test_wo045_luot_moi_nhat_cua_that.py::test_AC7_doi_MUC_PHU_khi_luoi_dang_tai_luoi_la_loc_CUOI` *(`⛔ không đo được: 50% ⛔ khác tất cả`)* — đúng `KQ-050 F-4`, lộ ra vì bài của phiếu này dựng thêm ca trên kho TEST ⇒ ⛔ phát `BG` với cổng đỏ |
| **Phần còn lại của `WO-023`** | `(f)(g)` → `(e)`. `WO-023` **giữ `DANG_LAM`** |
| **Câu hỏi mở** | [`HOI-056`](HOI-056-chu-het-gio-cho-cu-gan.md) `KHONG_CHAN` — chữ hết giờ cho cú `Gán` *(spec chỉ ghi cho `Bỏ gán`)*; làm phương án ⭐ |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/web/tep/goi_cua.js` | `(c)` `HAN_CHO = { ghi_ms: 30000 }` *(xuất — bài đặt nhỏ)*; `goi()` phương thức ≠ `GET` ⇒ `Promise.race([_goi(…), hẹn giờ])` ⇒ quá hạn ném `LoiCua('FLS-HET-GIO', 0, 'quá <s> s chưa có trả lời — <PT> <đường>')`; `GET` đi thẳng *(⛔ hạn)*; ⛔ `AbortController`, ⛔ tự thử lại. `CAU` ＋ `FLS-HET-GIO` *(cau/lam_gi nguyên văn `ⓕ3`)*, `MA_TU_MAN_HINH` ＋ `FLS-HET-GIO`. `(d)` `CAU` ＋ `FLS-DA-GHEP` · `FLS-KHONG-CON-MOI-NOI` · `FLS-CHUA-XONG` *(nguyên văn `ⓕ4`)* |
| `fls/repo/ghi_tay.py` | `(d)` `DaGhep.ma = "FLS-DA-GHEP"` · `ChuaXong.ma = "FLS-CHUA-XONG"` · `KhongCoMoiNoi.ma = "FLS-KHONG-CON-MOI-NOI"` *(docstring giữ bia mã cũ)*; `KhacNguon` **giữ** `FLS-CONFLICT-SOURCE` |
| `fls/api/bao.py` | `(d)` `MA_LOI` ＋ ba mã, đều **`409`**; khuôn thân ⛔ đổi *(`khac.moi_noi` của `DaGhep` vẫn ra)* |
| `fls/web/tep/man_f01_ghep.js` | `(c)` `_loi_bo_gan` lưu `ma_loi`; `ve_dong_bo_gan` — `FLS-HET-GIO` ⇒ `Chưa rõ bỏ gán đã xảy ra chưa — Cửa lỗi: <cau>`, mã khác ⇒ `Bỏ gán chưa xảy ra — …` như cũ. Cú `Gán` *(`(h)`)* cùng khuôn: `Chưa rõ gán đã xảy ra chưa — …` *(`HOI-056`)* |
| `tests/api/test_wo023_d_ma_409_pg.py` *(mới)* | 3 bài `AC-4` qua **cửa HTTP thật** kho TEST |
| `tests/web/test_wo023_cd_het_gio_va_cau_409.py` *(mới)* | 7 bài `AC-3` + `AC-4` phía màn; chữ nguyên văn đọc **từ `06_SCREEN_SPEC.md`** *(dòng `ⓕ3`/`ⓕ4`)*, ⛔ chép tay |
| `tests/web/test_wo045_luot_moi_nhat_cua_that.py` | `(j)` `_pham_vi_ca`: lằn **tiền** `F01` *(`/queue` · `/queue?…` · `/queue/summary` · `/queue/tu-chung`)* hỏi cửa thật với `?run_id=<ca.run>` *(`xu_ly.pham_vi_cua_yeu_cau` ⇒ `mot_lan_nap`)*, thân đặt dưới **đúng** đường màn gọi. Phép tự chứng `len(mong) < len(t_vnd)` **giữ** *(`Đ5`)* |
| `tests/web/ca_wo045.py` | `(j)` chú thích ⓒ: đính chính *"chỉ lần nạp mới nhất"* — **sai** *(cửa `/queue` đọc `chi_nap_that` = mọi lần nạp; số đo 05/10 là của kho TEST gần rỗng)*; câu cũ giữ gạch làm bia |
| `handoff/HOI-056-…md` *(mới)* | chữ hết giờ cho cú `Gán` |
| `docs/ITL/03_Dev/12_P6_WEB_PLAN.md` **v0.22** · `08_CHANGELOG_RELEASE.md` | quy ước thứ mười hai |

⭐ Rủi ro 2 của `WO-023` *(client cũ so mã)*: `grep -rn "\.ma ===\|\.ma !==" fls/web/tep/*.js` @ `7ec2dc0` ⇒ **1** phép so mã lỗi cửa: `man_f02.js:975` `e.ma !== 'FLS-CONFLICT-SOURCE'` — đường `/adjust` *(ca `KhacNguon`)* ⇒ **giữ** đúng. Bài Dev ghim mã cũ *(phiếu đo 02/10)*: `test_cua_ghi_pg.py:258` · `test_ghi_tay_pg.py:152` · `test_vong_f02_pg.py:211` · `test_lo_luu_f02.py:254/286/314` · `test_bao.py:97` — **cả bảy** là ca `KhacNguon` ⇒ **giữ**, ⛔ sửa bài nào. ⚠ `goi_cua.js` **⛔ có** hàm `dich` *(phiếu `AC-4` nhắc `goi_cua.js::dich`; `grep -n "function dich"` **0** — chỉ chú thích `:26`)*: phép dịch nằm ở hàm dựng `LoiCua`; bài đo ở đó.

## Cổng *(kết quả nguyên văn, `PG_DSN=postgresql://fls:fls@localhost:5433/fls`, `PYTHONUTF8=1`, @ `7b2b901` — mã ⛔ đổi ở `82522e1`)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest` | `5 failed, 2379 passed, 1 xfailed in 454.63s (0:07:34)` — `5 failed` = **đúng 5** `XPASS(strict)` *(3 `kq021` · 2 `kq050` — như `BG-054`)*. ⛔ đỏ nào khác. *(@ `7ec2dc0`, trước `(j)`: `6 failed` = 5 `XPASS` ＋ `test_AC7_doi_MUC_PHU…` — xem dòng `(j)`)* |
| `python tools/kiem_so_song.py` | `⛔ CONG SO SONG KHONG DAT — 55 lech/khong-do-duoc` — **= nền 55**; ⛔ `dong_bo_so_song --ghi` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — va no da do duoc that (146 file, 1566 bang, 702 o ngay, 104 ma QD), khong chi 'khong thay loi'` — đo **sau** khi viết tờ *(trước commit tờ)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `⇒ 17/20 khop · 3 lech (da do 20/20 phep)` · `✅ cong C1 DAT — bang khop ban khai, va no da do duoc that (20 phep tren 3 nguon)` — đo như dòng trên |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/Scripts/lint-imports.exe` | `Contracts: 9 kept, 0 broken.` |
| `python -m fls.db.pg_migrate` | ⛔ CHƯA CHẠY — ⛔ chạm schema |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev |
|---|---|
| **AC-3** *(c)* | `test_AC3_GHI_treo_qua_han__FLS_HET_GIO_cau_nguyen_van__DOC_treo_KHONG_het_gio`: `fetch` treo, `HAN_CHO.ghi_ms = 40` ⇒ `POST` ném `['FLS-HET-GIO', 'Máy chưa trả lời sau 30 giây — chưa biết lượt ghi đã vào sổ hay chưa.', 'Tải lại để xem trạng thái thật trước khi bấm lại.']` *(trùng từng byte dòng `ⓕ3`)*; `GET` treo cùng lúc **vẫn chờ** *(⛔ `FLS-HET-GIO`)* · `test_AC3_hang_HAN_mac_dinh_la_30_giay` *(`30000`)* · `test_AC3_HET_GIO_trong_hop_GO_CA_N__loi_trong_hop_nut_mo_lai` *(hộp ② ⇒ lỗi trong hộp, nút mở)* · `test_AC3_HET_GIO_ngoai_hop_ca5__CHUA_RO_bo_gan_da_xay_ra_chua` *(ca ⑤ ⇒ `Chưa rõ bỏ gán đã xảy ra chưa — Cửa lỗi: Máy chưa trả lời sau 30 giây…`, **⛔** `Bỏ gán chưa xảy ra`)* · `test_AC3_HET_GIO_cu_GAN__CHUA_RO_gan_da_xay_ra_chua` *(`HOI-056`)* · Rủi ro 3 `test_AC3_rui_ro_3_het_gio_roi_BAM_LAI__409_moi_noi_dung_chuyen` *(lượt 1 hết giờ ⇒ *"Chưa rõ…"*; bấm lại ⇒ thân `409` **thật** `FLS-KHONG-CON-MOI-NOI` ⇒ `Bỏ gán chưa xảy ra — Cửa lỗi: Giao dịch này không còn gán với lệnh nào — có thể vừa có người bỏ gán trước bạn.`, ⛔ *"Giá trị bạn gõ khác"*)*. **Đột biến** *(phá → chạy 16 bài → trả nguyên)*: bỏ hạn chờ ⇒ **5 failed** · hạn chờ áp cả cửa đọc ⇒ **1 failed** *(đúng bài `DOC_treo`)* · `Bỏ gán` luôn *"chưa xảy ra"* ⇒ **2 failed** · `Gán` luôn *"chưa xảy ra"* ⇒ **1 failed** |
| **AC-3** — số đo giờ lượt ghi *(spec chưa có)* | kho TEST *(`fls_test`, `fls_itl` **981** dòng · `fls_pm_link` **173**)*, cửa HTTP trong tiến trình *(`_may()`)*, 6 vòng `match` → `unmatch` trên một dòng: **`POST /unmatch` min 0,067 s · trung vị 0,102 s · max 0,119 s** · `POST /match` min 0,089 s · trung vị 0,100 s · max 0,130 s *(n=6)* ⇒ `30 s` ≈ **250 lần** lượt ghi chậm nhất đo được. ⚠ Kho TEST **nhỏ hơn sổ thật ~9 lần** *(8.387 dòng — `11` §7)*; lượt ghi trên sổ thật **⛔ đo** *(8088 chỉ đọc — ⛔ ghi)* |
| **AC-4** *(d)* | `tests/api/test_wo023_d_ma_409_pg.py::test_AC4_BON_ca_409_BON_ma_qua_cua_that` — cửa thật kho TEST: `match` dòng đã ghép ⇒ `(409, FLS-DA-GHEP)` *(thân còn `khac.moi_noi`)* · `unmatch` dòng ⛔ mối nối ⇒ `(409, FLS-KHONG-CON-MOI-NOI)` · `reopen` dòng chưa xong ⇒ `(409, FLS-CHUA-XONG)` · `/adjust` khác nguồn ⇒ `(409, FLS-CONFLICT-SOURCE)` *(`khac = {nguon: HD-NGUON-23}`)* — **4** ca, **4** mã. ⛔ Đỏ trên mã khi nhận: cả bốn `FLS-CONFLICT-SOURCE`. `::test_AC4_ghi_tay_CHI_con_MOT_lop_mang_CONFLICT_SOURCE` ⇒ **1** *(trước **4**)*. `::test_AC4_BA_ma_moi_khai_409_trong_MA_LOI`. Phía màn: `test_AC4_ba_ma_moi_CAU_nguyen_van_BA06_f4` *(trùng từng byte dòng `ⓕ4`; ⛔ đỏ cũ: `Lỗi chưa được mô tả: FLS-DA-GHEP`)*; ca **K** = bài Rủi ro 3 ở trên. **Đột biến**: `KhongCoMoiNoi` về mã cũ ⇒ **3 failed** · bỏ câu `FLS-CHUA-XONG` ⇒ **4 failed** *(gồm cổng phủ mã `test_goi_cua_phu_het_ma_loi.py`)* |
| **AC-15** *(j)* | ⓐ `pytest` toàn bộ @ `7ec2dc0` *(kho TEST sau khi bài `wo023` dựng thêm ca)* ⇒ `test_AC7_doi_MUC_PHU…` **ĐỎ** `⛔ không đo được: 50% ⛔ khác tất cả` — chính `KQ-050 F-4`. ⓑ @ `7b2b901` toàn bộ **xanh**. ⓒ Thêm **3** ca `dung_ca_wo045` *(kho TEST `VND` nạp thật 114 → 171 → 228 dòng)* rồi chạy bài ⇒ **passed**. ⚠ ⓓ Ở **đúng** trạng thái kho ấy bản bài **cũ** cũng xanh *(phân bố kho lúc đo chưa chạm ngưỡng)* — chiều đỏ của bản cũ tôi chỉ có từ lượt `pytest` toàn bộ ⓐ, ⛔ dựng lại được bằng tay. ⓔ Bài mới trên `man_f01.js` @ `14a4b72` *(mã trước `WO-045`)* ⇒ **ĐỎ** — nhưng vì `TypeError: Cannot read properties of null (reading 'appendChild') at man_f01.js:154` *(DOM giả trả `tbody null` cho lưới `innerHTML` cũ — `BG-048` đã ghi)*, ⛔ vì phép so lưới. ⓕ chú thích `ca_wo045.py` ⓒ khớp phạm vi thật |
| AC-6 | `pytest` **0** đỏ ngoài **5** `XPASS(strict)` · lint 9/0 · 40 tuyến · 31/31 · luật ký hiệu + token xanh |
| AC-7 *(phần này)* | `kiem_so_song` **55 = nền**; ⛔ `dong_bo --ghi`; `khop_owner --kiem` **ĐẠT 17/20** đo sau khi viết tờ *(trước commit tờ)* |
| AC-5 · AC-5b · AC-8 · AC-9 | ⏳ **chưa làm** — `BG` sau |

## Kho thật
- `KHONG_CHAM`. Kho TEST: mỗi lượt `pytest` thêm ca `dung_ca_wo023` *(4 dòng tiền + 2 lệnh + 1 dòng có nguồn)* + một mối nối thật *(`AC-4`: ghép `M2`)*; phép đo giờ thêm 1 ca + 6 cặp `match`/`unmatch`; `AC-15` thêm 3 ca `dung_ca_wo045`.

## Cách chạy để xem
- Kho TEST `--cho-web --cho-ghi --cong 8099`; hết giờ: trong console `FLS.HAN_CHO.ghi_ms = 1` rồi bấm `Bỏ gán` ⇒ dòng *"Chưa rõ bỏ gán đã xảy ra chưa — …"* *(lượt thật vẫn có thể vào sổ — tải lại để thấy)*.

## Dev tự thấy còn yếu
1. **Số đo giờ lượt ghi là của kho TEST nhỏ** *(981 dòng, máy cục bộ)* — sổ thật ⛔ đo được mà ⛔ ghi. `30 s` có biên rất rộng so với **0,1 s**; nhưng lượt ghi sổ thật có thể chậm theo cùng lớp lỗi `WO-051` *(trang `VND` 104 s)* nếu cửa ghi đọc lại hàng chờ — chưa ai đo.
2. **Hết giờ ⛔ huỷ `fetch`** *(đúng phiếu)* ⇒ câu trả lời thật về muộn bị **bỏ** *(`race` đã xong)*: lượt đã vào sổ mà màn vẫn nói *"Chưa rõ"* tới khi người tải lại. Đó là điều `ⓕ3` muốn *(tải lại để xem trạng thái thật)*, nhưng màn **có** câu trả lời mà ⛔ dùng.
3. `chi_tiet` của `FLS-HET-GIO` *(`quá 30 s chưa có trả lời — POST /queue/…`)* là chữ **tôi** đặt — spec chỉ khai `cau` + `lam_gi`. Nó hiện ở dòng đơn cách dưới lỗi *(cùng chỗ `chi_tiet` của mọi `LoiCua`)*.
4. Bài `test_goi_cua_phu_het_ma_loi.py::test_hai_ma_sinh_o_man_hinh_that_su_khong_den_tu_cua` mang chữ *"hai"* trong tên — nay là **ba** mã phía màn; bài vẫn đúng *(⛔ đếm)*, tên ⛔ sửa *(bài của Dev cũ — đổi tên ⛔ đổi lo)*.
5. `(j)`: chiều đỏ của **bản bài cũ** ⛔ dựng lại được bằng tay ở trạng thái kho lúc đo *(xem `AC-15` ⓓ)* — tôi dựa vào lượt `pytest` toàn bộ `7ec2dc0`. `_pham_vi_ca` chỉ áp bốn đường lằn tiền; nếu `F01` gọi thêm một đường `/queue…` mới thì đường ấy sẽ đọc cả kho tới khi ai thêm vào danh sách.
6. `HOI-056`: chữ cho `Gán` hết giờ là **phương án Dev** — nếu `fls-ba` chọn khác, đổi **một** dòng `ve_dong_gan`.
