# KQ-103 — biên bản kiểm `BG-102` *(ISP 3.1.2 · Step 7 · CG1 · R1)*

| | |
|---|---|
| **Thuộc** | `BG-102` · `WO-101` *(dải: WO-101 · BG-102 · KQ-103 R1 · KQ-104 R2 · KQ-105 R3)* |
| **Kiểm bởi** | `fls-test` — **R1** *(phiên cloud CON độc lập, ngoài máy orchestrator)* · 2026-11-17 |
| **Đối tượng** | nhánh `isp/CG1` @ `84bcdbf` *(mã `d6d50f4`)* · nền `isp/base-w3` @ `575926e` · worktree `/home/user/FLS-tobe/.claude/worktrees/isp-cg1` · cụm PG riêng **5444** |
| **Phán quyết** | **`ĐẠT`** — **0 phát hiện CHẶN** *(2 NÊN SỬA → orchestrator · 3 GHI NHẬN; chi tiết ở `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_CG1.md`)* |

> **Điều kiện PUSH** *(ISP mục 8)*: đủ **R1 · R2 · R3**, chặn = 0. R1 nay **ĐẠT · 0 chặn**; còn chờ R2 *(KQ-104)* · R3 *(KQ-105)*. ⇒ **chưa đủ PUSH** *(⛔ phải việc của R1)*.
>
> Mọi số R1 **tự chạy lại** *(⛔ tin BG)*, cụm 5444, venv `/home/user/FLS-tobe/.venv`, `export PG_DSN=…:5444/fls PG_DSN_TEST=…:5444/fls_test PYTHONUTF8=1`, chạy từ gốc worktree. Đột biến + bản sao H2 trên thư mục nháp `/tmp/r1_cg1/`, ⛔ chạm worktree.

