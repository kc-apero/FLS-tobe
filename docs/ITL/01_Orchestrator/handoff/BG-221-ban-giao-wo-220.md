# BG-221 — bàn giao `WO-220` *(ISP 3.1.2 · Step 34 · DT9: ảnh đáp án MID1–MID3 của OMC · SC · PS)*

| | |
|---|---|
| **Trạng thái** | `CHO_KIEM` — Dev xong 19/11 · nhánh `isp/DT9` *(nền `9bfe992`)* · chưa R1 |
| **Phát bởi** | `fls-dev` làn DATA *(phiên cloud con, Sonnet 5.5)* |
| **Ghi kho thật** | `KHONG` *(cụm PG 5445 chỉ chạy đường nền)* |

## 1 · Nguồn — duy nhất, ⛔ ứng viên thứ hai *(đo bằng `sa_ds.py`: 4 sổ `[COPY] … Data Ledger`)*
| Ảnh | Sổ `[COPY]` · id | Tab · lưới | Vùng đọc *(cột; hàng 10…)* |
|---|---|---|---|
| `omc_mid1` · `_mid2` · `_mid3` | `OMC Platform Data Ledger` · `1-blt0rXDehze-Hbpzeswmvr5LrCsUyngHPLn62mHDb8` | `CFA2 \| MID1 \| OMC Allocated Ledger` 6.239×63 · `CFA2 \| MID2 \| …` 1.479×63 · `CFA2 \| MID 3 \| OMC Platform Data Ledger` 919×63 | MID1 `D,J,K,Q,M,R,T,U,V,F,S` · MID2 `D,J,K,M,T,AA,U,V` · MID3 `O,P,S…AF,H,F` |
| `sc_mid1` · `_mid2` · `_mid3` | `SC Data Ledger \| H2.2025 (Luận's File)` · `1X54eYj5SjLcN_mqDTn67uY8eUsZ9LbAysa6rG911wHg` | `CFA2 \| MID 1 \| SC Allocated Ledger` 5.770 · `MID 2` 590 · `MID 3 \| SC Platform Data Ledger` 769 | như trên |
| `ps_mid1` · `_mid2` · `_mid3` | `PS Data Ledger \| H2.2025` · `1QRfU5gS36sA_P7987UWCY3T-0j_3PdkcwB2Su7nGJz0` | `CFA2 \| MID 1 \| PS Allocated Ledger` 8.514 · `MID 2` 3.348 · `MID 3 \| PS Platform Data Ledger` 2.079 | như trên |

⚠ Tên tab OMC MID1/MID2 viết **`MID1`/`MID2` liền** *(SC · PS · GI viết `MID 1`)* — lệch khoảng trắng, cùng nghĩa, 1 ứng viên ⇒ không dừng.
Đọc `values:batchGet` · `UNFORMATTED_VALUE` · khoá SA chỉ-đọc; bản thô `/tmp` chmod 600, **đã xoá**, ⛔ commit. Bản đồ cột lập bằng hàng tiêu đề 1–9 TRƯỚC khi đọc dữ liệu; ⛔ đọc `A:C` · `G` · `N:O` · Số CT · Diễn giải · Tài khoản.
⚠ Chênh môi trường: `google-auth` **chưa có** trong `.venv` *(brief nói có)* ⇒ `pip install google-auth requests` vào venv phiên *(⛔ đổi repo)*.

## 2 · Số dòng ảnh *(đếm DÒNG ảnh — Đ4)* và theo tháng
| Ảnh | Dòng | Theo tháng *(MID3: hàng CÓ khoá `vendor`)* | Ghi chú |
|---|---|---|---|
| `omc_mid1` | **6.230** | 202503…202512 × **623** | 0 hàng đệm |
| `omc_mid2` | **1.470** | × **147** | |
| `omc_mid3` | **900** | × **89** + **10** hàng tổng-tháng ⛔ khoá | 0 hàng ngoài ảnh |
| `sc_mid1` | **5.187** | 202504-06 × **427** · 07-12 × **651** | **574** hàng đệm *(phụ `dem`)* |
| `sc_mid2` | **581** | 04-10 × **63** · 11-12 × **70** | |
| `sc_mid3` | **750** | 04-06 × **61** · 07-12 × **93** + **9** tổng | **10** hàng ngoài ảnh *(`O` = `#N/A`/rỗng)* |
| `ps_mid1` | **8.505** | 202504…202512 × **945** | |
| `ps_mid2` | **3.339** | × **371** | |
| `ps_mid3` | **594** | × **65** + **9** tổng | **1.476** hàng ngoài ảnh *(`O` rỗng, cdt = 0)* |

