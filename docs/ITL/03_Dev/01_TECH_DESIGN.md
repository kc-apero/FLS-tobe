# 01 — TECH DESIGN: kiến trúc FLS độc lập

**Version:** v1.0 · **Ngày:** 2026-08-24 · **Chủ sở hữu:** Tech Lead
**Thay thế:** v0.1 *(bản copy chương trình FIN-ERP, 2026-07-17)* — đã khai tử.

**Căn cứ:** `QĐ-ITL-45` *(FLS độc lập code + DB)* · `QĐ-ITL-46` *(đích BQ, hoãn đấu nối)* · `QĐ-ITL-38` *(PG là bản ghi, app là nơi thao tác)* · `QĐ-VOI-04` *(Cloud SQL PG + BQ; bài học **BQ không chịu OLTP 64–77s**)* · `QĐ-ITL-34` *(máy chỉ đọc file kế toán)*.

---

## §1 · ADR-FLS-01 — Vì sao độc lập

**Bối cảnh.** FLS trả lời *"mỗi đồng đã đi rồi nghĩa là gì"*. Ba hệ đang chạy quanh nó: **FPS/P100** *(duyệt–chi, `fps_*`)* · **FPA-T4** *(engine P&L trên BQ)* · **A-CCR** *(đối soát số dư, đã port vào FPA-T4)*.

**Quyết định.** FLS có **repo riêng, DB riêng, vòng đời riêng**. Không port vào `FPA-T4/apps/api` như A-CCR đã làm.

**Phương án bị loại.**

| | Phương án | Vì sao loại |
|---|---|---|
| **B** | Port vào `FPA-T4/apps/api` *(đường A-CCR)* | Được `JWT`·`RBAC`·`BQClient`·FE shell·CI miễn phí, nhưng **khoá vòng đời FLS vào nhịp release của FPA** và tạo phụ thuộc DB dùng chung. FLS là hệ **ghi**, FPA là hệ **đọc** — trộn vào nhau là trộn hai bản chất workload |
| **C** | BQ-centric *(mọi thứ trên BigQuery)* | ⛔ **đã loại từ `QĐ-VOI-04`** — *"chết ở module giao dịch"*, có số đo: **BQ không chịu OLTP, 64–77s**; free-tier **không DML**, load-job APPEND **~2–4s/lần** |

**⚠ Hệ quả chấp nhận — nói thẳng, đây là chi phí lớn nhất của kiến trúc này.**

| Phải tự dựng | A-CCR có sẵn nhờ port |
|---|---|
| AuthN/AuthZ *(JWT fail-closed + RBAC)* | ✅ dùng của FPA |
| FE shell + design tokens | ✅ `apps/web`, Layout C |
| CI/CD, môi trường, deploy | ✅ của FPA |
| Client BQ có guard dataset | ✅ `get_t2_client()` |

⇒ **Giảm nhẹ: mượn PATTERN, không mượn codebase.** `A-CCR/03_Dev/09_P3_FPA_PORT_HANDOFF.md` đã ghi sẵn khuôn router / test / loader / append-only event-log — sao chép **cách làm**, viết lại **code**.

---

## §2 · Sơ đồ khối

```
NGUỒN — CHỈ ĐỌC, không bao giờ ghi (QĐ-ITL-34)
┌──────────────┬───────────────┬──────────────┬─────────────┐
│ Google Sheets│  fps_*  (FPS) │  A-CCR (BQ)  │ P100 Log    │
│ 13 workbook  │  đọc, ko ghi  │ đọc kết quả  │ 302.259 dòng│
└──────┬───────┴───────┬───────┴──────┬───────┴──────┬──────┘
       ▼               ▼              ▼              ▼
   ┌───────────────────────────────────────────────────────┐
   │ ADAPTER A–F   →  ITL-CANON (36 cột)                   │  ⟵ toàn bộ việc khó
   │ A P100 · B Cash/Bank · C A-CCR · D HR · E Platform    │
   │ F AP/AR (gói riêng, không chặn cutover — QĐ-ITL-03)   │
   └──────────────────────────┬────────────────────────────┘
                              ▼
   ┌───────────────────────────────────────────────────────┐
   │ LỚP SỔ (mỏng): 6 chép + 1 đánh số + 5 if + 1 join     │
   │ → bảng fls_itl : 14 trường ITL-CONTRACT + 36 canonical│
   │   + lớp danh tính/truy vết + cột song song *_thật     │
   └──────────┬─────────────────────────┬──────────────────┘
              ▼                         ▼
     ┌─────────────────┐        ┌──────────────────────┐
     │ APP (kế toán)   │        │ CÔNG BỐ → BQ  ⏸ HOÃN │
     │ lưới + hàng chờ │        │ (QĐ-ITL-46)          │
     │ + nhật ký       │        └──────────────────────┘
     └─────────────────┘
```

