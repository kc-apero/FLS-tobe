# BG-356 — bàn giao `WO-355` · 4 agent Voi: MỘT nhà cung cấp Anthropic (Opus 5.5 · Sonnet 5.5), đường gọi API THẬT

| | |
|---|---|
| **Thuộc** | `WO-355` |
| **Phát bởi** | `fls-dev` · 2026-11-23 |
| **Nhận** | `fls-test` (R1 → `KQ-357`) |
| **Nhánh** | `claude/bold-galileo-zukpaf-isp/AG2` · SHA mã **`cafbcd7`** (BG ở commit kế) |
| **Kho thật** | `KHONG_CHAM` (G0 BÓNG) · SA Google chỉ-đọc (dựng bể) · **0** lời gọi API thật |

## Đọc trong 5 phút

| | |
|---|---|
| **Mô hình từng agent** | A1 · A2 · A3 = **`claude-opus-5-5`** (agent LÀM) · A4 = **`claude-sonnet-5-5`** (phần KIỂM dùng mô hình — mở ở G1; hôm nay A4 vẫn MÃ THUẦN, phán cuối = MÃ `doi_chieu`). Một hãng: họ `anthropic`. Gemini **đã xoá** (`GEMINI_FLASH` · `GoogleChuaDung` · `"google"` khỏi `NGUON_THAT`). Họ `openai` **chừa chỗ** (`mo_hinh.HO_DE_DANH`: chốt chạy trước rồi `ChuaDung`, ⛔ adapter). |
| **Mô hình từng skill** | **12** skill `lam`/`bong` (A1 4 · A2 4 · A3 4) gọi `claude-opus-5-5`; **4** skill A4 = `ma` ⇒ "MÃ — ⛔ lượt API" *(thẻ `docs/ITL/06_Agent/A*.md` cột "mô hình skill gọi" + cột cùng tên ở §2 `report.html`; hàm `chuoi.mo_hinh_skill`)* |
| **Đã gọi thật chưa** | **CHƯA — 0 lời gọi.** `ANTHROPIC_API_KEY` **vắng** trong container này (`test -n` ⇒ rỗng; ⛔ in giá trị). AC-3 = **ĐỎ có tên "thiếu ANTHROPIC_API_KEY"** — ⛔ bịa số, ⛔ thay bằng GIẢ. |
| **Report GIẢ ↔ THẬT** | `docs/ITL/06_Agent/vong_that/REPORT_GIA_THAT.md` (+ `.json`) — cột GIẢ có số thật của đường ống; cột THẬT mọi ô = `⛔ thiếu ANTHROPIC_API_KEY`; exit **2**. Sinh bởi `tools/vong_that_voi.py` *(mới)*. |
| **Chi phí** | **0 USD · 0 token** (0 lời gọi — Đ3: mẫu số 0, ⛔ là "rẻ"). Bảng giá ghim trong mã, NGÀY TRA **2026-11-23** (skill `claude-api`): Opus 5.5 **$4 / $20** · Sonnet 5.5 **$2 / $10** mỗi 1 M token vào / ra · cache đọc $0,20 / $0,10. Trần mặc định một vòng **2 USD** (`--tran-usd`). |
| **Chạy thật khi có khoá** | trong container MỚI tạo sau khi chủ đặt khoá: `export FLS_CHO_GOI_API=1 FLS_ZDR_DA_BAT=1 FLS_HELDOUT_NOI_DUNG=/tmp/fls_be` ⇒ (1) `python tools/dung_be_giu_rieng.py --doc-song --ra /tmp/fls_be` ⇒ (2) `python tools/vong_that_voi.py --that --tran-usd 2` *(tập nhỏ, xem chi phí)* ⇒ (3) `… --that --be --tran-usd 6 --ghi` *(bể A/B)*. ⚠ `FLS_ZDR_DA_BAT=1` = người vận hành XÁC NHẬN tài khoản API đã bật ZDR (chốt thứ năm có sẵn từ `AG-R1-11`) — ⛔ đặt cho qua. |

## Bảng AC → bằng chứng