## Cổng chạy lại *(R1 tự đo — so với `BG-102`)*
| Lệnh | `BG-102` nói | R1 đo | Khớp |
|---|---|---|:-:|
| `python -m pytest tests/api/test_isp_gates_hd1.py` | exit 0 · `33 passed in 2.98s` | exit 0 · `33 passed in 2.97s` | ✅ |
| `python -m pytest tests/api tests/repo/test_doc_bao_cao_pg.py` | 14 node đỏ = đường nền | exit 1 · `3 failed · 414 passed · 11 errors` — 14 node, **đều trong** `duong_nen_bai_do.txt`; **0** node `test_isp_gates_hd1` | ✅ |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5444` *(script NHÁNH)* | `KẾT: ĐẠT` · `26 = 26 · chạy 2600 (mong ≥ 2493)` · web `3 = 3 · 664` | **`KẾT: ĐẠT`** · `26 = 26 (thêm 0 · bớt 0) · chạy 2600 · skipped 0 · deselected 0` · web `3 = 3 · 664` | ✅ |
| `--duong-nen` *(script **S0** @ `c1cf29b` lên mã CG1 — bản CHẶT HƠN, `-rfEx`)* | *(BG ⛔ chạy)* | **`KẾT: ĐẠT`** · `28 = 28 (XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 2600 (mong ≥ 2490)` · web `3 = 3` | ✅ *(→ `CG1-R1-01`)* |
| `.venv/bin/lint-imports` | `11 kept, 0 broken.` | exit 0 · `Contracts: 11 kept, 0 broken.` | ✅ |
| `python tools/soi_bang_tuyen.py` | `KHOP SQL … 40 tuyen` | exit 0 · `✅ ban khai KHOP SQL that o ca 40 tuyen` | ✅ |
| `python -m fls.db.pg_migrate` | `khong co gi de ap · pg_verify: khop` | exit 0 · `khong co gi de ap · pg_verify: khop` | ✅ |
| `python tools/kiem_so_song.py` | ⛔ CHƯA ĐO ĐƯỢC *(đường Windows gõ cứng — đường nền)* | exit 1 · `FileNotFoundError … .venv/Scripts/lint-imports.exe` — ⛔ do CG1 *(tệp ⛔ trong diff)* | ✅ *(đường nền)* |
| `GET /api/fls/v1/gates` *(tuyến THẬT · tệp mặc định)* | FINAL DAT `69.510/69.510` · HD1 KHÔNG ĐẠT `5/23` · chua_do_duoc 6 | **y hệt** *(R1 gọi HTTP thật qua `chay_cua.py`, token tạm; vỏ `{data,error,meta}` đủ)* · dat 1 · khong_dat 2 · chua_do_duoc 6 | ✅ |
| `GET …/gates` *(`--tep-do ''`)* | hai cổng `CHUA DO DUOC` · chua_do_duoc 8 *(+2)* | dat 0 · khong_dat 1 · **chua_do_duoc 8** *(+2 ĐÚNG; ⛔ 200 toàn xanh)* | ✅ |

## Bảng AC *(mỗi dòng mục 8 + test ID mục 6)*
| AC *(test)* | Mong | R1 đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| **AC-1** `CG1-B1` | `FINAL` dat true · `da_do` số ô + nhãn; `HD1_THANG` dat false · `'5/23 kỳ đạt'` · `ly_do` kỳ đỏ + dòng thiếu + ngày ảnh | Tuyến thật: FINAL `DAT` · `da_do='69.510/69.510 ô (… 7 khối × 9.930 dòng giữ sau tự soi)'` · `ly_do` có `69.769 ô` + `37 dòng tự soi loại` + `2026-08-26`; HD1 `KHÔNG ĐẠT` · `da_do='5/23 kỳ đạt'` · `ly_do` liệt **18** kỳ đỏ *(Σ 122 dòng)* + ngày ảnh. Nhãn Đ4 **đủ** *(xem `CG1-R1-02`)* | **ĐẠT** |
| **AC-2** `CG1-B2` | tệp vắng ⇒ cả hai `null` · `chua_do_duoc` **+2 đúng** · ⛔ 200 toàn xanh | Tuyến thật `--tep-do ''`: hai cổng `CHUA DO DUOC`; `chua_do_duoc` 6 → **8** *(hiệu +2)*; `dat < số cổng` · `chua_do_duoc ≥ 4+2`. Đếm `chua_do_duoc = sum(dat is None)`; 4 cổng kế toán *(DIF_BANK·VI·DONG_BO·BON_DUONG)* **LUÔN** `None` ⇒ luật *"⛔ bao giờ toàn xanh"* giữ | **ĐẠT** |
| **AC-3** `CG1-B3` | bài `/gates` sẵn có + `tests/api` xanh | 14 node đỏ của `tests/api`+repo **trùng khít** đường nền *(0 node CG1)*; bài `/gates` sẵn `test_cong_ra_duoc_va_KHONG_BAO_GIO_toan_xanh` v.v. PASSED; `--duong-nen` toàn bộ `26 = 26` *(và bản S0 `28 = 28`)* | **ĐẠT** |
| **AC-4** `CG1-B4` | phá MONG ⇒ ĐỎ, trả nguyên ⇒ xanh *(Đ5 hai chiều)* | R1 **độc lập 8/8 đột biến giết** trên bản sao `git archive` *(M1 parity · M2 HD1-dat · M3 Đ3 0/0 · M4 dem-bool · M5 gõ-cứng · M6 ngày-ảnh · M7 tự-mâu-thuẫn · M8 lọc-thieu)*, sha trả nguyên khớp; bài `CG1-B4` qua tuyến thật *(FINAL lệch 1 ô ⇒ đỏ; mọi kỳ đạt ⇒ HD1 `23/23` — hai chiều)* PASSED | **ĐẠT** |
| **AC-5** `Q8` | bài mới cộng `MONG_PYTEST_TOAN_BO` cùng commit | `2460 → 2493` *(+33 = `--collect-only` tệp mới)* ở `d6d50f4`; sàn `chạy 2600 ≥ 2493` giữ. **Lưu ý `CG1-R1-01`**: script nhánh dùng `-rfE` *(⛔ `x`)* · `2493`; bản S0 `-rfEx` · `2490` — orchestrator gộp phải lấy bản S0 + cộng `+33` *(→ 2523)* | **ĐẠT** *(kèm việc gộp `CG1-R1-01`)* |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến)* | **ĐẠT** | `doc_cong` luôn gắn 4 cổng `_CHUA_DO_DUOC` *(dat=None)* ⇒ ⛔ bao giờ toàn xanh *(đo tuyến + đột biến M4-tệp-vắng-biến-mất giết)*; `HD1_THANG` chỉ ĐỌC 5 khoá hợp đồng + ngày ảnh, **⛔ tính lại luật kỳ** *(đọc mã `_cong_hd1`)*; Đ3 *(`o==0`·`so_ky==0` ⇒ CHƯA ĐO ĐƯỢC — M3 giết)*; Đ5 *(MONG khai trước · cổng đỏ được hai chiều)*; `_dem` loại `bool`/âm/chuỗi *(M4 giết)*; tệp tự-mâu-thuẫn/sai-kiểu ⇒ cổng của khối ấy `None`, ⛔ kéo cổng kia *(R1 đo `loai_tu_soi > co` ⇒ FINAL CHƯA ĐO ĐƯỢC, HD1 nguyên; `so_ky` lệch ⇒ HD1 CHƯA ĐO ĐƯỢC, FINAL nguyên)* |
| **Dữ liệu** *(kho thật, chỉ đọc)* | **ĐẠT** | Kho `fls` cụm 5444 **RỖNG** *(fls_itl = 0 dòng — kết nối chỉ đọc, `FLS_CHO_GHI_THAT` ⛔ đặt)*; số HD1 là của **tệp đo tĩnh** *(ảnh 2026-08-26)*, ⛔ kho sống. R1 lấy `voi_so_luong.json` ở **ngọn `isp/H2` @ `b701ebb`** và chạy gate CG1 ⇒ **hợp đồng giữ** *(H2 chỉ THÊM 3 khoá, ⛔ bỏ; hai cổng y hệt)* — xem `CG1-R1-03` về 4 khoá `tong.*` ngoài hợp đồng |
| **Màn hình** *(trạng thái · thiết kế · phím · NFR)* | **N/A có lý do** | ISP mục 4 + Scope: *"N/A — F03 hiện cổng mới ở FG; bước này ⛔ sửa màn"*. Diff ⛔ chạm `fls/web/tep/**` *(R1 kiểm `git diff --stat`: 0 tệp màn)*. F03 đã in `da_do`+`ly_do` của mọi cổng sẵn *(`man_f03.js:33-35`)* ⇒ hai cổng mới hiện tự nhiên khi FG về |

## Phát hiện *(0 CHẶN — chi tiết + luật phòng ở sổ riêng)*
| Mã | Mức | Lớp | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|---|
| `CG1-R1-01` | **NÊN SỬA** | B2 | `tools/dung_moi_truong_isp.sh` *(nhánh vs S0)* · `duong_nen_bai_do.txt` | Script cổng nhánh CG1 **yếu hơn** bản S0 mới nhất: `-rfE` *(⛔ theo `xfail`)*, thiếu 2 dòng `XFAIL`, thiếu che DSN `S0-R3-03`, `MONG=2493` vs S0 `2490`. ⛔ che lỗi *(mã CG1 qua **cả** bản S0 chặt hơn: `28=28 · XFAIL 2=2`)*; chỉ là cổng ít chặt. Gộp phải lấy bản S0 + cộng `+33` *(→ 2523)* | **orchestrator** |
| `CG1-R1-03` | **NÊN SỬA** | B2 | `fls/repo/doc_bao_cao.py:967-971` *(`tong.o_parity·o_parity_khop·co·loai_tu_soi`)* | `FINAL` **buộc** đọc 4 khoá `tong.*` ⛔ có trong hợp đồng H2↔CG1 *(5 khoá `dat_hd1` + ngày ảnh)*. Hôm nay giữ *(đo ngọn H2)*; đổi tên ⇒ `FINAL` âm thầm `CHƯA ĐO ĐƯỢC` *(an toàn, chỉ B1 biết)*. Thêm 4 khoá vào lệnh "giữ tên" của vòng sửa H2 | **orchestrator** |
| `CG1-R1-02` | GHI NHẬN | B2 | `doc_bao_cao.py:964-1001` *(`_cong_final`)* · ISP §2 | Hai mẫu số `FINAL` cùng sống *(oracle `69.510/69.510` vs mọi dòng `69.706/69.769`)* sau `H2-R1-01`. Nhãn Đ4 **đủ** *(R1 đo tuyến: `da_do`+`ly_do` nói rõ 37 dòng tự soi loại + 259 ô ⛔ vào mẫu số)*. Chốt Q2 | orchestrator/BA |
| `CG1-R1-04` | GHI NHẬN | B1 | `fls/api/cua.py` · `xu_ly.py` · `tools/chay_cua.py` | 3 tệp ngoài bảng TRONG nhưng **đòi bởi** câu TRONG *"truyền vào (hợp đồng tầng 7)"*; ⛔ mặc định ở `fls/` *(M5 giết)*; `lint-imports` 11 kept. ⛔ lấn — có chủ ý *(Q1)* | *(ghi)* |
| `CG1-R1-05` | GHI NHẬN | B1 | `BA-07` §2 *(dòng `/gates`)* | Tài liệu BA lệch mã *(còn khai FINAL `null`)*. `02_BA` ⛔ của Dev *(đúng — ⛔ chạm)* | **BA** *(`fls-ba`)* |

## Bài thử mới *(`tests/nghiem_thu/`)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| *(không)* | R1 **⛔ thêm** bài nghiệm thu: phủ của `tests/api/test_isp_gates_hd1.py` **đủ** *(8/8 đột biến độc lập của R1 bị giết; Đ2/Đ3/Đ4/Đ5 đều có bài; B1…B4 qua tuyến thật)*. Nợ bài *(nếu có)* là của H2 *(`CG1-R1-03` — hợp đồng khoá)* + BA *(`CG1-R1-05`)*, ⛔ của CG1 | — |

## Môi trường R1 *(tự dựng)*
- `tools/dung_moi_truong_isp.sh --cong 5444` *(script S0 @ `c1cf29b`)* ⇒ `KẾT: ĐẠT` *(venv `/home/user/FLS-tobe/.venv` + cụm PG 16 cổng 5444)*; `pg_isready -h localhost -p 5444` = accepting.
- Sha xác nhận: `isp/S0` = `c1cf29b` · `isp/H2` = `b701ebb` · `isp/CG1` = `84bcdbf` · `isp/base-w3` = `575926e` — **khớp** brief.
- Script `--duong-nen` của NHÁNH CG1 **khác hành vi** bản S0 ⇒ R1 chạy **cả hai**, ghi cả hai *(trên; `CG1-R1-01`)*.
