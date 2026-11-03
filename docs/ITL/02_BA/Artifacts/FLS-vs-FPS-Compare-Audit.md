# FLS ↔ FPS — Bảng đối chiếu & Audit Checklist

**Version:** v1.0 · **Ngày:** 2026-08-22 · **Người lập:** Claude (đối chiếu code FPS thật) · **Chủ sở hữu:** COO-CFO
**Cặp tài liệu đi kèm:** `FLS-ERD-Full-Detail.md` (v0.4) · `FLS-Process-PM-den-ITL.md` (v1.4)

**Mục đích:** ERD/Process của FLS gắn nhãn `[E]` theo **spec** `AP-FPS-v3.3.md`, nhưng spec đã có drift so với code FPS đang chạy. File này đối chiếu ERD với **code thật** (`fps/db/schema.py` — DDL BigQuery đang chạy, twin PG ở `schema_pg.py`) để: (1) sếp check nhanh chỗ nào ERD nói khác code, (2) đội FLS biết phải model theo cái gì, (3) làm căn cứ audit khi thi hành `DEV-04`.

**Nguyên tắc số 1 (quan trọng nhất file):**

> **SSOT schema phía FPS = `fps/db/schema.py` + `fps/db/schema_pg.py`, KHÔNG phải spec.**
> Mọi nhãn `[E]` trong ERD phải re-verify với code trước khi thi hành. Ô đã verify mang nhãn `[C]`.
> Đây đúng là bài học FPS đã trả giá: spec drift 5 nguồn, đã có bug thật từ việc tin spec.

---

## §1 · Định vị hai hệ

| | **FPS** (đang chạy) | **FLS** (xây mới) |
|---|---|---|
| Trả lời câu hỏi | Tiền được **duyệt và chi** thế nào (TRƯỚC khi tiền đi) | Mỗi đồng **đã đi** rồi nghĩa là gì (SAU khi tiền đi) |
| Đối tượng lõi | Chuỗi phiếu PE→PA→PI→PM→PC + phê duyệt | Sổ cái `ITL` + đối soát + phân bổ + kỳ |
| Bản V0 | Quy trình tay + CSV/Gsheet (trước 2026) | Bộ Gsheet `P100 Bank/Cash → A-CCR → Mapping → ITL Raw/Adjusted` |
| Điểm nối | `fps_pm_slip.reference_number` ↔ dòng sao kê (`STM`) | nhận `pm_line_id`/`reference_number` từ FPS, trả `ITL` cho engine FPA |
| Downstream | FLS | Engine FPA-T4 (hợp đồng 13 cột theo vị trí) |

---

## §2 · 11 phát hiện đối chiếu code (đã verify, kèm vị trí)

