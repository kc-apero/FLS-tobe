# KQ-369 — biên bản kiểm `BG-368` *(R1 · `WO-367` OpenRouter + fleet eval đa mô hình)*

| | |
|---|---|
| **Thuộc** | `BG-368` · `WO-367` *(AC-7 đã bỏ → `WO-371`)* |
| **Kiểm bởi** | `fls-test` · 2026-11-27 · `isp/OR` ngọn `b219484` *(mã đo `78abf77`)* · cụm PG 16 cổng 5444 |
| **Phán quyết** | **ĐẠT CÓ ĐIỀU KIỆN** *(R1: 0 CHẶN · 5 NÊN SỬA · 4 GHI NHẬN)* — gom 5 NÊN SỬA vào MỘT vòng sửa trước R2; ⛔ ảnh hưởng gọi thật hôm nay *(chốt 0 byte giữ)* |

> Vai KIỂM: ⛔ sửa mã · ⛔ gọi API thật *(0 lời ra ngoài; chỉ `GET` công khai)* · ⛔ GCP · ⛔ khoá. Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_OR.md` v0.1 *(10 cột)*.

## Cổng
| Lệnh | Mong | Đo | |
|---|---|---|:-:|
| `--duong-nen --cong 5444` *(một lần)* | 28 = 28 · web 3 = 3 · sàn 5454/690 | **28 = 28** *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **5454** · `12 failed, 5426 passed, 2 xfailed, 14 errors` · web **3 = 3** · chạy **690** · `KẾT: ĐẠT` | ✅ |
| `lint-imports` | 11 kept | `11 kept, 0 broken` *(trong đường nền)* | ✅ |
| `git status --porcelain` sau đường nền | 0 | **0** dòng *(trước khi thêm 2 tệp của phiếu)* | ✅ |
| `kiem_tai_lieu` · `quet_pii_repo` | ĐẠT · 0 | `kiem_tai_lieu`: **546** file · 3191 bảng · 1002 ô ngày · 104 mã QĐ · `quet_pii_repo`: **0** chỗ số TK cá nhân · 0 tệp | ✅ |
| 65 bài `OR` *(36 + 10 + 19, `--collect-only`)* | xanh | 65/65 xanh trên bản sao `git archive` có `.git` | ✅ |

## Trọng tâm
1. **Hằng OpenRouter ↔ tài liệu sống** *(`GET openrouter.ai/docs/*.md`, 27/11)*: **11/11** khớp; riêng ca 402 `in_flight_budget` sai tên + ⛔ thử lại → `OR-R1-01`. `/models` **477** mô hình · `/endpoints/zdr` **953**.
2. **Chốt 0 byte**: **44/44** ca thiếu *(`--that` · `FLS_CHO_GOI_API` · `XAC_NHAN` · khoá × 3 chế độ che; giá trị `0`/`true`/` 1`/`yes`; đường khác; slug cấm)* = **0** lời; đối chứng đủ chốt **3/3** gửi. Khoá `sk-or-` ngoài `tests/` = **0** tệp *(`git grep --untracked`)*; ⛔ lộ ở `repr(adapter)`/nhật ký/thân. Lệch: `OR-R1-06`.
3. **Slug mặc định**: Opus 5.5 · Sonnet 5.5 có ở `/models` 27/11; giá **8/8** ô + canonical + ngữ cảnh khớp; 2/2 có ZDR *(bedrock · vertex)*. `google/*`: bài canh `AC3` + đột biến `M4` cắn. Fable 0 ZDR vẫn qua `--ung-vien` → `OR-R1-05`.
4. **Fleet ma trận** *(probe độc lập, máy chủ giả)*: 3 mô hình × bể → 6 lời, **thân giống nhau trừ `model`**; trần TỔNG dừng lời KẾ *(ô sau `bo_qua`/`VuotTran` có tên)*; trần MÔ HÌNH chỉ chặn ô cùng mô hình; nhãn `THẬT`/`ƯỚC`/`GIẢ` đúng nguồn; 401·402·429·503 in TÊN; chấm bằng MÃ `_cham_mu`. Lệch: 402 `in_flight` `-01`; trần quá `-07`.
5. **Biến vắng** `FLS_NHA_CUNG_CAP` ⇒ `anthropic` ✔ *(`duong_goi`, `tao_that` đòi `ANTHROPIC_API_KEY`)*; 3 đường gcp cũ: bài xanh trong đường nền.
6. **API lõi §I**: ⛔ chạy nguyên văn → `OR-R1-03`.
7. **Script chủ 09**: `read -s` + STDIN ✔ · binding mức bí mật ✔ · khoá ⛔ argv ✔; lệch `000000` → `OR-R1-02`.
8. **Đột biến**: **14** chỗ khác bảng Dev *(N1–N14)*: **4 CẮN** *(N6 N7 N8 N11)* · **10 SỐNG SÓT** → `OR-R1-04`.

## Cho vòng sửa
`OR-R1-01 … -05` *(NÊN SỬA)*, đóng bằng bài cắn đúng đột biến N1/N4/N5/N9. `-06 … -09` vào backlog.
