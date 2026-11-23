# KQ-236 — biên bản kiểm `BG-235` *(R1 · ISP 3.1.2 · Step 35 · H11 — AL.PLT OMC · SC · PS, cổng WP-C4c, KÈM DT9b `BG-242`)*

| | |
|---|---|
| **Thuộc** | `BG-235` · `WO-233` · `BG-242` · `WO-241` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R1; ⛔ sửa mã)* · 2026-11-19 · `isp/H11` @ `2110f53` · cụm `5444` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 2 NÊN SỬA · 4 GHI NHẬN` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H11.md`)* |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `--duong-nen --cong 5444` *(một lần, một mình)* | `KẾT: ĐẠT` · `12 failed · 4108 passed · 2 xfailed · 14 errors` = nền **28 = 28** *(thêm 0 · bớt 0)* · chạy **4136** *(mong ≥ 4136)* · skipped 0 |
| `tools/do_hd2.py --goi WP-C4c --dsn $PG_DSN_TEST` | `DAT` · khối = `hd2_cong.json` *(so `==` từng khoá)* · `khop/tong_o 19.591/19.591` |
| pytest `tests/oracle tests/bao_cao tests/cau_hinh tests/api/test_isp_gates_hd2.py tests/du_lieu/test_ix_ven_da_so.py tests/api/test_isp_config_ven.py` | **860 passed** *(C4c: 77)* |
| `lint-imports` · `kiem_tai_lieu.py` · `soi_bang_tuyen.py` | 11 kept 0 broken · ĐẠT *(375 tệp · 2.714 bảng)* · KHỚP SQL **46** tuyến |

## Mẫu số *(Đ4 — đo độc lập từ ảnh thô, ⛔ qua engine; khớp engine từng số)*
| Sổ | ô so | ô ⛔ so *(P chữ ×7)* | ô ≠ 0 *(so)* | khớp ≠ 0 | ô rỗng đáp án |
|---|---|---|---|---|---|
| OMC | 8.547 | 3.913 | 363 | 311 | 1.650 |
| SC | 6.230 | 4.144 | 1.216 | 965 | 2.575 |
| PS | 5.117 | 3.073 | **0** *(MID1 `pe≠0` 0/8.505)* | **0** | 4.386 |
| Σ | **19.894** | 11.130 | 1.579 | **1.276** | 8.611 |
`19.591` = **19.894 ô so − 303 lệch có tên** *(⛔ phải "19.591 đáp án khớp")*; trong đó 8.611 là đáp án rỗng ⇒ 0 · 1.276 khớp ≠ 0 · 9.704 `0=0` ⇒ **`H11-R1-02`**.

## Lệch 3 lớp
FLS **0** *(mong 0 · cả ba sổ)* · nguồn **303** = SC **251** *(69 hàng khoá của `lac` 72; PE_cdt đo độc lập cũng ra 251 ô)* + OMC **52** *(8 hàng: 7 `VD61` + 1 `VD654`; đo độc lập 49 ô ở dung sai 0,01)* · nghi lỗi OMC **0** *(⛔ lệch ngoài `lac`)*. Mỗi lớp có `mong`, đổi một ô ⇒ ĐỎ cả hai chiều *(thêm/bỏ tên `lac` ⇒ ĐỎ)*. Ghi nhận: lớp nguồn OMC là **quyết**, ⛔ đo; `lac` OMC gõ ở mã công cụ ⇒ `H11-R1-03`. `chua_co_dap_an`: OMC `202603–09` · SC/PS `202503` + `202603–09` — **có tên**, ⛔ "đạt".

## AC
| AC | Phán |
|---|---|
| AC-1 mẫu số khai trước, nhãn Đ4 | ĐẠT *(nhãn ở khối JSON; nhãn `/gates` thiếu ⇒ `-02`)* |
| AC-2 lệch 3 lớp, Đ5 hai chiều | ĐẠT |
| AC-3 khối `WP-C4c` · CG2 | ĐẠT — bài CG2 xanh; `HD2_WP_C4C` = true "19591/19591" · `HD2_WP_C4` "3/3 gói con đạt"; ⚠ nhãn `-02` |
| AC-4 ⛔ vòng tròn | ĐẠT — MID3 ⛔ đầu vào *(O từ Σ`pe` MID1)*. Đột biến 1 ô MID1 pe `+1000`: **SC** VD55·202504 ⇒ 36 ô FLS, chỉ vendor-tháng ấy · **PS** VD73·202504 ⇒ 2 ô `pe`·`cvl_pe` · **OMC** VD59·202503 ⇒ 2 ô, lớp nghi lỗi ⇒ ĐỎ; đổi O MID3 chỉ làm lệch ô O *(bài sẵn)* |
| AC-5 grep `VD\d+` ở `fls/bao_cao` | **0** · `def chia_theo_cach_tinh` **1** *(⛔ chép; H11 chỉ thêm `chia_dong` + kw, GI mặc định `True`)* |
| AC-6 Q8 | ĐẠT *(4.059 → 4.136, chạy 4.136)* |

## Đột biến *(16, bản sao `git archive 2110f53`, bộ C4c 77 bài)* — BỊ BẮT **14/16**
Bắt: O = `pe` dòng đầu · gộp SHQ2 vào RATE · `TOL` 1e6 · bỏ 1 tên `LAC_OMC` · ghép đảo thứ tự · P chữ ⇒ 0 · ô rỗng ⇒ bỏ · `nghi_loi` luôn True · `OMC.muon_rate=True` · và **5** cờ `LUAT_SO` *(`SC.pm_tong_thang` · `PS.pm_tong_thang` · `SC.muon_rate` · `PS.muon_rate` · `OMC.pm_tong_thang`)* — **cả 5 chỉ nhờ bài ghim dict**; bỏ bài ấy ⇒ **sống** ⇒ `H11-R1-01`. SỐNG: `doc_ven(so="GI")` mọi sổ trong `chay_wp_c4c` *(CLI ĐỎ, pytest xanh — `-04`)* · bỏ nhánh `tt` của engine *(chỉ bộ GI/H10 giữ)*.

## DT9b
- GI **42/42 dòng từng byte** *(so `ix_ven.json` trước `37e3fb2`, sau khi bỏ cột `so`)* · thứ tự 42 đầu là GI. Tổng **359** = 42 · 89 · 93 · 135; trùng `(so,vendor,No)` **0**; vendor ≠ `VD\d+` **0**.
- Vendor mới phủ MID3 **21/21 · 10/10 · 53/53** *(và MID1 cùng tập; IX.VEN thừa 0)*.
- `/config/ven`: khoá cấp trên ⛔ đổi, thêm `so` — nhưng 42 → 359 dòng ⇒ `DT9B-R1-01`.
- PII: `account` OMC·SC·PS = null · `network` SC·PS = null · OMC `network` = 14 nhãn kênh. Dòng GI `account` có tên là DT8 cũ *(owner 11/09 GIỮ)*, ⛔ mới.
- **Tái đo SA chỉ-đọc** *(chỉ đọc cột `No · vendor · pct · cashin_month · cashin_day` + `channel` OMC; ⛔ `account`, ⛔ `network` SC/PS; bản thô ⛔ ra đĩa)*: OMC **89/89** · SC **93/93** · PS **135/135** = **317/317** dòng, 0 lệch, hai chiều khoá thiếu 0. *(Cài `google-auth` vào venv chung.)*