| # | Chủ đề | ERD/spec nói | **Code FPS thật** | Mức |
|--:|---|---|---|:--:|
| 1 | Bảng PA | `GAP-ERD-03`: chưa có bảng canonical | `fps_pa_slip` (schema.py:467) + `fps_pa_line` (:485) **đã tồn tại** | Sửa ERD ✅ |
| 2 | `reference_number` | Ở PM **Line**, phải thêm vào canonical + UNIQUE + 1–1 STM (`QĐ-ITL-09`) | **Đã có**, ở **`fps_pm_slip` (SLIP)** — schema.py:579. BQ không enforce UNIQUE | ⚠ **NẶNG NHẤT** — xem §3 |
| 3 | `bank_account_id` | C14 chờ chốt: slip hay line | `fps_pm_slip.bank_account_id` — **SLIP** | Đóng C14 ✅ |
| 4 | Service dates | `PEL.service_start/end_date` — "cửa sổ dịch vụ ở PE Line" | Ở **`fps_pe_slip`** (SLIP); `fps_pe_line` **không có**. PI slip + PM slip cũng có ở slip | Sửa nguồn `SVC` ⚠ |
| 5 | Country | `CTY` toàn `???`, `GAP-ERD-13` FK không resolve | **`fps_cty(cty_code, cty_name)` đã có** + đã chuẩn hoá ISO (`Vietnam→VN`, `USA→US`, rỗng→NULL) | Đóng phần lớn ✅ |
| 6 | Tỷ giá | `FXR` là bảng mới | **`fps_exchange_rate(currency_from, currency_to, rate, effective_date)` đã có** | Align, đừng tạo trùng |
| 7 | PA scope | W9: "PA chỉ cho AdvancePayment" | PA **auto-create cho MỌI transaction type** (spec dòng 970 xác nhận SAI từ Step 10, rule đã lock) | Sửa ERD ⚠ |
| 8 | PC scope | "PC chỉ cho Tạm ứng (BT & Gấp)" | PC **auto-create cả TT/THU** khi PM M1 Approved (`Approved`, chain-audit-only); manual PC11→PC13 chỉ TUBT/TUG | Sửa ERD ⚠ |
| 9 | Reject | Cảnh báo `WHERE != 'Rejected'` ở 5 view | Filter **có thật** (`ledger_service.py`, cascade `pe.status`); reject semantics = **zero-line → Draft** (amount=0, row GIỮ) | Củng cố `QĐ-ITL-11` |
| 10 | Threshold | `THR` FPS_ApprovalThreshold `[E]` §1.33 | **Không có bảng threshold** — SSOT = `fps_szt` (lock Step 5.D 2026-05-24), logic tier ở `approval_plan.py` | ⚠ `GAP-ERD-23` |
| 11 | `TSI_MAP` | Bảng 13 cột `[E]` §10.2 | **Không có trong DDL** schema.py — xác minh view/computed | ⚠ `GAP-ERD-24` |

---

## §3 · Chủ đề lặp lại: **Slip vs Line** — chỗ dễ sai nhất khi nối 2 hệ

FPS giữ khá nhiều trường ở mức **Slip** trong khi ERD/luồng V0 giả định mức **Line**:

| Trường | ERD giả định | Code FPS | Rủi ro nếu không chốt |
|---|:--:|:--:|---|
| `reference_number` | Line | **Slip** | Luật `OP-03` "1 PMLine ↔ 1 ref" không dựng được: 1 PM Slip nhiều Line chỉ có 1 ref ⇒ ghép sao kê→line phải chia tiền theo tỷ lệ hoặc CR thêm cột line |
| `bank_account_id` | line (§12) / slip (§4) | **Slip** | Suy `le_owner` từ tài khoản phải đi từ slip |
| `service_start/end_date` | PE **Line** | **PE/PI/PM Slip** | `SVC` + `GAP-ERD-11/14` (khớp kỳ PE-vs-PI) phải xét ở slip; sai tầng = sai kỳ ghi nhận |
| `cdt_code` | — | **Slip canonical** (`fps_pe_slip.cdt_code`; line chỉ giữ `bgc_code`/`kr_code` denorm) | Trục CDT1 của ITL lấy từ slip |

**Cấu trúc line thật trong code** (để đội FLS khỏi đoán): `fps_pe_line(line_id, pe_id, tsi_id, bgc_code, kr_code, amount, pe_date, note, attachments)` · `fps_pm_line(line_id, pm_id, pi_line_id, tsi_id, amount, pm_date, note, attachments)`. Line = số tiền + khoá chain; phần mô tả/ngân hàng/kỳ dịch vụ nằm ở slip.

---

## §4 · Map entity ERD ↔ bảng FPS thật (39 bảng trong `schema.py`)

**Nhóm A — ERD có, code có (map thẳng, nạp cột từ code):**

