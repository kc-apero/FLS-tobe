# BG-071 — bàn giao `WO-070` *(ISP 3.1.2 · Step 1 · H1)* — `CA.GL` thuần: Nợ/Có × 5 tiền tệ → tồn luỹ kế · bVND · mUSD

| | |
|---|---|
| **Thuộc** | `WO-070` |
| **Phát bởi** | `fls-dev` *(làn **BE-HC**)* · 2026-11-16 |
| **Nhận** | `fls-test` — R1 `KQ-072` · R2 `KQ-073` · R3 `KQ-074` *(dải orchestrator cấp)* |
| **Commit** | nhánh **cục bộ** `isp/H1` @ `5c0a2e2` *(mã + bài thử — `5c0a2e2c6b103a5837cd5de5e8ae2a8499014931`)* — tách từ `329fa68`; ⛔ đẩy theo O2 = A *(orchestrator gộp vào `claude/laughing-bohr-331pt0` sau R3 rồi mới đẩy)*. Phiếu này nằm ở commit kế tiếp *(chỉ giấy)* |
| **Worktree** | `/home/user/FLS-tobe/.claude/worktrees/isp-h1` · cụm PostgreSQL riêng cổng **5435** *(`PG_DSN=…localhost:5435/fls` · `PG_DSN_TEST=…localhost:5435/fls_test`)* |
| **Spec đã đọc** | ISP `IncrementalStepPlan-FLS-Voi_v3.1.2.md` §1.3 · §2.1 · **Step 1 · H1** *(8 trường + Substep 1/2)* · AP `AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` §3.3.1 hàng PD `405` · `406 · 412` · §3.2.1 hàng `IX.FX` · AC9 *(sha256 đo lại `5cf6e576ff46f0886eb4…` — khớp WO)* · `SO_PHAT_HIEN_ISP-3.1.md` cột *luật phòng tái phạm* *(10 hàng `S0-R1-01…10`)* · `DUONG_NEN.md` §1 · §4.3 · `TIEN_DO.md` *Quy ước chạy song song* · `CLAUDE.md` Đ1–Đ5 · `10_HOP_DONG_AGENT.md` §3.3 |

## Cổng vào *(`05` §5)*
- git thật: `git log -1` = `329fa68 Nền wave 1: nhánh làm việc + isp/S0 @ 3d8318c …` trên nhánh `isp/H1`, cây sạch — khớp lệnh orchestrator.
- version hợp đồng: ISP 3.1.2 · AP v3.1.2 sha256 `5cf6e576…` khớp. Run id: WO ⛔ nói "đã chạy" ⇒ ⛔ cần.
- WO đủ trường §3.1 *(Màn hình: ⛔ chạm UI; Dữ liệu: `KHONG`)*.
- ⚠ Theo lệnh orchestrator *(⛔ tệp ngoài `fls/bao_cao/**` · `tests/bao_cao/**` · phiếu này)*: Dev **⛔ đổi** `Trạng thái` của `WO-070`, ⛔ thêm dòng dashboard §5, ⛔ sửa `handoff/README.md`, ⛔ ghi `08_CHANGELOG_RELEASE.md` — orchestrator ghi lúc gộp *(`TIEN_DO.md` · `S0-R1-08`)*.
- Luật phòng tái phạm của S0 đã áp: `S0-R1-04` *(lỗi in nguyên nhân MỘT dòng — có bài canh `"\n" not in`)* · `S0-R1-05` *(mọi phép "khớp" in mẫu số — bài 6 dòng đếm `60` ô so; B4 đòi `gl.py` có mã trước khi tin `KEPT`)* · `S0-R1-08` *(⛔ chèn bảng nhật ký dùng chung)* · `S0-R1-02` *(đường nền so bằng MÁY — `--duong-nen`)*.

## Substep 1 — test cases · kế hoạch tối thiểu · lệnh · giới hạn
1. **Test cases** *(chọn từ mục 6 của Step 1, phủ mọi dòng mục 8)*: `H1-B1` → AC-1 · `H1-B2` → AC-2 · `H1-B3` → AC-3 · `H1-B4` → AC-4, cộng Goal *"đúng tay tính trên 6 dòng tổng hợp"* *(ISP §2 · §3 Mock/static)* và *"tồn luỹ kế theo thứ tự dòng đưa vào"* *(ISP §3 Gồm)*. FE: N/A *(ISP §4 — lát cắt là hàm thuần)*.
2. **Kế hoạch tối thiểu**: một hàm thuần `tinh_gl(dong, fx)` + dataclass vào `DongGL` / ra `KetQuaDongGL` + hai lỗi có tên `ThieuTyGia` · `TienTeNgoaiGL` ở `fls/bao_cao/gl.py`; bài ở `tests/bao_cao/test_gl.py` *(+ `__init__.py` rỗng như mọi thư mục `tests/*`)*. ⛔ tuyến, ⛔ màn, ⛔ config, ⛔ kho.
3. **Lệnh** *(gốc worktree; `export PG_DSN='postgresql://fls:fls@localhost:5435/fls' PG_DSN_TEST='postgresql://fls:fls@localhost:5435/fls_test' PYTHONUTF8=1`)*: `/home/user/FLS-tobe/.venv/bin/python -m pytest tests/bao_cao/test_gl.py` · `/home/user/FLS-tobe/.venv/bin/lint-imports` · `bash tools/dung_moi_truong_isp.sh --cong 5435 --duong-nen`.
4. **Giới hạn**: số tổng hợp, ⛔ so với đáp án 406 *(H4)*; ⛔ dòng HR *(H7)*; ⛔ cột `CA` Cash/Bank qua `IX.ORG` *(C8)*; tỷ giá vào bằng THAM SỐ, ⛔ từ `IX.FX` trong kho *(C1 · C5)*.

