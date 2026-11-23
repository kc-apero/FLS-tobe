# BG-148 — bàn giao `WO-147` *(ISP 3.1.2 · Step 19 · DT8: ảnh IX.VEN Block 1 + đáp án MID1–MID3 của GI)*

| | |
|---|---|
| **Thuộc** | `WO-147` |
| **Phát bởi** | `fls-dev` làn **DATA** *(phiên cloud · Opus 4.8)* · 2026-11-18 |
| **Nhận** | `fls-test` *(R1 `KQ-149` · R2 `KQ-150` · R3 `KQ-151`)* |
| **Commit** | `claude/bold-galileo-zukpaf-isp/DT8` @ `0ba98c9` *(khuôn + bài + ảnh ①; BG = `795efa4` ②; đã đẩy)* · nền `eab6a21` *(ngọn nhánh làm việc)* |

## Tóm tắt

Đóng băng **bốn ảnh** cho bước AL.PLT/H9/H10 *(phân bổ nền tảng GI)*: đọc bản sao `GI Platform
Data Ledger` bằng khoá SA chỉ-đọc *(cột KHÔNG PII)*, dựng **bốn khuôn tệp riêng** và bốn ảnh qua
cổng `[ĐẠT]`:

| Ảnh | Khuôn | Dòng | checksum_noi_dung | kích thước |
|---|---|---|---|---|
| `tests/fixture/cau_hinh/ix_ven.json` | `ix_ven` | **36** Block 1 | `9a6bc3cac0bf496c` | 12 KB |
| `tests/fixture/dap_an/gi_mid1.json` | `gi_mid1` | **2 856** phân bổ *(+4 494 đệm)* | `5e054cfd05257bb7` | 780 KB |
| `tests/fixture/dap_an/gi_mid2.json` | `gi_mid2` | **1 463** *(RATE)* | `73887970320d39a3` | 426 KB |
| `tests/fixture/dap_an/gi_mid3.json` | `gi_mid3` | **11** đáp án tháng | `a43341bb8aea0c1c` | 6 KB |

*(Mọi ảnh < 2 MB ⇒ ⛔ cần khai nguyên nhân hình dạng — luật `DT4-R1-07`.)*

## Nguồn *(phiên cloud DATA tự đọc bằng khoá SA chỉ-đọc, ⛔ commit bản thô — WO-147)*

- **Tệp:** `[COPY] GI Platform Data Ledger | H2.2025 | Finance Report - ED - Dev 02-12-2023_Finance Monthly Audit_Table`
  · id `1rciS4fMaBAWsqfQYVPeCZ45E1PNRP2b0BkWRq6kO1z4` *(DUY NHẤT — 0 ứng viên khác khớp AP §3.4.1)*.
- **Sheet · vùng · thời điểm đọc (2026-11-18, UNFORMATTED_VALUE · SERIAL_NUMBER):**

| PD | Sheet | Lưới | Vùng đọc *(cột KHÔNG PII)* |
|---|---|---|---|
| 503 | `Vendor & Network Mapping` | 436 × 67 | `M3:V40` *(Block 1 `M:S` hàng 4–39)* |
| 505 | `CFA2 \| MID 1 \| GI Allocated Ledger` | 7 359 × 63 | `D,J,K,Q,M,R,T` hàng 10.. |
| 506 | `CFA2 \| MID 2 \| GI Allocated Ledger` | 1 472 × 63 | `D,J,K,M,T,AA` hàng 10.. |
| 507 | `CFA2 \| MID 3 \| GI Platform Data Ledger` | 274 × 63 | `O10:AF273` |

- ⛔⛔ **PII:** lập bản đồ cột từ hàng tiêu đề TRƯỚC, đọc vùng hẹp. ⛔ mang cột `A` *(Ngày/Số chứng
  từ)* · `B/C` *(Số CT/Diễn giải)* · `G` *(Tài khoản — vd 'R \| HoangACB')* · `N/O` *(File đính
  kèm)* · `H` *(Mã đối tác cá nhân)*. Cột `account` của IX.VEN = **Tên tài khoản** *(owner GIỮ
  11/09 — chỉ `Email Address` bị cấm)*. Bản thô ở `/tmp/dt8/` của phiên — ⛔ commit.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `tools/khuon_dong_bang/ix_ven.py` *(mới)* | Khuôn IX.VEN Block 1 *(khoá `dong_sheet`)*; cột `cach_tinh` SUY *(Network 'Max' / Vendor ∈ {VD341·VD444·VD428·VD62})*; `thieu_lac` = cổng 5 nhóm riêng *(Đ5 hai chiều)*. |
