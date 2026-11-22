# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `DT7` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.1 · **Ngày:** 2026-11-22 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-263`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 31 · DT7 · `WO-261` · `BG-262` · nhánh `isp/DT7` @ `4aec25f`

> **Luật của sổ:** sổ **chỉ THÊM**; vòng sau chỉ đổi ô `Trạng thái` của hàng đã có và thêm hàng mới.
> Lớp: **A1** lỗi mã · **B1** lệch spec / thiếu bài · **B2** spec/ISP/hợp đồng sai — chuyển orchestrator. Mức: **CHẶN** · **NÊN SỬA** · **GHI NHẬN**.
> ⛔ **Riêng tư:** sổ chỉ ghi số đếm, địa chỉ ô và tên cột — ⛔ giá trị ô. Bản đọc thô nằm ở `/tmp` *(chmod 600, đã xoá)*, ⛔ commit.
> **Nguồn đúng** *(chủ quyết 22/11)*: sổ P&L `[COPY] Report I General Ledger | P&L Report` `19NNTb…EU2g` — lệch so với chữ "sổ CF" của `WO-261` ⇒ ⛔ phát hiện.

## Số đo nền của R1 *(nhãn đếm gì — Đ4)*

| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| Đọc lại **cả 6 tab** *(4 Daily/YHQM + `417` HAI dấu cách)* bằng khoá SA chỉ-đọc `UNFORMATTED_VALUE`, **so từng ô bằng script riêng** *(⛔ dùng khuôn)*: ảnh → thô | 9.694 + 8.844 + 4.730 + 486 + 10.343 + 9.714 = **43.811 ô số ≠ 0** của ảnh | khớp **43.811/43.811** · lệch **0** |
| …thô → ảnh *(chiều ngược: ô số ≠ 0 ở hàng HD × cột trục giữ mà ảnh THIẾU)* | mẫu số hàng HD × trục = 3 × 440.448 + 2 × 50.616 + 4.218 = **1.426.794** ô | ảnh thiếu **0** |
| Hàng HD: nhãn `MÃ \| Tên` + khối + `dong_sheet` của ảnh ↔ quét độc lập từ thô | 888 × 5 + 74 = **4.514** hàng | khớp **4.514/4.514** |
| Trục: 3 tab Daily/3 tab YHQM cùng hàng trục; cột trục của ảnh có ở thô | 496 ngày · 57 kỳ | thiếu **0**; 3 tab cùng trục **có** |
| Ô CHỮ ở hàng HD × trục giữ *(thô)* | 60 + 60 + 60 + 5 + 60 + 240 = **485** | tập = {`-`}; khớp `o_loi` · **0** `#REF!`/`#N/A` ở hàng HD |
| Ô ngoài trục giữ ở hàng HD *(cột sau ngày đọc / năm > 2026)* | 6 tab | số ≠ 0 = **0** · chữ = **0** *(trừ `419`: **420** chữ `-`, khớp `tuong_lai_chu`)* |
| `#` lỗi toàn lưới thô | 6 tab | chỉ `414`: **17** `#REF!` *(vùng ghi chú, ⛔ hàng HD)*; 5 tab kia **0** |
| Tái chạy khuôn trên bản thô dựng từ lần đọc của TÔI *(22/11)* | 6 ảnh | `dong` · `phu` · `checksum_noi_dung` **giống từng byte 6/6** ⇒ ⛔ trôi sổ sống từ 20/11 |
| Phân loại `LOAI_MA` đo lại từ **công thức thật** cột `G` *(tab 418, 888 hàng)* | 74 mã | `la` **40** · `tong` **10** *(+`NPC` dạng `=sum(G67:67)` ⇒ kê KPI)* · `kpi` **17** · `trong` **7** *(5 hằng gõ tay `-` + 2 trống `CFO`·`PL5`)* ⇒ **40+10+17+7 = 74** khớp khai. ⚠ nhưng **không đồng nhất 12 khối** — `DT7-R1-01` |
| Quan hệ "PM+HR = PLA1 + HR" ở công thức `418` *(nguyên văn `='[MID] Report I PLA1 Daily I PM only'!G8+'[MID] Report I PLA3 Daily \| HR Only'!G8`)* | 440 hàng `la` ngoài khối `SHQ2` | **440/440** đúng dạng; 40 hàng `SHQ2` = công thức DƯ |
| `tu_kiem` **tính lại độc lập từ thô** *(⛔ dùng `tu_kiem` của bài)* | Daily 440.448 · YHQM 4.218 ô | Daily: số thật **10.364** · `0=0=0` **430.084** · lệch không-KPI **4** *(`GROUP` `GAC`·`NCFO` × 2 ngày 45597·45627)* · lệch KPI **510** *(`NPC` 408)* · không so được **0**. YHQM: số thật **1.579** · `0=0=0` **2.639** · lệch **0** · KPI **206** *(`NPC` 38)* · không so được **46.398**. **Khớp từng số `MONG_TU_KIEM`** |
| "`khong_so_duoc` 46.398" có THẬT? | thô `417` | **74** hàng HD · **1** khối `GROUP` *(lưới 92 hàng dữ liệu, 99 hàng, 576 cột)* ⇒ 11 khối × 74 × 57 = **46.398** là vắng thật ở nguồn, ⛔ ô rỗng giả khớp |
| `kiem_tuong_lai_rong` | cột kỳ tương lai có tiêu đề | số ≠ 0 vào cột có tiêu đề ⇒ **TỪ CHỐI exit 2**; số vào cột **không tiêu đề** ⇒ ⛔ bắt — `DT7-R1-02` |
| Mốc ngày | serial 45585…46080 | = 2024-10-20 (CN) … 2026-02-27 *(tính lại)*; cột 2024-10-20 mang ô ≠ 0: `414` **12** · `416` **7** · `418` **12** ⇒ `DT7-R1-07` |
| `chua_co_du_lieu` đúng nguồn | 6 ảnh | 26 · 10 · **88** *(HR Daily, từ 2025-12-02)* · 33 · 26 · 10 — khớp bài; **0** cột trong tập này có ô số ở ảnh |
| AC-7 | `tools/dong_bang_sheet.py` · `_cfa1.py` · `cfa1_*.py` | `git diff c1fc913..HEAD` = **0 tệp**; ảnh cũ đổi byte **0**; tệp đổi so nền = 17 *(15 mới + 2 sửa sàn `dung_moi_truong_isp.sh` · bài ghim)*, không tệp chung |
| Sàn pytest | 4.267 → 4.321 | thu thập thật `--collect-only`: nền `c1fc913` **4.267**, nhánh **4.321** = +54 = **48** bài `test_dap_an_pla.py` + **6** *(`test_R2_02_MOI_khuon…` tự tham số hoá theo 6 khuôn mới)*; `tests/web` 681 = 681 |
| PII | repo | `quet_pii_repo` **0 chỗ · 0 tệp**; ảnh chứa `@` = **0** |
| Kích thước ảnh *(luật `DT4-R1-07`)* | 4 ảnh > 2 MB | orchestrator **chấp nhận** *(22/11)*; tự đo tiêu thụ: `json.load(parse_float=Decimal)` ảnh lớn nhất **0,03 s** ⇒ nén không cần cho H8 ⇒ backlog |
| Đột biến *(bản sao `git archive`, trả nguyên)* | **16** | **13 cắn · 3 sống** — 6/6 mục phiếu cắn; 3 biến thể sống = `DT7-R1-02·03·09` *(chi tiết ở Ghi chú kiểm)* |
| `lint-imports` · `kiem_tai_lieu` | — | **11 kept / 0 broken** · ĐẠT *(411 file · 2.788 bảng · 909 ô ngày · 104 mã QĐ)* |
| `--duong-nen --cong 5447` *(một lần, một mình)* | 4.321 bài toàn bộ · 681 `tests/web` | ĐẠT: `12 failed · 4293 passed · 2 xfailed · 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** · thêm 0 · bớt 0 · chạy 4321 ≥ 4321 · skipped 0; `tests/web` đỏ **3 = 3** · chạy 681 ≥ 681 |

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `DT7-R1-01` | DT7 | R1 | B2 | GHI NHẬN | `BG-262` §9.3 *("đồng nhất 12 khối × 74 mã, 0 mã không đồng nhất")* · `tools/khuon_dong_bang/_pla.py` `LOAI_MA` | Phủ định SAI *(Đ1)*: khối **`SHQ2`** *(mở ở dòng sheet 946)* — **40 hàng `la`** ở cả `414`·`416`·`418` là công thức **DƯ** `=G{hàng GROUP}-SUMIFS(G$448:G$945,$F$448:$F$945,$F{n})` *(ví dụ dòng 947 `=G8-SUMIFS(…)`)*, ⛔ tra sổ `SUMIFS`/`=PLA1!G+HR!G` như 11 khối kia *(440 hàng, 440/440)*. `SHQ2` = `GROUP` − Σ 6 khối nhãn `CVL…ASA`. Ảnh · số · `tu_kiem` vẫn ĐÚNG *(phép cộng tuyến tính nên `SHQ2` lệch = 0)*; chỉ lời khai loại và nhãn `la` che mất ngữ nghĩa phần dư. | Ghi vào BG/WO của **H8**: `SHQ2` = phần dư của `GROUP` ở cả ba tab ⇒ engine SO.PLA phải dựng đúng thế *(⛔ cộng `PLA1+HR` rồi coi là tra sổ)*. Bước sau cân nhắc `loai='du'` *(⛔ đổi ảnh ở bước này)*. | Bài đếm hàng `=G?-SUMIFS` của `SHQ2` = 40 *(đo từ công thức)* | Mở |
| `DT7-R1-02` | DT7 | R1 | A1 | GHI NHẬN | `_pla.py` `kiem_tuong_lai_rong` · `truc_ngay` · `truc_ky` | Cổng cột tương lai chỉ nhìn cột **có tiêu đề** ngày/kỳ. Đột biến **B**: số `5` vào ô hàng HD ở cột `541` *(không tiêu đề)* của bản thô `417` ⇒ khuôn **ĐẠT, exit 0** *(đột biến SỐNG)* ⇒ số ≠ 0 ở cột không tiêu đề bị bỏ **im lặng**. Đo thật: **0** ô số ≠ 0 ngoài trục giữ ở cả 6 tab *(bảng nền)* ⇒ chưa mất số; lỗ ở cổng, ⛔ ở ảnh. Cùng nhóm Đ5 *(cổng xanh trên đột biến)*. | Quét mọi cột `values[hd]` ngoài trục giữ: số ≠ 0 ⇒ `ValueError`; chữ ⇒ vào `tuong_lai_chu`. | Đột biến "số ở cột không tiêu đề" ⇒ ĐỎ | Mở |
| `DT7-R1-03` | DT7 | R1 | B1 | GHI NHẬN | `tests/du_lieu/test_dap_an_pla.py` ↔ `_pla.py:63-76` | `LOAI_MA` *(40/10/17/7)* ⛔ có bài ghim: đột biến **M9** *(chuyển `EBITDA` `kpi`→`la` trong `_pla.py`, ảnh giữ nguyên)* ⇒ `178 passed`, **xanh**. Loại hàng chỉ được canh qua `loai` **ghi trong ảnh** *(bài AC-5)*; đổi khai ở khuôn rồi QUÊN sinh lại ảnh ⇒ không ai biết. | Bài ghim `Counter(LOAI_MA.values())` = `{la:40, tong:10, kpi:17, trong:7}` + `len == 74` + so với `loai` của ảnh. | Đột biến M9 ⇒ ĐỎ | Mở |
| `DT7-R1-04` | DT7 | R1 | B1 | GHI NHẬN | `BG-262` §9.3 *("⛔ kiểm lại ở 414/416")* | Kiểm xong: `414` khớp khai; `416`/`417` khối `GROUP`: `TAC` *(dòng 57)* và `CIT` *(58)* **KHÔNG có công thức** ở cột `G` *(nguồn HR để trống)* ⇒ loại thật = `trong`, khai = `la`. Số ảnh = 0 ở hai hàng ấy, ⛔ sai. | Ghi chú ở BG; ⛔ đổi ảnh. | — | Mở |
| `DT7-R1-05` | DT7 | R1 | B1 | GHI NHẬN | `BG-262` §4 *("KPI vì sao lệch … dấu HR ngược")* | Nguyên nhân KPI lệch chỉ đúng cho `EBITDA`/`EBIT`/`EBT`/`NP`/`PL6-8` *(14 ô mỗi mã ở Daily)*. **`NPC` chiếm 408/510** *(Daily)* và 38/206 *(YHQM)*: `NPC = sum(G67:67)` *(cộng dồn `NP`)*; hàng `NPC` của `416` **0 ô ≠ 0** *(1 ô số)* trong khi `414`/`418` có **470/496** ô ≠ 0 ⇒ lệch vì **HR không tính `NPC`**, ⛔ vì dấu. Số đếm 510/206 đúng. | Sửa chữ BG khi ghi lần sau; H8 coi `NPC` của PM+HR ⛔ bằng tổng hai tab. | — | Mở |
| `DT7-R1-06` | DT7 | R1 | B1 | GHI NHẬN | `BG-262` §3 *("PLA1 Daily 26 cột chưa có từ 46055 = 2026-02-01")* | Nhãn ngày lệch 1: serial **46055 = 2026-02-02** *(tính lại; cột `chua_co_du_lieu` đầu của ảnh = `2026-02-02`)*; 02-02…02-27 = **26** ngày ✓. "02-01" sẽ là 27. Ảnh · bài đúng. | Sửa chữ BG. | — | Mở |
| `DT7-R1-07` | DT7 | R1 | B2 | GHI NHẬN | AP `…ISP-Correction_2026-11-16.html` §3.3.1 *(dòng 939 · 867 · 891 — **4** chỗ ghi `21/10/2024`)* | AP: Daily "cột từ 21/10/2024"; sheet thật bắt đầu **2024-10-20 (CN)** và cột đó mang **12** *(`414`)* · **7** *(`416`)* · **12** *(`418`)* ô ≠ 0. BG giữ mốc thật *(đúng)*. H8 làm theo chữ AP ⇒ đáp án thiếu **31** ô ≠ 0. | Errata AP v3.1.3: mốc = 20/10/2024 *(hoặc quyết bỏ cột ấy)*; ghi vào WO của H8. | — | Mở |
| `DT7-R1-08` | DT7 | R1 | B2 | GHI NHẬN | `BG-262` §9.5 | Xác nhận: `417` thật sự chỉ có khối `GROUP` *(74 hàng HD)* ⇒ Y/H/Q/M của HR vắng ở **11 khối** *(46.398 ô không so được)*. `419` có đủ 12 khối vì là Σ-kỳ của `418`. ❓ BA: H8 có cần HR Y/H/Q/M 11 khối kia *(suy từ `416` Daily)* không? | Quyết ở WO của H8. | — | Mở |
| `DT7-R1-09` | DT7 | R1 | B1 | GHI NHẬN | `tools/dong_bang_sheet.py` `--mong` · `test_dap_an_pla.py:CHECKSUM` | Cổng khuôn đo **ĐẾM** dòng, ⛔ giá trị: đột biến **F2** *(đổi giá trị 1 ô thô đã ≠ 0, đếm giữ nguyên)* ⇒ `--mong` **ĐẠT, exit 0**; chỉ `checksum_noi_dung` khác. Giá trị đã ghim ở **ảnh** *(đột biến M1: đổi 1 ô ảnh ⇒ 3 bài đỏ)*, nên an toàn khi dùng; nhưng ai SINH LẠI ảnh từ nguồn trôi vẫn xanh nếu số ô không đổi. | Khi sinh lại: so `checksum_noi_dung` với `CHECKSUM` ghim — đã có bài. ⛔ cần sửa mã. | — | Mở |

## Ghi chú kiểm *(⛔ phát hiện)*
- **Đột biến 16 · 13 cắn · 3 sống.** *Ảnh* — M1 đổi 1 ô PLA1 Daily ⇒ 3 đỏ · M2 xoá khối `SHQ2` khỏi ảnh `419` ⇒ 6 · M3 đổi nhãn `GI→ZZ` ⇒ 4 · M4 `EBITDA` vào `la` ở ảnh `418` ⇒ 5 · M5 `MONG_TU_KIEM` lech 4→3 ⇒ 1 · M6 nới dung sai `1e-1` ⇒ 5 · M7 xoá 1 ô số ảnh `418` ⇒ 3 · M8 thêm ô số ngày tương lai ⇒ 1 · **M9 `LOAI_MA` ở `_pla.py` ⇒ xanh *(sống, `-03`)***. *Bản thô qua khuôn* — A số vào cột kỳ tương lai có tiêu đề ⇒ **TỪ CHỐI exit 2** · C `#REF!` vào hàng HD ⇒ ĐỎ `o_loi 61 ≠ 60` · D đổi nhãn mã ⇒ ĐỎ `thiếu 4` · E `#N/A` vào cột tương lai `419` ⇒ ĐỎ `tuong_lai_chu 2 dòng ≠ 1` · F ô 0 → số ⇒ ĐỎ `9695 ≠ 9694` · **B số ở cột không tiêu đề ⇒ ĐẠT *(sống, `-02`)*** · **F2 đổi giá trị ô đã ≠ 0 ⇒ ĐẠT *(sống, `-09`)***. Nền M0 = `48 passed`.
- Sáu mục phiếu: đổi 1 ô ảnh *(M1)* · xoá 1 khối *(M2)* · đổi nhãn mã *(M3 · D)* · thêm số tương lai *(M8 · A)* · mã KPI vào `la` *(M4 — ở ảnh; ở khuôn là M9 sống)* · sửa `MONG_TU_KIEM` *(M5)* ⇒ **6/6 cắn** ở dạng chính.
- `tu_kiem`: tính lại **độc lập từ thô** ra cùng 4 / 510 / 0 / 206 / 46.398; `KPI` tách RIÊNG, ⛔ lọt vào danh sách lệch không-KPI *(bài `test_AC5_o_KPI_khong_lot…` xanh)*.
- Mốc `21/10` đếm bằng `grep -c "21/10/2024"` trên AP = **4** *(Đ1: đếm cả hai nơi; ở `fls/`·`tools/` mốc là `SERIAL_MOC = 45585` = 20/10)*.
- Bản thô `/tmp/dt7r1` xoá sau đo; ⛔ commit.

## Changelog
- **v0.1** *(2026-11-22, `fls-test` R1 của `DT7`, `KQ-263`)*: khởi tạo — **9** phát hiện `DT7-R1-01…09` *(**0 CHẶN** · **0 NÊN SỬA** · 9 GHI NHẬN: B2 ×3 · B1 ×5 · A1 ×1)*. Nguồn khớp **100 %** *(43.811 ô số + 4.514 hàng HD; ảnh thiếu 0)*; tái chạy khuôn **giống từng byte 6/6**; đột biến **13/16 cắn** *(6/6 mục phiếu)*.
