# Kiểm TO-BE (Voi FLS phase 1 v0.4.1) theo luồng AS-IS thực tế

**Ngày:** 2026-11-06 · **Đầu vào:** artifact *Voi FLS-tobe-phase1* v0.4.1 (TO-BE), sơ đồ *Voi ITL AS-IS* (52 hộp, chép ở `docs/ITL/_tools/voi_asis_goc.json`), mã FLS @ `54fff27`.
**Mục đích:** bước tiền đề của kế hoạch fleet eval: TO-BE có đi đúng luồng người đang chạy hôm nay chưa. Một agent đo trên luồng sai thì kết quả đo cũng sai.

Ký hiệu: ✅ khớp · ⚠ lệch, cần sửa TO-BE hoặc cần owner chốt · ⛔ TO-BE thiếu hẳn một bước AS-IS đang làm.
Mã trong ngoặc `[oCA]`, `[pGHEP]`… là mã hộp của sơ đồ AS-IS gốc.

---

## 0 · Một sự thật phải biết trước khi đo: bốn "agent" hôm nay là MÃ, ⛔ chưa có LLM

`grep` lời gọi mô hình (`import anthropic|openai`, `messages.create`) trong `fls/` · `tools/` · `tests/` ⇒ **0 tệp**. Chuỗi `claude` duy nhất trong mã là tên tài khoản dịch vụ Google (`claude-code-access@…`).
⇒ Agent 1, 2, 3.1–3.3, 4 trên hình là **các chặng mã tất định**. Phần duy nhất có thể dùng LLM là phần dư L3 của A3.1 (suy diễn loại giao dịch) và phần nhận diện của A3.3 (§8 của artifact). Kế hoạch fleet eval phải nói rõ nó đo **phiên bản mã** (commit) hay **phiên bản LLM**.

## 1 · Khớp (6)

| # | Bước | AS-IS | TO-BE | Ghi chú |
|---|---|---|---|---|
| 1 | Đọc sao kê | `[pGB]` GScript đọc 6 cột chuẩn của mọi sheet `R \|` | Agent 1 đọc vùng chuẩn theo bản khai (`tools/chup_sao_ke.py`) | ✅ cùng vùng chuẩn |
| 2 | Khoá ghép lệnh chi | `[pGHEP]` VLOOKUP Số CT vào `PM_Unpivot` cột Z (Reference number) | A3.1: Reference No + Σ tiền (`fls/adapters/pm_join.py`, hình A–F) | ✅ cùng khoá; TO-BE chặt hơn: không lấy dòng đầu, N×M để người |
| 3 | Soát đủ giao dịch | `[pSOAT]` số dư nhập tay CCR ↔ lũy kế Ledger 112/111 theo ngày | Agent 4: số dư đầu + Σ Nợ − Σ Có = CCR (DIF = 0) | ✅ cùng phép; TO-BE liệt kê lệch từng TK · ngày |
| 4 | Bank và quỹ cùng một luồng | `[pGQ]` → `[pCH]` → `[pGOP]` gộp 112 + 111 | Agent 1–2: lằn Bank + Cash, một canon | ✅ (lằn Cash chưa bật — đã ghi ⛔ trên hình) |
| 5 | Một bảng ITL | `[dITLF]` "ITL AGGREGATE (dòng 319) đã bị **huỷ** vì Gsheet không chịu nổi bảng lớn" | SỔ ITL HIỆU LỰC — một bảng | ✅ TO-BE làm đúng việc AS-IS bỏ dở |
| 6 | Mặc định ô trống | `[pADJ]` CDT1 = SHQ2 · ID Payee = VD0 · Hoá đơn = "Nợ hoá đơn" | `fls/ledger/final_rule.py:61–72` dựng lại đúng ba mặc định để so khớp (parity) | ✅ cho parity; ⚠ xung đột với `NFR-I05` ("không mặc định im lặng") khi chạy thật — xem #11 |

## 2 · Lệch hoặc thiếu (8) — cần sửa trước khi đóng băng phiên bản để đo

