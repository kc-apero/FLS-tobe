# HOI-056 — Cú `Gán` *(`F01G`)* hết giờ `FLS-HET-GIO` in tiền tố nào? Spec chỉ ghi chữ cho `Bỏ gán`

| | |
|---|---|
| **Thuộc** | `WO-023` *(phần `(c)` — `BG-055`)* |
| **Hỏi bởi** | `fls-dev` · 2026-10-05 |
| **Loại** | `THIEU` |
| **Trạng thái** | ✅ `DONG` *(`fls-ba` trả `TL-056` 05/10 — phương án **1** = đúng điều Dev đã làm @ `BG-055`; spec khai thêm `BA-06` **v4.23** `ⓕ3` + `ⓦ` ⑤ ⓐ; ⛔ vòng 2 `WO-023`)* |
| **Chặn** | `KHONG_CHAN` *(Dev làm phương án ⭐; đổi chữ là một dòng)* |

## Bằng chứng
- Chỗ 1: `06_SCREEN_SPEC.md` `ⓕ3` *(v4.11, `:1055`)* — *"Quá hạn ⇒ lỗi mã `FLS-HET-GIO` … — **⛔ được** nói *"chưa xảy ra"*: lượt ghi có thể **đã** vào sổ. Ca ⑤ của nút `Bỏ gán` với mã này in *"Chưa rõ bỏ gán đã xảy ra chưa — …"* thay *"Bỏ gán chưa xảy ra — …"*."* — luật nói cho **mọi** lượt ghi, chữ chỉ cho **một** nút.
- Chỗ 2: `06_SCREEN_SPEC.md` `§4.5 ⓦ` ⑤ ⓐ *(v4.21)* — cú `Gán` lỗi in *"Gán chưa xảy ra — Cửa lỗi: <e.cau>"* *(khuôn ca ⑤ `Bỏ gán`)*; ⛔ nói gì về `FLS-HET-GIO`. Mã `(h)` *(`BG-053`)* + `(c)` cùng phiếu ⇒ cú `Gán` nay **có** hạn chờ `30 s` *(cửa ghi `/queue/<itl>/match`)* ⇒ dòng `Gán chưa xảy ra` sẽ **nói dối** đúng ca `ⓕ3` cấm.
- Phép đếm: nơi in tiền tố *"… chưa xảy ra — Cửa lỗi:"* trong `fls/web/tep/` @ `BG-055` — **2** *(`man_f01_ghep.js` `ve_dong_gan` · `ve_dong_bo_gan`)*; hộp `HT` *(`loi_trong_hop`)* ⛔ in tiền tố ⇒ ⛔ chạm.

## Phương án
| # | Phương án | Cái giá | Đề xuất |
|---|---|---|:-:|
| 1 | `Gán` dùng **cùng khuôn** `Bỏ gán`: `FLS-HET-GIO` ⇒ *"Chưa rõ gán đã xảy ra chưa — Cửa lỗi: <cau>"*, mã khác ⇒ *"Gán chưa xảy ra — Cửa lỗi: <cau>"* *(đã làm — bài `test_AC3_HET_GIO_cu_GAN__CHUA_RO_gan_da_xay_ra_chua`)* | một câu màn **chưa** nằm nguyên văn trong spec — `fls-ba` ghi vào `ⓕ3` hoặc `ⓦ` ⑤ ⓐ | ⭐ |
| 2 | Giữ *"Gán chưa xảy ra — "* cho mọi mã | trái luật `ⓕ3` *("⛔ được nói chưa xảy ra")* — người bấm lại, lượt đầu đã vào ⇒ `409 FLS-DA-GHEP` *(câu đúng, nhưng lời đầu đã sai)* | |
| 3 | `FLS-HET-GIO` ⇒ chỉ in `e.cau` + `e.lam_gi`, ⛔ tiền tố | khác khuôn `Bỏ gán` ngay cạnh — hai dòng lỗi cùng khối, hai giọng | |

---

# TL-056 — trả lời *(do `fls-ba` điền bên dưới, cùng tệp)*

| | |
|---|---|
| **Quyết** | ⭐ **Phương án 1.** Cú `Gán` dùng **cùng khuôn** `Bỏ gán`: mã `FLS-HET-GIO` ⇒ *"Chưa rõ gán đã xảy ra chưa — Cửa lỗi: <e.cau>"* ＋ `e.lam_gi` ＋ `e.chi_tiet`; mã khác ⇒ *"Gán chưa xảy ra — Cửa lỗi: <e.cau>"* *(như v4.21)*. Vì sao: luật `ⓕ3` *("⛔ được nói chưa xảy ra")* đã nói cho **mọi** lượt ghi — spec chỉ **thiếu chữ** cho nút thứ hai, ⛔ có ý nào khác. Phương án 2 nói dối đúng ca `ⓕ3` cấm *(người bấm lại, lượt đầu đã vào ⇒ `409 FLS-DA-GHEP`)*; phương án 3 cho hai dòng lỗi cạnh nhau hai giọng. ⭐ Spec khai luôn **khuôn chung** để nút thứ ba ⛔ phải hỏi lại: mọi dòng lỗi một cú GHI mang tiền tố *"<Việc> chưa xảy ra — "* ⇒ với `FLS-HET-GIO` đổi thành *"Chưa rõ <việc> đã xảy ra chưa — "*. `fls-ba` đếm lại 05/10 *(`grep "chưa xảy ra — "` `fls/web/tep/` @ `12b7230`, `Đ1`)*: đúng **2** nơi — `man_f01_ghep.js:725` *(`Gán`)* · `:1002` *(`Bỏ gán`)* = số của Dev. ⇒ Mã + bài `test_AC3_HET_GIO_cu_GAN__CHUA_RO_gan_da_xay_ra_chua` **đúng spec đã khai** ⇒ **⛔ vòng 2 `WO-023`**. `fls-test` đọc `AC-3` theo **Đính chính `TL-056`** ghi trong `WO-023` *(vế `Gán` thêm vào vế `Bỏ gán`)*. |
| **Ai quyết** | `fls-ba` trong thẩm quyền spec — chữ màn in của một luật đã có *(`ⓕ3`)*, ⛔ câu nghiệp vụ *(⛔ đổi con số nào, ⛔ đổi việc kế toán)* ⇒ ⛔ hỏi owner. |
| **Spec đã sửa** | `02_BA/06_SCREEN_SPEC.md` **v4.22 → v4.23** — `ⓕ3` thêm câu cú `Gán` + khuôn chung + phép đếm **2** nơi; `§4.5 ⓦ` ⑤ ⓐ ô *Luật* thêm vế `FLS-HET-GIO`. Phiếu: `WO-023` thêm **Đính chính `TL-056`** cho `AC-3`. |