## Lệch spec đã xử
| # | Spec nói | Đã làm | Căn cứ |
|---|---|---|---|
| L1 | ISP `H1-B1` mong *"bVND 2,5 · **mUSD 98,039…**"* | bài theo **CÔNG THỨC AP**: mUSD = `2,5 ÷ 25.500 × 10^3` = **0,098039…** *(= 98,039… **nghìn** USD)*; thêm hai dòng canh đơn vị `musd_no < 1` và `musd_no × 10^3` làm tròn 3 chữ số = `98.039` để bản đính chính ⛔ bị lật im lặng | **orchestrator đính chính 16/11** *(lệnh giao bước)*: AP §3.3.1 PD 406 *"BO/BP = tỷ giá × E\|F / 10^9 (bVND); BR/BS = BO\|BP ÷ USD × 10^3 (mUSD)"* ⇒ `98,039…` là sai đơn vị; đột biến `M1` *(× 10^6 — đúng con số ISP)* làm **4** bài đỏ |
| L2 | *"tồn = tồn trên + Nợ − Có"* — ⛔ nói tồn theo **từng tiền tệ** hay **một cột** | tồn **theo từng tiền tệ, bằng nguyên tệ**, cộng dồn theo thứ tự đưa vào cả bảng *(⛔ theo TK)* | đọc công thức: câu tồn đứng SAU *"tách Nợ/Có theo 5 tiền tệ"* và TRƯỚC bước BO/BP; cộng USD với VND bằng nguyên tệ vô nghĩa. ⚠ **Chưa đối chiếu số thật** *(repo ⛔ có ô nào của CALC ZONE `BM–BT`)* ⇒ câu hỏi **Q1** |
| L3 | ISP mục 6 chỉ có `H1-B1…B4` | thêm bài cho hành vi mà mã PHẢI có để ⛔ im lặng: tiền tệ ngoài 5 cột ⇒ `TienTeNgoaiGL`; float ⇒ `TypeError`; ngữ cảnh `Decimal` cố định; ⛔ sửa đầu vào; tỷ giá ≤ 0 ⇒ `ThieuTyGia` *(0 = dấu vết SUMIFS)* | `INV-I16` *(cấm mặc định im lặng)* · lệnh orchestrator *"Dùng Decimal, ⛔ float cho tiền"* · `fls/bao_cao/__init__.py` *("cùng đầu vào ⇒ cùng con số")*. Mỗi bài có đột biến cắn nó *(log §Đột biến)* |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/gl.py` *(mới)* | `CA.GL` thuần: `tinh_gl(dong, fx)` · `DongGL` · `KetQuaDongGL` · `TIEN_TE_GL` *(khuôn 5 cột, ⛔ chứa tỷ giá)* · `ThieuTyGia(LookupError)` · `TienTeNgoaiGL(ValueError)`. Docstring chép NGUYÊN VĂN công thức NOW 405 · 406, ánh xạ BO/BP/BR/BS → trường, ba hành vi AS-IS GIỮ, hai lỗi AS-IS ⛔ giữ |
| `tests/bao_cao/__init__.py` *(mới, rỗng)* | như mọi thư mục `tests/*` *(đo: `tests/ledger/__init__.py` · `tests/oracle/__init__.py` = 0 byte)* |
| `tests/bao_cao/test_gl.py` *(mới)* | **15** hàm `def test_` *(grep `^def test_`)* → **18** bài pytest thu thập *(2 hàm `parametrize`: ×2 · ×3 ⇒ 15 − 2 + 5)*; mọi số mong TÍNH TAY, ghi nguyên chữ số |
| `docs/ITL/01_Orchestrator/handoff/BG-071-ban-giao-wo-070.md` *(mới)* | phiếu này |

## Cổng *(kết quả nguyên văn — `PG_DSN='postgresql://fls:fls@localhost:5435/fls'` · `PG_DSN_TEST='postgresql://fls:fls@localhost:5435/fls_test'` · `PYTHONUTF8=1`, venv `/home/user/FLS-tobe/.venv`)*
⚠ Lượt đường nền chạy trên cây làm việc NGAY TRƯỚC commit `5c0a2e2` — cùng nội dung 3 tệp *(sha256 `gl.py` = `82c1921bc2763492…` trước và sau; `test_gl.py` ⛔ sửa sau lượt)*; bài đích + lint chạy lại trên `5c0a2e2`.

| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/bao_cao/test_gl.py` | exit 0 · `18 passed in 0.43s` *(cây `5c0a2e2`; trước commit: `18 passed in 0.47s`)* |
| `bash tools/dung_moi_truong_isp.sh --cong 5435 --duong-nen` *(= `python -m pytest` toàn bộ + `tests/web`, MÁY so tập đỏ với `duong_nen_bai_do.txt` theo node id)* | exit 0 · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` · toàn bộ: `12 failed, 2450 passed, 2 xfailed, 14 errors in 313.72s (0:05:13)` · `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · web: `3 failed, 661 passed in 179.66s (0:02:59)` · `[ĐẠT] đường nền tests/web  tập đỏ = đường nền: 3 = 3 node id (thêm 0 · bớt 0)`. Mẫu số *(Đ3)*: `2478 tests collected` = 12 + 2.450 + 2 + 14 = **2.460** của S0 + **18** của H1 *(`pytest --collect-only tests/bao_cao` ⇒ `18 tests collected`)* |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/FLS-tobe/.claude/worktrees/isp-h1/.venv/Scripts/lint-imports.exe'` *(`tools/kiem_so_song.py` dòng 406 `do_may` gọi cứng đường Windows; công cụ còn đọc kho THẬT — container ⛔ có)*. Y như S0 *(`BG-066` · việc NGOÀI ISP orchestrator đã đề xuất 16/11)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (174 file, 1855 bang, 723 o ngay, 104 ma QD), khong chi 'khong thay loi'`. Đ3 — phiếu này CÓ được soi: tạm cất nó ra ⇒ `173 file, 1848 bang`; trả vào ⇒ `174 file, 1855 bang` *(+7 = đúng 7 bảng của phiếu, K3 ⛔ thấy ô vỡ)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` — ĐỎ vì kho `fls` cục bộ RỖNG *(`B3` · `B4` · `C5` · `C5b` KHONG DO DUOC · `A1` · `B1` · `C6` DOI TRANG THAI)*, y như S0. ⭐ Cùng lệnh trên bản xuất nguyên `329fa68` *(`git archive`)* ⇒ `diff` **rỗng** *(36 dòng mỗi bên)* ⇒ ⛔ phải do H1 |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `.venv/bin/lint-imports` *(container: `bin/`, ⛔ `Scripts/*.exe`)* | exit 0 · `Contracts: 11 kept, 0 broken.` · dòng hợp đồng 11: `fls.bao_cao la engine bao cao/phan bo thuan, khong duoc biet tang kho KEPT` |
| `python -m fls.db.pg_migrate` *(⛔ chạm schema — chạy vì ISP Substep 2 ⑥)* | exit 0 · `khong co gi de ap` · `pg_verify: khop` |

## Bằng chứng từng AC
| AC | Mong | Bằng chứng *(bài · phép đo · đột biến cắn nó)* | Kết |
|---|---|---|---|
| AC-1 · `H1-B1` | bVND 2,5 · mUSD theo công thức AP *(0,098039… — đính chính L1)* | `test_H1_B1_dong_VND_No_ra_bVND_2_5_va_mUSD_theo_cong_thuc_AP` PASSED: `bvnd_no == 2.5` · `musd_no.quantize(1E-12) == 0.098039215686` · `musd_no < 1` · `(musd_no × 1000).quantize(0.001) == 98.039` · `no == {VND: 2500000000, 4 cột 0}`; cùng ca là dòng 1 của bài 6 dòng. Đột biến `M1` *(× 10^6 — đúng con số ISP)* ⇒ **4** đỏ *(B1 · B2 · 6 dòng · int)*; `M10` *(tiền vào cả 5 cột)* ⇒ **2** đỏ *(B1 · 6 dòng)* | đạt |
| AC-2 · `H1-B2` | tách đúng cột Có; tồn = tồn trước − Có | `test_H1_B2_dong_USD_Co_tach_dung_cot_Co_ton_bang_ton_truoc_tru_Co` PASSED: `co == {USD: 40000, 4 cột 0}` · `no` = 5 × 0 · tồn USD `100000` → `60000` = tồn trước − `40000` · tỷ giá tháng `202502` = `25000` *(⛔ `25500` của 202501)* · bVND Có `1` · mUSD Có `0.04`. Kèm `test_ton_luy_ke_theo_THU_TU_dong_dua_vao__giu_hanh_vi_AS_IS` PASSED *(đảo thứ tự ⇒ tồn USD giữa bảng `-40000`, tồn cuối y nguyên)*. `M4` *(tồn ⛔ luỹ kế)* ⇒ **3** đỏ · `M5` *(tra nhầm tháng)* ⇒ **3** đỏ | đạt |
| AC-3 · `H1-B3` | lỗi CÓ TÊN, ⛔ trả 0 | **5** bài B3 PASSED — tháng vắng · tháng có mà vắng cột tiền tệ · vắng USD *(mUSD cần)* · tỷ giá `0` · tỷ giá âm ⇒ `ThieuTyGia` mang `thang` · `tien_te` · `vi_tri`, thông điệp MỘT dòng *(`S0-R1-04`)*. `M2` *(tháng vắng ⇒ tỷ giá 0, đúng SUMIFS)* ⇒ bài tháng vắng đỏ · `M3` *(nhận tỷ giá 0)* ⇒ `[bang_0]` đỏ · `M9` *(gõ cứng USD 25.500)* ⇒ **3** đỏ gồm bài vắng USD | đạt |
| AC-4 · `H1-B4` | `fls/bao_cao` ⛔ chạm DB | `lint-imports` exit 0 · `11 kept, 0 broken` + `test_H1_B4_fls_bao_cao_khong_cham_kho__lint_imports_hop_dong_11` PASSED *(tiến trình con chạy riêng hợp đồng 11 ⇒ `Contracts: 1 kept, 0 broken.`; đòi `gl.py` có `def tinh_gl` TRƯỚC khi tin `KEPT` — Đ3: trước H1 gói chỉ có `__init__.py`, hợp đồng xanh trên tập rỗng: `Contracts: 11 kept, 0 broken.` lúc `329fa68`)*. Đ5: `M12` `import psycopg` ⇒ pytest **1** đỏ *(B4)* + `lint-imports exit=1 · Contracts: 10 kept, 1 broken. · vỡ: fls.bao_cao la engine bao cao/phan bo thuan, khong duoc biet tang kho BROKEN`; `M13` `import fls.db.kho` ⇒ y hệt; trả nguyên sha256 khớp | đạt |
| Goal *(ISP §2)* | *"đúng tay tính trên 6 dòng tổng hợp"* | `test_H1_sau_dong_tong_hop_khop_tay_tinh_tung_o` PASSED — **60** ô so *(6 dòng × (1 tỷ giá + 4 ô quy đổi + 5 ô tồn))*, 5/5 tiền tệ, 2/2 tháng, 3 dòng Nợ + 3 dòng Có; số mong ghi nguyên chữ số, phép tính tay cạnh từng hàng | đạt |
| Mục 8 · *"đỏ trước khi có mã"* | ĐỎ vì THIẾU hành vi | `ModuleNotFoundError: No module named 'fls.bao_cao.gl'` · exit 2 *(cú pháp bài sạch: `py_compile` exit 0)* — đúng lý do ISP ghi cho `H1-B1` *("module chưa có")* | đạt *(⚠ còn yếu #6)* |
| Mục 8 · 3 vòng review | R1 · R2 · R3 | chờ `KQ-072` | — |

## Log ĐỎ → XANH
**ĐỎ** *(cây `329fa68` + 2 tệp bài, ⛔ có `gl.py`)*:
```text
$ python -m py_compile tests/bao_cao/test_gl.py
exit=0
$ python -m pytest tests/bao_cao/test_gl.py
__________________ ERROR collecting tests/bao_cao/test_gl.py ___________________
tests/bao_cao/test_gl.py:40: in <module>
    from fls.bao_cao.gl import (
E   ModuleNotFoundError: No module named 'fls.bao_cao.gl'
=========================== short test summary info ============================
ERROR tests/bao_cao/test_gl.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.09s
exit=2
```
**XANH**: `18 passed in 0.47s` exit 0 *(trước commit)* · `18 passed in 0.43s` exit 0 *(cây `5c0a2e2`, `-vv`: 18/18 `PASSED`)*.

**Đột biến** *(Đ5 — kịch bản phá `gl.py` từng chỗ, chạy `test_gl.py`, trả nguyên; mỗi phép thay `assert` khớp ĐÚNG 1 lần)*: `gl.py sha256 gốc = 82c1921bc2763492` → `sau khi trả = 82c1921bc2763492 · KHỚP gốc` · **`đột biến: 13 · bị cắn: 13 · sống: 0`** · `sau trả nguyên: pytest exit=0 · 18 passed in 0.39s`.

| # | Phá gì | pytest | Bài đỏ |
|---|---|---|---|
| M1 | `× 10^3` → `× 10^6` *(đơn vị ISP)* | `4 failed, 14 passed` | B1 · B2 · 6 dòng · int |
| M2 | tháng vắng ⇒ `return 0` *(SUMIFS)* | `1 failed, 17 passed` | B3 tháng vắng |
| M3 | `gia <= 0` → `gia < 0` | `1 failed, 17 passed` | B3 `[bang_0]` |
| M4 | tồn = `no - co` *(⛔ luỹ kế)* | `3 failed, 15 passed` | B2 · 6 dòng · thứ tự |
| M5 | tỷ giá luôn tháng nhỏ nhất | `3 failed, 15 passed` | B2 · 6 dòng · B3 tháng vắng |
| M6 | bỏ ngữ cảnh `Decimal` cố định | `1 failed, 17 passed` | ngữ cảnh |
| M7 | bỏ chặn tiền tệ ngoài 5 cột | `1 failed, 17 passed` | `TienTeNgoaiGL` |
| M8 | nhận float | `3 failed, 15 passed` | float `[no]` `[co]` `[ty_gia]` |
| M9 | gõ cứng tỷ giá USD 25.500 | `3 failed, 15 passed` | B2 · 6 dòng · B3 vắng USD |
| M10 | tiền vào cả 5 cột | `2 failed, 16 passed` | B1 · 6 dòng |
| M11 | `fx.pop(...)` *(sửa đầu vào)* | `6 failed, 12 passed` | 6 dòng · thứ tự · B3 tháng vắng · `TienTeNgoaiGL` · ngữ cảnh · thuần |
| M12 | `import psycopg` | `1 failed, 17 passed` | B4 *(+ `lint-imports` `10 kept, 1 broken`)* |
| M13 | `import fls.db.kho` | `1 failed, 17 passed` | B4 *(+ `lint-imports` `10 kept, 1 broken`)* |

**Đường nền — hai lượt** *(lệnh orchestrator: ghi CẢ HAI nếu chạy lại)*:
1. Lượt 1 *(`2026-11-16T08:12Z`)* — **⛔ dùng làm bằng chứng**: log đặt ở scratchpad mà **mọi agent con của phiên điều phối DÙNG CHUNG**; làn BE-CF *(cổng 5434, `GOC = …/worktrees/isp-c1`)* cùng đặt tên `duong_nen_1.log` ⇒ phần đầu log bị ghi đè *(dòng tiêu đề mang `isp-c1` · `5434`)*, và một dòng `exit=143` lạ chen vào giữa. Phần đuôi của lượt H1 vẫn đọc được: `12 failed, 2450 passed, 2 xfailed, 1 warning, 14 errors in 314.35s` · `26 = 26` · `3 failed, 661 passed` · `3 = 3` · `DÙNG cụm cổng 5435` · `KẾT: ĐẠT` · exit 0.
2. Lượt 2 *(`2026-11-16T08:16:47Z`, log ở thư mục riêng của làn)* — số ở bảng Cổng. Tiêu đề: `GOC (mã fls) = /home/user/FLS-tobe/.claude/worktrees/isp-h1` · `cụm PG16 = /home/user/fls-pg16-5435 (cổng 5435)` · 7/7 `[ĐẠT]` phép kiểm môi trường. Hai bài chập chờn đã biết `tests/web/test_wo032_man_cua_that.py::test_AC3_…` / `::test_AC7_…` **⛔ đỏ** ở cả hai lượt *(web `3 = 3`)*.

## Kho thật
- `KHONG_CHAM`. Container ⛔ có sổ thật; `FLS_CHO_GHI_THAT` ⛔ đặt. `fls/bao_cao/gl.py` ⛔ mở kết nối nào *(hợp đồng 11 + đột biến `M12`/`M13` chứng minh cổng cắn)*. Bài `tests/bao_cao/test_gl.py` ⛔ chạm PG; kho test `fls_test` của cụm **5435** chỉ bị `conftest` dựng lại như mọi lượt pytest.

## Cách chạy để xem
- ⛔ chạm UI *(ISP §4: lát cắt là hàm thuần; đường vào lệnh/JSON thuộc H4)*.

## Dev tự thấy còn yếu
1. **Tồn theo từng tiền tệ bằng nguyên tệ là CÁCH ĐỌC công thức, ⛔ phải số đo** *(L2)*. Repo có **0** ô của CALC ZONE `BM–BT` *(đáp án 406 đóng băng ở `DT4`)* ⇒ Đ3: phép đối chiếu với AS-IS hôm nay chạy trên **tập rỗng**. Nếu AS-IS thật là MỘT cột tồn *(trộn tiền tệ)* hay tồn quy đổi *(bVND/mUSD)*, H4 sẽ đỏ ở cột tồn.
2. **CALC ZONE có 8 cột `BM–BT`, mã chỉ biết tên 4** *(BO · BP · BR · BS — từ AP)*. `BM · BN · BQ · BT` ⛔ có tên cho sheet 406 — đo grep `CALC ZONE\|BM–BT` *(16/11, trước phiếu này)*: **9** tệp `docs/` nhắc tên VÙNG *(AP ×4 · ISP ×2 · `TIEN_DO.md` · 2 bộ sinh ở `docs/ITL/_tools/`)*, **0** tệp `fls/` + `tools/` + `tests/`; tên CỘT duy nhất tìm được là `BM/BO` của sheet **HR** 407/408 *(AP: "BM/BO ép năm 2025")*, ⛔ của 406. Đoán *(tháng · tỷ giá · tồn bVND · tồn mUSD?)* thì ⛔ viết vào mã.
3. **Thứ tự phép tính mUSD *(÷ USD rồi × 10^3, đúng AP)* ⛔ bài nào ghim** — đổi sang `× 10^3 rồi ÷ USD` cho **6/6** dòng bằng nhau ở 28 chữ số *(đo bằng Python thuần, ⛔ pytest)*. Đây là đột biến **TƯƠNG ĐƯƠNG**, ⛔ lỗ hổng: trong `Decimal`, nhân/chia cho `10^3` *(và `10^9` của bVND)* chỉ dời SỐ MŨ — chính xác tuyệt đối — nên cả hai thứ tự chỉ có MỘT lần làm tròn *(phép ÷ USD)* trên cùng một giá trị. ⚠ Ở Sheets *(số thực nhị phân)* thì ⛔ tương đương — thêm một lý do cho dung sai của H4 *(#4)*.
4. **Sheets ≠ Decimal 28 chữ số**: ô mUSD vô hạn tuần hoàn *(dòng VND 2,5 ÷ 25.500)* sẽ lệch Sheets *(IEEE-754 ~15–17 chữ số)* ở chữ số ~16 ⇒ H4 phải KHAI dung sai; đòi bằng tuyệt đối là đỏ giả.
5. **`TIEN_TE_GL` là hằng trong mã.** Tôi xếp nó là *khuôn cột GL*, ⛔ luật số *(⛔ tỷ giá nào gõ cứng — đột biến `M9` gõ cứng USD 25.500 bị **3** bài cắn)*. Nhưng nếu `IX.FX` thêm tiền tệ thứ 6 *(app đã biết `EUR` — `fls/web/tep/thanh_phan.js:49`)*, engine ném `TienTeNgoaiGL` cho tới khi sửa mã — ồn, ⛔ im lặng, nhưng vẫn là sửa mã. Đọc 5 cột từ `IX.TMP`/`IX.FX` là việc của bước config sau.
6. **Pha ĐỎ trước khi có mã là đỏ ở bước THU BÀI** *(`ModuleNotFoundError` — đúng lý do ISP ghi cho `H1-B1`, "module chưa có")*, ⛔ đỏ từng bài theo hành vi. Bù lại bằng **13 đột biến sau khi xanh**: mỗi bài hành vi được thấy ĐỎ vì đúng lỗi nó canh *(log §Đột biến)* — nhưng đó là chứng minh SAU, ⛔ trước.
7. **`H1-B4` chạy `lint-imports` trong tiến trình con** `sys.executable -c …` — đã chạy ở Linux; trên Windows *(máy owner)* ⛔ thử. Tiến trình con kế thừa `os.environ` + ép `PYTHONUTF8=1` *(bẫy CLAUDE.md "in 0 byte")*.
8. ⛔ Ghim: tiền âm *(bút toán đảo)* đi qua như số thường; `bool` lọt qua kiểm kiểu như `int` *(`True` = 1)*; khoá tháng ⛔ kiểm dạng `yyyymm` — khoá sai kiểu/dạng rơi vào `ThieuTyGia` *(ồn, ⛔ im lặng)*.

## Câu hỏi cho orchestrator *(mỗi câu kèm phương án — đều `KHONG_CHAN` H1)*
| # | Câu | Phương án | Khuyến nghị |
|---|---|---|---|
| Q1 | Tồn của 406 là **5 cột theo tiền tệ, nguyên tệ** *(mã H1)*, hay một cột / cột quy đổi? Và tên 4 cột `BM · BN · BQ · BT` của CALC ZONE | **A** · giữ cách đọc của H1, để H4 so với đáp án 406 rồi sửa nếu lệch — được: ⛔ tốn gì bây giờ · mất: có thể làm lại phần tồn ở H4 *(nhỏ: một dòng + bài)*. **B** · orchestrator *(connector Drive, O7)* đọc **chỉ hàng tiêu đề** `BM:BT` của `Report I General Ledger` bản `[COPY]` *(⛔ giá trị)* trước H4 — được: bỏ đoán, `DT4` có khuôn sẵn · mất: vài phút phiên điều phối | **B** *(rẻ, gỡ cả câu tồn lẫn 4 tên cột)* + **A** trong lúc chờ |
| Q2 | Khoá tháng của `fx`: H1 dùng **`int` `yyyymm`** *(AP §3.2.1 "tháng yyyymm")*; C1 *(`fls/cau_hinh/fx.py`, làn BE-CF, đang chạy song song)* chưa thấy | **A** · chốt `int yyyymm` làm hợp đồng C1 ↔ H1, H4 nối — được: một kiểu · mất: C1 phải theo. **B** · H1 nhận cả `str` — được: dễ nối · mất: hai kiểu khoá, lệch kiểu thành lớp lỗi mới | **A** — lệch kiểu hôm nay đã ồn *(mọi dòng `ThieuTyGia`)*, ⛔ im lặng |
| Q3 | Chữ *"mUSD 98,039…"* ở ISP `H1-B1` vẫn còn trong ISP 3.1.2 *(tệp `02_BA` — Dev ⛔ sửa)* | **A** · orchestrator ghi đính chính vào `TIEN_DO.md` + gấp vào bản ISP vá kế tiếp *(§A.30: ISP cùng số AP)* · **B** · để nguyên, chỉ ghi ở BG này | **A** — R1/R2/R3 đọc ISP là nguồn sự thật duy nhất, dễ báo "lệch spec" ngược |
| Q4 | Scratchpad `/tmp/claude-0/…/e29eef16-…/scratchpad` **dùng chung** giữa mọi agent con của phiên điều phối — đã đo hai lần ghi đè trong lượt này: `duong_nen_1.log` *(làn BE-CF cổng 5434 ghi lên log của H1)* và `dot_bien.py` *(một agent khác ghi đè kịch bản đột biến của H1 sau khi H1 đã chép sang thư mục riêng)* | **A** · lệnh giao bước ghi rõ thư mục con riêng `scratchpad/<làn>_<bước>/` — được: hết va chạm, R1 tìm log dễ · mất: một dòng trong mỗi lệnh. **B** · để agent tự đặt tên duy nhất — được: ⛔ đổi gì · mất: tên chung chung *(`do.log`, `xanh.log`)* sẽ còn va | **A** — một bằng chứng bị ghi đè là một `BG` khai sai mà ⛔ ai thấy |

## Vòng sửa sau R1 *(KQ-072)*

| | |
|---|---|
| **Làm bởi** | `fls-dev` *(làn **BE-HC**, phiên mới)* · 2026-11-16 · orchestrator giao: `H1-R1-01` = **A** *(sửa mã)* · `H1-R1-05` ⇒ **dựng nốt BM · BN · BQ · BT** · làm luôn 5 GHI NHẬN `R1-02` · `03` · `04` · `06` · `07` |
| **Commit** | nhánh cục bộ `isp/H1` @ `7ced6b6` *(mã + bài)* · cha `30c1c4a` *(`KQ-072`)*; mục này ở commit kế tiếp *(chỉ giấy)*. ⛔ đẩy *(O2 = A)* |
| **Worktree · cụm** | `/home/user/FLS-tobe/.claude/worktrees/isp-h1` · cụm **5434** *(orchestrator giao cho vòng này; phần trên của phiếu chạy 5435)* · `PG_DSN=…localhost:5434/fls` · `PG_DSN_TEST=…localhost:5434/fls_test` · `PYTHONUTF8=1` · `PYTEST_ADDOPTS` trống · venv `/home/user/FLS-tobe/.venv` |
| **Phần cũ của phiếu** | ⛔ sửa — mục này CHỈ THÊM. Trạng thái `WO-070` ⛔ đổi *(orchestrator ghi)* |
| **Căn cứ** | `KQ-072` · `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H1.md` v0.1 *(7 hàng)* · `docs/ITL/01_Orchestrator/isp-3.1/CALC_ZONE_406.md` *(đọc ở checkout chính — tệp ở nhánh chính @ `1768668`, ⛔ có trong `isp/H1`)* · `07_API_CONTRACT.md` §4g v3.11 · v3.12 · `fls/canon/tien_te.py` *(chỉ import)* |
| **Cách làm** | TDD: viết **31** bài mới *(15 hàm)* vào `tests/bao_cao/test_gl.py`, chạy trên **mã cũ** *(`gl.py` sha256 `82c1921bc2763492…` = `5c0a2e2`)* ⇒ ĐỎ đúng lý do, lưu log, rồi mới sửa `gl.py`. Bài xanh sẵn trên mã cũ *(mã đúng, chỉ thiếu bài ghim)* chứng minh răng bằng **đột biến trên BẢN SAO** ngoài worktree. Mong tính tay bằng `Fraction` ngoài repo *(⛔ import `gl.py`)*. ⚠ Container khởi động lại giữa vòng *(giới hạn sử dụng)* sau pha đỏ: cây làm việc + scratchpad còn nguyên *(sha256 trước = sau)*, lượt xanh và mọi cổng dưới chạy SAU khởi động lại |
| **Log** *(scratchpad, ⛔ commit)* | `/tmp/claude-0/-home-user-FLS-tobe/e29eef16-56df-5253-a1b1-752daec60d67/scratchpad/hc_h1_sua/` — `do_truoc_pytest.log` · `do_truoc_ly_do.log` · `xanh_pytest.log` · `dot_bien.py` + `dot_bien.log` · `tinh_tay_bm_bt.py` + `.log` · `r1_tinh_tay_tren_ma_moi.log` · `r1_de_xuat_tren_ma_moi.log` · `duong_nen_luot*.log` · `cong_*.log` |

### Đã đổi *(vòng sửa)*
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/gl.py` | đủ **8** cột CALC ZONE BM–BT *(+4: BM · BN · BQ · BT)* · `ma_tien_te` ở cả 4 phép so tiền tệ · `TienKhongHuuHan` *(mới)* · tỷ giá ⛔ hữu hạn / mơ hồ ⇒ `ThieuTyGia` · docstring + thông điệp `ThieuTyGia` theo công thức ô. 223 → **383** dòng |
| `tests/bao_cao/test_gl.py` | +**15** hàm `def test_R1_0n_…` *(15 → 30 hàm)* ⇒ **18 → 49** bài thu thập; 18 bài cũ ⛔ sửa dòng nào *(chỉ thêm 4 dòng import: `ast` · `json` · `gl_mod` · `ma_tien_te`)* |
| `docs/ITL/01_Orchestrator/handoff/BG-071-…md` | mục này |

### Từng phát hiện → sửa gì → bằng chứng
| Mã | Sửa gì *(tệp:dòng @ `7ced6b6`)* | ĐỎ trên mã cũ / đột biến *(bản sao)* | XANH |
|---|---|---|---|
| `H1-R1-01` **NÊN SỬA** · A | `gl.py:268` `ma = ma_tien_te(d.tien_te)` MỘT lần đầu vòng; dùng `ma` cho kiểm 5 cột `:269` · khoá tồn `:279` · tách cột `:302-303` · tra `fx` `:274-275`; khoá của bảng `fx` cũng chuẩn hoá `:362`, **≥ 2** khoá cùng về một mã ⇒ `ThieuTyGia` *"tỷ giá mơ hồ"* `:368-373` *(⛔ chọn bừa — AS-IS chọn theo HAI cách: INDEX/MATCH lấy đầu, SUMIFS cộng đôi)*; `TienTeNgoaiGL` in cả mã gốc `repr` lẫn mã chuẩn hoá `:271`. Import `fls.canon.tien_te` `:141` *(hợp đồng 11 ⛔ cấm `fls.canon`)* | mã cũ: `[chu_thuong]` `[cach_dau]` `[NBSP_cuoi]` `[BOM_dau]` ⇒ `TienTeNgoaiGL: ⛔ dòng thứ 1 mang tiền tệ 'vnd'` · `' VND'` · `'VND\xa0'` · `'\ufeffVND'` *(4/4 — đúng số R1)*; cộng dồn `'usd'`+U+3000 ⇒ `TienTeNgoaiGL`; khoá `fx` `'usd'`/`' VND'` ⇒ `ThieuTyGia … ⛔ có cột VND` *(sai tên lỗi)*; khoá trùng ⇒ `DID NOT RAISE ThieuTyGia`. Đột biến `S-M04` *(mã dòng ⛔ qua `ma_tien_te`)* ⇒ 5 đỏ · `S-M05` *(khoá `fx` thô)* ⇒ 5 đỏ · `S-M06` *(khoá trùng ⇒ lấy đầu)* ⇒ 1 đỏ | 7 bài `test_R1_01_…` *(4 biến thể + cộng dồn cùng cột + khoá `fx` + khoá trùng)* PASSED; bài đề xuất của R1 `test_R1_03_so_tien_te_qua_ma_tien_te[4]` *(scratch R1, chạy với `PYTHONPATH` = worktree)* ⇒ PASSED |
| `H1-R1-02` | `gl.py:332-341` `_so_dung` = `_kieu_dung` + `is_finite()` ⇒ `TienKhongHuuHan(ValueError)` `:190-205` *(mang `nhan` · `vi_tri`; in NaN/Infinity được — ⛔ bao giờ là một số tiền)*; tỷ giá: `:375-376` `is_finite()` TRƯỚC phép so `<= 0` ⇒ `ThieuTyGia` | mã cũ — tiền: NaN/±Infinity × Nợ/Có ⇒ `DID NOT RAISE ValueError` *(6)*, sNaN ⇒ `decimal.InvalidOperation` ở `ton[d.tien_te] + no - co` *(2)*; tỷ giá: NaN/sNaN ⇒ `InvalidOperation` ở `if gia <= 0` *(4)*, Infinity VND ⇒ `InvalidOperation` ở `bvnd_co = ty_gia * co`, Infinity USD ⇒ `DID NOT RAISE` *(mUSD = 0 IM LẶNG)*. Đột biến `R1-M5` *(bỏ chặn tiền)* ⇒ 8 đỏ · `S-M03` *(bỏ chặn tỷ giá)* ⇒ 6 đỏ | `test_R1_02_tien_…[4 × 2]` + `test_R1_02_ty_gia_…[3 × 2]` = 14 PASSED; đề xuất R1 `test_R1_02_…[3]` PASSED |
| `H1-R1-03` | ⛔ đổi mã *(mã đúng — R1 tính tay)*; bài mới `test_gl.py:444` *(USD E = 100 · F = 30 — số của R1)*; dòng ④ của ca SGD *(`DONG_R1`, E = 500 · F = 100)* phủ thêm BQ/BT/BM/BN trên dòng hai vế | mã cũ: XANH *(đúng thiết kế)*. Đột biến bộ R1 viết lại cho mã mới: `R1-M1` *(Nợ thắng)* · `R1-M2` *(BP = 0 khi E ≠ 0)* · `R1-M6` *(Có ghi đè Nợ)* ⇒ mỗi lượt **2** đỏ *(`test_R1_03_…` + `test_R1_05_…ca_SGD…`)* — trên `e0bd4a6` cả ba SỐNG 18/18 | PASSED |
| `H1-R1-04` | docstring `gl.py:20-40` *(chép công thức Ô của AX:BT + ánh xạ 8 cột)* · `:68-76` ② **BA** ngữ nghĩa tra *(BO/BP INDEX/MATCH · BR/BS SUMIFS USD · BM/BN SUMIFS từng cột, VND ⛔ tra)* · `:85-94` ⓐ *(tháng vắng ⇒ BO·BP·BR·BS **ô rỗng** do `iferror`, **BM** mất số im lặng, BN `#DIV/0!`; ô tỷ giá trống ⇒ BO/BP = 0; tháng trùng)* · ① `:58-67` *(câu "repo ⛔ chép ô nào" thay bằng xác nhận của `CALC_ZONE_406.md`)*; thông điệp `ThieuTyGia` `:179-183`; lý do tỷ giá ≤ 0 `:377-382` | đọc ↔ `CALC_ZONE_406.md` *(R1 F-4)* — lời tả, ⛔ hành vi ⇒ ⛔ có bài đỏ; bài `H1-B3` cũ vẫn ghim thông điệp MỘT dòng + có tháng + tiền tệ | `test_H1_B3_…` PASSED *(thông điệp mới)* |
| `H1-R1-05` | `KetQuaDongGL` +4 trường theo thứ tự cột 406 `gl.py:238-245`: `vnd_ton_all` **BM** · `musd_ton_all` **BN** · `bvnd_ton` **BQ** · `musd_ton` **BT**. BQ/BT luỹ kế `:285-286`; BM `:290-297` = tồn VND + Σ tồn × tỷ giá **tháng của dòng** cho USD · SGD · COP · HKD *(chỉ tiền tệ có tồn ≠ 0)*; BN `:298` = BM ÷ USD ÷ 10^6; tồn ≠ 0 mà tháng thiếu tỷ giá tiền tệ ấy ⇒ `ThieuTyGia(tien_te = tiền tệ THIẾU)` + lý do *"BM/BN: tồn X ≠ 0 …"* | mã cũ: 4 bài `test_R1_05_…` ⇒ `AttributeError: 'KetQuaDongGL' object has no attribute 'vnd_ton_all'` *(3)* · `DID NOT RAISE ThieuTyGia` *(1)*. Đột biến: `S-M07` BQ ⛔ luỹ kế ⇒ 2 đỏ · `S-M08` BT ⛔ luỹ kế ⇒ 2 · `S-M09` BM ⛔ đánh giá lại *(tỷ giá tháng nhỏ nhất)* ⇒ 4 · `S-M10` BM đòi tỷ giá cả khi tồn = 0 ⇒ 13 · `S-M11` BM nhân tồn VND với tỷ giá VND ⇒ 3 · `S-M12` BN ÷ 10^9 ⇒ 6 · `S-M13` BM bỏ số hạng USD ⇒ 3 | 4 bài PASSED: 6 dòng tổng hợp **24** ô *(5/5 tiền tệ có tồn ≠ 0; dòng 4 đánh giá lại — BM `3.902.500.000` ≠ BQ × 10^9 `3.948.000.000`)* · ca SGD của R1 **24** ô *(BQ sau ④ = `0.237695344` = mong orchestrator; BT sau ④ khớp `0,009136326680426093…` của R1)* · `ThieuTyGia(202502, 'SGD', 2)` · hai ranh giới *(tồn 0 ⇒ ⛔ đòi tỷ giá; VND ⛔ tra tỷ giá)*. Tính tay độc lập: `tinh_tay_bm_bt.log` *(Fraction)*; kịch bản tính tay của R1 chạy trên mã mới ⇒ `══ TỔNG: 55 ô so · 0 lệch` |
| `H1-R1-06` | ⛔ đổi mã; 2 bài `test_gl.py:628-678`: ⓐ tiến trình con sạch nạp **mọi** mô-đun `fls.bao_cao` *(`pkgutil.walk_packages`)*, CHẠY `tinh_gl`, đòi `psycopg*` · `fls.db*` · `fls.repo*` ∉ `sys.modules` *(Đ3: đòi `fls.bao_cao.gl` đã nạp + 1 kết quả)*; ⓑ cây cú pháp `fls/bao_cao/**/*.py` ⛔ `import importlib` · `from importlib` · `__import__` *(Đ3: ≥ 2 tệp, > 100 nút)* | mã cũ: XANH. Đột biến *(kèm `lint-imports` trên bản sao)*: `S-M14` `importlib.import_module('fls.db.kho')` lúc nạp ⇒ **2** đỏ, lint `11 kept, 0 broken` · `S-M15` `__import__` trong `tinh_gl` ⇒ **2** đỏ, lint `11 kept` · `S-M16` importlib trong hàm ⛔ ai gọi ⇒ **1** đỏ *(chỉ ⓑ — đúng chỗ ⓐ ⛔ chạy tới)*, lint `11 kept` ⇒ cả ba lọt `lint-imports`, đúng điểm mù R1 đo | 2 PASSED |
| `H1-R1-07` | ⛔ đổi `_NGU_CANH` *(`gl.py:159`)*; 2 bài `test_gl.py:681-708`: BR · BN · BT của `H1-B1` so **chuỗi** `0.09803921568627450980392156863` *(chữ số 28 = 2, chữ số 29 = 7 ⇒ lên)*; ca **hoà ở chữ số 29** *(N = 2·10^27 + 1 · + 3, USD = 2 — số TỔNG HỢP)* ⇒ về chẵn `…000000` / `…000002` | mã cũ: BR đúng tuyệt đối *(dòng `>` của lỗi nằm ở BN — `AttributeError … 'musd_ton_all'`, tức assert BR đã qua)*. Đột biến: `R1-M3` prec 12 ⇒ 6 đỏ · `R1-M4` `ROUND_DOWN` ⇒ 2 · `S-M01` `ROUND_HALF_UP` ⇒ 1 *(ca chẵn)* · `S-M02` `ROUND_HALF_DOWN` ⇒ 1 *(ca lẻ)* — trên `e0bd4a6` `R1-M3` · `R1-M4` SỐNG 18/18 | 3 PASSED |

### Log ĐỎ → XANH *(`tests/bao_cao/test_gl.py`)*
**ĐỎ** *(`gl.py` = mã cũ sha256 `82c1921bc2763492…`, `test_gl.py` mới sha256 `76bfb7db010777a8…`)*: `python -m pytest tests/bao_cao/test_gl.py -rfE` ⇒ exit **1** · `28 failed, 21 passed in 0.95s`. 21 xanh = 18 bài cũ + `R1-03` *(1)* + `R1-06` *(2)*; 28 đỏ = `R1-01` 7 · `R1-02` 14 · `R1-05` 4 · `R1-07` 3 — lý do từng bài *(dòng `E` đầu)* ở bảng trên, đủ **28/28** khối *(`do_truoc_ly_do.log`)*; ⛔ bài nào đỏ vì cú pháp/thu bài.

**XANH** *(`gl.py` mới sha256 `c7c4094bd4e801a3…`)*: exit **0** · `49 passed in 1.91s` · `--collect-only tests/bao_cao` ⇒ `49 tests collected`. Sau đó sửa MỘT docstring *(`test_R1_02_ty_gia_…` — câu *"Infinity ⇒ lọt"* sai với chính log đỏ: Infinity ở cột VND ném `InvalidOperation` từ `Infinity × 0`; đo thêm trên mã cũ: dòng hai vế ⇒ bVND = mUSD = `Infinity` LỌT)* ⇒ `test_gl.py` sha256 `05d874d84d593762…` *(+2 dòng, ⛔ đổi assert)* ⇒ `49 passed in 0.68s`; đó là bản commit `7ced6b6`. Bài đề xuất của R1 *(scratch R1, ⛔ commit)*: trên `e0bd4a6` `7 failed, 1 passed` ⇒ trên mã mới `8 passed`.

**Đột biến** *(`dot_bien.py`, bản sao ngoài worktree — ⛔ chép `tests/conftest.py`; mỗi phép thay khớp ĐÚNG 1 lần; `gl.py` = `c7c4094b…` = bản commit, `test_gl.py` = `76bfb7db…` — khác bản commit đúng một docstring)*: `đột biến: 23 · bị cắn: 23 · sống/⛔ đo được: 0 []` · `đối chứng bản sao nguyên: 49 passed` · `sha256 bản sao sau trả = c7c4094bd4e801a3 · gốc c7c4094bd4e801a3 · KHỚP`.

### Cổng *(chạy lại — nguyên văn)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/bao_cao/test_gl.py` | exit 0 · `49 passed in 0.51s` *(cây `7ced6b6`)* · `--collect-only tests/bao_cao` ⇒ `49 tests collected` *(18 cũ + 31 mới)* |
| `/home/user/FLS-tobe/.venv/bin/lint-imports` | exit 0 · `Contracts: 11 kept, 0 broken.` · `fls.bao_cao la engine bao cao/phan bo thuan, khong duoc biet tang kho KEPT` *(nay `gl.py` import `fls.canon.tien_te` — hợp đồng 11 ⛔ cấm, hợp đồng 3 canon ⛔ đổi)* |
| `bash tools/dung_moi_truong_isp.sh --cong 5434 --duong-nen` **lượt 1** *(`12:45:55Z → 12:54:25Z`; cây làm việc = `gl.py` `c7c4094b…` + `test_gl.py` `76bfb7db…` — trước sửa docstring)* | exit 0 · 7/7 `[ĐẠT]` *(K2 `cụm CỦA MÌNH: … postmaster.pid cổng 5434 …` · K4 `26/26 di trú áp · pg_verify khớp 25 bảng/view (0 lệch)` · K5 `Contracts: 11 kept, 0 broken.` · K6 `chay 9845 / co 9967` · K7 `fls_itl = 0 dòng`)* · toàn bộ `12 failed, 2481 passed, 2 xfailed, 14 errors in 323.33s (0:05:23)` ⇒ `[ĐẠT] đường nền toàn bộ tập đỏ = đường nền: 26 = 26 node id (thêm 0 · bớt 0)` · web `3 failed, 661 passed in 182.12s (0:03:02)` ⇒ `[ĐẠT] … 3 = 3 node id` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` |
| ↳ **lượt 2** *(`12:55:11Z → 13:03:42Z`; cây = commit `7ced6b6`, `git status` sạch)* | exit 0 · 7/7 `[ĐẠT]` · toàn bộ `12 failed, 2481 passed, 2 xfailed, 14 errors in 316.32s (0:05:16)` ⇒ `26 = 26 node id (thêm 0 · bớt 0)` · web `3 failed, 661 passed in 189.95s (0:03:09)` ⇒ `3 = 3` · `══ KẾT: ĐẠT`. **Mẫu số** *(Đ3)*: `pytest --collect-only` ⇒ `2509 tests collected` = 12 + 2.481 + 2 + 14 = **2.509** = 2.478 *(R1 đo trên `e0bd4a6`)* + **31** *(bài mới)*; dòng tổng kết **0** `skipped` · **0** `deselected`; `PYTEST_ADDOPTS` trống. Hai bài chập chờn `tests/web/test_wo032_man_cua_that.py::test_AC3_…` / `::test_AC7_…` **⛔ đỏ** ở CẢ HAI lượt *(3 đỏ web = `test_wo022_tien_theo_tien_te_pg::test_AC5_…` · `test_wo022_v2_o_tien_pg::test_AC11_…` · `test_wo042_mot_tap_ky_tu_trang::test_AC11_…` — sổ thật rỗng, như R1)* |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | exit 0 · `✅ cong tai lieu DAT — va no da do duoc that (176 file, 1866 bang, 725 o ngay, 104 ma QD), khong chi 'khong thay loi'` *(cây `7ced6b6`, TRƯỚC khi thêm mục này — khớp số R1 đo sau `KQ-072`)* · lượt sau khi thêm mục này: exit 0 · `(176 file, 1872 bang, 725 o ngay, 104 ma QD)` — **+6** bảng = đúng 6 bảng của mục này, `K3 bang markdown khong lech (da do: 1872 bang)` ⇒ mục này CÓ được soi *(Đ3)* |
| `python docs/ITL/_tools/khop_owner.py --kiem` | exit 1 · `⇒ 11/16 khop · 5 lech   (da do 16/20 phep)` — y như `BG-071` và R1 *(`B3` · `B4` · `C5` · `C5b` KHONG DO DUOC · `A1` · `B1` · `C6` DOI TRANG THAI — kho `fls` @5434 RỖNG)* |
| `python tools/soi_bang_tuyen.py` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` |
| `python tools/kiem_thuyet_minh.py` | exit 0 · `✅ CONG THUYET MINH DAT — 31/31 nut co mat trong CA 2 ban` |
| `python -m fls.db.pg_migrate` *(⛔ chạm schema)* | exit 0 · `khong co gi de ap` · `pg_verify: khop` |
| `python tools/kiem_so_song.py` | **⛔ CHƯA ĐO ĐƯỢC** — exit 1 · `FileNotFoundError: [Errno 2] No such file or directory: '/home/user/FLS-tobe/.claude/worktrees/isp-h1/.venv/Scripts/lint-imports.exe'` *(như phần trên — chưa đổi)* |

