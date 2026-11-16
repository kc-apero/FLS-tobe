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
