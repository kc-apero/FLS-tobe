# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `HELD` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.1 · **Ngày:** 2026-11-23 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-340`)* · **Nguồn:** `WO-338` · `BG-339` *(`isp/HELD` `4407935`)*

> Vai KIỂM: ⛔ sửa mã · ⛔ gọi API thật · ⛔ ghi kho thật. Bể thật dựng lại ở scratchpad (chỉ đọc SA), **đã xoá**; chỉ số đếm ở đây, ⛔ nội dung. Cụm PG thử cổng 5444.
> Thang mức *(CHẶN · NÊN SỬA · GHI NHẬN)* như §1 sổ chung. Sổ chỉ THÊM.

## Số đo nền *(nhãn đếm gì — Đ4)*
| Phép đo | Mẫu số | Kết quả |
|---|---|---|
| Quét lịch sử `9840f27..4407935` | 7 commit · 2.971 dòng thêm | số TK/email/tên người/mã `FT`·`IBDN` thật **0** *(dãy ≥ 8 số = vân tay hex; "email" = decorator pytest; `FT26123ABC456` = chuỗi bịa của bài)* · `quet_pii_repo` **0** |
| Vân tay | `muoi = secrets.token_bytes(16)` HMAC-SHA256, muối ở `muoi.key` ngoài repo | ⛔ đảo bằng từ điển ngắn |
| Dựng lại bể từ SA chỉ-đọc (`Mapping L1` 14.266 dòng · PM 3.909) | A 65 · B 70 | mọi đếm khớp `DEM_BE.json`: tầng · nhóm · vũ trụ · ca/kỳ · `ro_ri_che` — **trừ** vân tay |
| Độc lập | 65 + 70 ca · 12 ca WO-329 · 20 tệp prompt | trùng **0 · 0** cả hai bể, cả ở HELD lẫn cây gộp; cấy 1 ca trùng ⇒ **1** *(tiền+tiền tệ+ngày và nội dung — 2/2 cắn)* |
| Fleet eval GIẢ trên bể dựng lại | mẫu số chính 65 mỗi bể | `luat_gia_v1` nối **2/25** ca phải-để-người (A) · **1/25** (B) ⇒ CHẶN; `chua_chot` **5** ca, mẫu số chính 65 = 70 − 5, `agent nối 0/5` |
| `pytest tests/agent/test_be_giu_rieng.py` | 32 bài | 32 passed không bể · **31 + 1 failed** với bể dựng lại *(vân tay, `HELD-R1-05`)* |
| Cây gộp thử `05d7a97` + `c4c9d40` + `4407935` | `--duong-nen --cong 5444` một mình | **`KẾT: ĐỎ`** — toàn bộ đo **33** vs mong **28**, thêm **5**, chạy **4.990** · web `3 = 3` ĐẠT · `kiem_tai_lieu` ĐẠT · `lint-imports` 11 kept · `quet_pii_repo` 0 |