## 3 · ⚠ "PS thiếu ĐÚNG 7 tháng 03–09/2026" — **KHÔNG tái lập như AP đã viết**
- Đo cả ba sổ: tháng có dòng chỉ `202503/04 … 202512` *(OMC 10 · SC 9 · PS 9)*; **không sổ nào có tháng 2026** ⇒ **7/7** tháng `202603…202609` có **0** dòng ở **CẢ BA** sổ, ⛔ chỉ PS. Đồng thời tháng `202601/02/10/11/12`-2026 cũng 0.
- Cái đo được là **PS thiếu `202503`** *(1 tháng, so kỳ đối chiếu OMC `202503…202512`; SC cũng thiếu `202503`)*. ⛔ **Không lấp**.
- Cổng IN trên mọi ảnh: `tháng có dòng … · thiếu so kỳ đối chiếu … · AP khai thiếu 202603…202609: 7/7 tháng có 0 dòng (mong 7; ⛔ lấp)`; một tháng 2026 lọt vào ⇒ `thang_2026@…` ĐỎ; đổi số dòng một tháng ⇒ `thang_lech@…` ĐỎ.
- **Khuyến nghị BA/orchestrator:** sửa câu AP §3.4.1 *(phạm vi tháng của sổ nguồn `H2.2025`)* hoặc cho đọc sổ kỳ 2026; H11 chỉ nên đối chiếu `chua_co_dap_an` cho tháng **ngoài** kỳ nguồn, không riêng PS.

## 4 · Khoá · cột thượng nguồn · bằng chứng ⛔ vòng tròn *(AC-2)*
- **MID3** *(3 ảnh)* mang `vendor` *(`H`, mẫu `VD[0-9]+`)* + `thang` *(`F`, `yyyymm`)* như DT8b. Hàng tổng-tháng ⛔ khoá. *(GI: 19 vendor × 11 tháng khoá duy nhất; ở đây khoá **lặp** — OMC 210 cặp / 890 hàng · SC 87 / 741 · PS 477 / 585 — ⛔ cổng "khoá trùng" như GI.)*
- **MID1** mang `vendor` · `thang` · `no` · `itl_id` · `pe` *(T)* + cột thượng nguồn **`f`** *(`F` = PS Có)* + `pm` *(S)* · `pm_ghi_chu`. Cổng `f == pe` trên mọi hàng.
- **Bằng chứng `FORMULA`** *(đọc `valueRenderOption=FORMULA`, cột `F,J,K,M,Q,R,S,T,U,V` MID1 cả 3 sổ — **116.423** ô công thức)*:
  · `T10 = ArrayFormula(iferror(F10:F,"Need to manual input"))` *(MỘT công thức tràn, cả 3 sổ)*;
  · `F = sumifs('Source (Looker)'!…)` *(OMC 6.230 · SC 5.187 · PS 8.505 ô)* — thượng nguồn là **Source (Looker)** *(PS/SC thêm `Vendor & Network Mapping`)*;
  · `R = if(J=…, VLOOKUP(C:C,{[Import]Report I General Ledger!AY:AY,…}))` ; `S = VLOOKUP(R,{[Import]GL!R:R,BE:BE},…)` ; `U = T/sum(T:T)*S` ; `V = if(or(S="Need to manual input",len(S)=0),U,S)`;
  · **công thức nhắc `MID2`/`MID3`: 0/116.423** ⇒ MID1 ⛔ tham chiếu MID2/MID3 ⇒ ⛔ vòng tròn; PE theo CDT1 của H11 lấy từ `f`/`pe` = Source (Looker). MID2 `AA = T/sum(T:T)` cùng tab *(5.393 ô, 0 tab ngoài)*.
- ⛔ Đ1: bằng chứng trên là phép đo trên nguồn 19/11, lưu **ở BG này**; pytest ghim `f == pe` trên ảnh, ⛔ gọi lại SA.

## 5 · Cờ `nguon_nghi_loi` OMC *(AC-3)* — bảng phụ `nguon_nghi_loi` *(1 dòng/ảnh OMC; SC·PS ⛔ có)*
- Lý do: `copy*Ledger_to_Report_Optimized()` đọc `row[45]` ngoài 30 cột *(AP §3.4.1)*. **Script ⛔ đọc được** *(không có trong repo — Đ1: `row[45]` có ở 9 tệp `docs/`, **0** ở `fls/`+`tools/`+`tests/` trước DT9; SA ⛔ có quyền Apps Script)* ⇒ phạm vi khai là **CẬN TRÊN**.
- Phạm vi *(hàng × cột đáp án = số ô)*: `omc_mid1` 6.230 × 5 = **31.150** · `omc_mid2` 1.470 × 4 = **5.880** · `omc_mid3` 900 × 14 = **12.600**. Tham chiếu đo: cột chỉ số 45 *(`AT`)* của tab MID 3 OMC chỉ có **2 ô chữ** / ≈ 810 hàng rỗng ⇒ lọc theo `row[45]` thấy rỗng gần như mọi hàng.
- H11 phải tách *đáp án nghi lỗi* khỏi *lệch FLS*; ⛔ sửa lỗi AS-IS.

