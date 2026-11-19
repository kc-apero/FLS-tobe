# WO-212 — ISP 3.1.2 · Step 33 · C7: IX.FX ký tháng + CHẶN tháng chưa ký/thiếu (D1)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 19/11 ~00:40 UTC |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-19 |
| **Nhận** | `fls-dev` làn **BE-CF** — **phiên cloud** (Sonnet 5.5 · medium, luật A) · cụm PG **5434** · nhánh `isp/C7` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp C5 — kho config chỉ-thêm `0027` · C9 · C8 · C11 · F4 SCR-F08) |
| **Dải phiếu** | `BG-213` · `KQ-214` (R1) · `KQ-215` (R2). Số trống kế tiếp: **216** |

## Vì sao
- ISP **Step 33 · C7** (wave W11) — nguồn sự thật duy nhất. Phụ thuộc C5 (đã gộp). Khái niệm mới duy nhất: **ký niêm phong (sign-off)**. Mở đường F5 (Step 37) và C13 (Step 36).

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 33** (· Step 14 C5 làm khuôn) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.5.3 **D1** (DECIDED · A: owner ký mỗi tháng; thiếu tháng = CHẶN) · §3.2.4 | 3.1.2 |
| `02_BA/07_API_CONTRACT.md` | §1 (actor từ token) · §4i | hiện hành |
| `fls/api/the.py` (`the.kiem` → `Nguoi`, JWT HS256 fail-closed) · `fls/cau_hinh/fx.py` · `fls/repo/cau_hinh_repo.py` · `fls/api/bang_tuyen.py` · `tools/soi_bang_tuyen.py` | cửa token + khuôn kho C5 | nền |
| `CLAUDE.md` | Đ1–Đ5 | — |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (C7-B1) | `POST /api/fls/v1/config/fx/{yyyymm}/sign` token hợp lệ ⇒ **201**; `GET /config/fx` thấy `trang_thai = 'da_ky'`, `actor` = người trong token, `ky_luc` do MÁY đặt | `tests/cau_hinh/test_ky_fx_pg.py` (pg) | tuyến chưa có |
| AC-2 (C7-B2) | ký lại cùng tháng ⇒ **409** có tên; kho ⛔ thêm dòng | pg | — |
| AC-3 (C7-B3) | `fx_cua('202511')` chưa ký ⇒ `FX_CHAN` có tên tháng; tháng THIẾU hẳn trong IX.FX ⇒ `FX_CHAN` (⛔ rơi về tháng gần nhất); `yyyymm` hỏng ⇒ 400/lỗi có tên | đơn vị + API | — |
| AC-4 (C7-B4) | thân yêu cầu tự khai `actor` khác token ⇒ bị BỎ QUA; `actor` = token | an toàn | — |
| AC-5 (C7-B5) | không token / token hỏng ⇒ **401** từ cửa sẵn có (hồi quy — ⛔ mã lỗi mới) | hồi quy | — |
| AC-6 (C7-B6) | `soi_bang_tuyen.py`: POST khai `bang_ghi=('fls_cau_hinh_ban','fls_cau_hinh_dong')`, ⛔ chạm `fls_itl`; kho chỉ-thêm (trigger `0027` giữ) | `soi` + pg | — |
| AC-7 | `07_API_CONTRACT.md` §4i: KHAI dòng tuyến POST mới ⬜ (orchestrator lật ✅ khi gộp) — ⛔ đổi tuyến cũ | diff | — |
| AC-8 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` | — |

## Ràng buộc
- ⛔ UI ký (F5) · ⛔ huỷ ký · ⛔ phân quyền theo vai (O11). ⛔ di trú mới (dùng `0027`). Ghi kho THẬT: `KHONG`.
- Engine đã gộp (H4…H9) ⛔ buộc phải đổi sang `fx_cua` ở bước này — chỉ cung cấp hàm; khai trong BG chỗ nào sẽ nối sau.

## Câu còn treo
- không có.
