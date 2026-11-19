# BG-246 — bàn giao `WO-245` *(ISP 3.1.2 · Step 32 · H7 — CA.GL dòng HR + SO.CFA3, cổng WP-C3c)*

| | |
|---|---|
| **Thuộc** | `WO-245` |
| **Phát bởi** | `fls-dev` làn BE-HC · phiên cloud · cụm PG **5435** · 2026-11-19 |
| **Nhận** | `fls-test` *(R1 → `KQ-247`, R2 cuối → `KQ-248`)* |
| **Commit** | `isp/H7` ⇒ `claude/bold-galileo-zukpaf-isp/H7` · ① mã+bài+tệp sinh `804aff3` · ② BG này |
| **Nền** | `b584561` + gộp `isp/DT6C` @ `2ee5ee5` (BG-250) + ngọn `claude/bold-galileo-zukpaf` |

## Kết luận một dòng
WP-C3c **ĐẠT**: **835/888** ô khớp đáp án thật + **53** lệch có chủ đích *(= mong)* · **0** lệch ngoài tên ·
`atol 1e-15`, `rtol 0`. `/gates` có thêm cổng `HD2_WP_C3C` = `true`; cổng cha `HD2_WP_C3` ghi `3/3 gói con`, 130 lệch có chủ đích.

## Nguồn đầu vào *(⛔ vòng tròn)*
- Lượt đầu H7 **DỪNG đúng luật** *(chưa có ảnh đầu vào HR riêng; chỉ có Y2024)* ⇒ orchestrator phát DT6c (`WO-249` → `BG-250`).
- Đầu vào: `tests/fixture/dau_vao/hr_ledger_2025.json` *(file H1000 Ledger, 10.105 hàng)*. Config: IX.FX (`ix_fx.json`) ·
  IX.HD (`atl_cay.json` + cột M `Code HR Allocate` của Mapping Master) · **IX.ORG đọc TỪ KHO** *(C8; chưa khai ⇒ ĐỎ có lý do)*.
- Luật cột V *(HD Final)* AS-IS: `I` khớp `code_hr` ⇒ `hd_code`, không khớp ⇒ `OGA | GAC - Other` *(mặc định khối 1 của
  `final_rule.MAC_DINH_THEO_KHOI`)*. Luật này được **xác nhận** trên 407 *(cặp I→V đúng 9.421/9.421 dòng, chỉ để xác nhận)*.
  ⛔ Không đọc cột nào của đáp án làm đầu vào.
- **Đáp án chính GL = 408**. Lý do: DT6c đã đối chiếu nguồn ↔ 408; 408 mang 2.302 hàng `ky_suy`. 407 = 408 + 11 hàng LE `#N/A`;
  CFA3 tính từ sheet 407, nhưng 11 hàng này làm lệch **0** ô ngoài tên. 413 có thêm Y2024, ngoài phạm vi đầu vào 2025.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/gl.py` | `hd_final_hr(code_hr, I)` ⇒ `(nhãn, mac_dinh)` · `cdt1_hr(org, cdt)` qua `cdt_cua`, CDT lạ ⇒ `CdtLaHR` *(`ma = "CDT_LA"`, ⛔ SHQ2)* · `HD_MAC_DINH_HR` = một bản khai ở `final_rule` |
| `fls/cau_hinh/hd.py` | `doc_code_hr_van_ban` — ảnh Mapping Master ⇒ `{code_hr: hd_code}` *(trùng / 0 dòng ⇒ `LoiHD`)* |
| `tools/do_hd2_c3c.py` *(mới)* · `tools/do_hd2.py` | `--goi WP-C3c [--dsn]`: dòng HR → `tinh_gl` *(H1/H4)* → ① Σ BA/BB theo (kỳ, V) ↔ 408 · ② `cfa1_daily` *(H5, trục = KỲ tháng, khối GROUP)* ↔ `cfa3` Σ ô ngày theo tháng. Không chép engine |
| `docs/ITL/_tools/hd2_cong.json` | thêm khối `WP-C3c`, sinh bằng `do_hd2.py --goi WP-C3c --dsn $PG_DSN_TEST --ghi` *(diff chỉ +77 dòng; các khối cũ giữ nguyên)* |
| `tests/bao_cao/test_gl_hr.py` *(4)* · `tests/oracle/test_do_hd2_c3c.py` *(10)* | AC-1…AC-5 |
| `tests/api/test_isp_gates_hd2.py` | ghim thêm cổng thứ 9 `HD2_WP_C3C` *(8 → 9 cổng; C3 77 → 130 lệch có chủ đích; `3/3 gói con`; `217518/217648 ô`)* |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` **4097 → 4111** *(= số bài thu thập; +14)*, cùng commit |

