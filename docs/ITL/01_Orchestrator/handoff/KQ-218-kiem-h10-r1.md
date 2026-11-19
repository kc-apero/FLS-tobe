# KQ-218 — R1 · `H10` (Step 28 · AL.PLT 5 vendor đặc biệt theo mã 'cách tính' · cổng WP-C4b)

| | |
|---|---|
| **Thuộc** | `WO-216` · `BG-217` · `isp/H10` @ `d236d41` · cụm `5444` |
| **Phát bởi** | `fls-test` R1 · 2026-11-19 |
| **Kết luận** | **ĐẠT CÓ SỬA** — 0 CHẶN · **1 NÊN SỬA** `H10-R1-01` *(hai cơ sở «tổng tháng»)* · 7 GHI NHẬN `H10-R1-02..08` |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H10.md` v0.1 |

## Số đo *(Đ4 — mỗi số một nhãn)*
| Nhãn | R1 đo |
|---|---|
| WP-C4b chạy lại | `DAT`: 209 = 165 + 44 · ô so 1.981 · ⛔ so được 945 · **ô ≠ 0 988** · lệch 0 · KS.AL 209 · bỏ qua 0 |
| (1) công thức AS-IS tái đo `FORMULA` | **5/5 mã chép đúng**: `MID1!E10` **1.012/1.012** ký tự giống BG · 7.350/7.350 hàng `E` một mẫu · `F3!S·T·AQ·AR·AS·AT·AU` giống; luật hoà `VD62` = engine. Lệch nhỏ BG: `M2!AA` có **3** mẫu *(1.230 · 205 · 28 `=V/V`)* — `H10-R1-07` |
| (1) ⛔ vòng tròn | `MID1!E` → Looker `I K O Q S` + VNM; Looker → VNM; VNM → Looker; **0** tham chiếu MID2/MID3/CFA1/`[Formula]` *(đi hết chuỗi: 668 công thức VNM · 114.279 `Looker!Q`)*; giới hạn: `Looker!N` PII ⛔ đọc |
| (1+) 4 hàm PE trên **Looker thật** *(R1 tự đo, 112.373 dòng)* | **2.856/2.856** dòng MID1 khớp `pe_tu_looker` · ≠ 0 **1.054** *(648 + 339 + 67)* · kiểu `khong` 385 dòng toàn 0 |
| (2) grep tên vendor | `fls/bao_cao` **0** · `fls/` 46 *(`-o`)* / 2 tệp · `tools/` 61 / 2 tệp — khớp BG; bảng hàm theo **nhãn** `cach_tinh`; mã lạ ⇒ `LoiPhanBo` có tên *(bài + M13 cắn)* |
| (3) hai cơ sở tổng tháng | **CÓ hai đường** trong `phan_bo.py`: `chia_nen_tang` *(C4a)* · `chia_theo_cach_tinh` *(C4b)*; ca tổng hợp `O ≠ ΣPE` ⇒ PM `30/30` vs `40/20`; trùng **209/209** trên ảnh *(`4,7e-9`)* ⇒ **NÊN SỬA** `H10-R1-01` |
| (4) mẫu số + `mong` hai chiều | mẫu số khớp BG *(209 · 408 · 2.856 · 1.981 · 945 · 988)*; **9/9** đột biến dữ liệu ĐỎ *(đáp án ×1,001 · →0 · +1e-3 · ô thường 0→1 · ô ⛔ so được 0→1 · xoá Vendor-tháng · bỏ vendor ở CFA1 đặc biệt / thường · ở MID1)* |
| (5) ⛔ vòng tròn | đột biến 1 ô MID1: **3/4** kiểu ĐỎ **đúng** ô `*_pe` Vendor-tháng ấy *(4 · 5 · 4 ô)*; kiểu `khong` sống vì `O = 0` *(`-06`)* |
| đột biến mã *(bản sao `git archive`)* | **13/17** cắn *(sống: M7 · M9 · M16 + M11 tương đương)* — `Max` 2/2 · `VD341·VD444` 3/3 · `VD428` 1/1 · `VD62` 3/5 · thường 1/1 |
| đường nền `--duong-nen --cong 5444` *(chạy một mình)* | **28 = 28** node id *(thêm 0 · bớt 0; XFAIL 2)* · chạy **3.742** *(mong ≥ 3.742)* · web **3 = 3** *(675)* · `KẾT: ĐẠT` |
| `lint-imports` · `kiem_tai_lieu` | 11 kept · 0 broken · `kiem_tai_lieu` ĐẠT *(345 tệp · 2.651 bảng)* |

## Phát hiện *(chi tiết ở sổ)*
- **`H10-R1-01` NÊN SỬA** — hai cơ sở tổng tháng cùng sống ở `phan_bo.py`; mỗi cổng một đường; hôm nay trùng nên xanh. Sửa: một nguồn + bài đối chứng *(việc Dev)*.
- `-02` donor `VD62`→`VD341` ⛔ bài ghim *(0 ô số thật)* · `-03` kiểu `VD62=khong` là mã chết, BG khai lệch hành vi · `-04` cổng ⛔ gọi 4 hàm PE *(R1 đo thay 2.856/2.856)* · `-05` ca `P<0 ∧ ΣPE≠0` ⛔ bài · `-06` MID1 `pe` của thường ⛔ `mong` · `-07` `M2!AA` 3 mẫu · `-08` «Max» khoá theo network ở AS-IS, theo nhãn ở TO-BE.

⛔ Kiểm không sửa mã. Kho thật `KHONG_CHAM`. Bản thô SA ở scratchpad, ⛔ commit.
