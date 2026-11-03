# WO-060 — Câu lỗi `FLS-DQ-FAILED` ⛔ còn chỉ sai đường · chế độ chỉ đọc khoá `Gán`/`Bỏ gán`/`Đảo` · ⛔ nút `Đảo` trên bút toán đã bị đảo · cổng quét `HT.nuot_phim` · `ST.dg_mo` theo `itl_id`

| | |
|---|---|
| **Trạng thái** | `MO` · ⏳ chờ `WO-051` → `WO-062` *(⭐ thứ tự 06/10, `fls-ba` sau nghiệm thu PO `WO-023`: `WO-051` → `WO-062` → **phiếu này** → `WO-047` → `WO-015` — ~~`fls-test` kiểm `WO-023` → `WO-051` → phiếu này → `WO-047` → `WO-015`~~)* · ưu tiên **TRUNG BÌNH** · ⭐ thêm `(f)` *(06/10 — nghi ⓖ `KQ-061`, tái hiện trước; chưa ai nhận ⇒ vẫn **vòng 1**)* *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Phát bởi** | `fls-ba` · 2026-10-05 |
| **Nhận** | `fls-dev` |
| **Vòng** | `1` |
| **Thứ tự với phiếu khác** | **Sau** [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) *(`CHO_TEST` — phiếu này sửa tiếp đúng các tệp `WO-023` vừa giao: `goi_cua.js` · `man_f01_ghep.js` · `man_f02.js`; nhận trước khi `KQ` của `WO-023` về là giẫm lên mã đang kiểm)* và **sau** [`WO-051`](WO-051-trang-hang-cho-vnd-104-giay-va-khung-cho-xem-them.md) *(giấu **98,8%** dòng `VND` khỏi `F01` — tầm lớn hơn mọi mục ở đây)*. ⭐ *(06/10)* và **sau** [`WO-062`](WO-062-luoi-f02-in-final-va-lo-luu-het-gio.md) *(cùng `man_f02.js` — phiếu ấy chạm lưới + lô lưu, chặn `C1`)*. **Trước** [`WO-047`](WO-047-mot-tap-ky-tu-cho-phep-so-tien-te-con-lai.md) *(sổ thật **0** ca)* · [`WO-015`](WO-015-so-actor-phu-moi-bang-va-luat-uat-ascii.md) *(⛔ con số nào đổi)* |
| **Vì sao ⛔ vòng 2 `WO-023`** | cả năm mục là **phát hiện ngoài phạm vi** của chính Dev khi làm `WO-023` *(`BG-052` mục 5/6 · `BG-053` mục 3 · `BG-054` mục 2 · `BG-057` mục 5)* — ⛔ mục nào là lỗi của mã `WO-023` giao; `WO-023` ⛔ đòi chúng |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B` cổng `B5`** *(kế toán đi hết một vòng ghép thật)* — ⓐ là câu kế toán đọc **mỗi lần** cửa ghi từ chối một cú `Gán`/`Ghép` *(khác tiền tệ, lệch tổng, lệnh chưa duyệt)*; và tác vụ **adjust** *(`F02` `Đảo` — ⓑ ⓒ)*.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ xoá thêm; giữ mắt xích *"ghép PM ↔ tiền"* đã lên FLS **⛔ nói sai việc**: hôm nay bị từ chối thì màn bảo người **đi xem màn khác** *(`Cổng hôm nay`)* mà ở đó mọi cổng có thể **xanh** — một kế toán *(`QĐ-ITL-27`: 2–3 người, ⛔ người thứ hai để hỏi)* sẽ kết luận *"máy hỏng"* hay hỏi người dựng hệ, trong khi lý do đúng đã in ngay dưới câu ấy.

### Vì sao năm mục một phiếu, và thứ tự trong phiếu
| Mục | Hại hôm nay | Ai gặp *(tầm)* | Chạm GHI? |
|---|---|---|:-:|
| **ⓐ** câu `FLS-DQ-FAILED` | `lam_gi` chỉ sang `Cổng hôm nay`; mã này **0** đường từ cổng | **mọi** `422` của cửa ghi — **5** lớp lỗi, ba màn | ⛔ — nhưng nói sai việc **ở mọi cú bị từ chối** |
| **ⓑ** chỉ đọc ⛔ khoá | nút ghi bấm được ⇒ `405` sau một vòng bấm/gõ; **lệch spec** `ⓦ` ② | mọi người mở sổ thật ⛔ bật ghi; nút `Đảo` **4.426** | ⛔ *(cửa vẫn `405`)* |
| **ⓒ** `Đảo` trên bút toán đã đảo | nút mời một cú chắc chắn bị `422` | sổ thật **2** nút *(UAT `27728`)* | ⛔ *(cửa vẫn từ chối)* |
| **ⓓ** cổng quét `nuot_phim` | màn mới quên hỏi ⇒ phím lọt sau lưng hộp, ⛔ ai thấy | phép canh *(rẻ — một bài tĩnh)* | ⛔ |
| **ⓔ** `ST.dg_mo` chỉ số | phần mở rộng diễn giải nhảy sang dòng khác khi danh sách bị thay | chỉ **chữ hiện** | ⛔ |

Gộp vì: cùng **ba tệp màn** `WO-023` vừa chạm *(`goi_cua.js` · `man_f01_ghep.js` · `man_f02.js`)*, cùng lớp *"màn nói đúng điều cửa sẽ làm"*, mỗi mục **một vài dòng**. Tách năm phiếu là năm lượt `BG`/`KQ` cho năm thay đổi nhỏ trên cùng tệp. Ưu tiên **TRUNG BÌNH**: ⛔ mục nào ghi sai vào sổ *(cửa đã chặn đúng cả ba ca ⓐ ⓑ ⓒ)*.

## Căn cứ
- [`BG-053`](BG-053-ban-giao-wo-023-phan-h.md) mục yếu **3** *(`fls-dev` 05/10)*: *"`lam_gi` của `FLS-DQ-FAILED` nói sai việc cho ca khác tiền tệ: "Mở màn “Cổng hôm nay” xem cổng nào đỏ." — cổng ⛔ đỏ; lý do thật nằm ở `chi_tiet`"*.
- [`BG-052`](BG-052-ban-giao-wo-023-phan-i.md) mục yếu **6**: *"nút `Gán` của `F01G` ⛔ khoá ở chế độ chỉ đọc … `BA-06` `ⓦ` ② bảng ghi `Gán` "khoá + câu `405` như nay""* · mục **5**: *"`ST.dg_mo` … vẫn là chỉ số"*.
- [`BG-057`](BG-057-ban-giao-wo-023-phan-f-g.md) mục yếu **5**: *"Nút `Đảo` vẫn hiện trên bút toán đã bị đảo (vd `27728` `#163563` — bấm ⇒ cửa trả lỗi "đã đảo")"*.
- [`BG-054`](BG-054-ban-giao-wo-023-phan-a-b.md) mục yếu **2**: *"Một màn mới thêm trình nghe phím mà quên hỏi `HT.nuot_phim` sẽ lọt — ⛔ có cổng quét"*.
- ⭐ **`fls-ba` đo lại 05/10** *(`Đ1` — đọc mã @ `12b7230`; sổ thật chỉ `SELECT` qua `docker exec fls-pg-1 psql`)*:

| Phép đo | Kết quả |
|---|---|
| `grep -rl FLS-DQ-FAILED fls tools` | **3** tệp: `bao.py` · `ghi_tay.py` · `goi_cua.js` ⇒ **0** cổng `ACC-1…4` ném mã này |
| lớp mang `ma = "FLS-DQ-FAILED"` ở `ghi_tay.py` | **5**: `LoiGhi` gốc `:106` · `ThieuLyDo` `:213` · `KhacTienTe` `:243` · `LechTong` `:249` · `ChuaDuyet` `:255` *(lớp gốc gồm cả `adj_id=… da bi dao truoc do` `:535` và thiếu `actor`)* |
| `grep -c cho_ghi fls/web/tep/man_f01_ghep.js` | **0** ⟷ `man_f01_lenh.js` `_chan_ghi` `:61` · `man_f02.js` `cho_ghi` `:94` *(nút `Đảo` `:1828` ⛔ hỏi)* |
| sổ thật `fls_adjustment` | **4.428** bút toán · bản đảo **2** · **đã bị đảo** **2** *(`#163563` `cdt1` · `#163565` `hd`, dòng `27728`, `sua_tay`)* |
| trình nghe phím `fls/web/tep/man_*.js` | `addEventListener('keydown'` **3** — cả 3 hỏi `nuot_phim` · `.onkeydown =` **2** — **⛔ hỏi** *(`man_f02.js:848` · `:2018`; `BG-054` chỉ `grep` dạng thứ nhất)* |

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/06_SCREEN_SPEC.md` | ⭐ `§4.5 ⓦ` **⑧** *(cả năm mục — luật, chuỗi nguyên văn, tầm)* | **v4.23** |
| `02_BA/06_SCREEN_SPEC.md` | `§4.5 ⓦ` ② *(bảng chế độ chỉ đọc — hàng đính chính v4.23)* · `ⓦ` ⑥ *(khuôn "giữ nếu `itl_id` còn" cho ⓔ)* · dòng *"F02 · hoàn tác"* *(chip `bản đảo của #N`)* | v4.23 |
| `02_BA/07_API_CONTRACT.md` | §5 dòng `FLS-DQ-FAILED` *(đính chính mô tả)* | **v3.13** |
| `02_BA/08_NFR.md` | `NFR-I03` *(chỉ đọc ⇒ đường ghi `405` — ⛔ đổi)* | như nay |
| `02_BA/06_SCREEN_SPEC.md` ⭐ *(`(f)`, 06/10)* | `§4.5 ⓦ` **⑨** *(kết quả cú `Gán` thuộc lệnh của nó — bảng ⓐ ⓑ ⓒ; áp **khi tái hiện được**)* | **v4.24** |
| `01_Orchestrator/handoff/KQ-061-kiem-wo-023-bg-052-den-bg-059.md` ⭐ | lăng kính **Logic** ⓖ *(nghi chưa chứng — đọc mã `man_f01_ghep.js:747-783`)* | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| **(a)** `fls/web/tep/goi_cua.js::CAU['FLS-DQ-FAILED']` — `cau` + `lam_gi` **nguyên văn** `BA-06` v4.23 `ⓦ` ⑧ ⓐ. `fls/api/bao.py::MA_LOI['FLS-DQ-FAILED']` — chuỗi mô tả theo `BA-07` v3.13 §5 *(HTTP **422** ⛔ đổi)* | ⛔ đổi mã, ⛔ tách mã theo lớp, ⛔ dịch `chi_tiet` *(chuỗi máy giữ nguyên)*; ⛔ đổi câu mã khác |
| **(b)** chế độ chỉ đọc *(`FLS_PHIEN.cho_ghi` ⛔ `true`)*: `F01G` nút `Gán` *(mọi nhãn: `Gán` · `Xác nhận gán …` · `Đổi sang giao dịch đã chọn`)* + `Bỏ gán` + phím `Enter` gán; `F02` ⑥ nút `Đảo` ⇒ **khoá** + `title` = câu `405` của `_chan_ghi` **một hằng dùng chung** *(⛔ bản gõ thứ hai — Dev chọn chỗ đặt)* | ⛔ đổi câu `405`, ⛔ đổi `NFR-I03`, ⛔ khoá nút **đọc** *(`ⓦ` ② giữ)*; ⛔ chạm `F01L` *(đã đúng)* |
| **(c)** `F02` ⑥: bút toán có bút toán khác **cùng** `but_toan[]` mang `reversal_of` = `adj_id` của nó ⇒ chip `chip lock` *"đã bị đảo bởi #M"* thay nút | ⛔ trường cửa mới, ⛔ đổi `doc_bao_cao.py`, ⛔ đổi luật ai được đảo *(`SM-I03`)* |
| **(d)** một bài `tests/web/` **tĩnh**: mọi `addEventListener('keydown'` **và** `.onkeydown =` trong `fls/web/tep/man_*.js` hỏi `HT.nuot_phim(e)` **hoặc** mang chú thích miễn **kèm lý do đo được** ngay trên dòng; hai chỗ `man_f02.js:848` · `:2018` ⇒ hỏi, **hoặc** Dev đo *(Chrome, `HT.mo` khi ô ấy đang focus)* rồi ghi chú thích miễn | ⛔ đổi `hop_thoai.js` *(cơ chế dấu `e._hop_thoai` — giới hạn đã biết, `ⓦ` ⑧)* |
| **(e)** `F01G` `ST.dg_mo` lưu `itl_id`, ⛔ chỉ số *(`man_f01_ghep.js:182` · `:501` · `:519` · `:583`)*; danh sách bị lượt mới thay ⇒ **giữ** nếu `itl_id` còn, **bỏ** nếu ⛔ *(khuôn `ⓦ` ⑥)* | ⛔ đổi diễn giải, ⛔ đổi `chon_itl` |
| ⭐ **(f)** *(06/10 — `KQ-061` Logic ⓖ, **nghi chưa chứng**; `BA-06` **v4.24** `ⓦ` ⑨)*: **TÁI HIỆN TRƯỚC.** Chrome **8099** kho TEST, chuột/phím `Input.*`: mở lệnh `A`, chọn ứng viên, `Gán`; CDP giữ `POST */match`; phím `j` *(hay chuột)* sang lệnh `B`, chọn một ứng viên ở `B`; ⓐ thả `200` ⇒ ghi `ST.mo` + `chon_itl` + lệnh đang hiện **sau** khi thả; ⓑ lượt khác: thả lỗi *(`Fetch.failRequest` hay `422` thật)* ⇒ quay lại `A` ⇒ có thấy dòng lỗi không; ⓒ trong lúc giữ: nút `Gán` của `B` khoá ⛔ / có lý do ⛔. **Tái hiện được** ⇒ sửa theo ⑨ ⓐ ⓑ ⓒ *(`gan` nhớ lệnh của chính nó; `loi_gan` ⛔ xoá trước lần vẽ đầu)*. **⛔ tái hiện được** sau ≥ 3 lượt *(mỗi lượt dán bằng chứng)* ⇒ `BG` ghi *"⛔ tái hiện — <lý do đo được>"*, **⛔ sửa** | ⛔ khoá phím đổi lệnh trong lúc chờ cửa *(⛔ trong ⑨ — người được đi tiếp)*. ⛔ đổi `ⓦ` ⑥ *(lựa chọn theo `itl_id`)*. ⛔ tự thử lại cú `Gán` |
| **Bài thử của Dev** *(`tests/web/**`, `tests/api/**`)*: một bài mỗi AC, **chứng minh ĐỎ trước** trên mã @ nhận phiếu | ⛔ sửa `tests/nghiem_thu/**` *(việc `fls-test`)*; nếu bài nghiệm thu nào ghim chuỗi `Cổng hôm nay` / `Cổng kiểm chất lượng` ⇒ `HOI`, ⛔ tự sửa |
| | `GAP-API-12` *(`la_ban_dao` nối theo `at` — nợ)* · `GAP-SCR-35` *(`F04` `S.chup` — nợ)* · migration nào |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(a)* | `LoiCua('FLS-DQ-FAILED', …)` ⇒ `cau`/`lam_gi` trùng **từng byte** hai chuỗi `BA-06` v4.23 `ⓦ` ⑧ ⓐ; chuỗi *"Cổng hôm nay"* **0** lần trong `goi_cua.js`; cú `Gán` cặp khác tiền tệ qua **cửa thật** kho TEST *(ca `M4` của `BG-053` `AC-10`)* ⇒ `#ghep-goc` chứa `lam_gi` mới **và** `chi_tiet` máy *(chữ nhỏ)* | bài Dev nạp `goi_cua.js` thật + cửa thật kho TEST | giữ `lam_gi` cũ ⇒ **ĐỎ**; bỏ `chi_tiet` khỏi dòng lỗi ⇒ **ĐỎ** |
| AC-2 *(a)* | `bao.py::MA_LOI['FLS-DQ-FAILED']` = `(422, <mô tả>)` — `<mô tả>` ⛔ chứa `ACC` | bài Dev | trả `ACC-1…4` ⇒ **ĐỎ**; đổi `422` ⇒ **ĐỎ** |
| AC-3 *(b)* | `cho_ghi` ⛔ `true`: nút `Gán` *(cả ba nhãn)* + `Bỏ gán` `F01G` + nút `Đảo` `F02` có `disabled`, `title` = **cùng** chuỗi `_chan_ghi` `man_f01_lenh.js:63-64` *(so từng byte, **một** nguồn)*; bấm chuột + phím `Enter` ⇒ **0** `POST`, hộp `Đảo` **0** lần mở. `cho_ghi = true` ⇒ ba nút **bấm được** như nay *(mẫu số)* | bài Dev cửa giả đếm `POST`; ⭐ Chrome **8097** sổ thật **chỉ đọc** *(⛔ 8088)*: mở `PM01698-1` *(hay lệnh đầu chip `Chưa gán`)* + dòng `27728` ⇒ đếm `disabled` + **0** `POST` | bỏ phép hỏi `cho_ghi` ở một nút ⇒ **ĐỎ** đúng nút ấy; gõ chuỗi `405` lần thứ hai ⇒ **ĐỎ** *(bài so nguồn)* |
| AC-4 *(c)* | `F02` ⑥ dòng có bút toán `A` và bản đảo `B` *(`B.reversal_of = A`)* ⇒ hàng `A` mang chip *"đã bị đảo bởi #B"* lớp `chip lock`, **0** nút `Đảo`; hàng `B` giữ chip *"bản đảo của #A"*; bút toán chưa bị đảo giữ nút *(mẫu số)*. Sổ thật chỉ đọc dòng `27728` ⇒ **0** nút `Đảo` trên **4** hàng ⑥ *(2 bản đảo + 2 đã bị đảo)* | bài Dev khuôn `but_toan[]` **từ cửa thật** kho TEST *(đảo một bút toán `sua_tay`)*; Chrome **8097** `F02.mo_drawer(27728)` | bỏ phép tìm `reversal_of` ⇒ **ĐỎ**; tìm nhầm theo `field` thay `adj_id` ⇒ **ĐỎ** *(ca hai bút toán cùng ô)* |
| AC-5 *(d)* | bài tĩnh quét `fls/web/tep/man_*.js`: mỗi trình nghe phím *(cả hai dạng)* hỏi `nuot_phim` **hoặc** mang chú thích miễn có lý do ⇒ xanh trên mã giao; bài in **danh sách** trình nghe đã quét *(số = số `grep` hai dạng)* | `pytest tests/web/<bài>` | thêm một `addEventListener('keydown'` ⛔ hỏi vào bản sao tạm ⇒ **ĐỎ**; thêm một `.onkeydown =` ⛔ hỏi ⇒ **ĐỎ** *(dạng `BG-054` sót)* |
| AC-6 *(e)* | mở rộng diễn giải hàng `itl_id = X`, lượt mới thay danh sách: `X` còn ⇒ **cùng** hàng `X` mở rộng *(dù chỉ số đổi)*; `X` ⛔ còn ⇒ **0** hàng mở rộng | bài Dev cửa giả hai lượt, đổi thứ tự | lưu chỉ số ⇒ **ĐỎ** *(ca thứ tự đổi)* |
| ⭐ AC-9 *(f)* | ⓐ `BG` dán **kết quả tái hiện** *(Chrome 8099: lệnh hiện sau khi thả `200` · `chon_itl` của `B` · dòng lỗi khi quay lại `A` · trạng thái nút `Gán` của `B`)* — **có / ⛔** cho từng vế ⑨ ⓐ ⓑ ⓒ. ⓑ Vế **có** ⇒ bài DOM `man_f01_ghep.js` thật, cửa giả `/match` treo, phím `j` qua trình nghe `document` thật: thả `200` khi `ST.mo = B` ⇒ `ST.mo` **vẫn** `B`, `chon_itl` của `B` **giữ**, **0** lượt `mo_lenh` tự khởi; thả lỗi ⇒ mở lại `A` ⇒ `#ghep-goc` chứa *"Gán chưa xảy ra — Cửa lỗi:"* *(hay *"Chưa rõ gán…"* nếu `FLS-HET-GIO`)*, đổi lệnh lần nữa ⇒ mất; nút `Gán` của `B` trong lúc chờ có `title` *"Đang chờ máy trả lời cú Gán của lệnh <A>."*. **Mẫu số**: `ST.mo = A` lúc thả `200` ⇒ **sang** lệnh kế như nay. ⓒ Vế **⛔** ⇒ ⛔ bài, ⛔ sửa | Chrome CDP + bài `tests/web/` *(chỉ vế có)* | *(vế có)* giữ `_nguoi_mo(lenh_ke_tiep)` vô điều kiện ⇒ **ĐỎ**; xoá `loi_gan` khi đổi lệnh trước lần vẽ ⇒ **ĐỎ**; chặn cả ca `ST.mo = A` ⇒ mẫu số **ĐỎ** |
| AC-7 | `pytest` toàn bộ: **0** đỏ **ngoài** danh sách `XPASS(strict)` mà `KQ` của `WO-023` để lại *(`BG` liệt kê từng tên)* · `lint-imports` **9 kept 0 broken** · `soi_bang_tuyen` khớp · `kiem_thuyet_minh` khớp · `test_luat_ky_hieu_man_hinh.py` + `test_moi_token_deu_duoc_khai.py` xanh *(chip mới ⛔ lớp CSS mới, ⛔ token mới)* · `kiem_tai_lieu` ĐẠT | lệnh ở `CLAUDE.md` | — |
| AC-8 | `BG` ghi `kiem_so_song`: nền đầu phiếu ⟷ cuối phiếu, ⛔ đỏ mới; ⛔ `dong_bo --ghi`. `khop_owner --kiem` chạy **sau** commit giấy cuối *(hay ghi "đo trên `<hash>`, trước tờ")* | đọc `BG` | — |