## Số đo WP-C3c *(Đ4: mỗi số ghi rõ nó đếm gì · mong khai TRƯỚC trong `MongC3c`)*
| Nhãn | Thực = Mong |
|---|---|
| hàng đầu vào · thiếu D *(không vào `tinh_gl`; AS-IS AX rỗng ⇒ BA 0)* · dòng vào engine | 10.105 · 462 · 9.643 |
| **ô so GL** = 12 kỳ 2025 × 10 nhãn V *(9 `code_hr` + OGA)* × {BA, BB} | **240** · đáp án ≠ 0: **93** |
| **ô so CFA3** = 54 mã *(không tính KPI)* × 12 kỳ — **hạt THÁNG** | **648** · đáp án ≠ 0: **170** · ô KPI loại 240 |
| **tong_o · khop · lech_co_chu_dich** | **888 · 835 · 53** *(GL 20 + CFA3 33)* |
| lệch ngoài tên | **0** |

**Lớp lệch có tên** *(Đ5: khác mong ⇒ ĐỎ cả hai chiều)*:
- `dap_an_khac_nguon` *(= `lech_co_chu_dich`, số Ô theo kỳ; orchestrator chốt khai theo kỳ, không lấp)*:
  GL `02:2 · 04:2 · 06:1 · 08:1 · 09:1 · 10:7 · 12:6`; CFA3 `02:4 · 04:3 · 10:13 · 12:13`.
  ⚠ **Kỳ 2025-04 mới phát hiện, ngoài danh sách BG-250**: số hàng và Σ PS Có khớp, nhưng PS **Nợ** của hàng `PIT | PIT Total`
  và `PIT` trần *(⇒ OGA)* khác. Cùng hiện tượng "chia lại PS Nợ" mà BG-227 §2 thấy ở 413.
- `chua_co_dau_vao`: 408 kỳ 2026-01 = **269** hàng *(không so)*; CFA3 có **17** ô tháng ≠ 0 ngoài kỳ so *(cả 17 ở 2026-01 = 12 mã thường + 5 KPI)*; 5 ô `-` *(2024-10-20)*.
- `ky_suy` *(AC-3)*: **2.302** hàng · Σ PS Có **6.763.528.503** · `BA`/`BB` rỗng **2.302/2.302**. Các hàng này không vào Σ, không bị hoá 0,
  không bị tính là FLS sai *(A rỗng ⇒ công thức không tra được tỷ giá)*. Bớt một hàng, hay một hàng có BA ⇒ ĐỎ *(bài)*.
- `hd_mac_dinh_oga` **20** hàng *(`PIT` trần · `PI…` · rỗng)* · `cdt_la` *(AC-2, theo giá trị nguồn)*: `COR_Terasofts` **592**
  *(khác hoa thường so với `COR_TeraSofts` trong CDT Correct)* · rỗng **59** · `INT | Insurance Total` 4 · `NIS | Net Income Staff` 3 · `COM | COM Total` 1.

**Dung sai**: đo trên ô khớp, chưa áp dung sai — GL max|lệch| 3,35e-17 · CFA3 9,34e-17 ⇒ `atol 1e-15` *(≥ ×10)*. Chứng ĐỎ:
+1e-12 vào một ô BA đáp án ⇒ ĐỎ đúng ô ấy. Phá luật `code_hr` hoặc hạ `atol` xuống 1e-30 ⇒ cổng ĐỎ; trả nguyên ⇒ ĐẠT.

