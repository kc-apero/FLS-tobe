# WO-045 — Lượt tải **mới nhất** thắng ở mọi màn còn lại · `Xem thêm` / `Tìm tiền` của `F01L` ⛔ bị khoá ở máy chỉ đọc · nút `Thử lại` của `②b`

| | |
|---|---|
| **Trạng thái** | ✅ **`DONG`** *(05/10 khuya — `fls-ba` nghiệm thu PO: [`KQ-050`](KQ-050-kiem-bg-048.md) ✅ ĐẠT **13/13**, 0 `CHAN` / `NANG` trong phạm vi; ⭐ ① đo: mã khi nhận gửi cặp sai **cùng VND trong dung sai** ⇒ cửa ghi **`200`** *(kho TEST `link_id 4163`)*, mã mới ⛔ gửi; bảng đối chiếu ý owner ở mục **Nghiệm thu PO** cuối phiếu; `F-1` ⇒ [`WO-051`](WO-051-trang-hang-cho-vnd-104-giay-va-khung-cho-xem-them.md) · `F-2` · `F-3` *(nâng `NANG`)* · `F-4` ⇒ [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) `(h)` ⓔ · `(i)` · `(j)`)* · ~~⭐ **`CHO_TEST`**~~ *(`fls-dev` 05/10 — [`BG-048`](BG-048-ban-giao-wo-045.md) @ `2b804e3`; [`HOI-049`](HOI-049-chu-so-trong-title-va-lop-nut-thu-lai.md) `KHONG_CHAN`)* · ~~`DANG_LAM`~~ *(`fls-dev` nhận 05/10 — cổng vào: git `14a4b72` = `origin`, mã `fls/**` = `db0adae`; `BA-06` **v4.20**; nền đo lại `pytest` **2302 passed, 4 xfailed** · `kiem_so_song` **55** — khớp)* · ~~`MO`~~ · ⭐ **SẴN SÀNG** *(05/10 — `WO-042` ✅ `DONG`, `KQ-046` ĐẠT 12/12; nền đo lại ở mục **Nền khi nhận**; ⭐ thêm ⑤ `KQ-046 F-3` — `BA-06` **v4.20** `ⓦ` ③)* · ~~⏳ chờ `WO-042` `DONG`~~ *(cùng hai tệp `man_f01_ghep.js` · `man_f01_lenh.js`; dựng trên cách chống chồng `_luot` của `WO-042` — nhận trước là sửa trên một nền đang kiểm)* · ưu tiên **CAO** — làm **TRƯỚC** [`WO-015`](WO-015-so-actor-phu-moi-bang-va-luat-uat-ascii.md) và [`WO-023`](WO-023-hop-modal-hop-cho-cua-va-ma-409.md) *(→ `DANG_LAM` → `CHO_TEST` → `DONG` / `TRA_LAI`)* |
| **Phát bởi** | `fls-ba` · 2026-10-05 |
| **Nhận** | `fls-dev` |
| **Vòng** | `1` |
| **Thứ tự với phiếu khác** | **Sau** [`WO-042`](WO-042-doi-chip-khi-dang-tai-va-mot-tap-ky-tu-trang.md) *(✅ `DONG` 05/10 — ~~`CHO_TEST` `BG-044`~~)*. **Trước** [`WO-047`](WO-047-mot-tap-ky-tu-cho-phep-so-tien-te-con-lai.md) *(THẤP — phiếu nhỏ, khác tệp)* · `WO-015` *(THẤP)* + `WO-023` *(THẤP — chạm lại cùng tệp; bài thử hộp của nó nên dựng trên màn đã chống chồng)* |

## Vì sao
- Tác vụ / mốc phục vụ *(`09_MILESTONES_HAI_TAC_VU`)*: **mốc `B` cổng `B5`** *(kế toán đi hết một vòng ghép thật)* — ①②⑤ nằm trên hai màn của đúng vòng ấy *(`F01G` gán lệnh ↔ giao dịch · `F01L` lằn lệnh chi, chung tab `② Hàng chờ`)*; ③ màn hàng chờ `F01`; ④ màn nạp `F04` *(mốc `A`)*.
- Mắt xích người được xoá *(`05_ROLES_HANDOFF` §2)*: ⛔ xoá thêm; phiếu này giữ mắt xích **"ghép PM ↔ tiền"** đã lên FLS **⛔ thua Sheets** — trên Sheets một bộ lọc ⛔ bao giờ trộn hai kết quả, và người chỉ xem ⛔ bao giờ bị giấu 92% một danh sách. `QĐ-ITL-27` *(2–3 kế toán, kiểm soát nằm trong máy)*: màn in sai / in thiếu im lặng là dạy người **tự đếm lại**.

