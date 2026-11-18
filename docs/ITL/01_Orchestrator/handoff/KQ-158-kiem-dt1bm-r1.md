# KQ-158 — kiểm `BG-157` (`WO-156`, DT1b nhãn thật mốc 18/11) · R1

| | |
|---|---|
| **Thuộc** | `WO-156` · `BG-157` @ `dbb54c2` (nhánh `isp/DT1BM`) |
| **Phát bởi** | `fls-test` (phiên cloud con, R1) · 2026-11-18 |
| **Kết luận** | **ĐẠT** — 0 CHẶN · **1 NÊN SỬA** (chỉ chữ, ⛔ đổi mã/số) · 3 GHI NHẬN ⇒ backlog |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT1BM.md` v0.1 |

## 1 · Tái lập độc lập trên dữ liệu thật *(mã tự viết, ⛔ gọi `phan_loai_ly_do.py`; SO = Drive `1U-IQVO…` 10.606.726 B, L1 = `UNFORMATTED_VALUE`, cột `B` `D:G`)*
| Số | BG-157 | Đo độc lập | |
|---|---|---|---|
| Dòng SO dùng | 12.590 | **12.590** | ✔ *(hàng 10…12599 liền mạch, 0 trống giữa ⇒ 22 hàng bị loại = 12600–12621)* |
| Dòng L1 dùng | 12.590 | **12.590** | ✔ |
| Khớp 1-1 | 12.571 | **12.571** *(duyệt theo `seq` ↔ Σ min theo nhóm: cùng)* | ✔ |
| Thiếu | 19 | **19** — `dong_sheet` trùng **từng số** với BG | ✔ |
| Nhãn | 12 / 7 | `KHONG_CO_SAO_KE` **12** *(L1 ⛔ có dòng cùng Số CT)* · `KHOA_LECH` **7** *(cả 7 chỉ `ps_co`)* | ✔ |

## 2 · Bài học `FORMATTED_VALUE`
- Chuẩn hoá Số CT **không** mất chữ số: cột `B` L1 vẫn là **chuỗi** ở cả hai kiểu đọc *(12.547 chuỗi, 0 số thực ≥ 1e15)*; 43 hàng dạng khoa học ở mỗi phía = **chữ trong ô**, khớp 43/43, giao với 19 thiếu = 0.
- Nhưng **tiền** còn phụ thuộc định dạng: SO là CSV hiển thị, L1 đủ số lẻ ⇒ **7/7 `KHOA_LECH` là sai số < 1 xu** *(1 dòng Δ≈1e-10; 6 dòng Δ≈3e-3)* ⇒ `DT1BM-R1-01` NÊN SỬA (nhãn đúng luật, **lời kiểm tay của BG sai kỳ vọng**: người kiểm sẽ thấy hai số bằng nhau ở 2 số lẻ). `-02` · `-03` GHI NHẬN.

## 3 · Mốc 26/08 không đổi
`pytest tests/du_lieu tests/oracle/test_do_voi_hd1.py` **502 xanh** · `git diff 498bd06..HEAD` **rỗng** trên ảnh 26/08, `phan_loai_ly_do.json`, `tests/oracle/` · cổng `python tools/phan_loai_ly_do.py` ĐẠT (19 dòng, mỗi dòng 1 nhãn).

## 4 · Cổng mốc mới — đột biến **16/16 ĐỎ** *(bản sao `git archive`, trả nguyên, nền xanh)*
Ảnh mốc: bớt/thêm 1 dòng · đổi `khoa_bam` · lật `khop` · `so_dong` khai lệch (5) · nhãn: đổi 1 · hoán vị 2 *(giữ số đếm — chỉ vân tay danh tính cắn)* · xoá 1 dòng · khoá thô lạ (4) · `MONG_MOC`: `so_thieu` · `van_tay_nhan` · `van_tay_anh` (3) · PII: email *(do máy quét)* · Số CT trong `ghi_chu` *(cắn bằng luật cấu trúc + vân tay, ⛔ bằng quét token — quét token chỉ chạy khi có CSV thô)* (2) · mã: `>`→`>=` luật seq · mặc định `MONG` 26/08 đổi (2).
**PII tự đo:** 15.042 token ≥5 chữ số từ SO — **0** trong tệp nhãn/BG/bài; ảnh mốc 56 trùng đều là `dong_sheet` (số 10–12621), `khoa_bam` hex16 ⛔ băm trực tiếp token.

## 5 · Cổng toàn bộ
`--duong-nen --cong 5447` (một lần, một mình): **ĐẠT** — tập đỏ = đường nền **28 = 28** (thêm 0 · bớt 0) · chạy 3307 (≥3307) · skipped 0 · deselected 0 · `lint-imports` 11 kept 0 broken. `kiem_tai_lieu.py`: K1/K2/K4–K6 OK, **K3 ĐỎ 1 lỗi** ở `01_Orchestrator/isp-3.1/TIEN_DO.md:155` *(cột 4≠2; tệp ⛔ nằm trong diff của `DT1BM` — có sẵn ở nền, ⛔ của bước này)*.

## 6 · Việc kế · bản thô
Orchestrator: sửa chữ BG mục "Cách kiểm" cho `KHOA_LECH` *(R1-01)*; sửa `TIEN_DO.md:155` K3 *(ngoài bước)*. Bản thô `/tmp/r1_dt1bm/` **đã xoá**; sổ này ⛔ mang giá trị ô.
