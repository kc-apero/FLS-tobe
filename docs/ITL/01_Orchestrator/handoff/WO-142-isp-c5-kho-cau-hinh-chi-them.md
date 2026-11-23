# WO-142 — ISP 3.1.2 · Step 14 · C5: kho config chỉ-thêm có phiên bản (di trú 0027) — IX.FX + IX.HD đọc từ kho

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 ~02:50 UTC (nền C4 sau vòng sửa R1 `31509bd`) |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **BE-CF** — **phiên cloud** (Opus 4.8 · medium) · cụm PG **5434** của phiên ấy · nhánh `isp/C5` |
| **Nền** | ngọn `claude/bold-galileo-zukpaf-isp/C4` SAU vòng sửa R1 (C4 = nhánh làm việc + `fls/cau_hinh/hd.py` + tuyến `/config/hd` tĩnh). Chế độ tăng tốc: C4 có `BG-123` + R1 `KQ-124` **0 CHẶN**; DT2 đã gộp. |
| **Dải phiếu** | `BG-143` (bàn giao) · `KQ-144` (R1) · `KQ-145` (R2) · `KQ-146` (R3). Số trống kế tiếp: **147** |

## Vì sao
- ISP **Step 14 · C5** — nguồn sự thật duy nhất. Khái niệm mới duy nhất: **lưu kho config**. Hợp đồng tuyến `/config/fx` · `/config/hd` ⛔ đổi (F4 dùng lại nguyên).

## Spec phải đọc
| Tệp | Mục | Version |
|---|---|---|
| `02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md` | §1 · §2.1 · **Step 14** (· Step 2 C1 · Step 11 C4) | 3.1.2 |
| `02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` | §3.2.3 IX.TMP ("snapshot có version") · §3.5.3 D1 · Q4 | 3.1.2 |
| `fls/db/migrations/0016_khai_cot.sql` · `fls/repo/khai_cot.py` · bài của chúng | **khuôn chép**: chỉ-thêm · `version` · `hieu_luc_tu` do MÁY đặt · đủ-hoặc-không trong một giao dịch · ⛔ bản mặc định · lỗi "nguồn lạ" ≠ "chưa khai" | nền |
| `fls/cau_hinh/fx.py` · `fls/cau_hinh/hd.py` · `fls/cau_hinh/nguon_tinh.py` · `fls/api/bang_tuyen.py` · `tools/soi_bang_tuyen.py` | handler C1 · C4 hiện đọc tĩnh | nền |
| `tests/fixture/ix_fx.json` (DT2) · `tests/fixture/cau_hinh/atl_cay.json` · `mapping_master_cfg.json` (DT3) | ảnh nạp | nền |
| `CLAUDE.md` | Đ1–Đ5 · **Cổng** (sinh lại hiện vật sau khi đổi `schema.py`) · Bẫy | — |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo | Chiều ĐỎ |
|---|---|---|---|
| AC-1 (C5-B1) | nạp `ix_fx.json` thật ⇒ phiên bản **1**; `GET /config/fx` trả số từ KHO, đúng số dòng và `lac` như ISP ghi (**37** dòng; `lac = ['202306']`) — nếu ảnh đo ra khác ⇒ ⛔ sửa cho khớp, dừng và báo (Đ1/Đ4: số nào đếm gì) | `tests/db/…` + `tests/api/test_isp_config_fx.py` (pg) | bảng chưa có |
| AC-2 (C5-B2) | nạp lại cùng ảnh ⇒ phiên bản **2**, checksum trùng ⇒ `khong_doi = true`, ⛔ ghi đè bản 1 | pg | — |
| AC-3 (C5-B3) | `UPDATE` / `DELETE` một dòng `fls_cau_hinh_ban` hoặc `fls_cau_hinh_dong` ⇒ trigger ĐỎ **có tên** | pg | — |
| AC-4 (C5-B4) | golden DDL + `pg_verify` xanh sau `--update-golden` CÓ CHỦ ĐÍCH; sinh lại ERD (`erd_export --write` · `sync_erd_doc.py` · `sinh_ban_do_tang.py`) | pg + diff | — |
| AC-5 | IX.HD cũng đọc từ kho (`/config/hd` giữ hợp đồng C4: 74 nút · 73 MM · `chenh_mapping_master`); kho RỖNG (chưa nạp) ⇒ lỗi "chưa khai" có tên, ≠ lỗi "nguồn lạ"; ⛔ rơi về ảnh tĩnh | pytest | — |
| AC-6 | GỠ `fls/cau_hinh/tinh/ix_fx_mau.json` + mọi tham chiếu (`fx.py:100` · `tests/api/test_isp_config_fx.py` · `tests/cau_hinh/test_nguon_tinh.py` · `tools/soi_bang_tuyen.py`); `soi_bang_tuyen.py` ĐẠT với tuyến khai nguồn KHO; `?run_id=` ⇒ `400` giữ nguyên | `soi` + pytest | — |
| AC-6b (`C4-R1-05(a)`, orchestrator 18/11) | gỡ luôn hai ảnh tĩnh trong gói của C4: `fls/cau_hinh/tinh/ix_hd_cay.json` + `ix_mapping_master.json` (ảnh MM gói mang bảng phụ `tho` 84 hàng — 51 hàng có chuỗi ≥ 6 chữ số — mà C4 ⛔ đọc). Kho chỉ lưu khoá cần cho tuyến (MM: `hd_code`); nạp đọc ảnh DT3 ở `tests/fixture/cau_hinh/` qua đường TRUYỀN VÀO. Nếu một bài/tuyến buộc phải giữ tệp tĩnh ⇒ khai lý do trong BG | `git ls-files fls/cau_hinh/tinh` + pytest | — |
| AC-8 (nợ C4 — orchestrator 18/11) | `C4-R2-01`: mọi ô hỏng ⇒ `LoiHD(HD_HONG)` có tên, kể cả chuỗi số ≥ 4.301 chữ số (`ValueError` của `int()`), số JSON 5.000 chữ số, `'['*100000` (`RecursionError`) · `C4-R2-02`: câu lỗi cắt giá trị dài · `C4-R2-03`: bài biên `_so` (`'+3'` · `'3_0'` · `''` · `'３'`) · `C4-R3-01`: ghim `ten`/`nhom`/`dong_sheet` của một nút thật trên `/config/hd` · `C4-R3-02`: bài hai mã chênh MM (thứ tự `sorted`) | pytest, mỗi bài ĐỎ trước | — |
| AC-7 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` | — |

## Ràng buộc
- Di trú số **0027** (`0027_cau_hinh_chi_them.sql`): `fls_cau_hinh_ban` (`bang` · `phien_ban` · `nguon` · `checksum` · `actor` · `luc`) + `fls_cau_hinh_dong` (`ban_id` · `khoa` · `gia_tri jsonb`) — chỉ-thêm (O5, `INV-I08`).
- ⛔ ký (C7). ⛔ bảng config khác (C6, C8…). ⛔ sửa ảnh DT2/DT3. ⛔ đổi hợp đồng tuyến.
- Ghi kho THẬT: `KHONG` — chỉ kho test PG (O4). ⛔ `docker compose down`.

## Câu còn treo
- không có.