### Vì sao ưu tiên **CAO**, và thứ tự **bên trong** theo tầm *(PO)*
| # | Hại hôm nay nếu ⛔ làm | Ai bị | Chạm GHI? |
|---|---|---|:-:|
| ① `F01G` `mo_lenh` · `tai_toan_so` | đổi lệnh bằng `j`/`k`/`↓` *(phím `NFR-I24` — cách kế toán **đi** qua danh sách)* hoặc gõ ô tìm ⇒ ứng viên của lệnh **trước** hiện dưới lệnh **đang mở**; `gan` *(`man_f01_ghep.js:653-661`)* gửi `itl_id` lấy từ chính danh sách ấy kèm `ma_lenh` đang mở | kế toán ghép thật | ✅ **sát** — cửa ghi chặn lệch tiền / khác tệ, cặp sai **trong dung sai** ⛔ bị chặn *(chưa đo)* |
| ② `F01L` lưới + `Xem thêm` + khoá chỉ đọc | ⓐ đổi rổ / lọc lúc lưới đang tải ⇒ lưới **trộn hai rổ** *(cùng hình `F-3`)*; ⓑ `Xem thêm` bấm hai lần ⇒ hàng lặp; ⓒ ở chế độ **chỉ đọc** *(mặc định — `NFR-I03`)* `Xem thêm` + `Tìm tiền` bị khoá ⇒ mỗi rổ chỉ thấy **50** dòng đầu: `may` chưa nhận theo lô **50 / 120** · `nguoi` **50 / 616** · `khong` **50 / 801** *(`/ro` sổ thật — `BG-044` `AC-7`, 8097 chỉ đọc 05/10)*, màn ⛔ nói còn | ⓐⓑ kế toán · ⓒ **mọi** người mở sổ thật ⛔ bật ghi: owner xem & quyết, kế toán tra trước khi ghép, mọi phép đo `fls-test`/`fls-ba` trên 8088 | ⛔ |
| ③ `F01` hàng chờ | đổi lọc tiền tệ / `den_pct` lúc đang tải ⇒ lọc cũ thắng; `Xem thêm` hai lần ⇒ hàng lặp | kế toán | ⛔ |
| ④ `F04` ảnh chụp | mở hai ảnh nhanh ⇒ ảnh **trước** thắng; màn và `S.chup` **nhất quán** với nhau *(`Nhận` gửi đúng ảnh đang hiện)* — sai so với cú bấm cuối | người nạp | gián tiếp |
| `(e)` nút `Thử lại` `②b` | lỗi / mất kết nối ⇒ lối ra duy nhất là bấm lại chip, màn ⛔ nói | kế toán | ⛔ |
| ⭐ ⑤ `F01` thanh lằn *(v4.20)* | rê chuột lên `Theo LỆNH CHI` ⇒ *"**1.345** dòng lệnh đang chờ tiền"* — số đo 09/09, sổ thật hôm nay `/ro` `tong` **1.601** *(⛔ cùng định nghĩa)*; màn in con số ⛔ ai đo lại | mọi người mở `F01` | ⛔ — gom vào đây vì **cùng tệp** `man_f01.js` *(③)*, một dòng chữ; ⛔ đáng một vòng `WO → BG → KQ` riêng |

⛔ **Không** xếp trên **CAO**: hôm nay **0** cú ghi sai đã thấy *(cửa ghi chặn mọi cặp lệch tiền / khác tệ; ① chưa đo được cặp nào lọt)*; hại là **đọc sai / đọc thiếu**. ⛔ **Dưới** CAO: ① chạm sát một cú GHI của vòng ghép thật, ② ⓒ giấu **58–94%** mỗi rổ ở chế độ mặc định — cao hơn `WO-015` *(⛔ con số nào đổi)* và `WO-023` *(cách hộp đóng mở)*.

⭐ **Vì sao gom một phiếu** *(⛔ năm phiếu)*: một luật *(`BA-06` v4.19 `§4.5 ⓦ` ①)* + một cách làm Dev đã có sẵn *(`_luot` của `WO-042`)*; mỗi chỗ là vài dòng. Năm vòng `WO → BG → KQ` *(mỗi vòng ~6–7 phút `pytest` + Chrome)* đắt hơn phần việc. ⛔ Vướng một chỗ ⇒ Dev mở `HOI` cho chỗ ấy và bàn giao phần còn lại **theo thứ tự ①→④** — ⛔ giữ ① chờ ④.