| AC | Mong | Kết | Bằng chứng |
|---|---|---|---|
| AC-1 · nhà cung cấp | chỉ họ `anthropic`, Opus 5.5 · Sonnet 5.5 ghim; xoá Gemini + mọi nhánh `google`; giao diện mở cho `openai` (⛔ adapter); thẻ + zip ghi đúng mô hình từng skill | **ĐẠT** | `fls/agent/mo_hinh.py` (`OPUS_5_5` · `SONNET_5_5` · `ADAPTER = {"anthropic": …}` · `HO_DE_DANH = ("openai",)`) · `fls/agent/chuoi.py` (A4 = `SONNET_5_5`; luật hai HỌ ⇒ **luật hai MÔ HÌNH** `kiem_a4_khac_mo_hinh`) · bài `test_WO355_khong_con_ho_google__chi_anthropic_ghim` · `test_WO355_giao_dien_theo_ho__openai_chua_cho__…` · `test_WO355_luat_hai_mo_hinh__…` · `test_mo_hinh_skill__…` · `python tools/sinh_the_agent.py --zip` ⇒ 4 thẻ + 4 zip sinh lại (A4: `dự kiến G1 (phần KIỂM, WO-355): claude-sonnet-5-5 họ anthropic (ghim)`). Grep `gemini\|google` (không phân hoa thường) trên `fls/agent` + 4 công cụ agent + `tests/agent`: **0** dòng mã sống; **7** dòng chú thích/docstring bia (`mo_hinh.py:9,67,68` · `chuoi.py:13,14` · `report.py:71` · `chay_agent_voi.py:217` — biên bản, Đ2) + **3** dòng bài canh VẮNG mặt (`test_mo_hinh.py:69,70,73`) |
| AC-2 · gọi thật đúng chuẩn | SDK `anthropic` chính thức (tra skill `claude-api`); 3 chốt giữ; nhật ký mỗi lời gọi: mô hình · token vào/ra · giây · USD ước (ngày tra); lỗi API ⇒ ĐỎ có tên, ⛔ rơi về GIẢ | **ĐẠT** (SDK GIẢ, ⛔ mạng) | `AnthropicMessages` gọi `client.messages.create` của SDK `anthropic` **2.12.0** (đã đối chiếu chữ ký `create` có `output_config` · `Usage` có `input_tokens`/`output_tokens`/`cache_*`); ⛔ `thinking` (Opus 5.5: `disabled`/`budget_tokens` ⇒ 400) · ⛔ `tool_choice` ép (400) · ⛔ `temperature` (400) · ⛔ `fallbacks` · `effort` đặt RÕ. Chốt: `--that` · `FLS_CHO_GOI_API=1` · khoá · ghim · (+ZDR ở `mo`) — bài cũ giữ nguyên + mô hình ⛔ có trong `BANG_GIA` ⇒ `CamGoiThat`. `NhatKyGoi` (12 trường, ⛔ nội dung) · `LoiApi` (lớp SDK · HTTP · request-id, `__cause__` None ⇒ ⛔ kéo thông điệp gốc) · `VuotTran` · mô hình phục vụ ≠ ghim ⇒ `LoiApi`. **22** bài `tests/agent/test_mo_hinh_that.py` — gồm chuỗi chạy TRỌN qua adapter thật (SDK giả) ⇒ A4 **4/4**, report đếm `mo_hinh_that` **3**, nhật ký **24** lời gọi = 2 × 12 skill; lỗi 529 ở lời gọi đầu ⇒ `DỪNG ở A1_RI/01_nguon_bank — LoiApi: APIStatusError HTTP 529`, 0 lượt ở A2–A4 |
| AC-3 · test THẬT vòng 1 | khi có khoá: (a) chuỗi 4 agent trên tập nhỏ (12 dựng + ≤ 20 bể) · (b) fleet eval A2.04 bể A/B bằng Opus thật ⇒ report MỘT trang GIẢ ↔ THẬT; chưa có khoá ⇒ ĐỎ có tên | **ĐỎ — thiếu ANTHROPIC_API_KEY** *(đúng nhánh WO khai)* | `python tools/vong_that_voi.py --that --be --ghi` ⇒ exit **2**, `**KẾT: ĐỎ** — thiếu ANTHROPIC_API_KEY · CamGoiThat: … FLS_CHO_GOI_API ≠ 1 · khoá ANTHROPIC_API_KEY vắng … · … FLS_ZDR_DA_BAT=1`. Bể dựng lại từ nguồn sống (SA chỉ-đọc) ngoài repo: **A 65/65 · B 70/70** ca, kỳ A↔B KHỚP, `DEM_BE.json` **không đổi**. Cột GIẢ có số (bảng dưới). Bài `test_AC3_thieu_khoa__exit_2__DO_co_ten__khong_so_THAT` |
| AC-4 · an toàn | ⛔ ghi kho/sổ; ⛔ nội dung/phản hồi thô trong repo (chỉ đếm + vân tay); khoá ⛔ in/log | **ĐẠT** | Mọi công cụ agent chỉ đọc ảnh/tệp đo; kho `fls_itl` **0** dòng trước và sau. Nhật ký + report JSON: chỉ số + vân tay 16 hex (bài ghim tập khoá 12 trường). Khoá lính canh `sk-ant-GIA-…` ⛔ xuất hiện ở stdout/nhật ký (2 bài). `--ghi-phat-lai` vẫn chỉ đi với `--gia` ⇒ phản hồi THẬT ⛔ bao giờ vào `phat_lai/`. `quet_pii_repo` **0** chỗ · 0 tệp. Bể: `/tmp/fls_be` dir 700 · tệp 600 |
| AC-5 | `--duong-nen` ĐẠT (sàn = thu thập thật + bài ghim cùng commit); `kiem_tai_lieu` · `lint-imports` 11 kept | xem §Cổng | sàn `MONG_PYTEST_TOAN_BO` **4997 → 5020** (= thu thập thật; +22 `test_mo_hinh_that.py` +1 `test_mo_hinh.py`; web **690** giữ) + `tests/test_dung_moi_truong_isp.py` cùng commit |