| ERD | Bảng code | Ghi chú |
|---|---|---|
| `CTY` | `fps_cty` | ERD tưởng chưa có — ĐÃ CÓ + ISO hoá |
| `LE` | `fps_le` | Code: `le_code, le_name, country, representative, is_active`. Cột ERD thêm (`is_entity`, `accr_code`) = CR mới |
| `VEN` | `fps_ven` | 5 cột `[A]` của ERD (`block_code, settlement_currency, payment_channel, payoneer_email, profitshare_active`) code CHƯA có = CR mới |
| `CDT` | `fps_cdt` | |
| `KR / PT / BGC` | `fps_kr / fps_pt / fps_bgc` | `BGC.parent_budget_code + level` = CR mới |
| `TMT / TLT / TUT / SZT` | `fps_tmt / tlt / tut / szt` | ⚠ `fps_szt` kiêm **threshold SSOT** |
| `EGR / EMP` | `fps_egr / fps_emp` | |
| `TSI / TSEV / TRT / TRI / TST` | `fps_tsi / fps_tev / fps_trt / fps_tri / fps_tst` | TSEV tên code = `fps_tev` |
| `TDT / TDI` | `fps_tdt / fps_tdi` | |
| `RTBSheet / RTBItem` | `fps_rtb_sheet / fps_rtb_item` | |
| `P110 / P130` | `fps_bank_account / fps_contract` | Cột ERD thêm ở P110 (`bank_sheet, range_*, opening_balance`) = CR mới |
| PE/PA/PI/PM/PC ×(Slip+Line) | `fps_pe/pa/pi/pm/pc_slip` + `_line` | Đủ 10 bảng — xem §3 slip-vs-line |
| `FXR` | `fps_exchange_rate` | ERD tưởng bảng mới |

**Nhóm B — ERD có, code KHÔNG có (spec-only, phải quyết):**

| ERD | Tình trạng | Quyết |
|---|---|---|
| `THR` | Bị code thay bằng `fps_szt` + `approval_plan.py` | `GAP-ERD-23` |
| `TSI_MAP` | Không trong DDL | `GAP-ERD-24` — xác minh view/computed |
| `Month` | Code không có bảng Month | Thuận lợi cho `GAP-ERD-22` (khai tử, thay `PRD`) |

**Nhóm C — Code có, ERD chưa dùng (cân nhắc cho FLS):**

| Bảng code | Vai | Vì sao FLS nên quan tâm |
|---|---|---|
| `fps_p140_org` | SSOT hierarchy tổ chức (SCD2, import-only) | Trục CDT/routing **theo thời điểm** — đúng bài toán "frozen-at-decision-time" mà FLS cần khi giải nghĩa dòng tiền quá khứ |
| `fps_approval_history` | Audit trail phê duyệt | Bổ sung `TSEV` khi FLS cần "ai duyệt lúc nào" |
| `fps_raw_upload` | Staging import | Tương đồng vai `STM` — tái dùng pattern validate schema-driven |
| `fps_id_counter` | Sinh ID atomic | Know-how chống trùng ID (đã fix bug dup thật) — áp cho `itl_id` |
| `fps_session` | Auth session | Không liên quan FLS data model |

**Nhóm D — FLS thuần mới (không có counterpart FPS, đúng là phần giá trị của FLS):** `ITL LGT STM ADJ ADT SVC PRD MSL ALR DRV ALC CSH RCN CNT ICO COA MAP VBK SRC RUN CHG ISS PSR PSS PST` + view `RPT_CommittedVsActual`.

---

## §5 · Change Requests FLS → FPS (gom BATCH, làm SAU khi Step 12.5 đóng)

FPS đang giữa migration BigQuery→PostgreSQL (Step 12.5, dualpg live). **Mọi schema change phải đi qua kỷ luật: sửa `schema.py` + `schema_pg.py` + parity test + migration script + rollback plan — không ALTER tay, không nhỏ giọt.** Danh sách CR tích luỹ từ 2 tài liệu FLS:

| # | CR | Nguồn | Ưu tiên đề xuất |
|--:|---|---|:--:|
| 1 | `reference_number` mức **line** (hoặc chốt nghiệp vụ ghép ở slip) | `QĐ-ITL-09` + §3 | **P1 — chốt TRƯỚC khi thiết kế mapping FLS** |
| 2 | `fps_ven` +5 cột (`block_code, settlement_currency, payment_channel, payoneer_email, profitshare_active`) + bảng `VBK` | ERD §1 | P2 |
| 3 | `fps_le` + `is_entity`, `accr_code` | ERD §1 (INV-I10) | P2 |
| 4 | `fps_bgc` + `parent_budget_code`, `level` (cây HD 3 cấp) | ERD §1 | P2 |
| 5 | `TSEV` + event `Delete`, `Reverse` | `GAP-ERD-09` (xoá đang xảy ra thật, 1.015 dòng) | P2 |
| 6 | `PEL.contract_id` nullable FK (đối soát chi vượt hợp đồng) | `GAP-ERD-18` | P3 |
| 7 | `fps_bank_account` + `bank_sheet`, `range_*`, `opening_balance` | ERD §4 | P3 |
| 8 | UNIQUE `reference_number` (PG constraint + app-layer check BQ) | `QĐ-ITL-09` | đi kèm #1 |

> **Luật vận hành:** CR nào cũng cần evidence vào ledger trước + sếp ký rồi mới làm (pattern §9.1 của FPS). FLS **không** được tự viết vào bảng `fps_*` — chỉ đọc; chiều ghi duy nhất là FPS tự ghi.

---

## §6 · Spec-drift FPS đã chốt mà FLS PHẢI kế thừa đúng (đừng học lại từ spec)

| Rule đã lock phía FPS | Nội dung | FLS ảnh hưởng |
|---|---|---|
| PA AUTO | PA auto-create cho **MỌI** transaction type (AP v3 dòng 970 sai) | ITL lường PA ở mọi chain |
| PC auto/manual | TT/THU: PC auto `Approved` audit-only · TUBT/TUG: manual PC11→PC13 | Đọc PC phân biệt auto/manual |
| Reject semantics | Reject = **zero-line → Draft** (amount=0, row giữ, AH xoá) | Dòng rejected ≠ dòng có tiền; tiền thật vẫn đọc từ sao kê |
| `ControlApprover` | Canonical (UI "Kiểm soát"); `LegalApprover` = legacy alias; cột `*_legal` còn dual-write | FLS đọc approval data dùng cột `*_control` |
| Chain ID V4 | `PE000001-E1 → PA…-A1 → PI…-I1 → PM…-M1 → PC…-C1` | Khoá drill-through của ITL |
| R7 | `Slip.amount = ΣLines` áp PI/PM/PC — **PE exempt** | Phép kiểm tổng tiền khi FLS đối soát |
| Slip vs Line | Slip chỉ khai báo ở PE; PA→PC theo Line-level (PELine-first) | Trục drill của `TSI_MAP`/ITL |
| Threshold | SSOT = `fps_szt` + `approval_plan.py` (SSOT display↔gate) | Thay cho `THR` spec |

---

## §7 · Bài học xây FPS → áp cho FLS v1 (know-how chuyển giao)

