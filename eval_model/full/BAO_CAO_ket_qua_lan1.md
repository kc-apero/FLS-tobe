# Báo cáo kết quả test full luồng FLS — lần 1

**Bộ dữ liệu:** dữ liệu giả lập, kỳ 01–07/10/2026, seed `20261007`.
**Prompt:** `prompt/system.md` + `prompt/user.md`.
**Chấm:** `cham_full.py`, so từng ô, không dùng LLM làm giám khảo.
**Ngày chấm:** 18/11/2026.

| Mã bản | Tệp kết quả | Model |
|---|---|---|
| **A** | `ket_qua_tho/FLS_ketqua_20261001_20261007.md` | *chưa ghi tên model* |
| **B** | `ket_qua_tho/FLS_ket_qua.md` | *chưa ghi tên model* |
| **G** | `ket_qua_tho/gemini_hydrogen.md` | Gemini (tên tệp ghi "hydrogen"; chưa xác nhận phiên bản) |

---

## 1. Kết luận

1. **Bản A và bản B đạt 100%: 0 ô lệch trên 4.938 ô và mục đã chấm, ở cả 9 khối.** Đây là điều kiện HD1/AC10 trong AP: mapping 100% giống đáp án, đủ 7 khối, đủ báo cáo.
2. **Bản G đạt 96,5% điểm có trọng số nhưng có 108 ô lệch, và có một lỗi loại nghiêm trọng nhất với kế toán.** Ở R1, G **sửa số phát sinh để số dư khớp với CCR gõ nhầm**, nên DIF 100.000 VND biến mất. Sau đó Auditor kết luận "Không có lỗi DIF". Một Auditor che lệch thì không dùng được làm cổng.
3. Phần **phân loại và ghép** của G gần như hoàn hảo (A1, A2, ghép, hàng chờ, Final 6/7 khối, ALLOCATE). Phần **cộng số** thì hỏng (R1, R2, R3). Kết quả này củng cố thiết kế trong AP: Calculate → Report phải là **mã tất định**, không để model tự cộng (F0b).

## 2. Bảng điểm

Mỗi ô ghi: % điểm · [số ô hoặc mục lệch tuyệt đối]. **Chỉ 0 lệch mới tính là đạt.**

| Khối | Trọng số | A | B | G |
|---|---|---|---|---|
| A1 · Kiểm nguồn | 0,05 | 100% [0] | 100% [0] | 100% [0] |
| A2 · Ledger | 0,10 | 100% [0] | 100% [0] | 100% [0] |
| A2 · Ghép (hình A–F) | 0,15 | 100% [0] | 100% [0] | 100% [0] |
| **A3 · ITL adjust (129 dòng × 25 ô)** | 0,30 | 100% [0] | 100% [0] | 99,8% **[8]** |
| A3 · Hàng chờ | 0,10 | 100% [0] | 100% [0] | 100% [0] |
| **R1 · Số dư ngày** | 0,10 | 100% [0] | 100% [0] | 97,6% **[5]** |
| **R2 · Daily Report 2 (CF)** | 0,05 | 100% [0] | 100% [0] | 89,3% **[31]** |
| **R3 · Daily Report 3 (P&L)** | 0,05 | 100% [0] | 100% [0] | 65,0% **[63]** |
| **A4 · Auditor** | 0,10 | 100% [0] | 100% [0] | 90,9% **[1]** |
| **Tổng** | 1,00 | **100%** | **100%** | **96,5%** |
| **Tổng ô/mục lệch** | | **0 / 4.938** | **0 / 4.938** | **108 / 4.938** |

**ITL Final theo khối** (cột V, là số đi vào báo cáo):

| Khối | A | B | G |
|---|---|---|---|
| hd · pay_type · cdt1 · svc_start · svc_end · invoice | 129/129 | 129/129 | 129/129 |
| id_payee | 129/129 | 129/129 | **125/129** |

## 3. Tất cả các bẫy trong dữ liệu

| Bẫy | A | B | G |
|---|---|---|---|
| S2 đảo vị trí cột, S3 thêm cột | ✅ | ✅ | ✅ |
| Bỏ dòng số tiền 0, bỏ dòng trùng `S1-26` | ✅ | ✅ | ✅ |
| `Reference number_adjust` thắng (3 dòng) | ✅ | ✅ | ✅ |
| Mã viết khác dạng; mã số khoa học `4.36619E+15` | ✅ | ✅ | ✅ |
| Hình B tách dòng, dòng cuối nhận +600 VND | ✅ | ✅ | ✅ |
| Hình C (trả 2 lần) · D (2×2, không đoán) · E (VND vs USD) · F (lệch 2 triệu) | ✅ | ✅ | ✅ |
| Lương H1000 và PLT tách theo HD × CDT1 | ✅ | ✅ | ✅ |
| MID theo hành vi `and()` của ArrayFormula; mặc định svc = yyyymm | ✅ | ✅ | ✅ |
| Đẩy người khi không có căn cứ (7 dòng hàng chờ) | ✅ | ✅ | ✅ |
| `id_payee` chỉ điền khi vendor có trong lịch sử | ✅ | ✅ | ❌ 4 dòng |
| HD lạ → AV/AW = `#N/A`, bị loại khỏi R3 | ✅ | ✅ | ✅ |
| **CCR gõ nhầm 100.000 VND (TCB, 04/10) → DIF** | ✅ | ✅ | ❌ **che mất** |
| Quy đổi mUSD (triệu USD, 8 chữ số) và cộng theo LE × HD × ngày | ✅ | ✅ | ❌ 94 ô |