## Phát hiện
| Mã | Mức | Nội dung | Trạng thái |
|---|---|---|---|
| `HELD-R1-01` | **CHẶN** | HELD dựng trên nền cũ (`9840f27`), ⛔ gộp được với ngọn AG `c4c9d40`: xung đột `tools/fleet_eval_voi.py` *(AG đổi `chay_skill(cho_noi_dung)` → `che_do`; `chay_agent_voi.chay(…che)`)* + sàn script/bài ghim *(4887 · 4928 · 4854)*. Giải bằng bản HELD ⇒ `TypeError` `fleet_eval_voi.py:76` ⇒ **4 bài đỏ thêm** *(2 của HELD `test_chay_be_chi_so…` · `test_chay_chuoi_be…`; 2 của AG `test_fleet_eval_ba_vong__khai_mong` · `test_fleet_eval__luat_noi_bua_bi_CHAN`)* + 1 bài sàn `test_S0_R3_02` *(thu thập thật **4.990** ≠ 4.854 — việc đặt sàn, không phải lỗi)* ⇒ 28 → 33. Cần dev gộp nền AG vào HELD và chuyển `VONG`/`chay_vong`/`chay_chuoi_be` sang `che_do` | mở |
| `HELD-R1-02` | **CHẶN** | `chay_agent_voi.o_ca` của AG đọc `c["tk"]`; ca bể **0/65** có `tk` *(12/12 ca WO-329 có)* ⇒ `KeyError 'tk'` trên bể. Chủ 06:00 "agent đọc toàn bộ nội dung + số TK" ⇒ bể phải mang `tk` mới đo được chế độ `mo` | mở |
| `HELD-R1-03` | NÊN SỬA | `BG-339` AC-4 dẫn bài `test_BE_THAT_che_0_lot_MONG_AC4` *(XFAIL)* và `test_BE_THAT_phep_do_ro_ri_ghim_dung_so_da_do` — **không còn** ở HEAD *(xoá/đổi tên ở `45352f2`; tên hiện tại `test_BE_che_ro_ri_phep_do_hop_le_va_ghim_so_da_do`)*. Khoảng trống "che bỏ sót số TK xen cách + tên có dấu" ⇒ hiện chỉ còn ở văn xuôi, ⛔ có dấu máy canh | mở |
| `HELD-R1-04` | NÊN SỬA | `do_ro_ri_che.do`: `hop_le` kiểm tổng `truoc_che > 0`, ⛔ theo từng loại. Trên bể thật `email` và `so_chung_tu` **trước che = 0 / 0** ⇒ "0 lọt sau che" của hai loại ấy là tập RỖNG (Đ3), `BG-339` in như số đo. Phép dò chỉ được chứng minh cắn trên mẫu bịa | mở |
| `HELD-R1-05` | NÊN SỬA | Muối vân tay ngẫu nhiên mỗi lần dựng và chỉ nằm ở container dev *(phiên tạm)*: dựng lại **đúng** (mọi đếm khớp) vẫn ĐỎ `test_BE_van_tay_khop_tep_dem_repo`; bể thật + muối ⛔ có chỗ lưu bền cho vòng thật sau. Đề xuất: muối dẫn xuất từ khoá bí mật ngoài repo, hoặc lưu bể ở kho bền | mở |
| `HELD-R1-06` | NÊN SỬA | Vòng `KHÔNG CHE` *(chế độ chính theo chủ)* gọi thẳng `luat(cav.o_ca(ca))`, **bỏ `chay_skill`** ⇒ ⛔ qua cổng skill/chốt; vòng đo luật, ⛔ đo đường ống. Sau khi gộp AG nên dùng `che_do="mo"` qua `chay_skill` | mở |
| `HELD-R1-07` | GHI NHẬN | Đáp án `phai_noi` = cột N `Mapping L1` *(công thức VLOOKUP, ⛔ "người chốt ở Ledge Final")*, chỉ nhận khi = dòng `pm_join` chọn ⇒ vòng tròn với `v0` *(6 mã hình A bị loại)*. Thẻ nêu 2 ca cài sẵn *(Ref dùng lại · Ref người đè `_adjust`)* — bể **0** ca loại này. L3 `mã khác`: **10/10** ca có mã dạng Ref ≠ Số chứng từ và mã ấy ⛔ ở PM ⇒ đáp án `DE_NGUOI` hợp lý. Nội dung chứa chính Số chứng từ **0/135** ⇒ recall ≈ 0 là trần của dữ liệu. Câu chủ Q3/Q4 giữ | mở |
| `HELD-R1-08` | GHI NHẬN | Bể A và B ⛔ độc lập nhau: **9** ca trùng *(D 5 — "toàn bộ D" — · B 1 · C 1 · E 1 · chuyển 1)*; hai cột A↔B không phải hai mẫu rời | mở |
| `HELD-R1-09` | GHI NHẬN | Ledge sống ĐỎ đúng *(mẫu số 0 ⇒ ĐỎ, ⛔ coi KHỚP; phép thay thế ghi nhãn "khác vật đo")*. Tái lập: lát **800** hàng đọc **15/16** lát *(11.875 ô ngày, 25 kỳ; lát `A810:A1609` hỏng)* ⇒ đọc được nếu lát nhỏ + thử lại; ĐỎ gỡ được. `DEM_BE.json` `ky_lech_so_dong` liệt 26 kỳ "lệch" với `song = 0` — nhiễu của mẫu số 0 | mở |
| `HELD-R1-10` | GHI NHẬN | Sàn gộp: 3 giá trị khác nhau ở 3 nhánh *(4887 · 4928 · 4854)* ⇒ đặt = thu thập thật cây gộp **4.990** + bài ghim cùng commit | mở |
