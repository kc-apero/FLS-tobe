# Fleet eval — bể GIỮ RIÊNG · bể A (dữ liệu CŨ) ↔ bể B (dữ liệu THẬT hiện tại) · 2026-11-23

⚠ **Report đo ĐƯỜNG ỐNG + CỔNG, ⛔ chất lượng mô hình**: agent = mô hình GIẢ tất định (`luat_v0` · `luat_gia_v1`), ⛔ gọi API thật. Chỉ số, ⛔ nội dung giao dịch. Sinh bởi `python tools/fleet_eval_voi.py --be-giu-rieng --ghi` (⛔ sửa tay).

| | bể A · dữ liệu CŨ | bể B · dữ liệu THẬT hiện tại |
|---|---|---|
| kỳ ĐÃ CHỐT (số kỳ) · kỳ ĐANG MỞ | 25 · 0 | 25 · 1 |
| ca / mong *(số MÃ tham chiếu; L3·chuyển·chưa chốt = số DÒNG bank)* | 65 / 65 | 70 / 70 |
| · tầng `A` (thực / mong) | 10 / 10 | 10 / 10 |
| · tầng `B` (thực / mong) | 5 / 5 | 5 / 5 |
| · tầng `C` (thực / mong) | 10 / 10 | 10 / 10 |
| · tầng `D` (thực / mong) | 5 / 5 | 5 / 5 |
| · tầng `E` (thực / mong) | 10 / 10 | 10 / 10 |
| · tầng `F` (thực / mong) | 10 / 10 | 10 / 10 |
| · tầng `L3_khong_ref` (thực / mong) | 5 / 5 | 5 / 5 |
| · tầng `L3_ma_khac` (thực / mong) | 5 / 5 | 5 / 5 |
| · tầng `chuyen` (thực / mong) | 5 / 5 | 5 / 5 |
| · tầng `chua_chot` (thực / mong) | — | 5 / 5 |
| ca nhóm `phai_noi` · `phai_nguoi` · `l3` · `chua_chot` | 29 · 25 · 11 · 0 | 30 · 25 · 10 · 5 |
| độc lập: trùng ca dựng WO-329 · trùng prompt/ví dụ agent | 0 · 0 | 0 · 0 |

## Vòng GIẢ trên bể (recall CHÍNH = nhóm `phai_noi`; `chua_chot` ⛔ vào)

| phiên bản (nội dung) | chỉ số | bể A | bể B |
|---|---|---|---|
| `v0-ma-tat-dinh` (`che_het`) | mẫu số chính (ca) | 65 | 65 |
|  | nối | 0 | 0 |
|  | nối sai | 0 | 0 |
|  | tỉ lệ nối sai | — | — |
|  | recall phải-nối | 0.0 | 0.0 |
|  | ca phải-để-người bị nối | 0 | 0 |
|  | L3 bị nối | 0 | 0 |
|  | điểm TB (0–2) | 1.5538 | 1.5385 |
| | `chua_chot`: ca · agent nối *(⛔ recall)* | 0 · 0 | 5 · 0 |
| `v1-gia-che-het` (`che_het`) | mẫu số chính (ca) | 65 | 65 |
|  | nối | 2 | 2 |
|  | nối sai | 2 | 1 |
|  | tỉ lệ nối sai | 1.0 | 0.5 |
|  | recall phải-nối | 0.0 | 0.0333 |
|  | ca phải-để-người bị nối | 2 | 1 |
|  | L3 bị nối | 0 | 0 |
|  | điểm TB (0–2) | 1.4923 | 1.5231 |
| | `chua_chot`: ca · agent nối *(⛔ recall)* | 0 · 0 | 5 · 0 |
| `v1-gia-che-noi-dung` (`che_noi_dung`) | **bị lớp 2 chặn (`CamGui`)** — ⛔ có số | ⛔ từ chối gửi: dãy ≥ 9 chữ số trong chuỗi (số TK?): 10 chỗ | ⛔ từ chối gửi: dãy ≥ 9 chữ số trong chuỗi (số TK?): 14 chỗ |
| `v1-gia-mo` (`mo` · CHÍNH) | mẫu số chính (ca) | 65 | 65 |
|  | nối | 2 | 2 |
|  | nối sai | 2 | 1 |
|  | tỉ lệ nối sai | 1.0 | 0.5 |
|  | recall phải-nối | 0.0 | 0.0333 |
|  | ca phải-để-người bị nối | 2 | 1 |
|  | L3 bị nối | 0 | 0 |
|  | điểm TB (0–2) | 1.4923 | 1.5231 |
| | `chua_chot`: ca · agent nối *(⛔ recall)* | 0 · 0 | 5 · 0 |

## Chuỗi 4 agent (GIẢ) — ô khớp ↔ máy *(mẫu số cổ định: các ô máy không phụ thuộc bể; phần phụ thuộc bể = G0 A2.04)*

| chế độ che | chỉ số | bể A | bể B |
|---|---|---|---|
| `mo` · CHÍNH | khớp / mẫu số · lệch · ⛔ đo được | 631/631 · 0 · 0 | 631/631 · 0 · 0 |
| `mo` · CHÍNH | G0 A2.04: nối · sai · recall · người-bị-nối | 2 · 2 · 0.0 · 2 | 2 · 1 · 0.0333 · 1 |
| `che_noi_dung` | khớp / mẫu số · lệch · ⛔ đo được | 195/631 · 0 · 0 | 195/631 · 0 · 0 |
| `che_noi_dung` | G0 A2.04: nối · sai · recall · người-bị-nối | None · None · None · None | None · None · None · None |
| `che_het` | khớp / mẫu số · lệch · ⛔ đo được | 631/631 · 0 · 0 | 631/631 · 0 · 0 |
| `che_het` | G0 A2.04: nối · sai · recall · người-bị-nối | 2 · 2 · 0.0 · 2 | 2 · 1 · 0.0333 · 1 |

## Đối chiếu kỳ ĐÃ CHỐT A ↔ B

- kết: **KHỚP**
- tập kỳ chốt A = B: **True** *(A 25 kỳ · B 25 kỳ)*
- Ledge Final đọc hôm nay ↔ ảnh đóng băng DT12 — kỳ ĐÃ CHỐT lệch số dòng: **0**/25 [] *(mẫu số: 12675 ô ngày)*; kỳ ĐANG MỞ (nhận thêm dòng sau ảnh — lớn lên là đúng): 1 `2026-11` ảnh 659 · sống 701