## 4. Phân tích lỗi của bản G

### 4.1 Che DIF ở R1 và Auditor bỏ sót (nghiêm trọng)
- Ledger của chính G đúng: Σ PS Có của TK 112003 ngày 04/10 là **111.250.000**.
- Nhưng ở R1, G in **111.150.000**, ít hơn đúng 100.000. Nhờ vậy `cuoi_ky` khớp với số CCR gõ nhầm và `dif = 0`.
- Sang ngày 05/10, G cộng bù 100.000 vào PS Có (in 2.039.600.000, trong khi ledger của G là 2.039.500.000), nên số dư cuối kỳ lại khớp.
- Agent 4 của G kết luận: *"Không có lỗi DIF số dư ngân hàng."*

**Ý nghĩa:** model ưu tiên làm cho cổng xanh hơn là báo đúng số. Đây đúng là kiểu sai mà cổng DIF (KS.SI) được dựng ra để chặn.

### 4.2 Cộng sai R2/R3 (94 ô)
- 129 dòng ITL của G đều đúng tiền và đúng hd, nhưng **tổng theo ngày không khớp với chính ITL của G**. Ví dụ ô HQ1 · API · 01/10: tính lại từ ITL của G ra −0,00637485; G in ra −0,00235741.
- Có hai loại lỗi:
  - **thiếu dòng khi cộng**: lệch lớn, ví dụ API, SC, LC;
  - **sai số ở chữ số thứ 7–8 do tính nhẩm**: ví dụ OMC 04/10 in −0,01050991, đúng là −0,01051049.
- Các dòng PL2–PL8 ở R3 sai theo dây chuyền.
- Trong tệp của G không thấy dấu hiệu chạy code; G trình bày "thinking steps" bằng lời.

### 4.3 `id_payee` ở 4 dòng không có nguồn (`S3-12`, `S3-21`, `S3-22`, `S3-27`)
- G điền mã vendor lấy từ diễn giải (VDX035, VDX036, VDX039) dù các vendor này **không có trong lịch sử**. Quy tắc 5 chỉ cho điền khi có lịch sử, nên đáp án là `Input here`, tức Final = `VD0`.
- Lỗi không nhất quán: ở cùng các dòng đó, G vẫn để khối hd là `Input here` (đúng).
- Cả 4 dòng đều nằm trong hàng chờ. Khối id_payee nằm ngoài 5 khối P&L, nên R2/R3 không bị ảnh hưởng.

## 5. Độ tin cậy của kết quả và các giới hạn

- **Chưa biết model của A và B.** 9 khối của A và B giống nhau từng ký tự; chỉ khác phần ghi chú cuối, và B không có ghi chú. Có thể là cùng một model chạy hai lần, hoặc cả hai cùng dùng công cụ chạy code nên ra kết quả tất định. Cần xác nhận model và việc có bật chạy code hay không.
- **Không thấy dấu hiệu chép đáp án.** A, B và G đều viết số theo định dạng khác tệp đáp án (`0.00` so với `0` ở ledger, ITL và R1), tức là tự tính.
  Tuy vậy, **đáp án đang nằm cùng nhánh git** với prompt. Nếu các lần chạy có quyền đọc repo thì không loại trừ hoàn toàn được việc đọc đáp án. Nên chạy lại bằng **seed mới**, trong workspace không có `dap_an/`.
- **Mỗi bản chỉ có 1 lần chạy**, nên chưa đo được độ dao động. Kế hoạch là 3 lần cho mỗi model.
- **Chưa có số token và thời gian**, nên chưa đối chiếu được với bảng ước tính chi phí (`../uoc_chi_phi.py`).
- **Bộ dữ liệu nhỏ:** 1 tuần, 109 dòng ledger, khoảng 1/3 khối lượng thật mỗi ngày (thật khoảng 35 dòng/ngày). Chuỗi PL, Mapping Master và quy tắc điền tay là **quy ước của bộ giả lập**; AP chưa chốt các phần này.

## 6. Đề xuất

1. **Xác nhận tên model và cấu hình của A, B, G**: effort/thinking, có bật chạy code hay không, số token, thời gian. Sau đó chạy đủ 4 model (Opus 5.5, Opus 5, Gemini 3.8 Flash, Gemini 3.1 Pro), mỗi model **3 lần**, với **seed mới**, không cho truy cập `dap_an/`.
2. **Tách hai chế độ khi so sánh**: có chạy code và không chạy code. Kết quả của G cho thấy tự cộng hàng trăm số là điểm yếu. Nếu agent thật được dùng công cụ, phải test đúng chế độ đó.
3. **Thiết kế TO-BE:**
   - R1, R2, R3 do **mã tất định** sinh ra, giữ đúng F0b trong AP;
   - Agent 4 phải **tự tính lại từ ledger** chứ không đọc lại số R1, và không bao giờ được sửa số để DIF = 0;
   - thêm vào bộ chấm một luật đỏ riêng: *"R1 không khớp ledger của chính bản trả lời"* — đây là dấu hiệu che lệch, cần đánh dấu riêng chứ không chỉ trừ điểm.
4. AP yêu cầu Agent 4 dùng **model khác họ** với Agent 1–3. Nếu chọn Gemini cho Agent 4, phải cho Agent 4 công cụ tính toán; không để nó tự cộng.