## Report GIẢ ↔ THẬT *(chép từ `REPORT_GIA_THAT.md`; chỉ số, ⛔ nội dung)*

Tập nhỏ = **12** ca dựng + **20/70** ca bể B (hạt 355) — theo nhóm `phai_noi` 20 · `phai_nguoi` 9 · `l3` 2 · `chua_chot` 1 · vân tay tập `4f5a3f7b1ee013f2`.

| chỉ số | GIẢ | THẬT |
|---|---|---|
| (a) ô ĐỘC LẬP khớp / mẫu số | 557/557 | ⛔ thiếu ANTHROPIC_API_KEY |
| (a) ô VÒNG TRÒN khớp / mẫu số | 74/74 | ⛔ thiếu ANTHROPIC_API_KEY |
| (a) A4 ĐẠT | 4/4 | ⛔ thiếu ANTHROPIC_API_KEY |
| (a) G0 A2.04: nối · nối sai · recall phải-nối · phải-người bị nối | 8 · 1 · 0,35 · **1** | ⛔ thiếu ANTHROPIC_API_KEY |
| (b) bể A (65 ca chính): nối · sai · recall · **phải-người bị nối** · L3 bị nối | 2 · 2 · 0,0 · **2** · 0 | ⛔ thiếu ANTHROPIC_API_KEY |
| (b) bể B (65 ca chính / 70): nối · sai · recall · **phải-người bị nối** · L3 bị nối | 2 · 1 · 0,0333 · **1** · 0 | ⛔ thiếu ANTHROPIC_API_KEY |
| token vào / ra · USD | — | 0 / 0 · 0 (0 lời gọi) |

⚠ Cột GIẢ là luật `luat_gia_v1` đứng thay mô hình — nó **TRƯỢT bar** `a3-1-ref` (0 ca phải-để-người bị nối) ở cả ba tập (1 · 2 · 1). Đó là mức nền vòng THẬT phải vượt, ⛔ số của Opus.

## Cổng — dán thật *(cụm PG 16 cổng 5436, kho RỖNG; `PYTHONUTF8=1`)*

