# WO-065 — ISP 3.1.2 · Step 0: môi trường test + đường nền cổng + khung hai gói mới

| | |
|---|---|
| **Trạng thái** | `CHO_TEST` *(16/11 — `fls-dev` phát `BG-066`; chờ R1 `KQ-067`)* |
| **Phát bởi** | orchestrator (phiên điều phối ISP, thay `fls-ba` phát phiếu) · 2026-11-16 |
| **Nhận** | `fls-dev` — agent làn **BE-CF** |
| **Dải phiếu** | `BG-066` (bàn giao) · `KQ-067` (R1) · `KQ-068` (R2) · `KQ-069` (R3) |

## Vì sao
- ISP `docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 0 · S0** — nguồn sự thật duy nhất của phiếu này.
- Mọi bước sau cần một lệnh dựng môi trường + một đường nền đo thật; container cloud ⛔ có Docker, ⛔ pytest, ⛔ `.venv` (đo 16/11).

## Căn cứ
- Người dùng 16/11: *"Xác nhận các recommend. Xác nhận ISP. Bắt đầu triển khai"* — O4 = A (chạy ở container: PostgreSQL 16 cục bộ cổng 5433).

## Spec phải đọc *(tệp · mục · version)*
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · Step 0 | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §1.3.3 · §5.3.1 HD5 | 3.1.2 · sha256 `5cf6e576…` |
| `CLAUDE.md` | Đ1–Đ5 · Cổng · Bẫy | — |
| `01_Orchestrator/isp-3.1/TIEN_DO.md` | Quy ước chạy song song | 16/11 |

## Phạm vi
| TRONG | NGOÀI |
|---|---|
| `tools/dung_moi_truong_isp.sh` (chạy lại được, ⛔ phá gì đã có): venv `/home/user/FLS-tobe/.venv` + `requirements.txt`; cụm PostgreSQL 16 ngoài repo, cổng 5433, role `fls`/`fls` có `CREATEDB`, kho `fls`; `python -m fls.db.pg_migrate` | sửa bất kỳ bài đỏ có sẵn nào — ghi tên vào đường nền, chuyển orchestrator |
| đường nền THẬT mọi cổng chạy được ở container → `docs/ITL/03_Dev/isp-3.1/DUONG_NEN.md` (lệnh · exit code · số đếm, bài đỏ ghi TÊN) | dữ liệu thật vào kho (`FLS_CHO_GHI_THAT` ⛔ đặt) |
| 2 gói rỗng `fls/cau_hinh` · `fls/bao_cao` (docstring vai) + 2 hợp đồng `.importlinter` (⛔ `psycopg` · `fls.repo` · `fls.db`) | `docker compose` (⛔ có Docker; ⛔ bao giờ `down`) |
| làm rõ của orchestrator: chứng minh kho test RIÊNG theo agent chạy được — hai lượt pg song song với `PG_DSN_TEST` khác nhau ⛔ giẫm nhau | |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (S0-B1) | `python -m pytest` có dòng tổng kết; mọi bài đỏ/lỗi ghi TÊN trong `DUONG_NEN.md` | chạy toàn bộ | — (đường nền, ⛔ sửa) |
| AC-2 (S0-B2) | 26/26 di trú áp; `pg_verify` exit 0 | `python -m fls.db.pg_migrate` | — |
| AC-3 (S0-B3) | `lint-imports`: 11 hợp đồng giữ (9 + 2) | `.venv/bin/lint-imports` | thêm `import psycopg` vào `fls/bao_cao/__init__.py` ⇒ ĐỎ, gỡ ⇒ xanh |
| AC-4 (S0-B4) | `do_voi_so_luong.py` exit 0, in `chay 9845 / co 9967` | `python tools/do_voi_so_luong.py` | — |
| AC-5 (S0-F1) | `python -m pytest tests/web` có dòng tổng kết (node headless) | chạy | — |
| AC-6 | hai lượt `pytest tests/db -k pg` (hoặc một tệp `*_pg.py` nhỏ) chạy SONG SONG với `PG_DSN_TEST` = `…/fls_test_a` và `…/fls_test_b` đều xanh; cả hai kho tồn tại | chạy song song, `psql -l` | — |

## Dữ liệu
- Bảng/cột chạm: kho `fls` cục bộ RỖNG (di trú) + kho test. Ghi kho THẬT: `KHONG` (container ⛔ có sổ thật).

## Câu còn treo
- không có.

## Rủi ro
1. `initdb` từ chối chạy bằng root ⇒ chạy qua user `postgres` (uid 102 có sẵn).
2. `pyproject.toml` đã có `-q` — ⛔ thêm `-q` (mất dòng tổng kết).
3. Thiếu `PYTHONUTF8=1` thì `lint-imports` im lặng in 0 byte.