| `tools/khuon_dong_bang/gi_mid1.py` *(mới)* | MID1 phân bổ 7 CDT1; lọc 2 856 hàng thật + đếm 4 494 đệm *(phụ `dem`)*; `#N/A` ITL ID giữ nguyên + 176 hàng ở phụ `itl_id_loi` *(AC-3)*; cổng `mã ∈ tập tham chiếu` trên TẬP ĐẦY ĐỦ *(AC-4)*. |
| `tools/khuon_dong_bang/gi_mid2.py` *(mới)* | MID2 RATE; cột `rate` = `so!` *(số HOẶC `#DIV/0!` — AC-3)*, `LOI_MONG={"rate":308}`; cổng ref-set. |
| `tools/khuon_dong_bang/gi_mid3.py` *(mới)* | MID3 đáp án: chọn 11 hàng *(AE/AF CHECK True)*; cổng **`Σ 6 PE_cdt = O ∧ Σ 6 PM_cdt = P`** đo lại ĐỘC LẬP *(TOL 1e-6)* ở `thieu_lac` *(DT8-B2)*. |
| `tools/dong_bang_sheet.py` *(sửa — bài đòi, AC-3/AC-5)* | Thêm **kiểu cột `so!`** *(số · rỗng · ô LỖI Sheets)* + `LOI_MONG` *(Đ5)*: ô lỗi GHI NGUYÊN + `o_loi`/`loi_theo_cot` *(ghim phân bố)*; ô ⛔số⛔rỗng⛔lỗi ⇒ "ô ⛔ số!" ⇒ ĐỎ *(đối xứng `so`)*. Khuôn ⛔ khai `so!` ⇒ **ảnh DT2…DT5 giữ TỪNG BYTE** *(cổng `cot_so_loi()=[]` ⇒ mọi nhánh mới tắt)*. Dùng `fls.canon.o_loi.la_o_loi` *(⛔ tự khai lại — `test_CHI_MOT_BAN_KHAI`)*. |
| `tests/fixture/cau_hinh/ix_ven.json` · `tests/fixture/dap_an/gi_mid{1,2,3}.json` *(mới)* | Bốn ảnh — cổng ĐẠT. |
| `tests/du_lieu/test_dap_an_gi.py` *(mới, 28 bài)* | DT8-B1/B2 + AC-3…AC-5 + `so!`; tái tạo byte-identical; mọi cổng mới chứng minh ĐỎ. |
| `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` *(Q8/AC-6)* | Sàn `MONG_PYTEST_TOAN_BO` **3141 → 3173** + bài ghim, cùng commit. |

> ⛔ **⛔ sửa** `TIEN_DO.md` / dashboard / changelog chung / `WO-147` *(WO-147 dặn)*. ⛔ chạm kho THẬT *(`Dữ liệu: KHONG`)*.

