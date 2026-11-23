# BG-330 — bàn giao `WO-329` · 4 agent vận hành Voi gọi API (A1 RI · A2 PR + SI.MAP · A3 SI.ITL · A4 Auditor)

| | |
|---|---|
| **Thuộc** | `WO-329` |
| **Phát bởi** | `fls-dev` · 2026-11-23 |
| **Nhận** | `fls-test` (R1 → `KQ-331`) · chủ đọc 4 agent trước khi cho chạy |
| **Commit** | `claude/bold-galileo-zukpaf-isp/AG` @ `7dc9214` (mã + bài) → ngọn nhánh mang thêm commit dán kết quả `--duong-nen` vào BG này *(đã đẩy)* |
| **Kho thật** | `KHONG_CHAM` · ⛔ gọi API thật · ⛔ bật agent |

## Đọc 4 agent trong 10 phút

1. **Mở report một trang** — `docs/ITL/06_Agent/report.html` *(ảnh: `docs/ITL/06_Agent/report.png`)*.
   Dòng KẾT hôm nay: **`KẾT: ĐẠT — 627/627 ô khớp · lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0 · chưa chạy 0 · A4 ĐẠT 4/4 agent`** *(chế độ PHÁT LẠI)*.
2. **Đọc 4 thẻ** *(mỗi thẻ ~2 phút; cũng có trong 4 zip `docs/ITL/06_Agent/goi/*.zip` đã gửi chủ 23/11)*:

| agent | thẻ | mô hình ghim *(phương án A — PROPOSED)* | checksum prompt | bộ skill — chạy TUẦN TỰ |
|---|---|---|---|---|
| A1 · Collect_raw_data | [`A1_RI.md`](../../06_Agent/A1_RI.md) | `claude-opus-5-5` ✅ | `9f84a5b36e62d7b0` | 01 Bank txns (sao kê + sổ AS-IS) → 02 FPS (PM line) → 03 H1000 → 04 PLT (GI · OMC · SC · PS) |
| A2 · Group Ledger + Mapping | [`A2_PR_MAP.md`](../../06_Agent/A2_PR_MAP.md) | `claude-opus-5-5` ✅ | `e9d149e87fff5474` | 01 dòng chuẩn 1-1 → 02 ghép Ref hình A–F → 03 hàng chờ người → **04 ghép theo NỘI DUNG (G0 bóng)** |
| A3 · SI.ITL — Adjust + Allocate | [`A3_SI_ITL.md`](../../06_Agent/A3_SI_ITL.md) | `claude-opus-5-5` ✅ | `fe71100066e826c8` | 01 ô Final 7 khối → 02 vùng sửa R–AT → 03 tự sinh MID → 04 Calculate · Allocate · Report (10 gói HD2) |
| A4 · Auditor | [`A4_AUDITOR.md`](../../06_Agent/A4_AUDITOR.md) | `gemini-3.8-flash` — **CHƯA ghim** (C2) | `8160a71f8ba50465` | 01 soát lớp (MÃ) → 02 cổng HD1 → 03 cổng HD2 → 04 report (MÃ) |

3. **Luật chạy** *(`fls/agent/chuoi.py`)*: skill `n+1` chỉ khi cổng skill `n` ĐẠT; agent `k+1` chỉ khi A4 (MÃ, `fls/agent/doi_chieu.py`) cho agent `k` khớp 100 % từng ô. Dừng ⇒ có TÊN: `DỪNG ở A2_PR_MAP/02_ghep_ref — cổng … ĐỎ` / `A4 TRƯỢT A2_PR_MAP: LECH 1 — ô đầu: voi:bank_tong.dong_theo_hinh.A`.
4. **Câu chủ** — §Câu chủ dưới (C1–C5), mỗi câu 2 phương án + khuyến nghị.