### Quyết định Dev tự đưa trong vòng *(⛔ có trong lệnh — R2 soi)*
| # | Chỗ | Đã làm | Vì sao · phương án bỏ |
|---|---|---|---|
| V1 | BN | `BM ÷ USD ÷ 10^6` — MỘT lần làm tròn | đại số bằng khuôn ô *(chia phân phối)*; BM cộng tích đúng tuyệt đối ⇒ BN = giá trị đúng làm tròn một lần. Bỏ: tính từng số hạng như ô *(4 lần làm tròn ⇒ lệch chữ số 28, ⛔ gần Sheets hơn vì Sheets là IEEE-754)* |
| V2 | BM · BN với VND | tồn VND cộng THẲNG vào BM, chia USD ở BN — ⛔ tra `fx[tháng]["VND"]` | công thức ô `… + BI + …` · `BI/USD`; VND là đơn vị của BM. Bỏ: nhân tỷ giá VND *(như BO/BP)* — lệch ô khi bảng có VND ≠ 1, và đòi thêm tỷ giá ô ⛔ đọc. Bài ghim: `test_R1_05_BM_chi_doi_…` ⓑ; đột biến `S-M11` cắn *(câu hỏi Q6)* |
| V3 | BM khi tồn = 0 | ⛔ đòi tỷ giá của tiền tệ có tồn = 0 | số hạng = 0 bất kể tỷ giá; AS-IS `0 × 0 = 0` cũng ⛔ mất số. Bỏ: đòi đủ 4 tỷ giá mỗi tháng — làm đỏ `H1-B1` *(bảng chỉ USD · VND)* và 13 bài *(`S-M10`)* mà ⛔ cứu được đồng nào |
| V4 | tiền ⛔ hữu hạn ↔ tỷ giá ⛔ hữu hạn | tiền ⇒ `TienKhongHuuHan` *(lớp MỚI, `ValueError`)*; tỷ giá ⇒ `ThieuTyGia` | R1 đề xuất *"TypeError/ValueError cho cả hai"*; tách vì tỷ giá ⛔ hữu hạn = ⛔ có tỷ giá dùng được *(cùng lớp `≤ 0`, cùng trường `thang`/`tien_te` để H4 gom)*, còn tiền hỏng là lỗi của DÒNG |
| V5 | khoá `fx` trùng sau chuẩn hoá | `ThieuTyGia` *"mơ hồ"* | hệ quả trực tiếp của việc chuẩn hoá khoá *(⛔ chuẩn hoá thì ⛔ có ca này)*. Bỏ: lấy khoá đầu *(= INDEX/MATCH — đoán im lặng)* |
| V6 | tên 4 trường | `vnd_ton_all` · `musd_ton_all` · `bvnd_ton` · `musd_ton` | theo khuôn đơn-vị-trước của `bvnd_no`/`musd_no`; *"TỒN ALL"* = chữ tiêu đề hàng 7 của BM. H4 nối theo tên này |

