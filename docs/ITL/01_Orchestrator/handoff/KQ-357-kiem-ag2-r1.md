# KQ-357 — biên bản kiểm `BG-356` *(R1 · `WO-355`)*

| | |
|---|---|
| **Thuộc** | `BG-356` · `WO-355` |
| **Kiểm bởi** | `fls-test` · 2026-11-24 · mã đo `5b6c525` *(nhánh `claude/bold-galileo-zukpaf-isp/AG2`)* · cụm PG 16 cổng 5447 |
| **Phán quyết** | **ĐẠT** *(R1: 0 CHẶN · 1 NÊN SỬA · 7 GHI NHẬN)* — AC-3 = ĐỎ có tên *"thiếu ANTHROPIC_API_KEY"* là **đúng** theo `WO-355` |

> Vai KIỂM: ⛔ sửa mã · ⛔ gọi API thật *(0 lời gọi ra ngoài; SDK `anthropic` 2.13.0 thật chỉ nối `127.0.0.1`)* · ⛔ ghi kho thật. Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_AG2.md` *(mã `AG2-R1-01…08`)*.

## Cổng chạy lại *(cây gộp thử = ngọn `origin/claude/bold-galileo-zukpaf` `bd3d27a` + `5b6c525`, gộp sạch, ⛔ commit; đã gỡ)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5447` *(một mình)* | `KẾT: ĐẠT` 28 = 28 · web 3 = 3 | `KẾT: ĐẠT` · toàn bộ **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)*, chạy **5020** bài *(mong ≥ 5020)*, `12 failed, 4992 passed, 2 xfailed, 14 errors` · web **3 = 3**, chạy **690** *(mong ≥ 690)*, `3 failed, 687 passed` | ✅ |
| `kiem_tai_lieu.py` | ĐẠT | `✅ … (519 file, 3065 bảng, 986 ô ngày, 104 mã QĐ)` | ✅ |
| `lint-imports` | 11 kept | `Contracts: 11 kept, 0 broken.` | ✅ |
| `quet_pii_repo.py` | 0 | `0 chỗ số TK cá nhân · 0 tệp` | ✅ |
| `pytest tests/agent` *(cây AG2)* | 133 | **133** passed | ✅ |
| `vong_that_voi.py --that --be` *(khoá vắng)* | exit 2, ĐỎ có tên | exit **2** · `KẾT: ĐỎ — thiếu ANTHROPIC_API_KEY` · cột GIẢ **557/557 · 74/74 · 4/4 · 8·1·0,35·1** | ✅ |