## Cổng *(kết quả nguyên văn)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/du_lieu/test_dap_an_gi.py` | `28 passed` |
| `pytest tests/du_lieu/` *(hồi quy thư mục chạm)* | `367 passed` |
| `pytest tests/canon/test_o_loi.py` | `6 passed` *(bản khai lỗi DUY NHẤT)* |
| `--duong-nen` *(toàn bộ, chạy MỘT MÌNH, cổng 5437)* | `KẾT: ĐẠT` — tập đỏ = đường nền *(28 node id + XFAIL 2)* · chạy **3173** bài · tests/web 3/3 = đường nền |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT (255 file · 2350 bang)` |
| `python -m fls.db.pg_migrate` | `26/26 di tru · pg_verify khop` *(⛔ chạm schema — chỉ xác minh)* |

## Bằng chứng từng AC
| AC | Bằng chứng của Dev | Đỏ-trước |
|---|---|---|
| **AC-1** *(DT8-B1)* | `test_DT8_B1_ix_ven_36_dong_5_nhom_rieng`: 36 dòng; nhãn ≠ thường = {Max,VD341,VD428,VD444,VD62} *(Max 12·VD341 6·VD444 8·VD428 3·VD62 1·thường 6 — Đ4)* | `test_DT8_B1_PHA_mot_nhom_rieng_thi_DO` *(VD341→VD999 ⇒ `thiếu` ⇒ ĐỎ exit 1)* |
| **AC-2** *(DT8-B2)* | `test_DT8_B2_mid3_sigma_chia_bang_O_P_doc_lap`: đo LẠI Decimal, **lệch 0** / 11 hàng; dư lớn nhất `5,085e-9` *(MONG lệch = 0)* | `test_DT8_B2_PHA_mot_o_chia_thi_DO` *(+1000 CVL_PE ⇒ `dong_sheet@10` ⇒ ĐỎ)* · `_PHA_tap_rong` *(AE=False ⇒ 0 hàng ⇒ TỪ CHỐI, Đ3)* |
| **AC-3** | `#N/A` ITL ID **176** ghi nguyên *(phụ `itl_id_loi`, khớp cột chính)* · `#DIV/0!` RATE **308** ghi nguyên *(cột `so!`, `loi_theo_cot` ghim)* — ⛔ hoá 0 | `test_AC3_mid2_PHA_doi_mot_DIV0_thanh_so` *(`rate 307≠308` ⇒ ĐỎ)* |
| **AC-4** | `test_AC4_anh_0_cot_cam` *(4 ảnh)* · ref-set `cdt1 ∈ 7 CDT1` đo trên **2 856 / 1 463** hàng *(ĐẦY ĐỦ, ⛔ tập con — `DT5-R1-01`)* · lời lỗi ⛔ in giá trị *(`DT5-R1-02`)* | `test_AC4_PII_co_ca_PHA_email` *(thêm 'Email Address' ⇒ TỪ CHỐI, giá trị `secret@…` ⛔ lọt stderr)* · `test_AC4_ref_set_cdt1_PHA` *(`cdt1_la@` ⇒ ĐỎ)* |
| **AC-5** | 4 khuôn = tệp riêng; `tools/dong_bang_sheet.py` sửa chỉ THÊM `so!` *(lý do: AC-3 đòi cột số-HOẶC-lỗi)*; `test_AC5_anh_cu_dung_tung_byte` *(ix_fx)* + ảnh gl_406 checksum `91987833…` không đổi *(hồi quy `test_dap_an_406` 35 bài xanh)* | `so!` chứng minh ĐỎ: `test_so_bang_cot_so_loi` *(chữ-thường ⇒ "ô ⛔ số!")* |
| **AC-6** *(Q8)* | `MONG_PYTEST_TOAN_BO` 3141→**3173** *(28 bài mới + 4 khuôn vào bài tham số hoá)* + bài ghim `test_dung_moi_truong_isp.py` cùng commit | `--duong-nen` đòi chạy ≥ 3173 |

## Kho thật
- `KHONG_CHAM` — `Dữ liệu: KHONG`; mọi kết nối PG chỉ-đọc *(fls_itl = 0 dòng)*.

## Dev tự thấy còn yếu / QUYẾT ĐỊNH PHẠM VI cần R soát
- **Hạt phân bổ MID1/MID2** *(mơ hồ spec — ISP liệt kê 3 ảnh nhưng chỉ gate MID3)*: tôi đóng băng
  **theo hàng phân bổ** *(khoá `dong_sheet`, cột KHÔNG PII)* — MID1 2 856 hàng *(Vendor×tháng×No×CDT1,
  PE)*, MID2 1 463 hàng *(+RATE)*. MID3 có khối đáp án tháng *(11 hàng, cổng Σ chia)*; MID1/MID2
  **⛔ có khối TOTAL** *(đo: 0 ô 'TOTAL' trong MID2)* nên ⛔ đóng băng mức tháng được. Khuyến nghị
  **A — giữ per-row** *(trung thực với sheet; H9/H10 đối chiếu từng hàng)*; **B — chỉ tháng** sẽ
  mất chi tiết phân bổ. Câu hỏi để trong tin nhắn cuối.
- **`gi_mid1` ⛔ mang `ITL ID` ở 2 448/2 856 hàng** *(nguồn rỗng — ITL ID chỉ trên hàng No đầu)*;
  176 hàng `#N/A` đã khai. Nếu H9 cần ITL ID đầy đủ ⇒ phải nối từ CFA1 *(⛔ trong phạm vi DT8)*.