| cổng | kết | dòng thật |
|---|---|---|
| `python -m pytest` (trong `--duong-nen`, `PYTEST_ADDOPTS` gỡ) | ĐẠT theo đường nền | `12 failed, 4992 passed, 2 xfailed, 14 errors in 1633.05s` = **28** node đỏ/XFAIL = đúng tập `duong_nen_bai_do.txt` (thêm 0 · bớt 0) · `tests/web`: `3 failed, 687 passed` = 3 = 3 |
| `--duong-nen --cong 5436` (chạy MỘT mình, trên `cafbcd7`) | **ĐẠT** | `[ĐẠT] đường nền toàn bộ tập đỏ + XFAIL = đường nền: 28 = 28 node id (trong đó XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 5020 bài (mong ≥ 5020)` · `[ĐẠT] đường nền tests/web … 3 = 3 … chạy 690 bài (mong ≥ 690)` · `[ĐẠT] lint-imports Contracts: 11 kept, 0 broken.` · `[ĐẠT] kho fls RỖNG fls_itl = 0 dòng` · `══ KẾT: ĐẠT — mọi phép kiểm khớp mong` |
| `tests/agent` | ĐẠT | `133 passed` *(trước khi thêm path tự đủ)* · riêng `test_mo_hinh_that.py` + `test_mo_hinh.py`: `34 passed` |
| `kiem_tai_lieu.py` | ĐẠT | `✅ cong tai lieu DAT — va no da do duoc that (518 file, 3060 bang, 986 o ngay, 104 ma QD)` *(trước BG này; chạy lại ở dòng cuối)* |
| `lint-imports` | ĐẠT | `Contracts: 11 kept, 0 broken.` |
| `soi_bang_tuyen.py` | ĐẠT | `✅ ban khai KHOP SQL that o ca 49 tuyen` |
| `kiem_thuyet_minh.py` | ĐẠT | `✅ CONG THUYET MINH DAT — 35/35 nut co mat trong CA 2 ban` |
| `quet_pii_repo.py` | ĐẠT | `[ĐẠT] 0 chỗ số TK cá nhân · 0 tệp` |
| `python -m fls.db.pg_migrate` | ĐẠT | `khong co gi de ap` · `pg_verify: khop` |
| `kiem_so_song.py` | **ĐỎ — ⛔ đo được (môi trường)** | `⛔ khong do duoc: kho ⛔ khong co dau thoi diem cua lan nap / anh chup` — cụm mới, kho RỖNG (`fls_itl` 0 dòng). Script gọi `.venv/Scripts/lint-imports.exe` (đường Windows) ⇒ trên Linux ngã `FileNotFoundError` cả ở NỀN `HEAD` chưa sửa; tôi đặt liên kết trong `.venv` (gitignore) để nó chạy tới phép kho |
| `khop_owner.py --kiem` | **ĐỎ có sẵn ở NỀN** | cây này lệch **2** khối (B1 · C6); NỀN `HEAD` sạch (worktree) lệch **3** (A1 · B1 · C6) ⇒ ⛔ do WO-355 (WO-355 ⛔ chạm `_AUDIT_ALIGNMENT_ROADMAP.md`) |
| `dong_bo_so_song.py --ghi` | ⛔ chạy | `kiem_so_song` ⛔ đo được ⇒ ⛔ có lệch để soạn |

## Trung thực về giới hạn

1. **0 lời gọi thật.** Mọi bằng chứng AC-2 là SDK GIẢ thay `sys.modules["anthropic"]` — đúng đường mã, nhưng ⛔ chứng minh API thật chấp nhận yêu cầu. Rủi ro còn lại khi gọi thật: (i) Opus trả chữ ngoài JSON ⇒ skill ĐỎ có tên (prompt đã dặn "DUY NHẤT một đối tượng JSON"; `doc_json_tra_loi` chịu đúng MỘT rào ```` ```json ````, ⛔ cắt chữ khác); (ii) kết quả công cụ `voi` lớn (557 ô ĐỘC LẬP) ⇒ token vào chưa đo — vì vậy trần 2 USD + chạy tập nhỏ trước.
2. **Luật hai HỌ đổi thành hai MÔ HÌNH** (A4 Sonnet ≠ A1–A3 Opus). Một hãng ⇒ độc lập về HỌ ⛔ còn; độc lập còn lại = mô hình khác + phán cuối là MÃ. Đây là hệ quả trực tiếp của quyết chủ, ghi để R1 soát.
3. **Thẻ eval `_chung.md` · `a4-soat.md` (`05_FleetEval/eval-cards`, chủ BA) vẫn ghi Gemini 3.8 Flash / "khác họ"** — Dev ⛔ sửa spec; cần BA cập nhật theo quyết chủ 23/11 (gợi ý `HOI`/`WO` BA).
4. Khối `thinking` Opus trả về đi NGUYÊN vào lượt sau (luật preserved thinking). Ở `mo` bộ che ⛔ đụng; ở `che_noi_dung`/`che_het` lớp 2 soát MỌI chuỗi — chữ ký `signature` (base64) về lý có thể chứa dãy ≥ 9 chữ số ⇒ `CamGui` có tên (chưa gặp, chưa đo).
5. `tools/dung_be_giu_rieng.py --doc-song` cần `google-auth` + `requests` — ⛔ có trong `requirements.txt` (có từ trước WO-355); tôi cài tay vào venv. `anthropic>=2.12` nay ở `requirements.txt`.