## Màn hình *(chạm UI — dòng lỗi một cú ghi · khối hành động `F01G` · khối ⑥ `F02`)*
- Thiết kế: `02_BA/06_SCREEN_SPEC.md` v4.23 `§4.5 ⓦ` ⑧ *(⛔ wireframe mới — mọi phần tử đã có lớp: `b`/`b tiny` `disabled`, `chip lock`, dòng lỗi ca ⑤)*.

| Trạng thái | Hiện gì |
|---|---|
| tải | như nay *(khối ⑥ / vùng ứng viên — ⛔ đổi)* |
| rỗng | ⑥ ⛔ bút toán ⇒ *"chưa ai gõ tay ô nào của dòng này"* *(như nay)* |
| lỗi | cửa ghi `422` `FLS-DQ-FAILED` ⇒ dòng lỗi *"<Việc> chưa xảy ra — Cửa lỗi: Phép ghi này trái một luật kiểm của cửa ghi nên máy chặn."* ＋ `lam_gi` mới ＋ `chi_tiet` chữ nhỏ |
| mất kết nối | như nay *(`FLS-MAT-KET-NOI` / `FLS-HET-GIO` — `ⓕ3` v4.23)* |
| có dữ liệu | chỉ đọc ⇒ nút ghi xám + `title` `405`; bút toán đã bị đảo ⇒ chip *"đã bị đảo bởi #M"* |