## Căn cứ
- [`BG-044`](BG-044-ban-giao-wo-042.md) *(`fls-dev` 05/10)* mục **`(d)`** — bảng **21** hàm `await` cửa rồi ghi trạng thái chung *(**5** có chống, **16** ⛔ — đọc mã, ⛔ đo)* + đề xuất *"**#6** là hình `F-3` y hệt trên `F01L`; **#2/#3** có thể làm `Gán` ghi đúng cặp mà màn đang hiện sai ứng viên"* · mục **Phát hiện ngoài phạm vi** *(`Xem thêm` `F01L` bị khoá ở máy chỉ đọc, 8097 đo `{co: true, disabled: true, title: "⛔ Cửa đang chạy ở chế độ CHỈ ĐỌC…"}`)*.
- [`HOI-043`](HOI-043-ba-bai-kq041-khong-the-xpass-va-nut-thu-lai.md) **Q4** + **`TL-043`** *(`fls-ba` 05/10)* — `②b` ⛔ bao giờ có nút `Thử lại`.
- `fls-ba` đọc lại mã 05/10 *(`Đ1`)*: `man_f01_lenh.js:69` `_nut` ⇒ `_chan_ghi` `:61` khoá **mọi** nút qua `_nut`, gồm `Xem thêm` `:544` và `Tìm tiền` `:491`; lưới `limit=50` `:554`; `man_f01.js:168` `Xem thêm` gắn `onclick` thẳng *(⛔ khoá — lệch giữa hai màn)*; `man_f01_ghep.js:1013-1043` `mo_lenh` đặt `ST.mo = ma` **trước** `await`, gán `ST.ung_vien` **sau** ⛔ kiểm lượt; `gan` `:653` gửi `/queue/{uv.itl_id}/match` `{pm_line_ids: [lenh.ma_lenh]}`.
- **`BA-08` `NFR-I03`** *(cửa mặc định chỉ đọc — luật về đường **ghi**)* · **`NFR-I24`** *(9 phím)* · **`QĐ-ITL-27`**.
- Quyết: **`fls-ba` trong thẩm quyền spec** *(hành vi trạng thái màn · màn khoá nút nào ở chế độ chỉ đọc — ⛔ đổi sổ, ⛔ tuyến mới, ⛔ khoá cửa mới, ⛔ token, ⛔ đổi `NFR-I03`)*. ⛔ câu nghiệp vụ.

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/06_SCREEN_SPEC.md` | ⭐ **§4.5 ⓦ** *(① bảng bốn ưu tiên · ② bảng thao tác ở chế độ chỉ đọc · ⭐ ③ `title` thanh lằn ⛔ số cứng — đoạn **v4.20**)* · **§4.5 ⓥ** bốn luật ①…④ + đoạn v4.19 *(① lượt bị thay được dừng ngay · ⑤ nút `Thử lại` `②b`)* | ⭐ **v4.20** *(③; ①② = v4.19)* |
| `02_BA/08_NFR.md` | `NFR-I03` · `NFR-I24` | hiện hành |
| `01_Orchestrator/handoff/BG-044-ban-giao-wo-042.md` | `(d)` bảng 21 hàm + *Phát hiện ngoài phạm vi* | — |
| `01_Orchestrator/handoff/HOI-043-…md` | `TL-043` | — |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| ⭐ **① `F01G`** `man_f01_ghep.js` — `mo_lenh` *(#2)* · `tai_toan_so` *(#3, gọi từ ô tìm + `mo_lenh`)*: kết quả của lượt **đã bị thay** *(lệnh khác / chữ tìm khác)* ⛔ vào `ST.ung_vien` / `ST.toan_so`, ⛔ vẽ; lượt mới nhất thắng *(`ⓥ` ①…④ áp cho trục **lệnh** + **chữ tìm**)* | ⛔ đổi `TRE_TIM` · ⛔ đổi cửa `itl-candidates` / `/so` · ⛔ `AbortController` / `goi_cua.js` |
| **② `F01L`** `man_f01_lenh.js` — ⓐ `ve_luoi` / `_ve_luoi` *(#6)* qua `_loc` *(`Xem <c> dòng` · `Quay lại` · `Bắt đầu tra` · lọc)*: lưới chỉ mang hàng của rổ / lọc **đang hiện** · ⓑ `Xem thêm` *(#7)*: ⛔ mở lượt thứ hai khi lượt trước còn bay · ⓒ chế độ chỉ đọc: `Xem thêm` + `Tìm tiền` **chạy**; trong hộp `Tìm tiền` nút `Ghép` **khoá** + câu `405` như nay *(bảng `ⓦ` ②)* | ⛔ đổi câu `405` · ⛔ đổi trang `limit=50` · ⛔ đổi `NFR-I03` / cửa *(đường ghi vẫn `405`)* · ⛔ lý do từng hàng *(`GAP-SCR-34`)* |
| **③ `F01`** `man_f01.js` — `ve_luoi` *(#10)* · `_xem_them` *(#11)* | ⛔ đổi năm hành động mỗi dòng · `_drawer_ghep` *(#12)* |
| **④ `F04`** `man_f04.js` — `_mo_chup` *(#17)* · `_ve_thu_tu` *(#18)*: màn + `S.chup` + `S.thu_tu` = ảnh bấm **cuối** | ⛔ `_soat` *(#19)* · `_nhan` *(#20)* — bấm **GHI** hai lần là lớp khác *(khoá nút chờ cửa ghi / `409` — `WO-023`)* · ⛔ #21 |
| **`(e)` `②b` nút `Thử lại`** *(`ⓥ` ⑤)*: lỗi + mất kết nối ⇒ nút `Thử lại` dưới câu lỗi *(lớp `b tiny` có sẵn)*; bấm ⇒ tải lại chip đang chọn, một lượt theo `ⓥ` | ⛔ đổi câu lỗi · ⛔ token / lớp CSS mới · ⛔ đổi `Artifacts/` |
| ⭐ **⑤ `F01` thanh lằn** *(`KQ-046 F-3`, `BA-06` v4.20 `ⓦ` ③)* — `man_f01.js` `_thanh_lan` *(`:766`)*: `title` nút `Theo LỆNH CHI` = `Lệnh chi đang chờ tiền — câu hỏi của việc (QĐ-ITL-122)` **nguyên văn**; ⛔ chữ số nào trong `title` hai nút | ⛔ đổi nhãn nút · ⛔ đổi `ST.lan` · ⛔ sửa chú thích bia `:756-758` *(số đo 09/09 — `Đ2`)* · ⛔ gọi cửa mới |
| **`(f)` Bài thử** `tests/web/**` *(+ `tests/api/**` nếu cần)* — một bài mỗi AC, **chứng minh ĐỎ trước** trên `HEAD` khi nhận; độ trễ **có kiểm soát** *(cửa giả chậm theo đường — ⛔ "bấm nhanh rồi mong")*; bài DOM chạy **mã màn thật** | ⛔ sửa `tests/nghiem_thu/**` · ⛔ #4 `gan` hai lần · #8 · #13 · #16 · #21 |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ *(phá gì thì phải đỏ)* |
|---|---|---|---|
| AC-1 *(① đổi lệnh)* | Bài DOM `man_f01_ghep.js` thật, cửa giả `itl-candidates` **chậm theo lệnh** *(lệnh `A` trả **sau** lệnh `B`)*: `mo_lenh(A)` rồi `mo_lenh(B)` khi `A` chưa về ⇒ sau khi **cả hai** xong: `ST.mo == B`; **mọi** `ST.ung_vien[i].itl_id` thuộc tập cửa trả cho `B` *(**0** của `A`)*; số hàng ứng viên trên DOM = số cửa trả cho `B` | bài DOM `tests/web/` | `mo_lenh` ⛔ kiểm lượt *(mã khi nhận)* ⇒ **ĐỎ** |
| AC-2 *(① ⭐ cú GHI)* | Cùng kịch bản AC-1, rồi `gan(the_lenh B)` với `ung_vien_chon = 0` ⇒ đúng **một** `FLS.ghi` tới `/queue/{X}/match` với `X` ∈ ứng viên của `B`, thân `{pm_line_ids: [B]}`; **0** cú ghi mang `itl_id` chỉ có ở `A` | bài DOM — đếm `FLS.ghi` giả | mã khi nhận ⇒ **ĐỎ** *(itl_id của `A` đi kèm `B`)* |
| AC-3 *(① ô tìm)* | `tai_toan_so` hai chữ `q1` rồi `q2`, lượt `q1` về **sau** ⇒ `ST.ung_vien` = cửa trả cho `q2`; mỗi lượt cách nhau > `TRE_TIM` *(đúng ca chú thích `:129-132` tự nêu)* | bài DOM | mã khi nhận ⇒ **ĐỎ** |
| AC-4 *(② ⓐ rổ)* | Bài DOM `man_f01_lenh.js` thật: lưới đang tải rổ `may` *(cửa chậm)*, bấm `Xem <c> dòng` rổ khác / `Quay lại` ⇒ sau khi cả hai xong: **mọi** hàng lưới thuộc rổ đang chọn *(**0** hàng rổ cũ)*; số hàng = cửa trả | bài DOM | `_ve_luoi` ⛔ kiểm lượt ⇒ **ĐỎ** |
| AC-5 *(② ⓑ `Xem thêm`)* | Bấm `Xem thêm` hai lần khi lượt đầu còn bay ⇒ đúng **một** `GET` trang kế; `pm_line_id` trên lưới **⛔ trùng** *(`len == len(set)`)* | bài DOM | mã khi nhận ⇒ **ĐỎ** *(hàng lặp)* |
| AC-6 *(② ⓒ chỉ đọc)* | `FLS_PHIEN.cho_ghi = false`: `Xem thêm` **⛔ `disabled`**, bấm ⇒ `GET` trang kế, lưới tăng; `Tìm tiền` ⛔ `disabled`, bấm ⇒ hộp mở, ứng viên hiện, nút `Ghép` trong hộp `disabled` + `title` câu `405` *(như nay)*; `Ghép N dòng tự chứng` · năm nút hàng `F01` vẫn `disabled`. `cho_ghi = true` ⇒ như nay | bài DOM — hai chế độ | khoá lại `Xem thêm` ⇒ **ĐỎ**; mở khoá `Ghép` ở chỉ đọc ⇒ **ĐỎ** |
| AC-7 *(③ `F01`)* | Đổi lọc tiền tệ khi lưới đang tải ⇒ lưới = lọc cuối; `_xem_them` hai lần ⇒ một `GET`, ⛔ hàng trùng | bài DOM | mã khi nhận ⇒ **ĐỎ** |
| AC-8 *(④ `F04`)* | `_mo_chup(c1)` rồi `_mo_chup(c2)`, `c1` về **sau** ⇒ `S.chup.chup_id == c2`, bốn ô đầu + `#nap-thu-tu` của `c2`; `S.thu_tu` của `c2` | bài DOM | mã khi nhận ⇒ **ĐỎ** |
| AC-9 *(`(e)` `Thử lại`)* | `②b` cửa trả lỗi ⇒ dưới `banner crit` có nút `Thử lại` *(`textContent` đúng chữ)*; bấm ⇒ đúng **một** lượt tải chip đang chọn; lượt ấy xanh ⇒ danh sách hiện, câu lỗi mất. Cùng với `FLS-MAT-KET-NOI` | bài DOM — hai ca | ⛔ nút ⇒ **ĐỎ**; bấm mở hai lượt ⇒ **ĐỎ** |
| AC-10 ⭐ *(Chrome — `②` ⓒ sổ thật)* | **8088 sổ thật CHỈ ĐỌC**, Chrome 1440×900, chuột thật *(`Input.dispatchMouseEvent`)*, chặn ⛔ `GET` nào khác: `F01L` ▸ `Xem <c> dòng` rổ `may` chưa nhận theo lô ⇒ bấm `Xem thêm` tới khi hết ⇒ số hàng lưới **=** `c` của `/ro` cùng lượt *(mong ≈ **120**, ⛔ **50**)*; `pm_line_id` ⛔ trùng; **0** `POST`; console **0** lỗi. Lặp với `Bắt đầu tra` *(rổ `nguoi`, `man_f01_lenh.js:221` — mong ≈ **616**)* | Chrome CDP | — |
| AC-11 *(Chrome — ① tay thật)* | **8099** kho TEST: mở lệnh `A`, giữ phản hồi `itl-candidates` của `A` ~2 s *(CDP `Fetch`)*, bấm `j` ⇒ lệnh `B`; thả `A` ⇒ danh sách ứng viên = của `B` *(đếm từ thân cửa thật cùng lượt)*. Đối chứng mã khi nhận *(worktree)* tái hiện **sai** | Chrome CDP | — |
| AC-13 *(⑤ thanh lằn)* | Bài DOM `man_f01.js` thật: `title` nút `Theo LỆNH CHI` **=** chuỗi `BA-06` v4.20 `ⓦ` ③ *(oracle **đọc thẳng** `06_SCREEN_SPEC.md`, ⛔ chép tay)*; `title` **cả hai** nút thanh lằn khớp `/[0-9]/` **0** lần | bài DOM `tests/web/` | trả lại `1.345` ⇒ **ĐỎ**; đổi một ký tự chuỗi ⇒ **ĐỎ** |
| AC-12 | Cổng `CLAUDE.md`: `pytest` **0** đỏ ngoài `xfail(strict)` đã khai · `lint-imports` **9 / 0** · `soi_bang_tuyen` **40** *(⛔ tuyến mới)* · `kiem_thuyet_minh` khớp · `kiem_tai_lieu` · `khop_owner --kiem` · `kiem_so_song` tách **nền đầu phiếu** ⟷ đỏ mới loại (c), bảng **cộng ra đúng tổng**; ⛔ `dong_bo --ghi` | lệnh + `BG` | — |

## Màn hình *(chạm UI)*
- Thiết kế: `02_BA/06_SCREEN_SPEC.md` **v4.19** `§4.5 ⓥ` *(đoạn v4.19)* + `§4.5 ⓦ`. Bản dựng `02_BA/Artifacts/` **⛔ đổi** *(⛔ token, ⛔ lớp CSS mới — nút `b tiny` đang có)*.

| Trạng thái | `F01G` ứng viên *(①)* | `F01L` lưới *(②)* | `②b` danh sách *(`(e)`)* |
|---|---|---|---|
| tải | giữ khung chờ tới khi lượt của lệnh **đang mở** xong | khung chờ tới khi lượt rổ **đang chọn** xong; `Xem thêm` ⛔ mở lượt hai | ⛔ đổi |
| rỗng | *"bật sẵn Toàn sổ"* như nay — **của lệnh đang mở** | câu rỗng của rổ đang chọn | ⛔ đổi |
| lỗi | lỗi của lượt **mới nhất** *(lỗi lượt cũ ⛔ hiện)* | `TT.loi` + `Thử lại` như nay — của lượt mới nhất | câu lỗi như nay **＋ nút `Thử lại`** |
| mất kết nối | như lỗi | như lỗi | `FLS-MAT-KET-NOI` như nay **＋ nút `Thử lại`** |
| có dữ liệu | chỉ ứng viên của `ST.mo` | chỉ hàng rổ đang chọn, ⛔ trùng; ở chỉ đọc vẫn lật trang được tới hết | ⛔ đổi |

## Dữ liệu
- Bảng/cột chạm: **⛔ bảng nào** — chỉ đọc qua cửa có sẵn *(`lenh-cho` · `lenh-cho/ro` · `itl-candidates` · `/so` · `/queue` · `/chup/*`)*. ⛔ tuyến mới, ⛔ khoá mới.
- Ghi kho THẬT: **`KHONG`**. Máy **8088** **CHỈ ĐỌC** *(chỉ `GET` cho `AC-10`)*. Mọi cú ghi *(nếu bài cửa cần dựng ca)* trên **kho TEST** qua **8099** / bài thử.
- Số dòng sổ thật đổi *(đã đếm — `fls-ba` 05/10)*: **0** — phiếu đổi **cái màn in**, ⛔ đổi sổ. ⇒ Báo động hiếm: ⛔ áp.

## Nền khi nhận *(`fls-ba` chép 05/10 — Dev đo lại ở cổng vào, ⛔ tin)*
| Cổng | Nền | Nguồn |
|---|---|---|
| git | `origin/feat/p2-oracle-parity` — commit giấy `fls-ba` nghiệm thu `WO-042` *(sau `47e9fa4` `KQ-046`)*; mã `fls/**` cuối = `db0adae` *(`WO-042`, ✅ `DONG`)*; `tests/nghiem_thu/` cuối = `47e9fa4` | `git log` |
| `pytest` | ⭐ **`2302 passed, 4 xfailed`** *(`KQ-046` đo cuối lượt @ `47e9fa4`; 4 = 3 `kq021` của `WO-023` ＋ `kq046::test_F1_*` của `WO-047` — **cả bốn** vẫn `xfail` sau phiếu này)* · ~~`BG-044`: 2297 passed, 6 xfailed~~ | `KQ-046` |
| `kiem_so_song` | **55** *(`KQ-046` — nền 50 ＋ 5 loại (c) của `WO-042`, tên trùng)*; `fls-ba` chạy lại sau tờ giấy nghiệm thu 05/10 — nhật ký §5 | `KQ-046` · lệnh |
| version spec | `BA-06` **v4.20** · `BA-07` **v3.12** *(⛔ chạm — của `WO-047`)* · `BA-08` hiện hành | header tệp |
| sổ thật | `/ro` *(`BG-044` `AC-7`, 8097)*: `may` **184** · `nguoi` **616** · `khong` **801** · `tu_chung` **64** · `tong` **1.601**; `may − tu_chung` **120** | `BG-044` |

## Câu còn treo
- ⛔ câu mới cho owner. `Q-FX-1` · `Q-TIEN-1` · `GAP-SCR-33` · `GAP-SCR-26` vẫn treo — ⛔ chặn: phiếu này ⛔ đổi luật ghép, luật in tiền hay nguồn con số; chỉ đổi **lượt nào được vẽ** và **nút nào bị khoá thừa**.
- ⚠ ① *"cặp sai trong dung sai có lọt cửa ghi ⛔"* **chưa đo** — `AC-2` chặn nó ở **màn** *(⛔ cú ghi nào mang `itl_id` của lệnh khác)*, nên ⛔ cần biết trước.

## Rủi ro
1. **Nền đang kiểm** — `WO-042` còn `CHO_TEST`; nếu `KQ` trả `TRƯỢT` mã ở `_luot`, phiếu này dựng trên nền đổi ⇒ chờ `DONG` *(trạng thái phiếu đã ghi)*.
2. **Năm chỗ, một luật** — dễ làm ① ② rồi để ③ ④ *"chưa kịp"*; `BG` phải có **một** bài đỏ-trước-xanh-sau cho **mỗi** AC-1…AC-9, thiếu ⇒ `KQ` `TRƯỢT`.
3. **Mở khoá nhầm nút ghi** ở chế độ chỉ đọc *(② ⓒ)* — cửa vẫn trả `405` *(⛔ ghi được)*, nhưng màn sẽ hứa điều nó ⛔ làm ⇒ `AC-6` đỏ chiều ngược.

## Đính chính `TL-049` *(2026-10-05, `fls-ba` — ⛔ viết lại dòng trên; đọc các dòng ấy theo bảng này)*
| Chỗ | Viết ở trên | Đọc là | Vì sao |
|---|---|---|---|
| `AC-13` vế hai | *"`title` **cả hai** nút thanh lằn khớp `/[0-9]/` **0** lần"* | bỏ mọi `QĐ-ITL-\d+` khỏi `title` **rồi** đếm `/[0-9]/` ⇒ **0** *(đúng bài `test_AC13_title_HAI_nut_KHONG_chu_so_ngoai_ma_quyet_dinh` của `BG-048`)* | chuỗi ⓐ mà chính `AC-13` vế một đòi mang `QĐ-ITL-122` = **3** chữ số ⇒ hai vế ⛔ thể cùng xanh nguyên văn; luật `ⓦ` ③ cấm **số đo**, mã quyết định là **tên** — `BA-06` **v4.21** `ⓦ` ③ |
| Phạm vi `(e)` · spec `ⓥ` ⑤ | *"lớp `b tiny` có sẵn"* ＋ spec v4.19 *"cùng dáng nút của khung `TT.chay`"* | lớp **`b tiny`** — ⛔ dáng `TT.loi` *(lớp `b`)* | vế `TT.chay` là lỗi viết spec — `BA-06` **v4.21** `ⓥ` ⑤ |

⇒ Mã `2b804e3` **đúng** cả hai; **⛔ vòng 2**. Mục yếu `BG-048` ②③ ⇒ `WO-023` `(h)` · ⑤ ⇒ `GAP-SCR-35` *(`TL-049`)* — **⛔** là AC của phiếu này.

## Nghiệm thu PO *(`fls-ba` · 2026-10-05 khuya — đọc `KQ-050` 13/13)*

Đối chiếu **ý owner** *(⛔ chỉ AC)*: phiếu này phải làm cho **thứ người đang nhìn là thứ máy sẽ ghi** — ứng viên dưới lệnh đang mở là của **chính** lệnh ấy, nên cú `Gán` ⛔ bao giờ mang dòng tiền của lệnh trước; người chỉ xem *(owner, kế toán tra trước khi ghép)* thấy **trọn** danh sách, ⛔ 50 dòng đầu; và màn ⛔ in con số ⛔ ai đo lại.

| Ý owner / spec | Lời gốc | Đo được *(`KQ-050`)* | Khớp |
|---|---|---|:-:|
| ⭐ Cú `Gán` ⛔ mang dòng tiền của lệnh **khác** — màn là chốt chặn | `BA-06` v4.19 `ⓦ` ① · `QĐ-ITL-27` *(kiểm soát nằm trong máy)* | ① Test **tự dựng** ca mạnh hơn `BG`: hai lệnh **cùng VND**, cặp sai **trong dung sai**. Mã khi nhận ⇒ `POST /queue/4161/match` ⇒ cửa ghi **`200`** *(một mối nối sai vào kho TEST — để làm vết)*; mã mới ⇒ `POST /queue/4168/match` đúng lệnh đang mở ⇒ **0** mối nối sai. Câu treo của phiếu *("cặp sai trong dung sai có lọt cửa ghi ⛔ — chưa đo")* **đã đo: LỌT** ⇒ màn là chốt **duy nhất**, và nay chặn | ✅ |
| Người chỉ xem thấy **trọn** danh sách | `BA-06` v4.19 `ⓦ` ② · `NFR-I03` *(chỉ khoá đường **ghi**)* | 8088 sổ thật chỉ đọc, chuột thật: rổ `may` **120/120** · `nguoi` **616/616** · `khong` **801/801** *(trước: 50 mỗi rổ)*, ⛔ trùng; `Ghép` trong hộp vẫn khoá + câu `405`; `POST` **0** | ✅ |
| Lượt mới nhất thắng ở `F01` · `F04` | `ⓦ` ① ③ ④ | `F01` USD lật **79** lần ⇒ **3.980** = thẻ = `dem_hang_cho`; `F04` ảnh bấm cuối thắng *(8.978 = thân ảnh `163589`)* | ✅ |
| Lỗi danh sách lệnh có lối ra | `ⓥ` ⑤ *(v4.21 `b tiny`)* | nút `Thử lại` lớp `b tiny`, bấm ⇒ **một** lượt *(3 `GET`)* ⇒ 736 dòng, câu lỗi mất | ✅ |
| Màn ⛔ in số đo cứng | `ⓦ` ③ *(v4.21)* | `title` = chuỗi spec nguyên văn; bỏ `QĐ-ITL-122` ⇒ **0** chữ số | ✅ |
| Năm trạng thái vùng ứng viên | `10` §3.1 *Màn hình* · `ⓦ` ④ | tải · lỗi · mất kết nối · có dữ liệu ✅ Chrome; **rỗng** ⛔ đo được *(sổ thật ⛔ có ca, mã ⛔ đổi nhánh ấy — `KQ-050` ghi thẳng)* | ✅ *(rỗng: có sẵn, ⛔ chạm)* |
| Sổ thật ⛔ đổi | `10` §4.4 · `INV-I08` | kho thật trước = sau; `dem_hang_cho` `{VND 4.242 · USD 3.980 · SGD 145 · HKD 20}` = bốn thẻ | ✅ |

⇒ **`DONG`**. Bốn phát hiện xếp *(PO 05/10 khuya)*:

| F | `KQ-050` | PO xếp | Nơi |
|---|---|---|---|
| `F-1` trang 2 `VND` `/queue` **95,1 / 81,1 s** *(`fls-ba` đo lại hàm thật: **104,33 s**)* | `NANG` ngoài phạm vi | **`NANG`** — giấu **98,8%** dòng `VND` khỏi `F01`; ⛔ chạm ghi | phiếu mới **`WO-051`** *(CAO, sau `WO-023`)* + `BA-08` **v1.4** `NFR-I30` *(ngưỡng trang ≤ `2 s` — khai mới, đo trước)* + `BA-06` **v4.22** `ⓦ` ⑦ *(khung chờ `Xem thêm`)* |
| `F-2` khung tải treo khi lượt ô tìm lỗi | `NHE` | `NHE` — spec có sẵn *(`ⓦ` ④ hàng lỗi)*, lỗi mã | `WO-023` `(h)` ⓔ · `AC-14` |
| `F-3` lựa chọn ứng viên là chỉ số, sống qua lượt tìm | `NHE` | ⭐ **nâng `NANG`** — chính ① của `KQ-050` cho thấy cửa ghi **nhận** cặp trong dung sai ⇒ ở ca `F-3` dòng người ⛔ chọn vào sổ **chỉ-thêm** bằng **một** `Enter` nếu khớp đúng tiền *(`NFR-I25` chỉ chặn ca lệch)*. ⛔ `CHAN`: cùng một lệnh, màn tô hàng mới, sổ thật 0 thao tác người | `BA-06` **v4.22** `ⓦ` ⑥ ⇒ `WO-023` **`(i)` đầu phiếu** · `AC-13` |
| `F-4` bài Dev `AC7_doi_MUC_PHU` phụ thuộc cả kho TEST | `NHE` | `NHE` | `WO-023` `(j)` · `AC-15` |

## Changelog
- 2026-10-05 khuya · `fls-ba` · **nghiệm thu PO** — `KQ-050` ĐẠT 13/13 ⇒ **`DONG`**; mục *Nghiệm thu PO* *(7 ý owner/spec khớp)*. ① của `KQ-050` trả câu treo *"cặp sai trong dung sai có lọt ⛔"*: **lọt** *(`200`)* ⇒ màn là chốt duy nhất. Xếp: `F-1` ⇒ **`WO-051`** · `F-2` ⇒ `WO-023 (h)` ⓔ · `F-3` *(nâng `NANG`)* ⇒ `WO-023 (i)` · `F-4` ⇒ `WO-023 (j)`. Spec `BA-06` **v4.22** · `BA-08` **v1.4**.
- 2026-10-05 · `fls-ba` · trả **`TL-049`** *(`HOI-049` ⇒ `DONG`)*: hai câu phương án **1** = điều Dev đã làm; mục **Đính chính `TL-049`** *(`AC-13` vế hai · lớp nút `(e)`)*; spec `BA-06` **v4.21**. Trạng thái **giữ** `CHO_TEST` — ⛔ vòng 2; `fls-test` kiểm `BG-048` theo đính chính.
- 2026-10-05 · `fls-dev` · ⇒ `CHO_TEST`: phát **`BG-048`** @ `2b804e3` *(13 AC có bằng chứng; `pytest` **2328 passed, 4 xfailed**; 26 bài mới, đỏ **25 / 26** trên mã khi nhận — bài xanh còn lại là hồi quy `cho_ghi = true`)* + **`HOI-049`** `KHONG_CHAN` *(`AC-13` "0 chữ số" ⟷ `QĐ-ITL-122` trong chuỗi spec · `b tiny` ⟷ dáng `TT.chay`)*.
- 2026-10-05 · `fls-dev` · nhận ⇒ `DANG_LAM`. Cổng vào: nhánh `feat/p2-oracle-parity` @ `14a4b72` *(= `origin`)*; mã `fls/**` cuối = `db0adae`; spec `BA-06` v4.20 *(header)*; nền `pytest` **2302 passed, 4 xfailed** *(375 s)* · `kiem_so_song` **55** — khớp mục *Nền khi nhận*. ⛔ run id: phiếu ⛔ nói "đã chạy".
- 2026-10-05 · `fls-ba` · nghiệm thu PO `WO-042` *(`KQ-046` ĐẠT)* ⇒ phiếu này **SẴN SÀNG**; ⭐ thêm **⑤** `F01` thanh lằn ⛔ số cứng *(`KQ-046 F-3` — cùng tệp `man_f01.js` mục ③; `BA-06` **v4.20** `ⓦ` ③)* ＋ **`AC-13`**; nền khi nhận đo lại *(pytest **2302 passed, 4 xfailed** · `kiem_so_song` **55**)*. `F-1` ⛔ vào phiếu này *(SQL / Python, khác lớp)* ⇒ `WO-047`.
- 2026-10-05 · `fls-ba` · phát **`WO-045`** `MO` từ `TL-043` *(`HOI-043` Q4)* + `BG-044` `(d)` + phát hiện ngoài phạm vi *(`Xem thêm` `F01L` bị khoá ở máy chỉ đọc)*. Spec `BA-06` **v4.19** *(`§4.5 ⓥ` đoạn v4.19 + `ⓦ` mới)*. Ưu tiên **CAO**, chờ `WO-042` `DONG`; thứ tự `WO-042` → `WO-045` → `WO-015` → `WO-023`.