- **"U3 #REF!" (giới hạn ISP)**: cột `U` *(MID computed)* của MID1 mang `#VALUE!` ở nguồn — **⛔
  mang vào ảnh** *(⛔ cột đáp án)*; giới hạn còn ở nguồn, đúng như ISP Step 19 §3 khai.


## Vòng sửa sau R1 (KQ-149)

> *(Thêm 2026-11-18 · `fls-dev` làn DATA · nhánh `isp/DT8` · commit ① `57118ff` = khuôn + bài + ảnh + sàn; commit ② = mục này. Phần trên **giữ nguyên** — các số `36` · `11` · `3173` ở trên là của bản đầu.)* Orchestrator chốt 4 mục NÊN SỬA; 8 GHI NHẬN `-05…-12` ⇒ backlog, ⛔ làm.

| Mã | Chốt | Đã sửa | Đỏ-trước *(cổng ⛔ đỏ ⇒ bài đỏ)* |
|---|---|---|---|
| `DT8-R1-01` | Đóng băng ĐỦ dải liền hàng **4…45 = 42 dòng** | `ix_ven` `--mong 42`; `VD341` `No` 1–12; ảnh + khuôn khai *"AP ghi 36 ⇒ errata"* | `test_DT8_R1_01_ix_ven_dai_lien…` đỏ trên ảnh 36 dòng; `…PHA_cat_o_36_hang` *(lưới cắt 36 ⇒ `36 dòng ≠ mong 42` ⇒ ĐỎ)* |
| `DT8-R1-02` | Khai mẫu số vế PM + bài PM ≠ 0 | `thieu_lac` in `PE: 1275/1771 ô ≠ 0 · PM: 0/1771 ô ≠ 0 — vế này chưa đo được trên dữ liệu thật` | `…cong_KHAI_mau_so…` đỏ trước; bài tổng hợp *(P = 600 = 6 × 100)* XANH + *(Σ PM = 601)* ĐỎ; **bỏ vế PM ⇒ 2 bài ĐỎ** *(đột biến 189/189 xanh ⇒ nay cắn)* |
| `DT8-R1-03` | **A**: 253 hàng số, cổng đo đủ 253 | chọn hàng bằng *"`O` là số"* ⛔ `AE ∧ AF`; `--mong 253`; hàng ngăn *(sheet 21, 44, …, 251)* ⛔ vào ảnh | `…253_hang_so…` · `…PHA_mot_hang_chi_tiet` *(+1000 ở sheet 273 ⇒ ĐỎ — bản cũ ⛔ thấy)*; đột biến chọn lại theo AE∧AF ⇒ 2 bài ĐỎ |
| `DT8-R1-04` | **A**: `U`/`V` vào ảnh `so!` + `LOI_MONG` phân bố | MID1/MID2 thêm cột `u`,`v`; công cụ `LOI_MONG[cột]` = `int` HOẶC `{loại lỗi: số}` *(đổi loại giữ nguyên tổng cũng ĐỎ)* | `…anh_mang_U_V…` ×2 · `…PHA_phan_bo_loi_UV_lech` ×4 *(loại→loại · lỗi→số · `#N/A` · `#REF!`)* · giao kèo ×1; đột biến "chỉ đếm tổng" ⇒ 3/4 ca ĐỎ |