## 6 · Lỗi ô ghi NGUYÊN + đếm theo cột *(AC-4 · phân bố ghim `LOI_MONG`)*
| Ảnh | `#N/A` ITL ID *(phụ `itl_id_loi`)* | `u` · `v` *(hoặc `rate`)* — loại → ô |
|---|---|---|
| `omc_mid1` | **559** | u, v: `#DIV/0!` 4.836 · `#VALUE!` 84 |
| `sc_mid1` | **592** | u, v: `#DIV/0!` 2.796 · `#VALUE!` 1.314 |
| `ps_mid1` | **1.069** | u, v: `#DIV/0!` 7.290 |
| `omc_mid2` | — | rate `#DIV/0!` 931 · u, v: `#DIV/0!` 798 · `#VALUE!` 462 |
| `sc_mid2` | — | rate `#DIV/0!` 273 · u, v: `#DIV/0!` 240 · `#VALUE!` 254 · **`#REF!` 8** |
| `ps_mid2` | — | rate `#DIV/0!` 3.339 · u, v: `#DIV/0!` 2.898 |
- PM chữ `Need to manual input` **tách** sang `pm_ghi_chu`, `pm` rỗng *(⛔ hoá 0)*: MID1 *(S)* OMC **5.899** · SC **5.038** · PS **8.359**; MID3 *(P)* OMC **559** · SC **490** · PS **439**. Chữ khác ⇒ TỪ CHỐI *(⛔ in giá trị ô)*.
- MID3 Σ 6 PE_cdt = `O`: lệch **0** *(OMC · PS)* · **72 hàng lệch ở SC** *(NGUỒN — ghi `lac`, khai MONG 72, ⛔ đỏ; sửa/đổi số ⇒ ĐỎ)*; Σ PM = `P`: lệch 0 *(nhưng **mẫu số vế PM = 0/N ô ≠ 0** ở cả ba — "chưa đo được", Đ3; vế PE ≠ 0: OMC 431 · SC 1.014 · **PS 0** ⇒ PS MID3 toàn 0)*.

## 7 · Kích thước ảnh *(luật `DT4-R1-07`: > 2 MB ⇒ nêu nguyên nhân)*
`omc_mid1` **4,24 MB** · `omc_mid2` 1,17 · `omc_mid3` 0,38 · `sc_mid1` **3,97 MB** · `sc_mid2` 0,47 · `sc_mid3` 0,33 · `ps_mid1` **6,02 MB** · `ps_mid2` **2,54 MB** · `ps_mid3` 0,25. **Nguyên nhân:** hạt = hàng phân bổ *(Vendor×tháng×No×CDT1)*; mỗi ô số bọc chuỗi + khoá `thu_tu`/`dong_sheet` + chuỗi lỗi Sheets đầy đủ *(~100 ký tự × 9.840 ô ở `omc_mid1`)*. Giữ nguyên *(ảnh phải mang chuỗi lỗi NGUYÊN — AC-4)*.

## 8 · Việc đã làm
| Tệp | Nội dung |
|---|---|
| `tools/khuon_dong_bang/_nen_tang.py` *(mới, ⛔ khuôn)* · `{omc,sc,ps}_mid{1,2,3}.py` *(9 tệp mới)* | thân chung + bảng MONG `DO` *(Đ5)*; mỗi khuôn một tệp *(AC-6)* |
| `tests/fixture/dap_an/{omc,sc,ps}_mid{1,2,3}.json` | 9 ảnh |
| `tests/du_lieu/test_dap_an_nen_tang.py` | **129** bài |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | `MONG_PYTEST_TOAN_BO` **3.754 → 3.892** *(= số bài thu thập; Q8)* |
- **⛔ sửa `tools/dong_bang_sheet.py`: KHÔNG** *(`git diff` rỗng)*; ảnh GI cũ đúng từng byte *(sha ghim ở bài)*.
- **ĐỎ trước:** `pytest tests/du_lieu/test_dap_an_nen_tang.py` ⇒ `126 failed, 3 passed` *(ảnh + khuôn chưa có; 3 bài xanh = sha ảnh GI cũ)* ⇒ sau mã: `129 passed`. Ca phá *(bỏ một dòng · tháng 2026 lọt · vendor là tên người · `f ≠ pe` · đổi một ô chia · tập rỗng · cột Email)* đều ĐỎ.
- Sàn *(`3.754`)* thấp hơn số thu thập cơ sở ~9 bài trước DT9 *(cơ sở 3.763)* — nâng một lần lên số thu thập thật.

## 9 · Cổng cuối
- `--duong-nen --cong 5445` (một lần, một mình): **KẾT ĐẠT** — toàn bộ `12 failed · 3864 passed · 2 xfailed · 14 errors` = tập đỏ nền 28 = 28 node id *(thêm 0 · bớt 0)*, chạy **3892** bài; `tests/web` `3 failed · 672 passed` = nền 3 = 3.
- `lint-imports`: 11 kept · 0 broken. `kiem_tai_lieu.py`: ĐẠT. Bản thô `/tmp` đã xoá.