## Bảng AC
| AC | Mong | Đo được *(nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| AC-1 | chỉ họ `anthropic`; mã ghim; ⛔ Gemini; `openai` chỉ giao diện | `ADAPTER` = `{anthropic}` · `HO_DE_DANH` = `(openai,)` · `BANG_GIA` 2 mô hình · 4 agent = `opus-5-5` ×3 + `sonnet-5-5` ×1 · `grep -ri gemini fls tools` = **5** dòng, **cả 5 chú thích/docstring bia**, **0** mã sống · `openai`: thiếu chốt ⇒ `CamGoiThat`, đủ chốt ⇒ `ChuaDung` · bí danh / chưa ghim / ngoài bảng giá ⇒ `CamGoiThat` | ĐẠT *(zip còn 3 dòng Gemini ở thẻ eval của BA: `AG2-R1-05`)* |
| AC-2 | SDK chính thức, tham số đúng `claude-api`, nhật ký, lỗi ⇒ ĐỎ có tên | Đối chiếu skill `claude-api`: ⛔ `thinking` · ⛔ `tool_choice` · ⛔ sampling · `output_config.effort` đặt rõ · `max_tokens` 16000 không streaming · giá Opus 4/20 · Sonnet 2/10 · cache ghi 1,25× · cache đọc 0,20/0,10 — **khớp**. **SDK thật 2.13.0 trước máy chủ cục bộ**: body đúng, khoá đi bằng header *(⛔ body)*, `usage` 123/45/6/7 ⇒ nhật ký đúng, USD khớp công thức. Lỗi HTTP **7/7 mã** *(400·401·403·404·429·500·529)* ⇒ `LoiApi` có mã, ⛔ khoá, ⛔ nội dung, `__cause__` None. `refusal`·`max_tokens`·`pause_turn` ⇒ `dung_o` có tên, **1** lời gọi, ⛔ rơi GIẢ | ĐẠT |
| AC-3 | có khoá ⇒ test thật; chưa có ⇒ ĐỎ có tên, ⛔ bịa số | khoá vắng *(`test -n` ⇒ rỗng)*; exit 2; cột THẬT mọi ô `⛔ thiếu ANTHROPIC_API_KEY`; **0** lời gọi thật, **0** USD *(Đ3: mẫu số 0 ⇒ ⛔ là "rẻ")*. Bể dựng lại từ nguồn sống: **A 65/65 · B 70/70**, kỳ KHỚP *(sau `pip install` tay — `AG2-R1-01`)* | **ĐỎ có tên — đúng WO** |
| AC-4 | ⛔ ghi kho · ⛔ nội dung thô · khoá ⛔ lộ | Δ ghi kho = **0** *(27 → 27; mẫu số 20 bảng)*. Chạy `--that --ghi` đầy đủ bằng SDK giả + khoá `sk-ant-GIA-…`: khoá **0** lần ở stdout + **≥ 3** tệp ghi; đoạn prompt skill **0** lần; nhật ký mỗi lời gọi đúng **12** khoá. `quet_pii_repo` **0** | ĐẠT |
| AC-5 | `--duong-nen` ĐẠT · `kiem_tai_lieu` · `lint-imports` | xem bảng Cổng | ĐẠT |

## Ba chốt gọi thật *(mục 3 của phiếu)*
**9/9** ca thiếu chốt bị chặn `CamGoiThat`, SDK ⛔ được dựng, **0** lời gọi: `FLS_CHO_GOI_API` vắng · `0` · `true` · rỗng · khoá vắng · rỗng · `FLS_ZDR_DA_BAT` vắng · `0` · `true`; thêm cờ `--that` vắng; ZDR ⛔ đòi ở `che_noi_dung`. **Đột biến 10/10 bị cắn đỏ** *(bản sao `git archive`, trả nguyên, `diff -r` = 0)*: M1 ZDR · M2 cờ env · M3 `LoiApi` kéo thông điệp gốc · M4 trần USD · M5 mô hình phục vụ ≠ ghim · M6 giá Opus · M7 gửi `thinking: disabled` · M8 khoá · M9 `--that` · M10 nhật ký ghi nội dung. Vượt trần ⇒ `VuotTran`, chuỗi `DUNG` có tên, nhật ký = số lời gọi; **trần chỉ chặn lời gọi KẾ** *(`AG2-R1-03`)*.

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | ĐẠT | luật hai MÔ HÌNH A4 ≠ A1–A3; mã ghim; chốt đủ năm; tham số khớp skill. Rủi ro còn lại chỉ đo được khi có khoá *(Opus trả chữ ngoài JSON · token vào lớn · khối `thinking` đi nguyên vào lượt sau)* |
| **Dữ liệu** | ĐẠT | G0 bóng Δ = 0; bể A 65/65 · B 70/70; mọi số có mẫu số |
| **Màn hình** | không áp dụng | WO không chạm màn hình *(web 3 = 3 là đường nền)* |

## Lệnh chạy thật của `BG-356` trên container MỚI
Bước (1) `dung_be_giu_rieng.py --doc-song` **ĐỎ** `ModuleNotFoundError: google` *(`AG2-R1-01`)*; sau khi cài tay chạy được. Bước (2) `vong_that_voi.py --that --tran-usd 2` chạy được nhưng **không `--ghi` ⇒ mất nhật ký từng lời gọi** *(`AG2-R1-04`)*. `export FLS_HELDOUT_NOI_DUNG` làm `chay_agent_voi.py` gãy *(`AG2-R1-02`)*. Chạy bước (1) làm bẩn `DEM_BE.json` *(`AG2-R1-06`)*.

## Phát hiện
| F | Mức | Nơi | Gửi |
|---|---|---|---|
| `AG2-R1-01` | `NANG` | `requirements.txt` thiếu `google-auth` · `requests` | `DEV` |
| `AG2-R1-02` | `NHE` | `chay_agent_voi.py:129-134` ↔ bố cục bể `a/ b/` | `DEV` |
| `AG2-R1-03` | `NHE` | trần USD chặn lời gọi kế | `DEV` |
| `AG2-R1-04` | `NHE` | nhật ký chỉ ghi khi `--ghi` | `DEV` |
| `AG2-R1-05` | `NHE` | zip: 3 dòng Gemini ở thẻ eval | `BA` |
| `AG2-R1-06` | `NHE` | `DEM_BE.json` bị ghi lại | `DEV` |
| `AG2-R1-07` | `NHE` | ⛔ `fallbacks` — refusal ⇒ dừng | orchestrator |
| `AG2-R1-08` | `NHE` | đường Vertex *(WO-359 / `isp/AG3`)* là đường chính; chốt phải dựng lại | orchestrator |

## Bài thử mới *(`tests/nghiem_thu/`)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| `test_kq357_ag2_r1_anthropic_that.py` *(27 bài)* | 10 đột biến M1–M10 trên bản sao `git archive` — bài dev + bài mới cắn **10/10** | ✅ 27/27 |

⚠ Bài mới ⛔ nằm trong `MONG_PYTEST_TOAN_BO` của cây gộp thử; khi gộp, orchestrator nâng sàn *(= thu thập thật, cùng commit — Q8)*: 5020 → **5047**.