## Dữ liệu
- Bảng/cột chạm: ⛔ *(chỉ đọc `but_toan[]` cửa đã trả)*.
- Ghi kho THẬT: `KHONG` *(Chrome sổ thật **8097** ⛔ `--cho-ghi`; ⛔ 8088)*.
- Số dòng dự kiến chạm *(đã đếm)*: **0** ghi. Hiển thị đổi: sổ thật **2** nút `Đảo` ⇒ chip *(`#163563` · `#163565`)*; chế độ chỉ đọc **4.426** nút `Đảo` + mọi `Gán`/`Bỏ gán` `F01G` ⇒ khoá.

## Câu còn treo
- `không có` — năm mục là chữ màn in + hành vi trạng thái màn trong thẩm quyền spec; ⛔ câu nghiệp vụ *(⛔ đổi con số nào, ⛔ đổi việc kế toán, ⛔ đổi luật ai được đảo)*.

## Rủi ro
1. **Bài cũ ghim chữ cũ.** Bài nào *(Dev hay nghiệm thu)* so nguyên văn *"Cổng kiểm chất lượng không đạt…"* / *"Cổng hôm nay"* sẽ đỏ — Dev `grep tests/` trước, ghi `BG`; bài `tests/nghiem_thu/**` ⇒ `HOI`, ⛔ sửa.
2. **`chi_tiet` là chữ máy không dấu** *(vd `dong so la 'USD' nhung dong lenh la ['VND']`)* — `lam_gi` mới dựa vào nó. Đủ đọc hôm nay; dịch là phiếu khác *(⛔ trong phiếu này)*.
3. **Khoá ở chỉ đọc là lớp màn** — cửa vẫn `405` *(`NFR-I03`)*; một màn mới quên khoá thì cửa vẫn chặn. ⛔ Có cổng quét *"mọi nút gọi `FLS.ghi` hỏi `cho_ghi`"* — nếu Dev thấy rẻ, gom vào bài (d) và ghi `BG`; ⛔ bắt buộc.
4. **ⓒ đọc trong một mảng** — `but_toan[]` hôm nay chở **mọi** bút toán của dòng *(`doc_bao_cao.py:478-482`)*; nếu mai cửa phân trang mảng ấy, phép tìm bản đảo sẽ hụt ⇒ chú thích ở mã.

