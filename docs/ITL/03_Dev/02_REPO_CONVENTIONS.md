# 02 — REPO CONVENTIONS: FLS

**Version:** v1.2 · **Ngày:** 2026-10-02 · **Chủ sở hữu:** Tech Lead
**Thay thế:** v0.2 *(bản copy chương trình, phương án `voi/`)* — đã khai tử.

**Căn cứ:** `QĐ-ITL-45` *(FLS repo riêng)* · `01_TECH_DESIGN` §4 · ⭐ **`QĐ-ITL-133`** *(owner 17/09 — quy ước theo MÃ)*.

---

## §1 · Repo — ĐÃ CHỐT (`QĐ-ITL-45`)

**Repo mới `FLS`, độc lập**, ngang hàng `FPA-T4` · `P100-R` trong `C:\Users\0_Apero Project\`.

| Điều | Chốt |
|---|---|
| Tên module gốc | `fls/` — không dùng prefix `fps_`/`voi_` |
| Với FPS/P100 | **vendor CHỈ ĐỌC** — không import code, không share bảng; đọc qua adapter |
| Với FPA | ghép bằng **`ITL-CONTRACT`**, không share codebase |
| CI | **dựng mới từ ngày đầu**, không kế thừa CI của FPS/FPA |
| DB | schema `fls_*` riêng; dữ liệu nguồn cần thì **đọc**, không migrate bảng chéo repo |
| Mượn của A-CCR | **PATTERN** *(router / test / loader / event-log append-only)*, **không** codebase |

---

## §2 · Quy ước cố định

- **Cấu trúc module** theo `01` §4 — ⛔⛔ **SỬA 17/09 (owner chốt: *quy ước theo MÃ*).** ~~*«mỗi module: `router.py / service.py / repo.py / models.py / schemas.py / tests/`»*~~ — đo được: ⛔ **0 tệp** nào trong `fls/` mang một trong năm tên ấy. Khuôn đó tả một kiến trúc `FastAPI` **chưa bao giờ được dựng**.
  ⭐ **Khuôn THẬT — theo VIỆC, ⛔ không theo tầng khung:** `adapters/` *(nguồn → canon)* · `canon/` *(khuôn + kiểm)* · `ledger/` *(dựng dòng sổ)* · `contract/` *(hợp đồng ra, dạng DATA)* · `repo/` *(chỗ DUY NHẤT chạm DB)* · `api/` *(cửa HTTP + bản khai `BANG_TUYEN`)* · `web/` *(JS thuần)* · `oracle/` · `kiem/` · `xuat/` · `db/`. ⛔ Tên tệp theo **việc nó làm** *(`chay_nap.py` · `khai_cot.py` · `nap_lo.py`)*, ⛔ không theo vai kỹ thuật.
- **Naming:** Python `snake_case`; API `kebab-case` theo `BA-07`.
  ⛔⛔ **SỬA 17/09 — `R-A2` CHỈ áp cho TÀI LIỆU, ⛔ KHÔNG cho tên bảng PostgreSQL.** Câu cũ ~~*«tên **bảng**/trường nguyên văn theo `BA-05`, kể cả lỗi chính tả nguồn»*~~ đọc theo mặt chữ thì **bắt** đặt tên bảng là `fls_itl_ledge` — vì tab thật tên `ITL Ledge`, **thiếu chữ `r`**. ⭐ Luật đúng: **tài liệu chép nguyên văn** *(kể cả `ENITY`, `filetring`, `(yyyymm`)*; **kho đặt tên SẠCH** — bê một lỗi chính tả vào tên bảng là cho nó sống mãi trong mọi câu `SQL`. Câu nối ba cách gọi ở **`BA-05` §TỪ ĐIỂN THỰC THỂ**, cổng `tests/test_tu_dien_thuc_the.py`.
  ⚠ **Trần độ dài là MỤC TIÊU, ⛔ không phải luật** *(đo 17/09: **17/75** tệp `fls/` vượt 300 dòng, cao nhất `api/nap_cua.py` **1.110** = `3,7×`)*. ⛔ Giữ *“≤ 300 dòng”* làm luật thì nó **bị vi phạm 17 lần mà ⛔ không ai đỏ** — một luật ⛔ không ai cưỡng chế làm hỏng uy tín của cả bản quy ước. ⇒ Phát biểu lại: **hàm ≤ 40 dòng** giữ làm mục tiêu; tệp vượt **500** dòng thì phải **giải thích được vì sao ⛔ không tách** *(thường là: tách ra sẽ đẻ bản sao thứ hai của một luật — đúng lý do `chay_nap.py` và `schema.py` dài)*.
- ⭐ **Repo layer bắt buộc từ ngày 0** — chỉ `fls/repo/` được import driver DB. Bài học FPS: 313 call-site không abstraction ⇒ migration 4–8 tuần rủi ro cao (`FLS-vs-FPS` §7).
- **SQL verbatim trong adapter**, luật nghiệp vụ ở facade — không trộn.
- **Import:** stdlib → external → internal absolute → relative; **cấm import vòng** *(import-linter trong CI)*; mũi tên một chiều về `canon`/`contract`.
- ⛔ **Cấm hardcode quy tắc nghiệp vụ** — ngưỡng/ma trận/tỷ lệ đọc từ bảng luật; `ITL-CONTRACT` là **DATA** *(một chỗ)*, không phải hằng rải khắp code. Hằng kỹ thuật *(timeout, page size)* thì được, `UPPER_SNAKE`.
- ⭐ **Actor ⛔ phải người khai MỘT chỗ** — `fls/repo/danh_muc_actor.py` *(`WO-011`)*: mọi tiến trình máy / công cụ kiểm ghi kho mang một hằng ở `ACTOR_MAY`; chỗ dùng **import**, ⛔ gõ lại chuỗi. Bài `tests/repo/test_danh_muc_actor.py` quét mọi hằng `…@fls…`/`…@apero.vn` trong `fls/`+`tools/` *(⛔ `tests/`)*. ⛔ Một công cụ ⛔ được mượn tên giống người *(`ke-toan@…`)* — đó là cách thước *"người thật"* vỡ. Dòng thử đường ghi mang `reason` `UAT <ngày>`; nhận UAT bằng `la_uat()` / `sql_khong_uat()`, ⛔ viết luật thứ hai.
- ⛔ **Cấm mặc định im lặng** *(`INV-I16`)* — máy không suy được thì trả `NULL` + trạng thái `UNMAPPED`, **không** gán giá trị cứng. Đây là bug gốc của sổ AS-IS.
- **Migration:** ⭐ `<NNNN>_<mô_tả>.sql` — **số thứ tự 4 chữ số**, ⛔ không phải `<timestamp>` *(sửa 17/09 cho khớp `0001`…`0023`)*. **Forward-only**, cưỡng chế bằng `checksum` sha256 trong sổ `fls_migration`.
  ⛔⛔ **⛔ KHÔNG có `down` — và đây là QUYẾT ĐỊNH, ⛔ không phải thiếu sót** *(owner chốt 17/09)*. Câu cũ ~~*«mỗi migration có `down`»*~~ là một **lời hứa treo suốt 23 migration**: đo được **0/23** có. Một lời hứa ⛔ không ai giữ **nguy hơn** việc ⛔ không hứa, vì người sau tin là có đường lùi.
  ⭐ **Đường lùi thật là `PITR` của Cloud SQL + kho là `append-only`** *(`INV-I08` — ⛔ không một `DELETE` nào trong cả hệ)*, ⛔ không phải một câu `down` gõ tay mà ⛔ chưa ai chạy thử. Xem `04_DB_IMPLEMENTATION`.
- **Commit:** conventional commits; branch `feat/ fix/ chore/`; PR ≤ 400 dòng; squash merge.
- **Secrets:** env / secret manager, không bao giờ trong code; `.env*` trong `.gitignore`; **không commit service-account key**.
- **Test** ⭐ đặt ở **`tests/` gốc repo, soi gương cây `fls/`** *(sửa 17/09: đo được **0** test trong `fls/`, **128** tệp ở `tests/`)* — ~~*«đặt cạnh module»*~~ khai tử. Lý do giữ hình hiện tại: nhiều cổng **quét CẢ THƯ MỤC `fls/`** *(cấm `UPDATE`/`DELETE`, quét mã nguồn, `import-linter`)*, trộn test vào đó là bắt mọi cổng phải học cách **loại trừ** — và một cổng có ngoại lệ là **một cổng sắp chết**.
  ⛔ Test chạm tiền đi trên **PG container thật** *(`FLS-vs-FPS` §7 mục 7)*, ⛔ không `sqlite` giả.

## §3 · Ba luật ranh giới — cưỡng chế, không nhắc nhở

| # | Luật | Cưỡng chế |
|--:|---|---|
| 1 | Không ghi vào `fps_*` / P100 | vendor chỉ mở kết nối **read-only** tới nguồn |
| 2 | Không ghi vào file Google kế toán | service account chỉ có quyền **viewer** |
| 3 | Không tự tính lại đối soát số dư | adapter C **đọc** kết quả A-CCR, không có code tính lại |

## §4 · Luật cho phiên AI trong repo

1. Đọc `00_MASTER_INDEX` + `01_TECH_DESIGN` + task trong `03_IMPLEMENTATION_PLAN` trước khi sửa file nào.
2. ⭐ **SSOT là CODE, không phải spec** *(`FLS-vs-FPS` §Nguyên tắc số 1)* — mọi con số/tên trường phải **re-verify với code hoặc phép đo**, không lấy từ tài liệu. Bài học 24/08: ba lần báo số sai vì tin nguồn thứ cấp.
3. Không sửa file ngoài phạm vi task; cần sửa chéo module → ghi `GAP`, không tự làm.
4. Sau sửa BE: tự chạy test module đó + `import-linter`, mới báo xong.
5. Không tự đổi schema/API/hợp đồng — đổi spec trước (`BA-05`/`BA-07`), theo `ORC-07`; đổi `ITL-CONTRACT` là **CR loại 3** kèm test tương thích.

## Changelog
- **v1.2** (2026-10-02, `WO-011`): §2 thêm quy ước **sổ actor một chỗ** + luật nhận UAT một hàm *(thước mốc `B` vỡ ba lần vì chuỗi actor máy gõ rải — `KQ-010 F-2`)*.
- **v1.1** (2026-09-17, `QĐ-ITL-133` — ⭐⭐ **BỐN QUY ƯỚC ĐƯỢC SỬA CHO KHỚP MÃ, ⛔ không phải ngược lại**): owner chốt *“sửa quy ước cho khớp thực tế”* sau khi đo `17/09`. ⛔⛔ **Vì sao hướng ấy đúng ở ĐÂY, và ⛔ không đúng ở mọi chỗ:** cả bốn dòng bị sửa đều mô tả một kiến trúc `FastAPI` **chưa bao giờ được dựng** — chúng ⛔ không phải tiêu chuẩn bị bỏ, chúng là **mô tả sai**. ⭐ Riêng dòng `down` thì owner quyết **thật**, ⛔ không phải quyết cho khớp: đường lùi là `PITR` + sổ `append-only`, ⛔ không phải một câu `down` gõ tay mà ⛔ chưa ai chạy thử. **Bốn chỗ:** ⓐ khuôn module `router/service/schemas` *(đo: `0` tệp)* → khuôn **theo VIỆC**; ⓑ `R-A2` **chỉ áp cho tài liệu**, ⛔ không cho tên bảng *(nếu không thì bảng phải tên `fls_itl_ledge`)*; ⓒ migration `<timestamp>` → **`<NNNN>` 4 chữ số**, và **⛔ không có `down`** *(đo: `0/23`)*; ⓓ test *“cạnh module”* → **`tests/` gốc** *(đo: `0` trong `fls/`, `128` tệp ở `tests/`)*. ⚠ **Và một lời hứa bị hạ cấp có chủ ý:** *“tệp ≤ 300 dòng”* từ **luật** → **mục tiêu** *(đo: `17/75` tệp vượt)* — một luật bị vi phạm 17 lần mà ⛔ không cổng nào đỏ thì nó **làm hỏng uy tín của cả bản quy ước**, ⛔ không chỉ của riêng dòng ấy.
- **v1.0** (2026-08-24): Viết lại cho **repo `FLS` độc lập** (`QĐ-ITL-45`). Khai tử phương án `voi/`. Thêm: repo layer từ ngày 0, cấm mặc định im lặng (`INV-I16`), 3 luật ranh giới cưỡng chế, luật AI **"SSOT là code"**.
