# Vòng 1 test THẬT — GIẢ ↔ THẬT · 2026-11-23

> Sinh bởi `python tools/vong_that_voi.py --ghi` (`WO-355` AC-3) — ⛔ sửa tay. CHỈ số đếm + vân tay; ⛔ nội dung giao dịch, ⛔ phản hồi mô hình. G0 BÓNG: ⛔ ghi kho/sổ.

**KẾT: ĐỎ** — thiếu ANTHROPIC_API_KEY · CamGoiThat: ⛔ gọi API thật: `FLS_CHO_GOI_API` ≠ 1 · khoá `ANTHROPIC_API_KEY` vắng trong biến môi trường · chế độ che `mo` gửi nguyên văn tên · số TK ⇒ đòi `FLS_ZDR_DA_BAT=1` (ZDR — quyết chủ 23/11)

Mong (khai trước, Đ5): THẬT CHẠY được · A4 ĐẠT 4/4 · 0 ca phải-để-người bị nối ở mọi tập. Khác ⇒ ĐỎ.

| | |
|---|---|
| mô hình | A1_RI `claude-opus-5-5` · A2_PR_MAP `claude-opus-5-5` · A3_SI_ITL `claude-opus-5-5` · A4_AUDITOR `claude-sonnet-5-5` *(A4 = mô hình DỰ KIẾN G1; hôm nay MÃ)* |
| tập nhỏ | 12 ca dựng + 20 ca bể B · mẫu 20/70 ca bể B (hạt 355) · theo nhóm {'chua_chot': 1, 'l3': 2, 'phai_nguoi': 9, 'phai_noi': 20} · vân tay `4f5a3f7b1ee013f2` |
| bể A/B | có (ngoài repo) |
| che | `mo` (chủ 23/11: đọc toàn bộ) |

## (a) Chuỗi 4 agent trên tập nhỏ

| chỉ số | GIẢ | THẬT |
|---|---|---|
| ô ĐỘC LẬP khớp / mẫu số | 557/557 | ⛔ thiếu ANTHROPIC_API_KEY |
| ô VÒNG TRÒN khớp / mẫu số | 74/74 | ⛔ thiếu ANTHROPIC_API_KEY |
| ô lệch · ⛔ đo được | 0 · 0 | ⛔ thiếu ANTHROPIC_API_KEY |
| A4 ĐẠT (agent) | 4/4 | ⛔ thiếu ANTHROPIC_API_KEY |
| dừng ở | — | ⛔ thiếu ANTHROPIC_API_KEY |
| G0 A2.04: nối · nối sai · recall phải-nối · phải-người bị nối | 8 · 1 · 0.35 · 1 | ⛔ thiếu ANTHROPIC_API_KEY |

## (b) Fleet eval A2.04 — bể A (CŨ) · bể B (THẬT hiện tại)

| chỉ số | GIẢ bể A | THẬT bể A | GIẢ bể B | THẬT bể B |
|---|---|---|---|---|
| ca (mẫu số chính) | 65 | ⛔ thiếu ANTHROPIC_API_KEY | 65 | ⛔ thiếu ANTHROPIC_API_KEY |
| nối | 2 | ⛔ thiếu ANTHROPIC_API_KEY | 2 | ⛔ thiếu ANTHROPIC_API_KEY |
| nối sai | 2 | ⛔ thiếu ANTHROPIC_API_KEY | 1 | ⛔ thiếu ANTHROPIC_API_KEY |
| tỉ lệ nối sai | 1.0 | ⛔ thiếu ANTHROPIC_API_KEY | 0.5 | ⛔ thiếu ANTHROPIC_API_KEY |
| recall phải-nối | 0.0 | ⛔ thiếu ANTHROPIC_API_KEY | 0.0333 | ⛔ thiếu ANTHROPIC_API_KEY |
| ca phải-để-người bị nối | 2 | ⛔ thiếu ANTHROPIC_API_KEY | 1 | ⛔ thiếu ANTHROPIC_API_KEY |
| L3 bị nối | 0 | ⛔ thiếu ANTHROPIC_API_KEY | 0 | ⛔ thiếu ANTHROPIC_API_KEY |
| điểm TB 0–2 | 1.4923 | ⛔ thiếu ANTHROPIC_API_KEY | 1.5231 | ⛔ thiếu ANTHROPIC_API_KEY |

## Token + chi phí (THẬT)

Giá tra skill `claude-api` ngày **2026-11-23** (Opus 5.5 $4/$20 · Sonnet 5.5 $2/$10 / 1M token vào/ra) — USD là ƯỚC.

| lời gọi | token vào | token ra | cache đọc | cache ghi | giây | USD ước |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 |

**0 lời gọi thật** (Đ3: mẫu số 0 ⇒ ⛔ có số token/chi phí để báo — đây là KẾT QUẢ, ⛔ là "rẻ").