## Changelog
- 2026-10-06 · `fls-ba` · ⭐ **mở rộng** sau nghiệm thu PO `WO-023` *(chưa ai nhận ⇒ vẫn **vòng 1**)*: thêm **`(f)`** — nghi ⓖ của `KQ-061` *(cú `Gán` đang chờ mà người đổi lệnh ⇒ cửa trả kéo màn sang lệnh kế của lệnh cũ / lỗi bị xoá trước khi ai thấy)* thành việc **tái hiện trước, sửa sau** *(`AC-9`)*; spec `BA-06` **v4.24** `ⓦ` ⑨. Vì sao vào đây ⛔ phiếu mới: cùng tệp `man_f01_ghep.js` *(ⓑ ⓔ của phiếu)*, cùng lớp *"màn nói đúng điều cửa vừa làm"*, ⛔ chạm ghi sai *(cửa chặn đúng)*. Thứ tự: **sau** `WO-062` *(cùng `man_f02.js`)*.
- 2026-10-05 · `fls-ba` · phát phiếu từ phát hiện ngoài phạm vi `WO-023` *(`BG-052` mục 5/6 · `BG-053` mục 3 · `BG-054` mục 2 · `BG-057` mục 5)*; spec `BA-06` **v4.23** `ⓦ` ⑧ · `BA-07` **v3.13** §5. Nợ ⛔ vào phiếu: `GAP-API-12` · dấu `e._hop_thoai` *(giới hạn đã biết)* · `GAP-SCR-35`.
