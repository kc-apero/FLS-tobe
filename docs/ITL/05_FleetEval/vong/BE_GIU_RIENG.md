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
| `v0-ma-tat-dinh` (TẮT) | mẫu số chính (ca) | 65 | 65 |
|  | nối | 0 | 0 |
|  | nối sai | 0 | 0 |
|  | tỉ lệ nối sai | — | — |
|  | recall phải-nối | 0.0 | 0.0 |
|  | ca phải-để-người bị nối | 0 | 0 |
|  | L3 bị nối | 0 | 0 |
|  | điểm TB (0–2) | 1.5538 | 1.5385 |
| | `chua_chot`: ca · agent nối *(⛔ recall)* | 0 · 0 | 5 · 0 |
| `v1-gia-tat-noi-dung` (TẮT) | mẫu số chính (ca) | 65 | 65 |
|  | nối | 2 | 2 |
|  | nối sai | 2 | 1 |
|  | tỉ lệ nối sai | 1.0 | 0.5 |
|  | recall phải-nối | 0.0 | 0.0333 |
|  | ca phải-để-người bị nối | 2 | 1 |
|  | L3 bị nối | 0 | 0 |
|  | điểm TB (0–2) | 1.4923 | 1.5231 |
| | `chua_chot`: ca · agent nối *(⛔ recall)* | 0 · 0 | 5 · 0 |
| `v1-gia-bat-noi-dung` (BẬT-đã-che) | mẫu số chính (ca) | 65 | 65 |
|  | nối | 2 | 2 |
|  | nối sai | 2 | 1 |
|  | tỉ lệ nối sai | 1.0 | 0.5 |
|  | recall phải-nối | 0.0 | 0.0333 |
|  | ca phải-để-người bị nối | 2 | 1 |
|  | L3 bị nối | 0 | 0 |
|  | điểm TB (0–2) | 1.4923 | 1.5231 |
| | `chua_chot`: ca · agent nối *(⛔ recall)* | 0 · 0 | 5 · 0 |
| `v1-gia-khong-che` (KHÔNG CHE) | mẫu số chính (ca) | 65 | 65 |
|  | nối | 2 | 2 |
|  | nối sai | 2 | 1 |
|  | tỉ lệ nối sai | 1.0 | 0.5 |
|  | recall phải-nối | 0.0 | 0.0333 |
|  | ca phải-để-người bị nối | 2 | 1 |
|  | L3 bị nối | 0 | 0 |
|  | điểm TB (0–2) | 1.4923 | 1.5231 |
| | `chua_chot`: ca · agent nối *(⛔ recall)* | 0 · 0 | 5 · 0 |

## Chuỗi 4 agent (GIẢ) — ô khớp ↔ máy *(mẫu số cổ định: các ô máy không phụ thuộc bể; phần phụ thuộc bể = G0 A2.04)*

| cờ nội dung | chỉ số | bể A | bể B |
|---|---|---|---|
| TẮT | khớp / mẫu số · lệch · ⛔ đo được | 627/627 · 0 · 0 | 627/627 · 0 · 0 |
| TẮT | G0 A2.04: nối · sai · recall · người-bị-nối | 2 · 2 · 0.0 · 2 | 2 · 1 · 0.0333 · 1 |
| BẬT-đã-che | khớp / mẫu số · lệch · ⛔ đo được | 627/627 · 0 · 0 | 627/627 · 0 · 0 |
| BẬT-đã-che | G0 A2.04: nối · sai · recall · người-bị-nối | 2 · 2 · 0.0 · 2 | 2 · 1 · 0.0333 · 1 |

## Đối chiếu kỳ ĐÃ CHỐT A ↔ B

- kết: **ĐỎ — ⛔ đo được: Ledge sống ⛔ đọc hết giờ (ô ngày giải mã 0, lát hỏng 0)**
- tập kỳ chốt A = B: **True** *(A 25 kỳ · B 25 kỳ)*
- Ledge Final đọc hôm nay ↔ ảnh đóng băng DT12: **⛔ đo được** (mẫu số 0 ô ngày giải mã; lát hỏng 0 — đọc Ledge hết giờ liên tục) ⇒ ĐỎ, ⛔ coi là KHỚP
- phép THAY THẾ *(khác vật đo)*: dòng bank sống ở `Mapping L1` ↔ dòng Ledge đóng băng, trên 26 kỳ — lệch **8** kỳ: `2025-11` bank 475 · Ledge 477, `2026-02` bank 438 · Ledge 439, `2026-03` bank 582 · Ledge 584, `2026-04` bank 599 · Ledge 600, `2026-05` bank 536 · Ledge 537, `2026-06` bank 611 · Ledge 613, `2026-07` bank 683 · Ledge 686, `2026-11` bank 748 · Ledge 659