## Hai lời chủ đến GIỮA lượt — đã làm theo
| Lời chủ 23/11 | Đã làm | Còn lại |
|---|---|---|
| *"nhận raw input (4 nguồn: Bank txns, FPS, H1000, PLT), chạy agents để adjust, mapping, allocate → Report … mapping dựa trên nội dung giao dịch … fleet eval nhiều vòng"* | A1 nhận đủ **4 nguồn / 9 ảnh** (Σ dòng ảnh = khai, vân tay) · A2 thêm skill **04 ghép theo nội dung** (bộ che nội dung + luật cứng + chấm rubric `a3-1-ref`) · A3 thêm skill **04 Calculate/Allocate/Report** (10 gói HD2) · **`tools/fleet_eval_voi.py`**: 3 vòng (v0 mã → v1 tắt nội dung → v1 bật nội dung đã che), chấm MÙ, phán bar, `docs/ITL/05_FleetEval/vong/TONG_HOP.md` | vòng THẬT cần bể giữ riêng + C1–C4; A3 gợi ý ô vùng sửa (G0) **chưa dựng** — cần ảnh Manual input 22 tháng |
| *"cho tôi 4 file zip tương đương 4 agents, cần bao gồm các bộ skill"* | `python tools/sinh_the_agent.py --zip` ⇒ `docs/ITL/06_Agent/goi/{A1_RI,A2_PR_MAP,A3_SI_ITL,A4_AUDITOR}.zip` — thẻ + `00_he_thong.md` + 4 skill + bản phát lại + thẻ fleet eval (+ vòng · report) — **đã gửi chủ** | chủ sửa tệp skill ⇒ chép về `fls/agent/skill/<agent>/` ⇒ `--gia --ghi-phat-lai` ⇒ `sinh_the_agent.py` ⇒ cổng |

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/agent/` *(mới — 9 tệp)* | `che` (NFR-I13 trắng + chốt đen) · `mo_hinh` (giao diện nhà cung cấp, PHÁT LẠI/GIẢ/THẬT có chốt) · `skill` (bộ skill có số) · `cong_skill` · `doi_chieu` (A4) · `chuoi` · `report` · `ghep_noi_dung` · `o` |
| `fls/agent/skill/<4 agent>/` *(20 tệp `.md`)* | prompt hệ thống + 16 skill — NGUỒN của prompt, checksum vào phiên bản |
| `tools/chay_agent_voi.py` · `tools/fleet_eval_voi.py` · `tools/sinh_the_agent.py` | chạy chuỗi + report · fleet eval nhiều vòng · thẻ + zip |
| `docs/ITL/06_Agent/` | 4 thẻ · `report.html` · `report.png` · `phat_lai/*.json` (bản ghi phát lại — sinh bằng mô hình GIẢ) · `goi/*.zip` |
| `docs/ITL/05_FleetEval/vong/` | 3 vòng + `TONG_HOP.md` |
| `tests/agent/` *(50 bài)* · `tests/fixture/agent/` | bể ca DỰNG 12 ca + đáp án (PII BỊA) |
| `.importlinter` | `fls.agent` vào hợp đồng 1 (cấm `psycopg`) — giữ **11** hợp đồng; cấm `fls.db/repo/api/web` canh bằng bài AST |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` 4772 → **4822** (= thu thập thật, +50) |

## Bằng chứng từng AC
| AC | Bằng chứng *(số đo thật)* |
|---|---|
| AC-1 thẻ | 4 thẻ sinh máy; `tests/agent/test_skill_tang.py::test_the_agent_ghi_dung_checksum_prompt` ×4 — checksum trong thẻ = máy tính (sửa prompt chưa sinh lại thẻ ⇒ ĐỎ) |
| AC-2 skill tuần tự | 4 agent × 4 skill số `01…04` (`test_bo_skill_04_skill_so_lien` ×4; số nhảy ⇒ `LoiBoSkill`) · **phá cổng skill giữa**: `test_AC2_pha_cong_skill_giua__chuoi_DUNG_dung_cho` — +1 ở `voi:theo_ky.2025-01.map_fls` ⇒ `DỪNG ở A2_PR_MAP/02_ghep_ref — cổng tong_ky:map_fls+pm_noi ĐỎ`, A2.03–04 + cả A3 `chưa chạy` |
| AC-3 gọi API | `test_mo_hinh.py` (10 bài): thiếu MỖI chốt (`--that` · `FLS_CHO_GOI_API` · khoá) ⇒ `CamGoiThat`; bí danh / chưa ghim ⇒ chặn; ⛔ chốt ⇒ SDK `anthropic` ⛔ được nhập · `test_che.py` (14 bài): gián điệp nhận 2 yêu cầu, **0** lần thấy tên · số TK · email · Số chứng từ · Diễn giải; **phá bộ che ⇒ gián điệp thấy số TK** (bài có răng) |
| AC-4 report | `report.html`: 627 ô · 13 skill `lam` · mẫu số · khớp · lệch · ⛔ đo được · thiếu · thừa · chưa chạy từng skill · nhãn mỗi ô (Đ4) · khối lệch AS-IS có tên riêng · khối G0 riêng |
| AC-5 chứng minh | phát lại ⇒ `627/627`, lệch 0 (`test_AC5_phat_lai__KET_DAT_lech_0`) · đột biến 1 ô ⇒ ĐỎ đúng ô `voi:bank_tong.dong_theo_hinh.A` agent 2273 ↔ máy 2272 (`test_AC5_dot_bien_mot_o__A4_DO_dung_o`) · xoá `voi_so_luong.json` ⇒ `KHONG_DO_DUOC` ở nguồn `voi` + `cong`, `A4 TRƯỢT A2_PR_MAP` |
| AC-6 Q8 | sàn 4822 + bài ghim cùng commit · `lint-imports` 11 kept · `kiem_tai_lieu` ĐẠT · `quet_pii_repo` 0 · `--duong-nen` — xem §Cổng |

## Câu chủ *(AP còn PROPOSED / chưa ký — mỗi câu 2 phương án + khuyến nghị)*
| # | Câu | Phương án 1 | Phương án 2 | **Khuyến nghị** |
|---|---|---|---|---|
| **C1** | Mô hình **A hay B** *(Voi F0b — chốt sau vòng chọn N8)* | **A**: Opus 5.5 làm · Gemini 3.8 Flash kiểm — đúng nhất ngay, dữ liệu qua Anthropic + Google | **B**: Qwen 3.8 làm · gpt-oss-120b kiểm — rẻ nhất (~$2,77 một lượt sổ), cần vận hành endpoint | **A cho G0** (bóng, ⛔ ghi): một vòng cả sổ ~$83,87 ($41,94 theo lô) là nhỏ; chốt lại sau vòng N8 trên bể giữ riêng. Mã đã theo giao diện họ ⇒ đổi B = thêm một adapter. ⚠ Mã cố ý ⛔ bật `fallbacks` của Opus 5.5 (rơi sang mô hình khác = đổi phiên bản trong im lặng) — refusal ⇒ dừng có tên |
| **C2** | A4 **khác họ** — nhà cung cấp + mã ghim | Gemini 3.8 Flash qua API Google, mã chính xác lúc mở tài khoản | Giữ A4 = MÃ thuần (`doi_chieu`) cho tới G1, mô hình A4 chỉ chép cổng | **2 tới G1**: phán đã là mã; adapter Google **chưa dựng** (`GoogleChuaDung`, chốt chạy trước) — dựng khi chủ ghim mã |
| **C3** | Cửa **G0–G3** *(ngưỡng 95 % · 98 % · mẫu 10 % · 4 tuần — Voi trang 3, câu ⑤)* | Giữ ngưỡng đề xuất, mở theo từng đơn vị | Siết: G1 chỉ khi 2 vòng liên tiếp 0 ca phải-để-người bị nối | **2 cho A2.04** (ghép nội dung chạm tiền, `INV-I16`); ngưỡng chung giữ đề xuất. Hôm nay mọi agent ở **G0 bóng** — ⛔ ghi gì |
| **C4** | **Gửi nội dung giao dịch ra API** *(mâu thuẫn: WO-329 AC-3 "Diễn giải ⛔ rời máy" ↔ lời chủ 23/11 "mapping dựa trên nội dung")* | TẮT (mặc định hôm nay): agent chỉ thấy tiền · tiền tệ · ngày · mã ứng viên — vòng 2 bể dựng: recall 0,29 | BẬT nội dung ĐÃ CHE (`<SO>` · `<TEN>` · `<EMAIL>` · `<DT>`) — vòng 3 bể dựng: recall 0,86, 0 nối sai | **2, sau khi ĐO trên dữ liệu thật** (`NFR-I13 ②`): đo tỉ lệ tên lọt qua bộ che trên 7.712 ô diễn giải trước; bộ che tên là danh sách ĐEN (họ Việt) — SẼ lọt tên lạ. Thêm chế độ không lưu dữ liệu (ZDR) của nhà cung cấp |
| **C5** | **Bể giữ riêng** cho fleet eval thật *(đáp án = ITL Ledge Final AS-IS)* | DATA làn đọc live qua SA (đã có khoá) → `FLS_HELDOUT_NOI_DUNG` ngoài repo | Dùng `sao_luu/` trên máy chủ | **1**: một WO làn DATA dựng ~60 ca theo thẻ `a3-1-ref` (D · E · F · L3 + ca chuyển), chỉ ĐẾM trong repo |

## Cổng *(nguyên văn)*
| Lệnh | Kết quả |
|---|---|
| `python -m pytest tests/agent` | `50 passed in 11.47s` |
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5447` | **`KẾT: ĐẠT`** — toàn bộ `12 failed, 4794 passed, 2 xfailed, 14 errors` ⇒ tập đỏ + XFAIL = đường nền **28 = 28** node id (thêm 0 · bớt 0) · chạy **4822** bài (mong ≥ 4822) · `tests/web` `3 failed, 687 passed` ⇒ **3 = 3** · chạy 690 (mong ≥ 690) · lint 11 kept · di trú 27/27 · HD1 chay 9845 / co 9967 |
| `python tools/chay_agent_voi.py` *(phát lại)* | `KẾT: ĐẠT — 627/627 ô khớp · lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0 · chưa chạy 0 · A4 ĐẠT 4/4` |
| `python tools/fleet_eval_voi.py` | v0 `0 nối · ĐẠT bar` · v1-tắt `2 nối · 0 sai · recall 0.2857` · v1-bật `6 nối · 0 sai · recall 0.8571` · 0 ca phải-để-người bị nối |
| `.venv/bin/lint-imports` | `Contracts: 11 kept, 0 broken.` |
| `python docs/ITL/_tools/kiem_tai_lieu.py` | `✅ cong tai lieu DAT — … (489 file, 2962 bang, 968 o ngay, 104 ma QD)` *(trước khi thêm BG này)* |
| `python tools/quet_pii_repo.py` | `[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp` *(sau `git add` — quét tệp theo dõi)* |
| `python tools/soi_bang_tuyen.py` | `✅ ban khai KHOP SQL that o ca 49 tuyen` |
| `python tools/kiem_thuyet_minh.py` | `✅ CONG THUYET MINH DAT — 35/35 nut co mat trong CA 2 ban` |
| `python tools/kiem_so_song.py` | ⛔ **CHƯA CHẠY được**: `FileNotFoundError: …/.venv/Scripts/lint-imports.exe` — công cụ cứng đường Windows (có sẵn, ⛔ do WO này) |
| `python docs/ITL/_tools/khop_owner.py --kiem` | `A1 · B1 · C6 ⛔ ĐỔI TRẠNG THÁI` — **y hệt trên HEAD gốc `1157359`** (đo bằng worktree): kho cổng 5447 RỖNG, ⛔ do WO này |
| `python -m fls.db.pg_migrate` | ⛔ chạm schema — ⛔ chạy |

## Dev tự thấy còn yếu
1. **Phép so `hd2:` và `cong:` gần vòng tròn**: đường agent và đường máy cùng đọc `hd2_cong.json` / cổng `doc_cong_*` — bắt lỗi CHÉP của agent, ⛔ bắt engine HD2 cũ. Engine HD2 thật cần kho có IX config (`tools/do_hd2.py --dsn`), kho test ở container rỗng ⇒ 9/10 gói `KHONG DAT: IX.* ⛔ đọc được` khi chạy lại. Phần `voi:` thì KHÔNG vòng tròn: agent gọi engine chạy lại (`do_voi_so_luong.do()`), máy là tệp đã ghi.
2. **Agent A1–A3 hôm nay chủ yếu CHÉP số engine** — đúng AP ("luật kiểm vẫn là mã", v0 = mã), nhưng giá trị mô hình chỉ ở A2.04 (ghép nội dung). A3 gợi ý ô vùng sửa, A4 thêm cờ: **chưa dựng**.
3. **Bản phát lại sinh bằng mô hình GIẢ** — ⛔ có một lượt API thật nào. Số fleet eval (recall 0,86 …) là của **luật giả trên 12 ca dựng**, ⛔ số mô hình.
4. **Bộ che tên người là danh sách ĐEN** (35 họ Việt) bên trong ngoại lệ nội dung — trái tinh thần `NFR-I13 ③`; vì vậy cờ nội dung TẮT mặc định và việc bật là C4. Bộ che đã cắn một lần trong buổi (nuốt `PM` của mã sau tên — bia ở `che.py`, bài `test_che_ten_KHONG_nuot_ma_PM`).
5. `fls.agent` cấm `fls.db/repo/api/web` bằng **bài AST**, ⛔ hợp đồng import-linter riêng (giữ 11 để khỏi kéo theo `gop_buoc_isp.py` · `kiem_so_song` · tài liệu `NFR-I16`). Test soi xem có muốn hợp đồng thứ 12.
6. `test_report_html_khop_tep_trong_repo` chỉ soát dòng KẾT, ⛔ so cả trang (trang mang ngày sinh).
7. Adapter Anthropic viết theo skill `claude-api` (`messages.create`, `output_config.effort`), **⛔ chạy thật lần nào** — SDK `anthropic` ⛔ có trong `requirements.txt`.

## Vòng sửa sau quyết định chủ 23/11 *(sau `d8898c3`)*

> Chủ: *"Không cần che nội dung hay stk, cho phép agents access toàn bộ, vì agents có thể học mapping, sẽ có 1 vài stk ngân hàng sẽ chỉ chi một loại giao dịch nhất định."* ⇒ **C4 đã chốt: MỞ**.

| Đổi | Bằng chứng |
|---|---|
| `fls/agent/che.py`: chế độ mặc định `mo` — dữ liệu công cụ đi NGUYÊN VĂN (nội dung · số TK · tên); chỉ bỏ `Email Address` (`PM_COT_RIENG_TU`, CLAUDE.md). Hai chế độ cũ giữ làm tuỳ chọn `--che che_noi_dung` / `--che che_het` | `test_MAC_DINH_mo__noi_dung_va_so_TK_di_nguyen__chi_bo_Email_Address` · bài che cũ gọi RÕ chế độ |
| A2.04 đọc thêm `noi:<ca>.tk` (số TK nguồn chi) — prompt: TK là tín hiệu thu hẹp ứng viên, ⛔ thay luật cứng | checksum prompt A2 → `e9d149e87fff5474` (thẻ + zip sinh lại) |
| Fleet eval thêm vòng 4 `v1-gia-mo` | `6 nối · 0 sai · recall 0.8571 · 0 ca phải-để-người bị nối` (luật GIẢ chưa dùng TK — mô hình thật mới học được TK) |
| Q8: `MONG_PYTEST_TOAN_BO` 4822 → **4824** | `tests/agent` `52 passed` |

⚠ Hệ quả cần chủ biết (⛔ chặn): dữ liệu gửi API giờ gồm tên người + số TK thật ⇒ nên bật chế độ **không lưu dữ liệu (ZDR)** với nhà cung cấp trước vòng thật; `NFR-I13` (BA) cần BA ghi lại quyết định này — Dev ⛔ sửa `02_BA`.

**Cổng sau vòng này:** `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5447` ⇒ **`KẾT: ĐẠT`** — toàn bộ `12 failed, 4796 passed, 2 xfailed, 14 errors` ⇒ tập đỏ + XFAIL **28 = 28** (thêm 0 · bớt 0) · chạy **4824** (mong ≥ 4824) · `tests/web` **3 = 3** · chạy 690 · lint 11 kept · `tests/agent` `52 passed`.

## Quyết định chủ 23/11 (tiếp) — đã ghi vào thẻ agent
| Câu | Chủ chốt | Ở đâu |
|---|---|---|
| C1 mô hình | **Phương án A** — Claude Opus 5.5 làm (A1–A3) · Gemini 3.8 Flash kiểm (A4) | 4 thẻ dòng "Mô hình ghim" |
| ZDR | **Bật** cho vận hành (Messages API) — bật theo TỔ CHỨC qua Anthropic, ⛔ công tắc trong mã | thẻ dòng "Dữ liệu & lưu giữ" |
| Lưu dữ liệu cho fleet eval | **Chấp nhận** gửi theo lô (Batches API — Anthropic giữ 29 ngày) để giảm 50 % giá | như trên |
| C5 bể giữ riêng | **Dựng** — việc kế (đọc live qua SA, ngoài repo; đáp án hai tầng: PM line · HD+CDT1 cho L3) | chưa làm trong BG này |
Còn mở: mã Gemini chính xác (A4 chưa ghim) · ZDR phía Google.
