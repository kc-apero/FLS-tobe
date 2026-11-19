# KQ-232 — Kiểm R2 CUỐI · ISP 3.1.2 · WO-226 *(alias ITE)*

| | |
|---|---|
| **Từ → Đến** | fls-test (R2, Sonnet 5.5) → orchestrator |
| **Mã kiểm** | `isp/ITE` @ `c43a67c` · cây gộp thử `thu/ITE` = `origin/claude/bold-galileo-zukpaf` @ `06db9f9` + `isp/ITE` · sổ `SO_PHAT_HIEN_ISP-3.1_ITE.md` v0.2 |
| **Kết** | **ĐẠT** — 0 CHẶN · 0 NÊN SỬA · `ITE-R1-01` **đóng** · `ITE-R1-02` GHI NHẬN ⇒ backlog |

## 1 · Cây gộp thử
Xung đột **2 tệp**: `tools/dung_moi_truong_isp.sh` (`MONG_PYTEST_TOAN_BO`) + `tests/test_dung_moi_truong_isp.py` (bài ghim sàn + chú thích gộp). Gộp tay: giữ nhánh làm việc (4034) + ITE (+30 +20) ⇒ sàn **4084** = thu thập thật (đường nền chạy 4084 ≥ 4084). `07_API_CONTRACT.md` ⛔ xung đột: changelog v3.25 đứng trên v3.24 (nhánh làm việc v3.24).

## 2 · Soát
1. **`/gates`** *(`doc_cong_hd2` trên `hd2_cong.json` thật, 8 cổng)*: `C3A` lech **35** · `C3B` **42** · `C3` **77** (`Σ 216683/216760 + 77`); `C2` · `C4` · `C4A` · `C4B` = **0**; `C5` `null` có tên. Khai sai `mong` ⇒ `false`; hỏng khoá ⇒ `null` có tên *(bài ghim)*. Qua tuyến `/gates` thật có trường `lech_co_chu_dich` *(`xu_ly.py:212`)*.
2. **`khop` ⛔ cộng lệch**: C3a **205140** · C3b **11543** *(JSON + oracle)*; cổng đòi `khop + lech == tong_o` **và** `lech == mong`.
3. **`07_API_CONTRACT.md`** v3.25: dòng `/gates` + changelog; chỉ THÊM.
4. **Đột biến 6/6 ĐỎ** *(bản sao `git archive`, 4 bộ liên quan)*: bỏ trường `/gates` · cổng cộng lệch vào `khop` · bỏ điều kiện `lech == mong` · cha ⛔ Σ · mong một chiều · dụng cụ đo cộng lệch vào `khop` JSON.
5. **Cổng**: 5 bộ liên quan **196 passed**. `--duong-nen --cong 5434` MỘT lần, một mình: toàn bộ 12 failed · 4056 passed · 2 xfailed · 14 errors = **28 = 28** node id *(thêm 0 · bớt 0)*, 4084 bài. ⚠ phiên chạy bị cắt ở giới hạn 10 phút **sau** phần toàn bộ ⇒ phần `tests/web` của script ⛔ chạy; chạy riêng `pytest tests/web` = **3 failed · 672 passed = 675** *(3 = đường nền; ⛔ tự so node id)*. `lint-imports` 11 kept · 0 broken · `kiem_tai_lieu` ĐẠT *(376 tệp · 104 mã QĐ)* · `soi_bang_tuyen` 46/46.

## 3 · Giao
ĐẠT ⇒ orchestrator gộp. Cổng gộp: nhớ nâng sàn lên **4084** *(đã khớp ở cây thử)*. `ITE-R1-02` ⇒ backlog.