### Số đo *(nguồn thật, khoá SA chỉ-đọc, 18/11 — mỗi số đếm MỘT vật)*
| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| `IX.VEN` Block 1, vùng `M3:S60` | hàng sheet 4–45 liền, 0 hàng trống ngăn | **42 dòng** *(Max 12 · VD341 **12** · VD444 8 · VD428 3 · VD62 1 · thường 6)*; hàng 46–51 rỗng *(6 hàng)*; hàng 52+ = bảng CDT1 *(9 hàng có dữ liệu tới hàng 60)* |
| `MID3` `O10:AF273` | 264 hàng | **253** hàng `O` là số *(11 tổng-tháng sheet 10–20 + 242 chi tiết)* + **11** hàng ngăn; 0 ô rỗng/⛔ số trong 14 cột × 253 |
| `MID3` Σ chia | 253 hàng | lệch **0** · dư lớn nhất `5,085e-9` *(PE)* |
| `MID3` mẫu số vế | 253 × 7 = **1.771** ô mỗi vế | PE ≠ 0: **1.275** · **PM ≠ 0: 0** |
| `MID1` `U` / `V` *(2.856 hàng ảnh)* | 2.856 ô mỗi cột | `U`: số 946 · rỗng 372 · `#VALUE!` **754** · `#DIV/0!` **784** — `V`: số 1.178 · rỗng 165 · `#VALUE!` **733** · `#DIV/0!` **780** |
| `MID2` `U` / `V` *(1.463 hàng)* | 1.463 ô mỗi cột | mỗi cột: rỗng 189 · `#VALUE!` **1.008** · `#DIV/0!` **266** *(0 số)* |
| Lỗi `#REF!` · `#N/A` ở `U`/`V` | cả hai sheet | **0** · **0** |
| Cột cũ của 4 ảnh đọc lại | mọi `dong_sheet` cũ | **0** ô đổi *(chỉ THÊM hàng/cột)* |

⚠ **Khác số R1**: `KQ-149` nêu `MID1` `U` = 754 + 4.636 trên 6.336 ô *(đo cả **lưới**, kể cả 4.494 hàng ĐỆM ngoài ảnh)*; ảnh chỉ mang 2.856 hàng thật ⇒ `#DIV/0!` của `U` ở ảnh là **784**, ⛔ 4.636 *(phần còn lại nằm ở hàng đệm)*. Dùng số đo trên hàng ảnh.

### Errata cho orchestrator ghi *(ISP / AP — ⛔ Dev ghi)*
1. **AP/ISP "Block 1 = 36 dòng"** ⇒ nguồn liền tới hàng 45 = **42 dòng** *(6 hàng `VD341` `No` 7–12; `MID1` dùng tới `No` 12)*. `BG` bản đầu ghi `nguon = M3:V40` — vùng thật là `M4:S45`.
2. **ISP "U3 `#REF!`"** ⇒ phân bố thật ở `U`/`V`: `#VALUE!` + `#DIV/0!`; `#REF!` = 0, `#N/A` = 0. *(`BG` bản đầu chỉ nêu `#VALUE!` — thiếu `#DIV/0!`, phần lớn.)*
3. **Đ4**: `×7` của `WO-147` AC-1 đếm **cột** `M:S`, ⛔ CDT1 *(`-11` — ghi nhận, ⛔ sửa ở đây)*.

### Ảnh · sàn
| Ảnh | Dòng | `checksum_noi_dung` | Kích thước |
|---|---|---|---|
| `ix_ven.json` | **42** | `77f81455901c3667` | 14 KB |
| `gi_mid1.json` | 2.856 *(+4.494 đệm)* | `515868c0b100ba35` | 1,65 MB |
| `gi_mid2.json` | 1.463 | `eb36e99f5a9cee7d` | 1,26 MB |
| `gi_mid3.json` | **253** | `3b93f232a0bedc0a` | 97 KB |

Sàn `MONG_PYTEST_TOAN_BO` **3173 → 3188** *(+15 bài: `test_dap_an_gi.py` 28 → 43)* + bài ghim `test_dung_moi_truong_isp.py` cùng commit ①. Ảnh DT2…DT5 **không đổi một byte** *(`git diff` chỉ 4 ảnh của DT8; `tests/du_lieu` xanh)*. Bản thô `/tmp/dt8_sua/` — ⛔ commit.

### Cổng *(chạy MỘT lần ở cuối)*
| Lệnh | Kết quả |
|---|---|
| `pytest tests/du_lieu` | xanh *(gồm `test_dap_an_gi.py` 43 bài)* |
| `dung_moi_truong_isp.sh --duong-nen --cong 5437` *(một mình)* | `KẾT: ĐẠT` — toàn bộ: tập đỏ = đường nền **28 = 28** *(thêm 0 · bớt 0)* · chạy **3188** bài *(mong ≥ 3188)* · `tests/web` **3 = 3** · chạy 667 |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `kiem_tai_lieu.py` | `✅ cong tai lieu DAT (258 file · 2366 bang)` |

---
Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01EC3zCUYYd4w2PCe9b1GKUs