## Bằng chứng từng AC *(ĐỎ trước)*
| AC | ĐỎ trước | Xanh sau |
|---|---|---|
| AC-1 · H7-B1 | `pytest tests/oracle/test_do_hd2_c3c.py` ⇒ lỗi thu thập *(`tools.do_hd2_c3c` chưa có)*. Lần chạy thật đầu: `cfa3.o_so_dap_an_khac_0 thực 170 ≠ mong 147` *(mong lần đầu khai sai; nguyên mẫu độc lập đo 182 − 12 = 170 ⇒ sửa bản khai theo số đo)* | `do_hd2 --goi WP-C3c` ⇒ `KẾT: DAT`; Đ3 đáp án rỗng ⇒ ĐỎ; 8 đột biến `mong` ⇒ ĐỎ |
| AC-2 · H7-B2 | `pytest tests/bao_cao/test_gl_hr.py` ⇒ `ImportError` | 4 passed; lạ ⇒ `CdtLaHR` `CDT_LA`, không nhắc `Headquarters2` |
| AC-3 | *(cùng lượt AC-1)* | `test_H7_AC3_ky_suy_KHONG_hoa_0…` |
| AC-4 | `test_isp_gates_hd2.py` ⇒ 11 failed *(ghim 8 cổng)* | 73 passed; bài quét tệp thật CG2 xanh |
| AC-5 | *(cùng lượt AC-1)* | +1 tỷ VND vào E của một dòng GAH 2025-03 ⇒ ĐỎ **đúng** ô GL `GAH·BA` + lá GAH và mọi tổ tiên trong cây; xoá giá trị đáp án ⇒ lưới engine giữ nguyên |
| AC-6 · Q8 | — | xem Cổng |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `tools/dung_moi_truong_isp.sh --duong-nen --cong 5435` *(chạy một mình trên `804aff3`)* | **`KẾT: ĐẠT`**. Toàn bộ: tập đỏ + XFAIL **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **4111** *(mong ≥ 4111)* · skipped 0 · deselected 0. `tests/web`: **3 = 3** · chạy 675. ⚠ Lần chạy đầu bị cắt ở phần `tests/web` vì giới hạn thời gian 10 phút của lệnh nền *(phần toàn bộ lúc ấy đã [ĐẠT] 28 = 28)*; chạy lại một lần, đủ cả hai phần. |
| `lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT` *(381 tệp · 2724 bảng · 892 ô ngày · 104 mã QĐ)* |

## Câu hỏi cho chủ / BA
1. **Gán kỳ cho `ky_suy`**: nguồn ghi kỳ **2025-10** cho **1.125** hàng mà DT6b đã gán theo "hàng trên" *(06/07/08)*. Có đổi quyết định gán kỳ không? *(BG-250 §2; WP-C3c hiện để các hàng này ngoài Σ.)*
2. `COR_Terasofts` *(592 hàng)* chỉ khác `COR_TeraSofts` ở chữ hoa/thường. Có thêm alias vào CDT Correct không? Hôm nay cổng xếp chúng vào `CDT_LA`.
3. CFA3 hiện so theo **tháng** vì ảnh đầu vào chỉ mang `ky`. Có giữ cột A *(ngày)* trong `hr_ledger_2025` để so theo ngày không?

## Kho thật
`KHONG_CHAM`. ⛔ Drive/Sheets. IX.ORG nạp vào **`fls_test`** *(actor `bai-h7`)* để `--ghi` chạy được.

## Dev tự thấy còn yếu
- Hạt tháng của CFA3 *(ở trên)*. 20 mã KPI vẫn chưa có engine *(cùng giới hạn H5)*.
- `MongC3c` khai số ô theo kỳ, chưa khai từng ô ⇒ nếu ô lệch **đổi chỗ trong cùng kỳ** mà số ô không đổi thì cổng vẫn xanh.
  Ô lệch và số liệu chi tiết vẫn tái tạo được bằng `in_bao`.
