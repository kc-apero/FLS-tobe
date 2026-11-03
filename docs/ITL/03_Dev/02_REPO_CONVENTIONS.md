# 02 — REPO CONVENTIONS: FLS

**Version:** v1.0 · **Ngày:** 2026-08-24 · **Chủ sở hữu:** Tech Lead
**Thay thế:** v0.2 *(bản copy chương trình, phương án `voi/`)* — đã khai tử.

**Căn cứ:** `QĐ-ITL-45` *(FLS repo riêng)* · `01_TECH_DESIGN` v1.0 §4.

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

- **Cấu trúc module** theo `01` §4; mỗi module: `router.py / service.py / repo.py / models.py / schemas.py / tests/`.
- **Naming:** Python `snake_case`; tên bảng/trường nguyên văn theo `BA-05` *(kể cả lỗi chính tả nguồn — `R-A2`)*; API `kebab-case` theo `BA-07`; file ≤ 300 dòng, hàm ≤ 40 dòng.
- ⭐ **Repo layer bắt buộc từ ngày 0** — chỉ `fls/repo/` được import driver DB. Bài học FPS: 313 call-site không abstraction ⇒ migration 4–8 tuần rủi ro cao (`FLS-vs-FPS` §7).
- **SQL verbatim trong adapter**, luật nghiệp vụ ở facade — không trộn.
- **Import:** stdlib → external → internal absolute → relative; **cấm import vòng** *(import-linter trong CI)*; mũi tên một chiều về `canon`/`contract`.
- ⛔ **Cấm hardcode quy tắc nghiệp vụ** — ngưỡng/ma trận/tỷ lệ đọc từ bảng luật; `ITL-CONTRACT` là **DATA** *(một chỗ)*, không phải hằng rải khắp code. Hằng kỹ thuật *(timeout, page size)* thì được, `UPPER_SNAKE`.
- ⛔ **Cấm mặc định im lặng** *(`INV-I16`)* — máy không suy được thì trả `NULL` + trạng thái `UNMAPPED`, **không** gán giá trị cứng. Đây là bug gốc của sổ AS-IS.
- **Migration:** `<timestamp>_<mô_tả>.sql`, forward-only ở production, mỗi migration có `down`. Xem `04_DB_IMPLEMENTATION`.
- **Commit:** conventional commits; branch `feat/ fix/ chore/`; PR ≤ 400 dòng; squash merge.
- **Secrets:** env / secret manager, không bao giờ trong code; `.env*` trong `.gitignore`; **không commit service-account key**.
- **Test** đặt cạnh module; test chạm tiền đi trên **PG container thật** *(`FLS-vs-FPS` §7 mục 7)*, không sqlite giả.

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
- **v1.0** (2026-08-24): Viết lại cho **repo `FLS` độc lập** (`QĐ-ITL-45`). Khai tử phương án `voi/`. Thêm: repo layer từ ngày 0, cấm mặc định im lặng (`INV-I16`), 3 luật ranh giới cưỡng chế, luật AI **"SSOT là code"**.
