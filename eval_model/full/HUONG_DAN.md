# Hướng dẫn chạy test full luồng (4 agent trong 1 lượt) cho từng model

## 1. Gửi gì cho model, giấu gì

| Gửi cho model ✅ | ⛔ KHÔNG gửi (chứa đáp án) |
|---|---|
| `prompt/system.md` → ô **system prompt** | `dap_an/` |
| `prompt/user.md` → tin nhắn **user** | `FLS_dataset_DAP_AN.xlsx` |
| hoặc `prompt/prompt_mot_tep.md` (gộp cả hai) nếu giao diện không có ô system | `kiem_cham/`, `ket_qua_cham/` |

`input/` và `FLS_dataset_INPUT.xlsx` chỉ là bản để người đọc; nội dung đã nằm sẵn trong `prompt/user.md`.

Nếu model chạy dưới dạng agent có quyền đọc file hoặc repo, hãy **xoá `dap_an/`, `kiem_cham/` và `FLS_dataset_DAP_AN.xlsx` khỏi workspace của nó** trước khi chạy.

## 2. Cấu hình gợi ý (giữ giống nhau giữa các model)

| Model | Cấu hình |
|---|---|
| Claude Opus 5.5 / Opus 5 | effort `medium`, `max_tokens` ≥ 64000 (dùng streaming), không bật fallback sang model khác |
| Gemini 3.8 Flash / 3.1 Pro | thinking mức medium (hoặc tương đương), max output tối đa cho phép |

Nếu model có công cụ chạy code, ghi lại là **bật hay tắt** cho từng lần chạy: kết quả của hai chế độ này khác nhau, không nên trộn trong cùng một bảng.

## 3. Lưu kết quả

Lưu **nguyên văn** câu trả lời của mỗi lần chạy vào `ket_qua_tho/<ten_model>_<lan>.md`, ví dụ `ket_qua_tho/opus55_1.md`. Nếu lấy được, ghi kèm số token vào/ra và thời gian chạy (để đối chiếu bảng chi phí).

Gợi ý: chạy mỗi model **3 lần** để thấy độ dao động.

## 4. Chấm

```bash
cd eval_model/full
python cham_full.py ket_qua_tho/*.md
```

Lệnh in bảng so sánh 9 khối. Mỗi ô có **% điểm** và **[số ô lệch tuyệt đối]**; chỉ 0 lệch mới tính là đạt. Chi tiết từng ô lệch ghi ở `ket_qua_cham/<ten>.json`. Gửi lại các file `.md` thô (hoặc `.json`) để làm báo cáo.

## 5. Bộ dữ liệu (kỳ 01–07/10/2026, toàn bộ là dữ liệu bịa)

| Họ | Số dòng | Bẫy chính cài vào |
|---|---|---|
| Bank / quỹ (4 sheet) | 112 dòng thô → 109 dòng ledger | S2 đảo vị trí cột, S3 thêm cột; 2 dòng số tiền 0; 1 dòng trùng; 3 dòng có `_adjust` thắng; mã viết sai dạng; mã số khoa học |
| Phiếu chi PE → PI → PM | PE 79 · PI 48 · PM 79 | Hình A 68 · B 9 (tách dòng, lệch 600 VND) · C 1 (trả 2 lần) · D 1 · E 1 · F 1 · KHONG_GHEP 10; 1 HD không có trong Mapping Master |
| H1000 (lương) | 12 dòng / 3 đợt chi | Tách 1 dòng bank thành nhiều dòng HD × CDT1 |
| PLT (GI/OMC/SC/PS) | 14 dòng / 5 Combine Code | Tiền vào/ra USD và VND, tách theo CDT1 |

Đáp án gồm 129 dòng ITL (7 khối + ALLOCATE), 7 dòng hàng chờ, R1 / R2 / R3 cho 7 ngày, và 6 lỗi Auditor: 1 DIF do CCR gõ nhầm, 1 dòng TRUNG, 1 HD_LA, 3 GHEP_LECH.

## 6. Sinh lại (nếu cần bộ khác)

```bash
python sinh_full.py <seed> && python tao_prompt.py && python kiem_bo_cham.py && python xuat_xlsx.py
```

`kiem_bo_cham.py` bắt buộc phải in `OK`. Lệnh này chứng minh đáp án được chấm 100% và bộ chấm bắt được từng chỗ cố tình làm hỏng.
