# BG-169 — bàn giao WO-168 · ảnh `cfa1_dau_vao` (đầu vào H5)

**Nhánh** `isp/DTCF` · commit ① `c6faff7` · nền `b0bbe02`. Ghi kho thật: KHÔNG. Bản thô chỉ ở `/tmp` phiên, **đã xoá** *(`/tmp/dtcf` ⇒ không tồn tại)*.

## Kết quả AC *(mỗi số nói nó đếm gì — Đ4)*
| AC | Kết quả |
|---|---|
| AC-1 | `tests/fixture/dap_an/cfa1_dau_vao.json` · **12.590 dòng sổ** · `dong_sheet` 10…12599 liên tục · cổng `--mong 12590` ĐẠT · checksum `9ea323cb88dc357f` · 3,68 MB. 22 hàng đuôi (12600–12621) loại theo WO-156 *(⚠ đo lúc cắt: cả 22/22 hàng còn ≥1 ô không rỗng ở cột A·D·E·F·G·R·V — WO ghi "0 ô khoá"; bản thô đã xoá nên không đo lại; số 12.590 khớp mốc)*. Ngày CSV hiển thị `MM/DD/YYYY` — 12.590/12.590 ô khớp một định dạng, 0 ô không đọc được ⇒ ISO; khoảng 2024-10-21…2026-11-17. Tiền 2 số lẻ. |
| AC-2 | **24 LE đo được** *(không có `GROUP`, không có `SGO1`)*; có `SGO2`·`BGO2`·`HGO6`. **2.137 dòng lỗi khuôn** `tach_nguon` ⇒ `le = null` (không đoán): 1.331 nhóm `1_gạch` + 806 nhóm `0_gạch`, cả hai có tiền tố `R \| `. HD Final lấy mã trước ` \| `: **14 dòng ∉ ATL 74** — 5 nhóm: rỗng 1 · `Server Cost` 7 · `oga` 4 · `GAC - Other` 1 · `ofR` 1 *(không ép về mã gần nhất)*. 120 dòng `itl_id` là chuỗi lỗi Sheets. |
| AC-3 | Chỉ ĐO, không chốt — xem bảng dưới. |
| AC-4 | Ảnh 0 cột B/C/Email/tk/bank; cột G chỉ dùng tách LE rồi bỏ; lời lỗi chỉ mang `dong_sheet`; bài có ca phá *(đổi 1 byte ảnh ⇒ 2 bài ĐỎ → trả nguyên ⇒ xanh)*. |
| AC-5 | `MONG_PYTEST_TOAN_BO` **3377 → 3389** + bài ghim cùng commit. `--duong-nen --cong 5437` MỘT lần: ĐẠT — 3389 bài ≥ 3389 · web 667 ≥ 667 · lint-imports 11 kept · `kiem_tai_lieu` ĐẠT. |

## AC-3 — GROUP: ứng viên × ô khớp *(⛔ chốt — orchestrator/BA chốt)*
Đo: ô = (mã HD, ngày) có ≥1 dòng sổ vs ô `gt ≠ 0` của GROUP trong `cfa1_daily.json` *(15.954 ô)*.
| Ứng viên | ô | khớp | thừa |
|---|---|---|---|
| Σ mọi LE | 3.276 | 3.109 | 167 |
| Σ mọi LE trừ CN | 3.125 | 2.973 | 152 |
| Σ LE có chữ `GO` | 2.500 | 2.384 | 116 |
| Σ mọi LE trừ 4 LE kia | 2.098 | 1.981 | 117 |
| Σ 4 LE kia *(SGO2·SGO1·BGO2·HGO6)* | 1.592 | 1.530 | 62 |
| Σ LE tiền tố `V` | 1.173 | 1.122 | 51 |

⚠ **Phép đo này KHÔNG phân biệt được**: ngay LE trực tiếp, SGO2 chỉ khớp 1.440/10.547 ô đáp án, BGO2 86/1.664, HGO6 56/1.605, SGO1 0/3.585 ⇒ đáp án là số tích luỹ/khác dòng-phát-sinh, nên "ô có dòng" chỉ có độ phủ ~20%. Xếp hạng trên chỉ phản ánh số ô, không phải đúng-sai. Cần phép so theo GIÁ TRỊ (đổi tiền + luỹ kế) — việc của H5.

## Câu hỏi
1. 5 LE đáp án vs 24 LE sổ: `GROUP`/`SGO1` không xuất hiện ở sổ ⇒ có bảng ánh xạ LE→khối nào không? *(khuyến nghị: BA phát bảng ánh xạ trước H5.)*
2. 2.137 dòng lỗi khuôn (17%) có tiền tố `R \| ` nhưng sai khuôn `<tk>_<bank> <curr>_<le>` ⇒ BA/owner quyết có mở rộng `tach_nguon` không *(khuyến nghị: không đoán; H5 báo phần thiếu theo `le = null`)*.