### Kho thật
- `KHONG_CHAM`. Container ⛔ có sổ thật; `gl.py` ⛔ mở kết nối *(hợp đồng 11 + 2 phép đo động mới)*. Bài `tests/bao_cao/**` ⛔ chạm PG; lượt đường nền dựng lại `fls_test` @5434 như mọi lượt. Kho `fls` @5434 `fls_itl` = **0** *(K7 của script)*.

### Dev tự thấy còn yếu *(vòng sửa)*
1. **4 cột mới chưa đối chiếu SỐ THẬT** — mong là tay tính theo công thức ô, ⛔ theo giá trị ô *(`CALC_ZONE_406.md` chỉ chép công thức; giá trị bản sao hôm nay `#REF!`/`#DIV/0!` — `B-DATA-1`)*. H4 mới là phép đo quyết định.
2. **V2 *(VND ⛔ tra tỷ giá ở BM/BN)* là đọc NGUYÊN VĂN ô** — nếu chủ ý của owner là *"Σ tồn × tỷ giá"* kể cả VND, thì trên bảng có VND = 1 hai cách ra **cùng** số; chỉ khác khi bảng thiếu cột VND hoặc VND ≠ 1 *(C1 có kiểm VND = 1 không — chưa đọc)*. Đã ghim bằng bài để đổi là ĐỎ *(Q6)*.
3. **BN một lần làm tròn ≠ khuôn ô** *(V1)* — chênh với cách tính từng số hạng ở chữ số ~28, nhỏ hơn dung sai Sheets ↔ Decimal của H4 *(~16)* nhiều bậc; nhưng bài `test_R1_07_…` so BN **bằng tuyệt đối** ⇒ đổi sang tính từng số hạng sẽ ĐỎ bài ấy *(chủ ý: ghim một lần làm tròn)*.
4. **BM chỉ đúng tuyệt đối khi tổng ≤ 28 chữ số** — ⛔ bẫy `Inexact`: tồn × tỷ giá vượt 28 chữ số thì làm tròn IM LẶNG *(R1 đã ghi cho tồn; thực tế `numeric(20,2)` × tỷ giá ≤ 7 chữ số ≤ 27)*.
5. **Ca hoà `R1-07` là số TỔNG HỢP phi thực tế** *(2·10^27 VND, USD = 2)* — chỉ để chữ số 29 rơi đúng `5`. Ghim ngữ cảnh, ⛔ ghim nghiệp vụ.
6. **Phép đo `sys.modules` chỉ thấy đường CHẠY tới với MỘT đầu vào** *(một dòng VND)* — import động nằm sau nhánh dữ liệu khác *(vd. chỉ khi gặp EUR)* thì chỉ phép quét cây cú pháp bắt; phép quét ⛔ bắt `getattr(builtins, …)` hay `exec`. Hai phép cộng lại hẹp hơn *"⛔ chạm DB"* tuyệt đối — đủ cho điểm mù R1 đo *(3/3 đột biến cắn)*.
7. **`TienTeNgoaiGL` nay chấp nhận rộng hơn Sheets** *(hành vi ⓓ: `' VND'` vào cột VND, AS-IS rơi khỏi 5 cột — suy từ công thức ô)* ⇒ nếu sổ thật có ca ấy, H4 sẽ thấy lệch ở cột VND — sổ thật hôm nay **0 / 8.387** *(`07_API_CONTRACT.md` §4g)*.
8. Còn từ phần trên: `bool` lọt kiểm kiểu như `int`; khoá tháng ⛔ kiểm dạng `yyyymm` *(yếu #8 — ⛔ trong danh sách R1, ⛔ sửa)*.
9. **Thứ tự bài**: 31 bài mới nằm CUỐI tệp, cùng tệp với 18 bài cũ *(⛔ tách `test_gl_r1.py`)* — để một lệnh `pytest tests/bao_cao/test_gl.py` vẫn là cổng của H1.

### Câu hỏi cho orchestrator *(vòng sửa — đều `KHONG_CHAN`)*
| # | Câu | Phương án *(được · mất)* | Khuyến nghị |
|---|---|---|---|
| Q5 | Bài đề xuất của R1 *(`…/r1_h1/de_xuat/test_kq072_h1_r1.py`, nay `8 passed`)* có chuyển vào `tests/nghiem_thu/` không? Dev ⛔ được ghi `tests/nghiem_thu/**` | **A** · R2 chuyển *(đúng chủ sở hữu)* — được: bài nghiệm thu độc lập với bài Dev · mất: trùng nội dung với `test_R1_01/02/03` của Dev *(3 hàm)*. **B** · bỏ, coi `test_R1_*` của Dev là đủ — được: một chỗ · mất: Test ⛔ có bài riêng | **A** |
| Q6 | V2 — BM/BN ⛔ tra tỷ giá VND *(nguyên văn ô)* hay *"Σ tồn × tỷ giá"* kể cả VND *(chữ của lệnh giao)*? | **A** · giữ nguyên văn ô *(mã hiện tại)* — được: parity H4 đúng từng chữ ô · mất: ⛔ đối xứng với BO/BP. **B** · nhân tỷ giá VND — được: một luật tra cho mọi tiền tệ · mất: lệch ô khi bảng thiếu/sai VND, sửa 1 dòng + bài `test_R1_05_BM_chi_doi_…` | **A** — trên bảng hợp lệ *(VND = 1)* hai cách cùng số; chỉ khác ở bảng hỏng, nơi C1 nên chặn |
| Q7 | Sổ `SO_PHAT_HIEN_ISP-3.1_H1.md` — Dev ⛔ đổi trạng thái hàng *(⛔ thuộc làn; sổ chỉ THÊM)* | orchestrator/R2 đổi `mở` → `đã sửa` cho 7 hàng theo bảng trên | — |