★ **Đọc sơ đồ theo độ khó, không theo thứ tự:** hộp **ADAPTER** là toàn bộ công việc. Hộp **LỚP SỔ** là *6 phép chép + 1 phép đánh số + 5 câu `if` giống nhau + 1 phép join* — vài trăm dòng code.

⚠ Và **66% dòng phải gõ tay không phải tính chất của lớp sổ** — nó là **hệ quả của phép ghép PM ở thượng nguồn**: cột `HDCode` trống ⇒ `Classifying` rỗng ⇒ cờ `Input here` ⇒ máy gán mặc định. **Cải thiện phép ghép là đòn bẩy lớn nhất** (`QĐ-ITL-44` việc ④).

---

## §3 · Tech stack

| Lớp | Chọn | Lý do |
|---|---|---|
| BE | ~~**Python + FastAPI**~~ → ⭐ **Python + `http.server` thư viện chuẩn** | ⛔⛔ **SỬA 17/09 — đo mã đang chạy: repo ⛔ KHÔNG có FastAPI.** `fls/api/cua.py` dựng trên `ThreadingHTTPServer` của stdlib; ⛔ không một dòng `import fastapi` nào trong `fls/` *(chuỗi `fastapi` chỉ có trong `.venv`, là phụ thuộc gián tiếp của `import-linter`)*. Định tuyến đi qua **bản khai** `fls/api/bang_tuyen.py` — **37 tuyến**, mỗi tuyến khai sẵn bảng nó đọc/ghi, có cổng `soi_bang_tuyen` đối chiếu với **SQL thật**. ⭐ Hình ấy ⛔ không phải thiếu sót: nó là thứ cho phép cổng *«tuyến này chạm bảng nào»* **đo tĩnh được** — một router động ⛔ không cho phép |
| DB | **PostgreSQL** — dev **Docker $0**, prod **Cloud SQL** *(PITR bật)* | `QĐ-VOI-04`; **BQ không chịu OLTP** |
| Truy cập DB | ⭐ **Repo layer từ ngày 0** | `FLS-vs-FPS` §7 mục 2: FPS trả giá **313 call-site không abstraction** ⇒ migration 4–8 tuần rủi ro cao. SQL verbatim trong adapter, luật nghiệp vụ ở facade |
| Đọc Sheets | Sheets API + service account, **chỉ đọc**, có retry backoff | sổ nặng, hay `503`; đo thật: **4/7 khối/buổi** |
| FE | ~~React~~ → ⭐ **JS thuần, ⛔ không khung** | ⛔ **SỬA 17/09:** `fls/web/tep/` là `.js`/`.css`/`.html` viết tay *(`man_f01.js`, `goi_cua.js`, `hop_thoai.js`…)*; ⛔ không `react`, ⛔ không bước dựng. Ràng buộc đi kèm: hợp đồng `import-linter` *«`fls.web` chỉ được gọi `fls.api`»* |
| Công bố ra BQ | ⏸ **hoãn** — `QĐ-ITL-46` | |
| AuthN/Z | JWT ngắn hạn **fail-closed** + RBAC | chuẩn kế thừa từ FPA; **tự dựng** |

---

## §4 · Ranh giới module

```
fls/
  adapters/      # A–F: nguồn → ITL-CANON. Mỗi adapter một package, có version riêng
  canon/         # ITL-CANON 36 cột: schema + validate. KHÔNG import adapters
  ledger/        # lớp sổ mỏng: dựng fls_itl từ canon; sinh itl_id; 5 câu if
  contract/      # ITL-CONTRACT 14 trường — SSOT dạng DATA, không phải hằng trong code
  oracle/        # ảnh chụp đóng băng + tự soi + parity (QĐ-ITL-36/37)
  repo/          # repo layer: mọi truy cập DB đi qua đây. SQL verbatim
  api/           # cửa HTTP (stdlib `http.server`) + BANG_TUYEN 37 tuyen — mong, khong chua luat
  web/           # FE: JS thuan trong `web/tep/`, phuc vu boi `web/phuc_vu.py`
```

**Luật phụ thuộc:** mũi tên một chiều về `canon` và `contract`; **cấm import vòng**; giao tiếp chéo qua interface, **không qua bảng của nhau**. Cưỡng chế bằng `import-linter` trong CI.

⛔ **Ba luật ranh giới ngoài repo:**

