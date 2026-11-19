# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `DT9` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.1 · **Ngày:** 2026-11-19 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-222`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 34 · DT9 · `WO-220` · `BG-221`

> **Luật của sổ:** sổ **chỉ THÊM**; vòng sau chỉ đổi ô `Trạng thái` + thêm hàng. R1 đầy đủ; mức **GHI NHẬN** ⇒ backlog. Lớp: **A1/A2** lỗi mã · **B1** lệch spec/thiếu bài · **B2** spec/ISP/hợp đồng sai — chuyển orchestrator. Mức: **CHẶN** · **NÊN SỬA** · **GHI NHẬN**.
>
> ⛔ **Riêng tư:** chỉ số đếm, số dòng sheet, tên cột — ⛔ giá trị ô. Bản đọc thô ở thư mục tạm của phiên, ⛔ commit.

## Số đo nền của R1 *(nhãn đếm gì — Đ4)*

| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| Đọc lại nguồn bằng khoá SA chỉ-đọc, so **TỪNG Ô** *(100 %, ⛔ mẫu)* — 9 ảnh, cột đáp án + khoá | **298.166** ô *(ảnh 9: 68.530 · 11.760 · 14.400 · 57.057 · 4.648 · 12.000 · 93.555 · 26.712 · 9.504)* | lệch **0** |
| Hàng thuộc ảnh, chọn độc lập *(MID1/2: `Vendor ID` ≠ rỗng · MID3: `O` là số)* | 9 ảnh · 6.230/1.470/900 · 5.187/581/750 · 8.505/3.339/594 | thiếu **0** · thừa **0** |
| Hàng nguồn ngoài ảnh | SC MID1 574 · SC MID3 10 · PS MID3 1.476 | khớp `dem`/`ngoai_anh` |
| Số dòng theo tháng *(đếm DÒNG ảnh)* | 9 ảnh | khớp `THANG_MONG` ở **9/9** |
| Ô cột `thang` bắt đầu `2026` *(mọi hàng nguồn của 9 tab MID, kể hàng ngoài ảnh)* | 9 tab | **0** |
| Cột ngày/tháng của các tab thượng nguồn *(Source (Looker) cột `date` ×3 · `MID \| Source (Luận)` cột `Month`)* chứa `2026` | OMC 110.079 · SC 12.992 + 326 · PS 12.985 ô | **0** |
| `f == pe` đo từ nguồn *(cột `F` ↔ `T`)* | 6.230 + 5.187 + 8.505 hàng | khớp *(nằm trong 298.166)* |
| Σ 6 PE_cdt = `O`, đo độc lập | OMC 900 · SC 750 · PS 594 hàng số | lệch **0 · 72 · 0**; tập 72 hàng SC **trùng 72/72** `lac` của ảnh |
| PM ô ≠ 0 *(MID3, 7 ô × hàng)* | 6.300 + 5.250 + 4.158 ô | **0/0/0** *(vế PM "chưa đo được" đúng — Đ3)* |
| Công thức MID1: nhắc MID2/MID3 *(toàn tab MID1 + bao đóng)* | OMC 49.315 · SC 45.306 · PS 83.556 ô công thức ở MID1; bao đóng OMC 15 tab · SC 7 · PS 7 | **0** nhắc MID2/MID3 · **0** vòng |
| Cột `AT` *(chỉ số 45)* OMC — ô chữ | MID1 6.239 · MID2 1.479 · MID3 919 hàng | **34** · **0** · **3** *(1 là hàng tiêu đề)* |
| PII: ký tự `@` trong 9 ảnh · tên cột lạ · `vendor` ≠ `VD\d+` | 9 ảnh | 0 *(72 `@` ở `sc_mid3` là chuỗi `dong_sheet@N` của `lac`)* · 0 · 0 |
| Công cụ chung `dong_bang_sheet.py` + `fls/` | `git diff 9bfe992..HEAD` | **0** dòng |
| Đột biến trên bản sao `git archive` | **15** | **14 cắn · 1 sống** *(`DT9-R1-02`)* |

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `DT9-R1-01` | DT9 | R1 | B2 | **NÊN SỬA** | `IncrementalStepPlan-FLS-Voi_v3.1.2.md` Step 34 · `DT9-B1` *("PS thiếu đúng 7 tháng 03–09/2026")* · AP §3.4.1 | Tái đo độc lập: **0** ô tháng `2026…` ở cả 9 tab MID **và** ở cột ngày của 4 tab thượng nguồn; 7/7 tháng `202603…202609` có 0 dòng ở **CẢ BA** sổ *(OMC · SC · PS)*, ⛔ riêng PS. Cái đo được là PS thiếu `202503` so kỳ OMC *(SC cũng thiếu)*. Tiêu chí `DT9-B1` đúng chữ **không thể đạt**; Dev đã IN cổng đúng điều đo được *(đúng)*. | Orchestrator sửa câu AP/ISP *(kỳ sổ `H2.2025` = 202503/04…202512)* **hoặc** giao sổ kỳ 2026; H11 đối chiếu `chua_co_dap_an` theo tháng ngoài kỳ nguồn, ⛔ riêng PS. | Tiêu chí ISP khai điều đã đo bác bỏ ⇒ phép đo của Dev đi kèm số đếm 7/7. | Mở |
| `DT9-R1-02` | DT9 | R1 | B1 | **NÊN SỬA** | `tests/du_lieu/test_dap_an_nen_tang.py:252` *(`len(anh["lac"]) == MID3_LECH_PE[ten]`)* | Bài ghim `lac` SC chỉ **đếm** *(72)*. Đột biến đổi TÊN một hàng trong `lac` *(`dong_sheet@478`→`@11`, đếm vẫn 72)* ⇒ **129/129 XANH**. `checksum_noi_dung` ⛔ phủ `lac`; `lac` không bị so với `thieu_lac` tính lại. Tập đúng đã đo: 72/72 trùng nguồn. | Ghim **tập** 72 `dong_sheet` *(hoặc `anh["lac"] == thieu_lac(dong)["lac"]`)*, hai chiều. | Cổng đếm-tên-không-đếm-tập *(cùng họ `Đ5`)*. | Mở |
| `DT9-R1-03` | DT9 | R1 | B1 | GHI NHẬN | `BG-221` §6 *("72 hàng lệch ở SC — NGUỒN")* · `_nen_tang.py` `lech_pe` | 72 hàng gộp **hai loại**: **70** có `Σ cột chia = 0` *(còn `O` ≠ 0 — **chưa chia**, 408/432 ô PE_cdt rỗng)* và **2** có Σ ≠ 0 *(chia lệch thật)*; **69** có `vendor` + **3** hàng tổng-tháng; dải `dong_sheet` 478–741. Không hàng nào `O = 0`. | Khi H11 dùng: tách *chưa chia* ↔ *chia lệch*; ghim thêm số 70/2. | Một số `lech` hai nghĩa ⇒ khai từng nghĩa. | Mở |
| `DT9-R1-04` | DT9 | R1 | B1 | GHI NHẬN | `BG-221` §4 *("0/116.423 ô công thức nhắc MID2/MID3")* | Số 116.423 *(10 cột MID1 × 3 sổ)* không tái lập từ R1 vì R1 đọc phạm vi khác *(**toàn tab** MID1 + bao đóng)*; kết luận dương **vững hơn**: toàn tab MID1 *(178.177 ô công thức)* + `CFA1` + `Vendor & …Mapping` + `[Import]…GL` + `Source (Looker)` + tab tháng + `MID \| Source …` + `9.2.Exchange Rate`: **0** nhắc `MID2/MID3`, **0** vòng. 2 lần nhắc `CFA2` ở MID1/CFA1 là **chuỗi chữ** *(`=AA7&" CFA2"`, so khớp `"Need to Allocate to CFA2"`)*, ⛔ tham chiếu tab. Phụ: cột `date` của `Source (Looker)` SC *(12.667/12.992)* · PS *(12.985/12.985)* là `#NUM!`/`#VALUE!` — thượng nguồn của `sumifs F`; ⛔ suy ra gì về `F`. | Ghi bằng chứng bao đóng vào `BG` kế; khai cột `date` lỗi cho H11. | — | Mở |
| `DT9-R1-05` | DT9 | R1 | B1 | GHI NHẬN | `BG-221` §7 *(nguyên nhân > 2 MB)* · ảnh `{omc,sc,ps}_mid1` · `ps_mid2` | Nguyên nhân thiếu một mảnh: khoá `o_loi` **nhân đôi** từng ô lỗi — `omc_mid1` **1,07/4,24 MB** *(25 %)* · `ps_mid1` **1,57/6,02** *(26 %)* · `ps_mid2` **0,99/2,54** *(39 %)*; `dong` chiếm 2,85/3,96/1,43. Ảnh ghi `indent=1`. Chuỗi lỗi nguyên ở `dong` bắt buộc *(AC-4)*; bản nhân đôi ở `o_loi` thì do công cụ chung. | Giữ *(công cụ chung ⛔ đổi — AC-6)*; nêu `o_loi` ở `BG`; cân nhắc `o_loi` chỉ đếm khi công cụ chung mở. | Luật `DT4-R1-07` nêu **đủ** nguyên nhân. | Mở |
| `DT9-R1-06` | DT9 | R1 | B1 | GHI NHẬN | `BG-221` §5 *(`nguon_nghi_loi`, "AT chỉ 2 ô chữ")* | `BG` chỉ đo `AT` của MID3 *(R1: 3 ô chữ = 1 tiêu đề + 2 hàng — khớp)*. R1 đo thêm: MID1 **34/6.239** ô chữ *(hàng 8, 10, rồi mỗi 7 hàng)** · MID2 **0/1.479** ⇒ cận trên 31.150 ô của `omc_mid1` **cao hơn** thực tế lọc `row[45]` *(nếu cột đó là cột lọc)*; script ⛔ đọc được ⇒ vẫn **không** kết luận. | H11 tách cờ theo hàng có chữ ở `AT` khi có script. | Đ1: nêu phạm vi đo của số. | Mở |

## Changelog
- **v0.1** *(2026-11-19, `fls-test` R1 của `DT9`, `KQ-222`)*: khởi tạo — **6** phát hiện `DT9-R1-01…06` *(**0 CHẶN** · **2 NÊN SỬA** `-01` B2 · `-02` B1 · **4 GHI NHẬN** B1)*. Nguồn khớp **298.166/298.166 ô**; đột biến **14 cắn · 1 sống**.