1. **Khảo sát V0 trước, giữ nguyên lý — thay chỗ thực thi.** 2 file FLS đã làm đúng (như FPS làm với quy trình tay). Nguyên lý đối soát 2 nguồn + 1 dòng hiệu số của kế toán là ĐÚNG — chỉ bỏ 644 cột công thức tay (`QĐ-ITL-21`).
2. **Repo layer từ ngày 0.** FPS trả giá 313 call-site không có abstraction → migration 4-8 tuần rủi ro cao. FLS: mọi data access qua repo layer ngay từ v1, SQL verbatim trong adapter, domain rules ở facade.
3. **Cổng là điều kiện CHẶN, không phải con số để xem.** V0 có `DIF` nhưng không chặn (đang đỏ −9,53 tỷ mà giai đoạn sau vẫn chạy). FPS know-how: CI allowlist đỏ = dừng; fail-fast pair guard. FLS: `DIF = 0` + `INV-I06` phải là gate chặn pipeline.
4. **Mặc định im lặng = bug.** V0 gán 6.843 giá trị mặc định im lặng (`Headquarters2`, `VD0`). FPS know-how tương ứng: error text 100% từ BE, không silent-skip (bug J-LEGACY-SKIP). FLS: trạng thái `UNMAPPED`/`rejected` tường minh (`QĐ-ITL-19`).
5. **Khoá phải bền + sinh atomic.** `itl_id` V0 = số thứ tự dòng sau SORT (nhập lùi ngày = đánh số lại). FPS từng có bug dup line_id thật → fix bằng `fps_id_counter` atomic. FLS: `natural_key` UNIQUE + surrogate sinh atomic.
6. **Parity test cho mọi cặp twin.** FPS: BQ↔PG twin repo + parity test là contract. FLS: hợp đồng 13 cột theo VỊ TRÍ với engine FPA (`POS-13`) phải có test khoá vị trí chạy mọi milestone (`INV-I07`).
7. **Reconcile mỗi phiên + evidence trước khi ký.** FPS: reconcile 16/16 mỗi phiên dualpg; run-id chỉ ghi sau khi CI `success`. FLS: `RCN` + `RUN` log đúng vai này — giữ kỷ luật.
8. **Sổ đăng ký nguồn phải sống.** V0 `SRC` đang hỏng (288 ô `#REF!`), 278 cạnh IMPORTRANGE động đổi im lặng. FLS: `SRC`/`RUN` có versioned contract, đổi nguồn = event có log.
9. **Câu hỏi nghiệp vụ đi trước thiết kế.** `GAP-ITL-31` (vì sao DIF lệch −9,53 tỷ) và `GAP-ITL-29` (4.940 dòng tiền RA không lệnh) phải có câu trả lời của kế toán TRƯỚC khi chốt data model mapping — giống FPS phỏng vấn sếp trước mỗi SPEC.

---

## §8 · Checklist audit cho sếp (10 câu hỏi soát nhanh đội FLS)

| # | Câu hỏi | Đạt khi |
|--:|---|---|
| 1 | Nhãn `[E]` nào đã re-verify với `schema.py`? | Mọi entity nhóm A §4 có nhãn `[C]` trước `DEV-04` |
| 2 | `reference_number` chốt slip hay line? | Có quyết định ghi thành `QĐ-*`, kèm cách chia tiền slip→line nếu giữ slip |
| 3 | `DIF = 0` có chặn pipeline không? | Là gate chặn tự động, không phải dashboard |
| 4 | −9,53 tỷ lệch từ 20/08 đã có lời giải chưa? | Kế toán trả lời `GAP-ITL-31` bằng văn bản |
| 5 | 4.940 dòng tiền RA không lệnh — phân loại xong chưa? | `GAP-ITL-29` có bảng phân loại nguyên nhân |
| 6 | `itl_id` mới có bền không? | Nhập lùi ngày KHÔNG đổi id dòng cũ (test được) |
| 7 | Mặc định im lặng đã bỏ chưa? | Không còn `Input here`→giá trị giả; có báo cáo tồn `UNMAPPED` |
| 8 | Cổng kiểm cột `Final` + phần gõ tay? | `AUD-2` có cơ chế, không chỉ so `Classifying` |
| 9 | CR sang FPS có đi đúng kỷ luật không? | Batch sau 12.5, twin schema + parity + sếp ký (§5) |
| 10 | FLS có ghi vào bảng `fps_*` không? | KHÔNG — chỉ đọc; mọi bổ sung dữ liệu đi qua FPS |

---

## Changelog
- **v1.0** (2026-08-22): Khởi tạo. Đối chiếu ERD v0.3→v0.4 với `fps/db/schema.py` (39 bảng): 11 phát hiện §2, chủ đề slip-vs-line §3, map entity 4 nhóm §4, 8 CR gom batch §5, 8 rule kế thừa §6, 9 bài học chuyển giao §7, checklist audit 10 câu §8.