| # | Bước | AS-IS thực tế | TO-BE đang vẽ | Hệ quả cho fleet eval | Đề xuất |
|---|---|---|---|---|---|
| 7 | **Pháp nhân TK** | Pháp nhân **nằm sẵn trong tên sheet**: `R \| <số TK>_<bank> <tiền tệ>_<LE>` `[oNH]`, và `[dMM]` Mapping Master tra *tên sheet → LE* `[pGHEP]` bước [3] | k1: **máy đề xuất** pháp nhân từ TK chi + pháp nhân trả trên sổ cái PM, kế toán khai, owner ký | Đo một bước tự suy thứ AS-IS đã có sẵn; ca kiểm sẽ thiếu đáp án | ⚠ Lấy LE từ tên sheet + Mapping Master làm nguồn khai; máy đề xuất chỉ để **đối chiếu** (bắt sheet đặt tên sai) |
| 8 | **Người đè mã Ref** | Cột `Reference number_adjust` **người gõ đè** ở 58/60 nguồn bank + 7/8 quỹ; công thức: có `_adjust` thì `_adjust` thắng (`Ra-soat-Cau-truc-R-va-ERD.md:48–56`) | Ảnh đọc `Reference number` cuối; hình không có bước này (`GAP-KHAI-02`) | Mất **tín hiệu người sửa** — đúng loại tín hiệu fleet eval cần lưu (override) | ⛔ Thêm `ref_adjust` vào bản khai + ảnh; đánh dấu dòng bị đè |
| 9 | **PP (2) · khoá ghép lương** | Kế toán **dán tay** tối đa 5 giao dịch bank (số FT, TK, tiền) cho từng khoản vào dòng 4–8 sheet *No n* `[oKTL]`; H1000 Final nối về ITL bằng **VLOOKUP Số CT** `[dH1F]` | A3.2: máy khớp **Σ đợt** của một venture trong kỳ | Khoá ghép AS-IS là **số FT do người gán**, không phải Σ ⇒ đáp án có sẵn cho từng ca | ⚠ A3.2 dùng số FT người đã dán làm khoá chính; Σ chỉ để soát |
| 10 | **PP (2) · độ mịn** | Đơn vị đợt = **5 pháp nhân × 5 loại** (NIS L1 · NIS L3 · COM L2 · INT · PIT) `[dPR]`; `[pTACH]` đã tách tới **từng nhân viên** với HDCode, CDT1, pháp nhân; lương có **PE trong P100** `[oDN]` | GĐ1 chỉ gắn **LE theo venture**; KRF để GĐ2 | GĐ1 TO-BE **lùi** so với AS-IS (AS-IS đã có HD/CDT1); và lương có thể đã được A3.1 ghép qua Ref của PE lương | ⛔ Owner chốt: GĐ1 nạp thẳng H1000 (đã tách) thay vì tự khớp Σ? |
| 11 | **Ô bỏ trống ở ADJUSTED** | Kế toán gõ khi Classifying báo "Need to manual input"; ô trống nhận **mặc định** `[pADJ]` | Lớp sửa chỉ-thêm; `NFR-I05` cấm mặc định im lặng | Hai bên ra **khác số** trên mọi dòng mặc định (vd 1.642/1.642 `id_payee` = VD0) | ⚠ Owner chốt: TO-BE giữ mặc định để parity, hay hiện "chưa biết"? |
| 12 | **PP (3) · nền tảng nối vào đâu** | `[dPL]` Platform Data Ledger **"không vào ITL"**; `[oALL]` PHÂN BỔ: **map PE qua PM** bằng Combine Code (Vendor-Date-NoTrans), chia theo **CDT1**; Mapping Master dùng GI/OMC/PS/SC Ledger làm **cơ sở phân bổ** (`fls/adapters/mapping_master.py` ⓓ: 21 mã có phương pháp) | A3.3: 4 chi phí **không có trên FPS** → mapping với **bank txns** → allocate **venture** | Hai mô tả trái nhau: AS-IS nối lên **PE/PM** (tức CÓ trên FPS) và là bước **phân bổ**, TO-BE nối với **bank** ở bước nạp | ⛔ Owner chốt (đặt cạnh lời owner 04/11). Nếu theo AS-IS: venture = **CDT1** (trả lời luôn §7 câu 5) |
| 13 | **PP (3) · bốn loại** | Looker cấp GI · OMC; **SC** và PS do chủ file tự cập nhật `[oDT]`; Mapping Master có SC Ledger | TO-BE ghi OMC · GI · **Server** · PS | Một loại khác tên (SC ↔ Server); Server chưa thấy nguồn | ⚠ Hỏi: Server là SC, hay một nguồn thứ năm? |
| 14 | **Đầu ra** | `[oRPT]` Report General Ledger \| CF: **quy đổi tiền tệ**, SUMIFS theo **KRF × ngày** / Y-H-Q-M; H1000 có báo cáo riêng `[oRH]` | XUẤT báo cáo daily vào CCR theo TK · pháp nhân · ngày; chưa quy đổi | Đầu ra TO-BE khác hình với báo cáo người đang đọc | ⚠ Ghi rõ: báo cáo daily CCR **thay** hay **thêm** cạnh Report GL? Có quy đổi không? |

## 3 · Sửa nhỏ trên hình

- Sổ HR năm: AS-IS có **6 sổ** (thêm 2026), hình TO-BE ghi "4 sổ" `[dH1000]`.
- Hai lỗi dữ liệu AS-IS có thật: PIT 2025 gọi tháng 6 **hai lần**, NIS 2025 **thiếu** tháng 12 `[dH1000]`; tách lương 2025-10: No 4 (INT) lệch 567.500, No 5 (PIT) lệch ≈ 510,8 tr `[pTACH]`. Đây là nguồn **ca cài sẵn** tốt cho eval của A3.2 và Agent 4.
- Ghép hình C (N giao dịch × 1 PM line, Σ khớp — 80 mã · 394 dòng) mã đã xử lý (`pm_join.py:28`), nhưng chữ trên hình chỉ nói "Σ line = tiền dòng". AS-IS cũng có ca này: "một PMLine ứng nhiều giao dịch thì chỉ điền một mã" `[oCA]`.
- Nhịp: CA gõ Ref **sau khi chi, không giờ cố định** `[oCA]`; FLS chụp mỗi giờ ⇒ cùng một dòng có thể L3 ở lượt này, L1 ở lượt sau. Đáp án của ca kiểm phải ghi **theo ảnh nào**.

## 4 · Kết luận

TO-BE đi đúng **xương sống** của AS-IS cho PP (1): đọc vùng chuẩn → ghép Reference number → soát số dư CCR → một bảng ITL. Kế hoạch fleet eval cho Agent 1, 2, A3.1 và Agent 4 có thể dựng ngay trên đó.

**PP (2) và PP (3) chưa theo luồng thực tế** (#9, #10, #12, #13): TO-BE đang mô tả một cách làm mới, không phải cách người đang làm. Chưa nên đóng băng A3.2, A3.3 để đo cho tới khi owner chốt bốn điểm này. Nếu không, fleet eval sẽ chấm chúng theo một đáp án mà chính AS-IS không dùng.
