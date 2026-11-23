# KQ-331 — R1 `WO-329` / `BG-330` *(ISP 3.1.2 · AG — 4 agent vận hành Voi gọi API)*

| | |
|---|---|
| **Kết quả** | **TRƯỢT** — **3 CHẶN · 3 NÊN SỬA** · 4 GHI NHẬN |
| **Phát phiếu** | `fls-test` *(vai KIỂM — ⛔ sửa mã · ⛔ gọi API thật · ⛔ ghi kho thật)* · 2026-11-23 · `isp/AG` `d8898c3` + cây gộp thử với `origin/claude/bold-galileo-zukpaf` `4f88282` · cụm 5444 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_AG.md` *(v0.1, `AG-R1-01…10`)* |
| **Gửi** | `DEV` — vòng sửa R1 *(`AG-R1-01…06`)*; chủ đọc `AG-R1-01` trước khi tin con số 627/627 |

## Kết luận
Đường ống chạy đúng và chặn đúng: chuỗi dừng đúng chỗ, 3 chốt gọi API chặn đủ, tầng sạch, 4 zip khớp nguồn. Nhưng **"khớp 100 %" chưa nói được điều chủ đang hiểu**, và cây gộp **đỏ**.

| # | Kiểm | Đo được | Kết |
|---|---|---|---|
| 1 | **"627/627" có thật không** | Thật **về đường ống**, ⛔ về mô hình. Bản phát lại do mô hình **GIẢ** sinh *(chép nguyên kết quả công cụ, `nguon_tra_loi = gia-lap` 4/4)* nhưng `report.html` ghi `claude-opus-5-5 ✅` và **0** lần chữ "giả"/"chứng minh". Vòng tròn: sửa `hd2_cong.json` ⇒ **627/627 y nguyên**; vòng tròn đầy đủ **70/627 = 11,2 %** *(`nguon` 28 · `hd2` 27 · `cong` 15)*; `voi` **557/627** không tròn với engine *(sửa 1 ô ⇒ LECH 1)*. Mẫu số 627 = **ô của các mẫu skill**, ⛔ "mọi dữ liệu": `voi` khoá số **318/660** · `hd2` **27/621**. A4 bắt đúng lỗi chép *(chép sai 1 ô ⇒ cổng ĐỎ)* | **CHẶN** `AG-R1-01` · NÊN SỬA `AG-R1-05` |
| 2 | Chuỗi tuần tự | Phá cổng giữa A2.02 ⇒ `DỪNG ở A2_PR_MAP/02_ghep_ref`, **10/16** skill `chưa chạy`. A4 TRƯỢT A2 *(ô `voi:tong.map_fls` +7)* ⇒ A3 · A4 `chưa chạy`, **0** lượt API *(A1 8 · A2 8)* | **ĐẠT** |
| 3 | Gọi API + bộ che | 3 chốt + ghim: **9/9 CHẶN**; đủ chốt ⇒ MỞ; `anthropic` ⛔ nhập khi bị chặn. Bộ che trên 10 ca khó BỊA: lọt **5/10** *(số TK chấm · gạch ×2 · điện thoại gạch · tên Hoa-thường)*, lớp 2 bắt **0/5**; mặc định TẮT (`null`) đúng C4; cờ `--cho-noi-dung` mở tự do | **CHẶN** `AG-R1-03` · NÊN SỬA `AG-R1-04` |
| 3b | Khớp quyết chủ 23/11 | C1 ✓ *(Opus 5.5 · G0 bóng · ⛔ `fallbacks`)* · C4 mặc định TẮT ✓ · C5 ✓ *(bể giữ riêng = `WO-338`)* · **C2 ✗** *(A4.02/03 `loai: lam` gọi `gemini-3.8-flash` chưa ghim; `--that` dựng đủ 4 nhà cung cấp ⇒ A1–A3 cũng ⛔ chạy thật được)* · C3 chưa vào mã | NÊN SỬA `AG-R1-06` · GHI NHẬN `AG-R1-10` |
| 4 | Tầng | `lint-imports` **11 kept**. Đột biến `import fls.db.kho` · `import psycopg` ⇒ lint + bài AST ĐỎ; `from fls.repo …` trong hàm ⇒ bài AST ĐỎ *(lint xanh)*; `importlib.import_module` ⇒ **xanh** | **ĐẠT** · GHI NHẬN `AG-R1-08` |
| 5 | Zip | skill = nguồn **20/20** byte · thẻ zip = thẻ docs **4/4** · checksum thẻ = máy tính = tính lại từ zip **4/4** · PII **0** | **ĐẠT** |
| 6 | Cây gộp thử | xung đột **2 tệp**, cùng một loại *(sàn `MONG_PYTEST_TOAN_BO` 4822 ↔ 4857)*, giải = thu thập thật **4.907** ⇒ 0 dấu xung đột. `kiem_tai_lieu` ĐẠT *(498 file · 2.996 bảng)* · `lint-imports` 11 kept · `quet_pii_repo` **0**. **`--duong-nen --cong 5444` MỘT lần, một mình: `KẾT: ĐỎ`** — toàn bộ `14 failed · 4877 passed · 2 xfailed · 14 errors` ⇒ **30 ≠ 28** *(thêm 2, bớt 0)*; web `3 failed · 687 passed` ⇒ **3 = 3** *(chạy 690)* | **CHẶN** `AG-R1-02` |

## Vì sao cây gộp đỏ *(gốc của `AG-R1-02`)*
Nhánh làm việc đã gộp H14: `hd2_cong.json` có thêm gói **`WP-C5c`** *(+980 dòng)*. Bản phát lại tra theo vân tay yêu cầu ⇒ vân tay A3.04 đổi ⇒ `KhongCoBanGhi` ⇒ `test_AC5_phat_lai__KET_DAT_lech_0` + `test_AC2_thu_tu_skill_va_agent` đỏ; mẫu số 627 → **631**, `chưa chạy 71`. Cần *(DEV, sau gộp)*: `--gia --ghi-phat-lai` · `--ghi-report` · `sinh_the_agent.py --zip` · nâng sàn = thu thập cây gộp *(4.907 lúc đo)* **cùng commit**.

## Đã làm ⇒ KIỂM ⛔ sửa mã
Mọi đột biến + cây gộp trên `git worktree` bản sao, đã gỡ; `git status` của nhánh `isp/AG` chỉ thêm **2 tệp** *(phiếu này + sổ)*. Lỗi do chính KIỂM trong lúc đo: symlink `.venv` bị `git add -A` ở cây gộp làm `quet_pii_repo` ĐỎ *"1 tệp ⛔ đọc được"* — gỡ khỏi chỉ mục ⇒ **0 chỗ** *(⛔ phát hiện của mã)*.

## Điều kiện ĐẠT ở R1 vòng sau
1. `AG-R1-01`: report một trang ghi **khối "Báo cáo này chứng minh gì / ⛔ chứng minh gì"** + nhãn bản phát lại *"sinh bằng mô hình GIẢ"* cạnh cột mô hình; tách ô vòng tròn *(`hd2`·`cong`·`nguon`)* khỏi ô độc lập.
2. `AG-R1-02`: gộp thử `origin/claude/bold-galileo-zukpaf` ⇒ `tests/agent` xanh ⇒ `--duong-nen` **28 = 28 · 3 = 3**.
3. `AG-R1-03`: bộ che bắt số có dấu `.`/`-`/cách + tên Hoa-thường; lớp 2 bắt dãy ≥ 9 chữ số **sau khi bỏ dấu**; thêm ≥ 3 bài ca khó *(có răng — phá bộ che ⇒ ĐỎ)*.
4. NÊN SỬA `AG-R1-04…06` hoặc DEV ghi lý do hoãn có chữ ký chủ.

⛔ Ngoài phạm vi vòng này: `kiem_so_song.py` *(BG-330 đã khai cứng đường Windows)* · `khop_owner.py --kiem` *(y hệt HEAD gốc)* · ⛔ API thật.