| # | Luật | Nguồn |
|--:|---|---|
| 1 | **Không ghi vào bảng `fps_*`** — chỉ đọc. Chiều ghi duy nhất là FPS tự ghi | `FLS-vs-FPS` §5 |
| 2 | **Không ghi một ô nào vào file Google của kế toán** | `QĐ-ITL-34` · sự cố 13/08 |
| 3 | **Không tự tính lại phép đối soát số dư** — đọc kết quả A-CCR, dòng `226` | `QĐ-ITL-18` · `QĐ-ITL-25` |

---

## §5 · Hai thứ phải có trong thiết kế từ đầu, thêm sau là migration đau

### 5.1 · Cột song song `*_thật` — `QĐ-ITL-35`

Mỗi trường `Final` cần **hai cột**:

| Cột | Nội dung | Cổng |
|---|---|---|
| `hd`, `cdt1`, … | **y như sổ**, kể cả chỗ máy gán mặc định | ✅ parity **100% từng ô** |
| `hd_thật`, `cdt1_thật`, … | **NULL** ở chỗ máy tự bịa *(cờ `Input here`)* | ⛔ **không** vào parity — vào hàng chờ |

⚠ Bị siết bởi `AUD-12`: cột `*_thật` **chỉ** biến giá trị **máy tự bịa** thành `NULL`. **Không bao giờ** chạm giá trị người nhập — *input trong sheet là SSOT*.

### 5.2 · Oracle là một cấu phần, không phải một script — `QĐ-ITL-36/37`

`fls/oracle/` phải là code có test, không phải file tạm:

- **Ảnh chụp đóng băng** từ **FILE GỐC** `ITL Ledge`, chụp **cả đầu vào lẫn đầu ra** cùng một lần đọc, có `run_id` + ngày.
- ⛔ **Không** dùng `ITL_altered` *(sai 680 `HD` + 1.048 `CDT`)*. ⛔ **Không** dùng **bản copy** — nó **tự sản xuất giá trị mặc định** với **0 ô lỗi**, nguy hơn `#REF!`.
- **Tự soi:** kiểm `Final == f(Classifying, U)` từng dòng; dòng không tự nhất quán ⇒ **loại khỏi oracle** *(bị gõ giữa hai lần đọc)*.
- **Đọc có retry + tích luỹ**: đo thật **4/7 khối mỗi buổi**, có khối trượt **3/3 kể cả lát 1.500 dòng** ⇒ code phải **lưu tăng dần**, không để một lỗi phá cả lần đọc.

---

## §6 · Rủi ro kỹ thuật & đối sách

| Rủi ro | Đối sách |
|---|---|
| ⭐ **2–3 kế toán không dùng app** — rủi ro số một, là **hành vi** không phải kỹ thuật | `06_SCREEN_SPEC` phải liệt kê **hành vi Sheets nào bắt buộc**; thiếu một cái là họ về Sheets |
| File gốc đọc không đều *(`503`, timeout)* | đọc từng cột, **retry 3–4 lần**, **lưu tăng dần**; không kết luận từ dữ liệu một phần |
| Trôi hợp đồng 14 trường | `test_itl_contract_v1_lock.py` — khoá cả 14 vị trí, chạy mọi milestone (`INV-I07`) |
| Adapter dựng lại không khớp sổ | **`ACC-1…4`** — 4 bất biến chính xác, ⛔ **cấm viết một con số dung sai** |
| Repo layer bị bỏ qua khi gấp | `import-linter`: chỉ `fls/repo/` được import driver DB |
| Mất công người gõ khi máy ghi | máy **không có quyền ghi** lên vùng người gõ; nhật ký 7 trường `AUD-1` |
| Số trong tài liệu già đi mà không ai biết | ⭐ **mọi con số phải trỏ về code hoặc phép đo, kèm ngày** — bài học 24/08: ba lần báo số rồi phải sửa, cả ba do tin nguồn thứ cấp |

---

## Changelog
- **v1.0** (2026-08-24): Viết lại hoàn toàn cho **FLS độc lập** (`QĐ-ITL-45`). Khai tử bản copy chương trình v0.1. `ADR-FLS-01` kèm hai phương án bị loại và **chi phí thật của độc lập**. Sơ đồ khối đọc theo **độ khó** *(adapter là việc khó; lớp sổ là 6 chép + 1 đánh số + 5 `if` + 1 join)*. Chốt **repo layer từ ngày 0**, 3 luật ranh giới ngoài repo, **cột song song `*_thật`** và **oracle là cấu phần** — hai thứ thêm sau là migration đau.
