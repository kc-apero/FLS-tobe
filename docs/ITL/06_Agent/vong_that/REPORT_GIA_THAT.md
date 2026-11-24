# Vòng 1 test THẬT — GIẢ ↔ THẬT · 2026-11-24

> Sinh bởi `python tools/vong_that_voi.py --ghi` (`WO-355` AC-3) — ⛔ sửa tay. CHỈ số đếm + vân tay; ⛔ nội dung giao dịch, ⛔ phản hồi mô hình. G0 BÓNG: ⛔ ghi kho/sổ.

**KẾT: ĐỎ** — thiếu FLS_GCP_PROJECT (đường google-cloud) · CamGoiThat: ⛔ gọi API thật: cờ `--that` vắng · `FLS_CHO_GOI_API` ≠ 1 · `FLS_GCP_PROJECT` vắng (đường google-cloud) · `FLS_CLAUDE_WORKSPACE_ID` vắng (đường google-cloud — workspace `wrkspc_…` của tổ chức Anthropic gắn với project) · chế độ che `mo` gửi nguyên văn tên · số TK ⇒ đòi `FLS_GC_DU_LIEU_XAC_NHAN=1` (người vận hành xác nhận: project công ty · chế độ giữ dữ liệu của tổ chức Anthropic MỚI — ZDR cũ ⛔ mang sang; BG-360)

Mong (khai trước, Đ5): THẬT CHẠY được · A4 ĐẠT 4/4 · 0 ca phải-để-người bị nối ở mọi tập. Khác ⇒ ĐỎ.

| | |
|---|---|
| mô hình | A1_RI `claude-opus-5-5` · A2_PR_MAP `claude-opus-5-5` · A3_SI_ITL `claude-opus-5-5` · A4_AUDITOR `claude-sonnet-5-5` *(A4 = mô hình DỰ KIẾN G1; hôm nay MÃ)* |
| tập nhỏ | 12 ca dựng + 0 ca bể B · VẮNG (⛔ $FLS_HELDOUT_NOI_DUNG/b) · theo nhóm {'phai_nguoi': 5, 'phai_noi': 7} · vân tay `0669118e3590e44b` |
| bể A/B | VẮNG |
| che | `mo` (chủ 23/11: đọc toàn bộ) |
| đường gọi thật | `google-cloud` (claude.googleapis.com, Anthropic managed — CHÍNH, WO-359) |

## (a) Chuỗi 4 agent trên tập nhỏ

| chỉ số | GIẢ | THẬT |
|---|---|---|
| ô ĐỘC LẬP khớp / mẫu số | 557/557 | ⛔ thiếu FLS_GCP_PROJECT |
| ô VÒNG TRÒN khớp / mẫu số | 74/74 | ⛔ thiếu FLS_GCP_PROJECT |
| ô lệch · ⛔ đo được | 0 · 0 | ⛔ thiếu FLS_GCP_PROJECT |
| A4 ĐẠT (agent) | 4/4 | ⛔ thiếu FLS_GCP_PROJECT |
| dừng ở | — | ⛔ thiếu FLS_GCP_PROJECT |
| G0 A2.04: nối · nối sai · recall phải-nối · phải-người bị nối | 6 · 0 · 0.8571 · 0 | ⛔ thiếu FLS_GCP_PROJECT |

## (b) Fleet eval A2.04 — bể A (CŨ) · bể B (THẬT hiện tại)

⛔ bể giữ riêng VẮNG (`$FLS_HELDOUT_NOI_DUNG`) — dựng bằng `tools/dung_be_giu_rieng.py --doc-song` (ngoài repo).

## Token + chi phí (THẬT)

Giá tra ngày **2026-11-23** (Opus 5.5 $4/$20 · Sonnet 5.5 $2/$10 / 1M token vào/ra) · đường — — USD là ƯỚC.

| lời gọi | token vào | token ra | cache đọc | cache ghi | giây | USD ước |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0.0 | 0.0 |

**0 lời gọi thật** (Đ3: mẫu số 0 ⇒ ⛔ có số token/chi phí để báo — đây là KẾT QUẢ, ⛔ là "rẻ").
