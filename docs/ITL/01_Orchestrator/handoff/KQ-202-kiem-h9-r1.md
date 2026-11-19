# KQ-202 — R1 · `H9` + `DT8b` (Step 24 · AL.PLT GI vendor thường + KS.AL, WP-C4a)

| | |
|---|---|
| **Thuộc** | `WO-200` · `BG-201` · `WO-204` · `BG-205` · `isp/H9` @ `c29f905` · cụm `5444` |
| **Phát bởi** | `fls-test` R1 · 2026-11-18 |
| **Kết luận** | **ĐẠT CÓ ĐIỀU KIỆN** — 0 CHẶN · **1 NÊN SỬA** · 5 GHI NHẬN → giao R2 `KQ-203` |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H9.md` v0.1 |

## Số đo *(Đ4 — mỗi số một nhãn)*
| Nhãn | R1 đo |
|---|---|
| RATE đúng trên ca ≠ 0 tổng hợp? | **ĐÚNG** — 2.934 ca ngẫu nhiên chia được *(2.220 theo tổng tháng: O = 0 ∧ P > 0)* so `Fraction`: lệch RATE 0 · Σ chia = O/P 0 lệch; Σ PE = 0 ⇒ `LoiPhanBo` có tên |
| đột biến mã *(15)* | cắn **13** *(RATE ×3 · tổng tháng ×2 · chia 0 · dung sai KS.AL · làm tròn · đặc biệt ×2 · cổng ×3)*; **sống 2**: bỏ `ks_al` ở cổng *(`H9-R1-02`)* + 1 đột biến rỗng của chính R1 *(⛔ tính)* |
| đột biến đầu vào/đáp án cổng *(10 + baseline)* | đỏ **8** đúng chỗ *(đổi 1 Vendor-tháng thường ≠ 0 ⇒ ĐỎ cả đầu vào lẫn đáp án)* · XANH **2**: P-chữ đáp án *(`H9-R1-01`)* · vendor đặc biệt *(`-05`)* |
| WP-C4a `DAT` | 44 Vendor-tháng · ô so **420** · ⛔ so được **196** *(28 × 7, P = chữ)* · ô ≠ 0 **0** · lệch **0** · bỏ qua 5 nhãn / **15** vendor |
| DT8b tái đo SA chỉ-đọc | CFA1 **2.448/2.448** ô · MID3 **3.542/3.542** ô + **253/253** khoá *(≥ 20 ô: toàn tập)* |
| 14 cột cũ MID3 trước/sau DT8b | **4.048/4.048** giống từng byte |
| PII | 0 cột cấm · vendor 209/209 + 408/408 khớp `VD\d+` · `pm_ghi_chu` hoá 0 = **0** |
| đường nền `--duong-nen --cong 5444` | **28 = 28** · chạy 3.629 · web 3 = 3 · `KẾT: ĐẠT` |
| `lint-imports` · `kiem_tai_lieu` | 11 kept 0 broken · ĐẠT |

## Phát hiện
- **H9-R1-01 (NÊN SỬA)** — 196 ô ⛔ so được: đáp án ≠ 0 trong đó = 0, nhưng cổng ⛔ khai `mong`; đột biến ở Vendor-tháng P-chữ ⇒ XANH. Thêm `o_khong_so_khac_0` mong 0.
- GHI NHẬN: `-02` `ks_al_vm` hằng · `-03` RATE ⛔ đo trên dữ liệu thật *(PE rỗng — H10)* · `-04` quyết ngầm *tổng tháng gồm vendor đặc biệt* · `P < 0` · `-05` đặc biệt đếm ⛔ giá trị · `DT8B-R1-01` `pe` chữ ⇒ khuôn nổ `TypeError` *(không lộ giá trị)*.

⛔ Kiểm không sửa mã. Kho thật `KHONG_CHAM`; bản thô SA ở scratchpad, ⛔ commit.
