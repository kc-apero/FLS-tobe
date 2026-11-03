# FLS P0 — Nền + bốn cổng chống drift · Implementation Plan

> ✅ **ĐÃ CHẠY XONG 2026-08-26** — repo `C:\Users\0_Apero Project\FLS`, nhánh `feat/p0-foundation`, **9 commit**.
> Cổng ra: `pytest` **34 passed** *(29 offline + 5 trên PG 16 container)* · `lint-imports` **2 kept 0 broken** ·
> `pg_migrate --dry-run` **170 dòng DDL** · `erd_export --write` + `git diff` **không đổi**.
>
> **Bốn chỗ plan này sai, đã sửa khi chạy** *(ghi lại để không lặp)*:
> 1. `test_smoke` bản plan **xanh ngay** dù chưa có file nào — thư mục rỗng đã là namespace package (PEP 420). Siết thành *"phải có `__init__.py`"*.
> 2. `.importlinter` liệt kê `fls.adapters/canon/ledger/oracle/api` **chưa tồn tại** ⇒ import-linter báo lỗi; thiếu `include_external_packages = True`. Danh sách nay lớn dần theo pha.
> 3. `ERD_ISLANDS` khai **2 bảng**, cổng G-ERD-3 chạy thật ra **4** — thiếu `fls_run`, `fls_reject`. **Cổng bắt được lỗ của chính plan đề ra nó.**
> 4. `test_content_key_trung_thi_bi_chan` ghim cứng `content_key='trung'` ⇒ **chạy lượt 2 trên cùng DB thì câu INSERT ĐẦU nổ**, test đỏ vì lý do sai.
>
> **Mở mới:** `GAP-ERD-P0-01` — `fls_itl.run_id` là `NOT NULL`, trỏ tới `fls_run.run_id` nhưng **không có FK** ⇒ gõ sai `run_id` là mất lineage trong im lặng. Cần Tech Lead quyết.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dựng nền repo `FLS` + toàn bộ schema `fls_*`, với ERD là **hiện vật sinh ra từ code** và **4 cổng chạy được** khiến drift thiết kế↔ERD trở thành build đỏ thay vì phát hiện muộn.

**Architecture:** Schema khai báo **một lần** dưới dạng dữ liệu Python có cấu trúc (`Table`/`Column`), rồi **sinh ra cả DDL lẫn ERD** từ cùng nguồn đó. Không có đường nào để DDL và ERD lệch nhau, vì chúng không phải hai bản viết tay. Cổng ERD là 3 test cộng với cổng khoá hợp đồng 14 trường.

**Tech Stack:** Python 3.12 · psycopg v3 · pytest · import-linter · PostgreSQL 16 *(Docker ở dev)* · FastAPI *(P4, chưa dùng ở P0)*

**Spec:** `03_Dev/04_DB_IMPLEMENTATION.md` v1.0 *(schema)* · `03_IMPLEMENTATION_PLAN.md` v1.0 §1 *(vì sao cần cổng)* · `02_BA/11_INVARIANTS.md` v0.5 · `02_BA/05_DATA_DICTIONARY_ERD.md` v0.6

## Global Constraints

- Repo `FLS` **độc lập**, module gốc `fls/`, ngang hàng `FPA-T4`/`P100-R` — `QĐ-ITL-45`, `02_REPO_CONVENTIONS` §1.
- **Chỉ `fls/repo/` được import driver DB** — cưỡng chế bằng `import-linter` trong CI, từ ngày 0.
- File ≤ **300 dòng**, hàm ≤ **40 dòng**. Python `snake_case`. Tên bảng/trường **nguyên văn** theo `BA-05`, kể cả lỗi chính tả nguồn (`R-A2`).
- ⛔ **Cấm mặc định im lặng** (`INV-I16`): không suy được ⇒ `NULL` + `work_status='UNMAPPED'`, không gán giá trị cứng.
- ⛔ **Không ghi** vào `fps_*` / P100 / file Google kế toán (`QĐ-ITL-34`, `QĐ-ITL-45`).
- Test chạm tiền chạy trên **PG container thật**, ⛔ không sqlite giả.
- Migration **forward-only** ở production; cột `*_thyt` và `canon` **phải có trong migration ĐẦU TIÊN** (`QĐ-ITL-35`).
- `ITL-CONTRACT` v1.0 = **14 trường đọc THEO TÊN**, `le` = cột `P` (**không** `BL`) — `QĐ-ITL-42`, `QĐ-owner-0820`.
- Conventional commits; branch `feat/`; PR ≤ 400 dòng.

### Lệch có chủ ý khỏi khuôn FPS — ghi rõ để không bị hiểu là tuỳ tiện

FPS khai schema bằng `dict[str, str]` chứa DDL thô (`P100-R/fps-backend/fps/db/pg_schema.py`). P0 **không** copy khuôn đó, vì **không thể sinh ERD từ chuỗi DDL mà không viết bộ phân tích SQL**, và drift ERD là rủi ro số một của dự án này (`03_IMPLEMENTATION_PLAN` §1).

Đổi lại mất khả năng "đọc SQL bằng mắt" ⇒ bù bằng **golden-file test** (`Task 3` Step 5): DDL sinh ra được chụp vào `tests/golden/ddl.sql` và mọi thay đổi hiện nguyên văn trong diff của PR.

---

## File Structure

| File | Trách nhiệm |
|---|---|
| `fls/db/model.py` | `Column` · `Table` — **SSOT duy nhất** của schema. Không import gì trong `fls/` |
| `fls/db/schema.py` | Khai báo 10 bảng + 2 view bằng `model.py`. Không chứa hàm |
| `fls/db/render.py` | `render_ddl()` · `render_erd_mermaid()` · `render_erd_json()` — thuần hàm |
| `fls/db/erd_export.py` | CLI: `python -m fls.db.erd_export --write` ghi hiện vật ERD |
| `fls/db/pg_migrate.py` | CLI áp DDL; `--dry-run` chạy offline không cần DB |
| `fls/db/triggers.py` | DDL trigger cưỡng chế `INV-I03` · `INV-I04a` |
| `fls/contract/itl_contract.py` | 14 trường `ITL-CONTRACT` v1.0 dạng **DATA** |
| `tests/db/test_render.py` | unit của bộ sinh |
| `tests/db/test_erd_gates.py` | **G-ERD-1 · G-ERD-2 · G-ERD-3** |
| `tests/db/test_invariants_pg.py` | trigger trên PG thật |
| `tests/contract/test_itl_contract_v1_lock.py` | khoá 14 trường (`INV-I07`) |
| `ERD-CONTRACT.json` · `ERD-CONTRACT.mmd` | hiện vật ERD, **sinh ra**, được commit |
| `tests/golden/ddl.sql` | ảnh chụp DDL để đọc bằng mắt trong PR |

---

### Task 1: Bộ xương repo + hai cổng tĩnh

**Files:**
- Create: `pyproject.toml`, `requirements.txt`, `.importlinter`, `fls/__init__.py`, `fls/db/__init__.py`, `tests/__init__.py`
- Test: `tests/test_smoke.py`

**Interfaces:**
- Consumes: —
- Produces: package `fls` import được; `pytest` và `lint-imports` chạy được

- [x] **Step 1: Viết test đỏ**

```python
# tests/test_smoke.py
def test_package_importable():
    import fls
    assert fls.__name__ == "fls"
```

- [x] **Step 2: Chạy để thấy nó đỏ**

Run: `pytest tests/test_smoke.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'fls'`

- [x] **Step 3: Dựng bộ xương**

```toml
# pyproject.toml
[project]
name = "fls"
version = "0.1.0"
requires-python = ">=3.12"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q --strict-markers"
markers = ["pg: cần PostgreSQL thật (không chạy offline)"]
```

```
# requirements.txt
psycopg[binary]>=3.2.0
pytest>=8.0.0
import-linter>=2.0
```

```ini
# .importlinter
[importlinter]
root_package = fls

[importlinter:contract:1]
name = Chi fls.repo duoc import driver DB
type = forbidden
source_modules = fls.adapters, fls.canon, fls.ledger, fls.contract, fls.oracle, fls.api
forbidden_modules = psycopg

[importlinter:contract:2]
name = Cam import vong
type = independence
modules = fls.canon, fls.contract
```

Tạo `fls/__init__.py`, `fls/db/__init__.py`, `tests/__init__.py` rỗng.

- [x] **Step 4: Chạy cả hai cổng**

Run: `pip install -r requirements.txt && pytest -v && lint-imports`
Expected: 1 passed · `lint-imports` in `Contracts: 2 kept, 0 broken`

- [x] **Step 5: Commit**

```bash
git add pyproject.toml requirements.txt .importlinter fls tests
git commit -m "chore: bo xuong repo FLS + cong pytest/import-linter"
```

---

### Task 2: `model.py` + bộ sinh DDL

**Files:**
- Create: `fls/db/model.py`, `fls/db/render.py`
- Test: `tests/db/test_render.py`

**Interfaces:**
- Consumes: —
- Produces:
  - `Column(name: str, type: str, null: bool = True, default: str | None = None, fk: str | None = None, pk: bool = False, unique: bool = False, generated: str | None = None, comment: str = "")`
  - `Table(name: str, columns: tuple[Column, ...], kind: str = "table", erd_entity: str = "", island_reason: str = "", view_sql: str = "")`
  - `render_ddl(t: Table) -> str`

- [x] **Step 1: Viết test đỏ**

```python
# tests/db/test_render.py
from fls.db.model import Column, Table
from fls.db.render import render_ddl


def test_render_ddl_cot_co_ban():
    t = Table(name="fls_demo", columns=(
        Column("demo_id", "bigint", null=False, pk=True),
        Column("ten", "text", null=False),
        Column("ghi_chu", "text"),
    ))
    sql = render_ddl(t)
    assert sql.startswith("CREATE TABLE IF NOT EXISTS fls_demo (")
    assert "demo_id bigint NOT NULL PRIMARY KEY" in sql
    assert "ten text NOT NULL" in sql
    assert "ghi_chu text," in sql or "ghi_chu text\n" in sql


def test_render_ddl_fk_unique_default_generated():
    t = Table(name="fls_demo", columns=(
        Column("k", "text", null=False, unique=True),
        Column("le", "text", fk="fls_le.le_code"),
        Column("mo", "boolean", null=False, default="false"),
        Column("khac", "boolean", generated="(le IS NOT NULL)"),
    ))
    sql = render_ddl(t)
    assert "k text NOT NULL UNIQUE" in sql
    assert "le text REFERENCES fls_le(le_code)" in sql
    assert "mo boolean NOT NULL DEFAULT false" in sql
    assert "khac boolean GENERATED ALWAYS AS (le IS NOT NULL) STORED" in sql


def test_render_ddl_view_dung_view_sql():
    t = Table(name="v_demo", columns=(Column("a", "text"),),
              kind="view", view_sql="SELECT 'x' AS a")
    assert render_ddl(t) == "CREATE OR REPLACE VIEW v_demo AS SELECT 'x' AS a;"
```

- [x] **Step 2: Chạy để thấy nó đỏ**

Run: `pytest tests/db/test_render.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'fls.db.model'`

- [x] **Step 3: Viết code tối thiểu**

```python
# fls/db/model.py
"""SSOT của schema fls_*. Khai báo MỘT lần, sinh ra cả DDL lẫn ERD.

Vì sao không dùng dict[str, str] DDL thô như FPS: không sinh được ERD từ chuỗi SQL
mà không viết bộ phân tích SQL, và drift ERD là rủi ro số một (03_IMPLEMENTATION_PLAN §1).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Column:
    name: str
    type: str
    null: bool = True
    default: str | None = None
    fk: str | None = None          # "bang.cot"
    pk: bool = False
    unique: bool = False
    generated: str | None = None   # biểu thức của GENERATED ALWAYS AS ... STORED
    comment: str = ""


@dataclass(frozen=True)
class Table:
    name: str
    columns: tuple[Column, ...]
    kind: str = "table"            # "table" | "view"
    erd_entity: str = ""           # tên entity tương ứng trên ERD của BA
    island_reason: str = ""        # lý do KHÔNG có FK về fls_itl (G-ERD-3)
    view_sql: str = ""
```

```python
# fls/db/render.py
"""Sinh DDL và ERD từ fls.db.model. Thuần hàm, không chạm DB."""

from __future__ import annotations

from fls.db.model import Column, Table


def _render_column(c: Column) -> str:
    parts = [c.name, c.type]
    if c.generated:
        parts.append(f"GENERATED ALWAYS AS {c.generated} STORED")
        return " ".join(parts)
    if not c.null:
        parts.append("NOT NULL")
    if c.default is not None:
        parts.append(f"DEFAULT {c.default}")
    if c.pk:
        parts.append("PRIMARY KEY")
    if c.unique:
        parts.append("UNIQUE")
    if c.fk:
        table, col = c.fk.split(".")
        parts.append(f"REFERENCES {table}({col})")
    return " ".join(parts)


def render_ddl(t: Table) -> str:
    if t.kind == "view":
        return f"CREATE OR REPLACE VIEW {t.name} AS {t.view_sql};"
    body = ",\n  ".join(_render_column(c) for c in t.columns)
    return f"CREATE TABLE IF NOT EXISTS {t.name} (\n  {body}\n);"
```

- [x] **Step 4: Chạy để thấy nó xanh**

Run: `pytest tests/db/test_render.py -v`
Expected: 3 passed

- [x] **Step 5: Commit**

```bash
git add fls/db/model.py fls/db/render.py tests/db/test_render.py
git commit -m "feat(db): model schema co cau truc + bo sinh DDL"
```

---

### Task 3: `fls_itl` + `seq_itl_id` — bỏ `fls_id_counter`

**Files:**
- Create: `fls/db/schema.py`, `tests/golden/ddl.sql`
- Test: `tests/db/test_schema_fls_itl.py`

**Interfaces:**
- Consumes: `Column`, `Table`, `render_ddl` từ Task 2
- Produces: `SEQUENCES: dict[str, str]` · `TABLES: dict[str, Table]` · `CREATE_ORDER: tuple[str, ...]`

★ **Sửa spec ngay tại đây.** `04_DB_IMPLEMENTATION` §5/§6 nói sinh `itl_id` bằng bảng `fls_id_counter`, dẫn *"pattern `fps_id_counter` — đã fix bug dup thật ở FPS"*. Đọc code FPS thật thì cách FPS **fix** là **bỏ bảng counter**: *"UPDATE+SELECT 2 round-trip, 36% độ trễ, streaming-buffer trùng ID → THAY bằng SEQUENCE + DEFAULT"* (`P100-R/fps-backend/fps/db/pg_schema.py:9`). Bài học bị đọc ngược. `itl_id` là danh tính đóng băng (`INV-I04a`) nên trùng id là hỏng khoá cả sổ ⇒ **dùng SEQUENCE**. Ghi vào `GAP-PLAN-02`.

- [x] **Step 1: Viết test đỏ**

```python
# tests/db/test_schema_fls_itl.py
from fls.db.render import render_ddl
from fls.db.schema import CREATE_ORDER, SEQUENCES, TABLES

CONTRACT_14 = ("doc_date", "doc_no", "memo", "curr", "ps_no", "ps_co", "acct",
               "le", "itl_id", "hd", "pay_type", "cdt1", "svc_start", "svc_end")


def test_khong_con_fls_id_counter():
    """FPS da khai tu pattern counter — FLS khong duoc copy lai."""
    assert "fls_id_counter" not in TABLES
    assert "seq_itl_id" in SEQUENCES


def test_itl_id_sinh_bang_sequence_va_la_pk():
    col = {c.name: c for c in TABLES["fls_itl"].columns}["itl_id"]
    assert col.pk is True
    assert col.default == "nextval('seq_itl_id')"


def test_du_14_truong_hop_dong():
    have = {c.name for c in TABLES["fls_itl"].columns}
    assert set(CONTRACT_14) <= have


def test_5_cot_thyt_va_canon_co_trong_migration_dau():
    """QD-ITL-35: them sau la migration tren bang da day du lieu."""
    have = {c.name for c in TABLES["fls_itl"].columns}
    assert {"hd_thyt", "pay_type_thyt", "cdt1_thyt",
            "svc_start_thyt", "svc_end_thyt", "canon"} <= have


def test_lineage_va_run_deu_not_null():
    cols = {c.name: c for c in TABLES["fls_itl"].columns}
    for n in ("source_system", "source_sheet", "source_row", "run_id",
              "contract_version", "canon_version", "mapping_version"):
        assert cols[n].null is False, n


def test_content_key_unique():
    cols = {c.name: c for c in TABLES["fls_itl"].columns}
    assert cols["content_key"].unique is True
    assert cols["content_key"].null is False


def test_fls_itl_dung_dau_create_order():
    assert CREATE_ORDER[0] == "fls_le", "fls_le la cha FK, phai truoc"
    assert "fls_itl" in CREATE_ORDER


def test_render_duoc_khong_no():
    assert render_ddl(TABLES["fls_itl"]).startswith("CREATE TABLE IF NOT EXISTS fls_itl (")
```

- [x] **Step 2: Chạy để thấy nó đỏ**

Run: `pytest tests/db/test_schema_fls_itl.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'fls.db.schema'`

- [x] **Step 3: Khai báo schema**

```python
# fls/db/schema.py  (phần 1/2 — fls_le + fls_itl)
"""Khai bao 10 bang + 2 view cua FLS. Chi khai bao, khong ham.

Nguon: 03_Dev/04_DB_IMPLEMENTATION v1.0 §2-§6b.
LECH CO CHU DICH: bo fls_id_counter, dung SEQUENCE (xem plan P0 Task 3).
"""

from __future__ import annotations

from fls.db.model import Column as C
from fls.db.model import Table

SEQUENCES: dict[str, str] = {
    "seq_itl_id": "CREATE SEQUENCE IF NOT EXISTS seq_itl_id START 1",
}

_FLS_LE = Table(
    name="fls_le", erd_entity="LEGAL_ENTITY",
    island_reason="danh muc phap nhan — fls_itl tro TOI no, khong nguoc lai",
    columns=(
        C("le_code", "text", null=False, pk=True, comment="ma phap nhan"),
        C("le_name", "text", null=False),
        C("is_entity", "boolean", null=False, default="true",
          comment="INV-I10: nhan khong-phai-phap-nhan (USD, HotBonus) => false"),
    ))

_FLS_ITL = Table(
    name="fls_itl", erd_entity="ITL_ROW",
    columns=(
        # ── lop C · danh tinh (INV-I04a/b) ──
        C("itl_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')",
          comment="cap luc staged roi DONG BANG; KHONG theo vi tri dong"),
        C("content_key", "text", null=False, unique=True,
          comment="INV-I04b: hash(source_system,source_sheet,doc_date,ps_no,ps_co,doc_no,seq_trung)"),
        # ── lop C · lineage (INV-I05) ──
        C("source_system", "text", null=False, comment="P100|Cash|A-CCR|HR|Platform"),
        C("source_sheet", "text", null=False),
        C("source_row", "int", null=False),
        # ── lop C · run (INV-I12) ──
        C("run_id", "text", null=False),
        C("contract_version", "text", null=False),
        C("canon_version", "text", null=False),
        C("mapping_version", "text", null=False),
        # ── lop C · trang thai ──
        C("raw_frozen", "boolean", null=False, default="false",
          comment="INV-I03: true => trigger cam UPDATE/DELETE"),
        C("is_flash", "boolean", null=False, default="true", comment="INV-I14"),
        C("period_state", "text", null=False, default="'open'", comment="INV-I13: open|locked"),
        C("created_at", "timestamptz", null=False, default="now()"),
        # ── lop A · 14 truong ITL-CONTRACT v1.0, doc THEO TEN (QD-ITL-42) ──
        C("doc_date", "date", comment="A(0) Ngay chung tu. INV-I11: date khong phai chuoi"),
        C("doc_no", "text", comment="B(1) So chung tu. AUD-12: KHONG mang nghia thoi gian"),
        C("memo", "text", comment="C(2) Dien giai"),
        C("curr", "text", comment="D(3) Don vi tien te"),
        C("ps_no", "numeric(20,2)", comment="E(4) PS No"),
        C("ps_co", "numeric(20,2)", comment="F(5) PS Co"),
        C("acct", "text", comment="G(6) Tai khoan"),
        C("le", "text", fk="fls_le.le_code", comment="P(15) SSOT phap nhan — KHONG dung BL"),
        C("hd", "text", comment="V(21) Final khoi 1 — Budget Code"),
        C("pay_type", "text", comment="Z(25) Final khoi 2 — Loai giao dich"),
        C("cdt1", "text", comment="AD(29) Final khoi 3 — Chu du toan"),
        C("svc_start", "date", comment="AH(33) Final khoi 4"),
        C("svc_end", "date", comment="AL(37) Final khoi 5"),
        # ── lop A' · cot song song (QD-ITL-35) ──
        C("hd_thyt", "text", comment="NULL o cho may tu bia. KHONG vao parity"),
        C("pay_type_thyt", "text"),
        C("cdt1_thyt", "text"),
        C("svc_start_thyt", "date"),
        C("svc_end_thyt", "date"),
        C("work_status", "text", null=False, default="'ok'",
          comment="INV-I16: ok|UNMAPPED|rejected"),
        # ── lop A' · khoi 6-7 ngoai hop dong P&L (QD-owner-0824) ──
        C("id_payee", "text", comment="AP Final khoi 6 — goi y doc tu canon[Y]"),
        C("invoice", "text", comment="AT Final khoi 7 — link hoa don"),
        # ── lop A' · ALLOCATE: may goi y, nguoi override thang ──
        C("cdt1_cfa1", "text", comment="AU goi y = cdt1"),
        C("cdt1_cfa2", "text", comment="AV goi y = VLOOKUP Mapping Master"),
        C("alloc_method", "text", comment="AW goi y = VLOOKUP Mapping Master"),
        C("cdt1_cfa2_classify", "text", comment="SNAPSHOT goi y luc override (US-025)"),
        C("alloc_method_classify", "text"),
        # ── lop A' · phap nhan tra (QD-ITL-10) ──
        C("le_payer", "text", fk="fls_le.le_code", comment="ai THUC tra; NULL neu nguon thieu"),
        C("is_intercompany", "boolean",
          generated="(le IS NOT NULL AND le_payer IS NOT NULL AND le <> le_payer)",
          comment="cam nhap tay — may suy"),
        # ── lop A' · audit/workflow ──
        C("pic", "text", comment="BJ giu cot, CHUA len UI"),
        C("audit_status", "text", comment="BK khac work_status"),
        # ── lop B · canonical 36 cot ──
        C("canon", "jsonb", null=False,
          comment="36 cot nguyen van theo VI TRI — 4 cot AH-AK trung ten, luu theo key la mat cot"),
    ))
```

```python
# fls/db/schema.py  (phần 2/2 — CREATE_ORDER; 8 bảng phụ + 2 view ở Task 4)
TABLES: dict[str, Table] = {t.name: t for t in (_FLS_LE, _FLS_ITL)}

CREATE_ORDER: tuple[str, ...] = ("fls_le", "fls_itl")
```

- [x] **Step 4: Chạy để thấy nó xanh**

Run: `pytest tests/db/test_schema_fls_itl.py -v`
Expected: 8 passed

- [x] **Step 5: Chụp golden DDL để đọc bằng mắt trong PR**

```python
# them vao tests/db/test_schema_fls_itl.py
import pathlib

GOLDEN = pathlib.Path("tests/golden/ddl.sql")


def test_golden_ddl_khop(request):
    from fls.db.schema import CREATE_ORDER, SEQUENCES, TABLES
    out = "\n\n".join(
        [*(s + ";" for s in SEQUENCES.values()),
         *(render_ddl(TABLES[n]) for n in CREATE_ORDER)]) + "\n"
    if request.config.getoption("--update-golden", default=False):
        GOLDEN.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN.write_text(out, encoding="utf-8")
    assert GOLDEN.read_text(encoding="utf-8") == out, (
        "DDL doi ma golden chua cap nhat. Chay: pytest --update-golden")
```

```python
# them vao tests/conftest.py
def pytest_addoption(parser):
    parser.addoption("--update-golden", action="store_true",
                     help="ghi lai anh chup DDL/ERD")
```

Run: `pytest tests/db -v --update-golden && pytest tests/db -v`
Expected: lượt 2 — all passed, và `tests/golden/ddl.sql` xuất hiện trong `git status`

- [x] **Step 6: Commit**

```bash
git add fls/db/schema.py tests/db/test_schema_fls_itl.py tests/conftest.py tests/golden/ddl.sql
git commit -m "feat(db): fls_itl 3 lop + seq_itl_id (bo fls_id_counter, xem GAP-PLAN-02)"
```

---

### Task 4: Tám bảng phụ + hai view

**Files:**
- Modify: `fls/db/schema.py`
- Test: `tests/db/test_schema_phu.py`

**Interfaces:**
- Consumes: `Column`, `Table` (Task 2); `TABLES`, `CREATE_ORDER` (Task 3)
- Produces: `TABLES` đủ 10 bảng + 2 view; `CREATE_ORDER` sắp theo phụ thuộc FK

- [x] **Step 1: Viết test đỏ**

```python
# tests/db/test_schema_phu.py
from fls.db.schema import CREATE_ORDER, TABLES

MONG_DOI = {"fls_le", "fls_itl", "fls_adjustment", "fls_journal", "fls_run",
            "fls_reject", "fls_mapping_master", "fls_source", "fls_queue_event",
            "fls_queue_state", "fls_queue_reason_weekly"}


def test_du_bang_va_view():
    assert MONG_DOI <= set(TABLES)


def test_journal_du_7_truong_AUD_1():
    cols = {c.name for c in TABLES["fls_journal"].columns}
    assert {"itl_id", "field", "value_before", "value_after",
            "actor", "at", "value_source", "reason"} <= cols


def test_hai_view_co_view_sql():
    for n in ("fls_queue_state", "fls_queue_reason_weekly"):
        assert TABLES[n].kind == "view"
        assert TABLES[n].view_sql.strip(), n


def test_create_order_cha_truoc_con():
    for name in CREATE_ORDER:
        t = TABLES[name]
        if t.kind == "view":
            continue
        for c in t.columns:
            if c.fk:
                parent = c.fk.split(".")[0]
                assert CREATE_ORDER.index(parent) <= CREATE_ORDER.index(name), (
                    f"{name}.{c.name} tro toi {parent} nhung {parent} tao sau")


def test_view_tao_sau_moi_bang():
    ten_view = [n for n in CREATE_ORDER if TABLES[n].kind == "view"]
    ten_bang = [n for n in CREATE_ORDER if TABLES[n].kind == "table"]
    assert max(CREATE_ORDER.index(v) for v in ten_view) > max(
        CREATE_ORDER.index(b) for b in ten_bang)
```

- [x] **Step 2: Chạy để thấy nó đỏ**

Run: `pytest tests/db/test_schema_phu.py -v`
Expected: FAIL — `test_du_bang_va_view` báo thiếu 9 tên

- [x] **Step 3: Khai báo tiếp**

```python
# them vao fls/db/schema.py, TRUOC khoi TABLES/CREATE_ORDER
_FLS_ADJUSTMENT = Table(
    name="fls_adjustment", erd_entity="ADJUSTMENT_ENTRY",
    columns=(
        C("adj_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id"),
        C("field", "text", null=False),
        C("value_after", "text"),
        C("state", "text", null=False, default="'posted'",
          comment="SM-I03: posted|reversed. KHONG co deleted"),
        C("reversal_of", "bigint", fk="fls_adjustment.adj_id",
          comment="dao chi bang but toan moi (INV-I08)"),
        C("actor", "text", null=False),
        C("at", "timestamptz", null=False, default="now()"),
    ))

_FLS_JOURNAL = Table(
    name="fls_journal", erd_entity="JOURNAL",
    columns=(
        C("jrn_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id"),
        C("field", "text", null=False),
        C("value_before", "text"),
        C("value_after", "text"),
        C("actor", "text", null=False),
        C("at", "timestamptz", null=False, default="now()"),
        C("value_source", "text", null=False, comment="nguon goi y luc gõ"),
        C("reason", "text"),
    ))

_FLS_RUN = Table(
    name="fls_run", erd_entity="RUN",
    island_reason="so lan chay — fls_itl.run_id tro toi, khong FK nguoc",
    columns=(
        C("run_id", "text", null=False, pk=True),
        C("contract_version", "text", null=False),
        C("canon_version", "text", null=False),
        C("mapping_version", "text", null=False),
        C("started_at", "timestamptz", null=False, default="now()"),
        C("row_count", "int"),
        C("state", "text", null=False, default="'queued'", comment="SM-I04"),
    ))

_FLS_REJECT = Table(
    name="fls_reject", erd_entity="REJECT",
    island_reason="dong bi loai TRUOC khi vao so nen khong the FK toi fls_itl (ACC-4)",
    columns=(
        C("rej_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("run_id", "text", null=False, fk="fls_run.run_id"),
        C("source_system", "text", null=False),
        C("source_sheet", "text", null=False),
        C("source_row", "int", null=False),
        C("reason", "text", null=False, comment="ACC-4: ly do CO TEN, khong duoc rong"),
    ))

_FLS_MAPPING_MASTER = Table(
    name="fls_mapping_master", erd_entity="MAPPING_MASTER",
    island_reason="danh muc HD — tra theo gia tri hd, khong FK vi hd co the UNMAPPED",
    columns=(
        C("hd_code", "text", null=False, pk=True),
        C("need_cfa2", "text"),
        C("method_cfa2", "text"),
        C("code_hr", "text"),
        C("coa1", "text"),
        C("coa2", "text"),
    ))

_FLS_SOURCE = Table(
    name="fls_source", erd_entity="SOURCE",
    island_reason="manifest pipeline — pipeline ghi, F06 doc (DD-I07)",
    columns=(
        C("source_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("source_key", "text", null=False, unique=True, comment="'R | HoangACB' | 'file▸sheet'"),
        C("src_type", "text", null=False, comment="Bank|Cash|CCR|Platform|Mapping"),
        C("last_seen_at", "timestamptz"),
        C("lag_days", "int"),
        C("cutoff_date", "date"),
        C("txn_count", "int"),
    ))

_FLS_QUEUE_EVENT = Table(
    name="fls_queue_event", erd_entity="QUEUE_EVENT",
    columns=(
        C("evt_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id"),
        C("evt_type", "text", null=False, comment="reason|defer"),
        C("reason", "text"),
        C("defer_until", "date"),
        C("actor", "text", null=False),
        C("at", "timestamptz", null=False, default="now()"),
    ))

_V_QUEUE_STATE = Table(
    name="fls_queue_state", kind="view", erd_entity="QUEUE_STATE",
    columns=(C("itl_id", "bigint"), C("reason", "text"),
             C("defer_until", "date"), C("defer_count", "int")),
    view_sql="""
SELECT itl_id,
       (ARRAY_AGG(reason ORDER BY at DESC)
          FILTER (WHERE evt_type = 'reason'))[1]            AS reason,
       MAX(defer_until) FILTER (WHERE evt_type = 'defer')   AS defer_until,
       COUNT(*) FILTER (WHERE evt_type = 'defer')::int      AS defer_count
FROM fls_queue_event
GROUP BY itl_id""".strip())

_V_QUEUE_REASON_WEEKLY = Table(
    name="fls_queue_reason_weekly", kind="view", erd_entity="QUEUE_REASON_WEEKLY",
    columns=(C("tuan", "date"), C("so_lan", "int")),
    view_sql="""
SELECT DATE_TRUNC('week', at)::date AS tuan,
       COUNT(*)::int                AS so_lan
FROM fls_queue_event
WHERE evt_type = 'reason'
GROUP BY 1
ORDER BY 1 DESC""".strip())
```

```python
# THAY khoi TABLES/CREATE_ORDER cuoi file
TABLES: dict[str, Table] = {t.name: t for t in (
    _FLS_LE, _FLS_RUN, _FLS_ITL, _FLS_ADJUSTMENT, _FLS_JOURNAL, _FLS_REJECT,
    _FLS_MAPPING_MASTER, _FLS_SOURCE, _FLS_QUEUE_EVENT,
    _V_QUEUE_STATE, _V_QUEUE_REASON_WEEKLY,
)}

CREATE_ORDER: tuple[str, ...] = (
    "fls_le", "fls_run", "fls_itl", "fls_adjustment", "fls_journal",
    "fls_reject", "fls_mapping_master", "fls_source", "fls_queue_event",
    "fls_queue_state", "fls_queue_reason_weekly",
)
```

- [x] **Step 4: Chạy cả hai file test**

Run: `pytest tests/db -v --update-golden && pytest tests/db -v`
Expected: all passed

- [x] **Step 5: Commit**

```bash
git add fls/db/schema.py tests/db/test_schema_phu.py tests/golden/ddl.sql
git commit -m "feat(db): 8 bang phu + 2 view, CREATE_ORDER theo phu thuoc FK"
```

---

### Task 5: G-ERD-1 — ERD sinh ra từ code, lệch là build đỏ

**Files:**
- Create: `fls/db/erd_export.py`, `ERD-CONTRACT.json`, `ERD-CONTRACT.mmd`
- Modify: `fls/db/render.py`
- Test: `tests/db/test_erd_gates.py`

**Interfaces:**
- Consumes: `TABLES`, `CREATE_ORDER` (Task 4)
- Produces: `render_erd_json(tables) -> dict` · `render_erd_mermaid(tables) -> str`; CLI `python -m fls.db.erd_export --write`

- [x] **Step 1: Viết test đỏ (G-ERD-1)**

```python
# tests/db/test_erd_gates.py
import json
import pathlib

from fls.db.render import render_erd_json, render_erd_mermaid
from fls.db.schema import TABLES

JSON_PATH = pathlib.Path("ERD-CONTRACT.json")
MMD_PATH = pathlib.Path("ERD-CONTRACT.mmd")


def test_g_erd_1_json_khop_code():
    """G-ERD-1: doi schema ma quen sinh lai ERD => do."""
    assert json.loads(JSON_PATH.read_text(encoding="utf-8")) == render_erd_json(TABLES), (
        "ERD-CONTRACT.json lech schema. Chay: python -m fls.db.erd_export --write")


def test_g_erd_1_mermaid_khop_code():
    assert MMD_PATH.read_text(encoding="utf-8") == render_erd_mermaid(TABLES), (
        "ERD-CONTRACT.mmd lech schema. Chay: python -m fls.db.erd_export --write")


def test_erd_json_co_quan_he_fk():
    erd = render_erd_json(TABLES)
    cap = {(r["from"], r["to"]) for r in erd["relations"]}
    assert ("fls_journal", "fls_itl") in cap
    assert ("fls_itl", "fls_le") in cap
```

- [x] **Step 2: Chạy để thấy nó đỏ**

Run: `pytest tests/db/test_erd_gates.py -v`
Expected: FAIL — `ImportError: cannot import name 'render_erd_json'`

- [x] **Step 3: Viết bộ sinh ERD + CLI**

```python
# them vao fls/db/render.py
def render_erd_json(tables: dict[str, Table]) -> dict:
    """Hien vat ERD dang may doc duoc. Sap xep on dinh de diff sach."""
    entities = []
    relations = []
    for name in sorted(tables):
        t = tables[name]
        entities.append({
            "table": t.name,
            "kind": t.kind,
            "erd_entity": t.erd_entity,
            "island_reason": t.island_reason,
            "columns": [{"name": c.name, "type": c.type, "null": c.null,
                         "pk": c.pk, "unique": c.unique, "fk": c.fk}
                        for c in t.columns],
        })
        for c in t.columns:
            if c.fk:
                relations.append({"from": t.name, "to": c.fk.split(".")[0],
                                  "via": c.name})
    relations.sort(key=lambda r: (r["from"], r["to"], r["via"]))
    return {"contract": "ERD-CONTRACT", "version": 1,
            "entities": entities, "relations": relations}


def render_erd_mermaid(tables: dict[str, Table]) -> str:
    lines = ["erDiagram"]
    for name in sorted(tables):
        t = tables[name]
        lines.append(f"    {t.name} {{")
        for c in t.columns:
            khoa = "PK" if c.pk else ("FK" if c.fk else "")
            lines.append(f"        {c.type.split('(')[0]} {c.name} {khoa}".rstrip())
        lines.append("    }")
    for name in sorted(tables):
        for c in tables[name].columns:
            if c.fk:
                lines.append(f'    {c.fk.split(".")[0]} ||--o{{ {name} : "{c.name}"')
    return "\n".join(lines) + "\n"
```

```python
# fls/db/erd_export.py
"""Sinh hien vat ERD tu schema. Offline, khong cham DB.

  python -m fls.db.erd_export            # in ra man hinh
  python -m fls.db.erd_export --write    # ghi ERD-CONTRACT.json + .mmd
"""

from __future__ import annotations

import argparse
import json
import pathlib

from fls.db.render import render_erd_json, render_erd_mermaid
from fls.db.schema import TABLES


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    js = json.dumps(render_erd_json(TABLES), indent=2, ensure_ascii=False) + "\n"
    mmd = render_erd_mermaid(TABLES)
    if args.write:
        pathlib.Path("ERD-CONTRACT.json").write_text(js, encoding="utf-8")
        pathlib.Path("ERD-CONTRACT.mmd").write_text(mmd, encoding="utf-8")
        print("da ghi ERD-CONTRACT.json + ERD-CONTRACT.mmd")
    else:
        print(js)
        print(mmd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [x] **Step 4: Sinh hiện vật rồi chạy cổng**

Run: `python -m fls.db.erd_export --write && pytest tests/db/test_erd_gates.py -v`
Expected: 3 passed

- [x] **Step 5: Chứng minh cổng THẬT SỰ bắt được drift**

```bash
python - <<'EOF'
import pathlib, json
p = pathlib.Path("ERD-CONTRACT.json"); d = json.loads(p.read_text(encoding="utf-8"))
d["entities"] = [e for e in d["entities"] if e["table"] != "fls_journal"]
p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
EOF
pytest tests/db/test_erd_gates.py::test_g_erd_1_json_khop_code -v
```
Expected: **FAIL** kèm câu *"ERD-CONTRACT.json lech schema"* — cổng sống. Rồi khôi phục:
`python -m fls.db.erd_export --write && pytest tests/db -v` → all passed

- [x] **Step 6: Commit**

```bash
git add fls/db/render.py fls/db/erd_export.py tests/db/test_erd_gates.py ERD-CONTRACT.json ERD-CONTRACT.mmd
git commit -m "feat(db): G-ERD-1 sinh ERD tu code, lech schema la build do"
```

---

### Task 6: G-ERD-2 + G-ERD-3 — đầy đủ entity và không bảng mồ côi

**Files:**
- Modify: `tests/db/test_erd_gates.py`, `02_BA/05_DATA_DICTIONARY_ERD.md` *(trong repo tài liệu)*
- Create: `fls/db/erd_policy.py`

**Interfaces:**
- Consumes: `TABLES` (Task 4); `render_erd_json` (Task 5)
- Produces: `ERD_ISLANDS: frozenset[str]` · `BA_ERD_DOC: pathlib.Path`

★ **Đây là cổng bắt đúng drift đã phát hiện ngày 26/08**: ERD của BA có 10 entity, code có 10 bảng + 2 view, chỉ 3 chỗ khớp, và `fls_journal` vắng mặt.

- [x] **Step 1: Viết test đỏ (hai cổng)**

```python
# them vao tests/db/test_erd_gates.py
import re

from fls.db.erd_policy import BA_ERD_DOC, ERD_ISLANDS


def _entity_trong_doc_BA() -> set[str]:
    """Doc khoi ```mermaid erDiagram trong 05_DATA_DICTIONARY_ERD.md."""
    txt = BA_ERD_DOC.read_text(encoding="utf-8")
    khoi = re.search(r"```mermaid\s*\nerDiagram\n(.*?)```", txt, re.S)
    assert khoi, "khong tim thay khoi erDiagram trong doc BA"
    return set(re.findall(r"^\s{4}(\w+)\s*\{", khoi.group(1), re.M))


def test_g_erd_2_moi_bang_trong_code_deu_co_tren_ERD_BA():
    """Chieu 1: them bang ma quen ve len ERD => do."""
    thieu = set(TABLES) - _entity_trong_doc_BA()
    assert not thieu, f"bang co trong code nhung VANG tren ERD cua BA: {sorted(thieu)}"


def test_g_erd_2_moi_entity_tren_ERD_BA_deu_ton_tai_trong_code():
    """Chieu 2: ERD ve entity khong co thuc => do."""
    du = _entity_trong_doc_BA() - set(TABLES)
    assert not du, f"entity tren ERD cua BA nhung KHONG co trong code: {sorted(du)}"


def test_g_erd_3_moi_bang_toi_duoc_fls_itl_hoac_khai_island():
    """G-ERD-3: khong co bang mo coi lang le."""
    canh: dict[str, set[str]] = {}
    for n, t in TABLES.items():
        if t.kind == "view":
            continue
        canh[n] = {c.fk.split(".")[0] for c in t.columns if c.fk} | {n}
    # lan truyen: bang nao noi duoc voi fls_itl qua FK (ke ca gian tiep, hai chieu)
    ke = {n: set() for n in canh}
    for n, ds in canh.items():
        for d in ds:
            if d in ke:
                ke[n].add(d)
                ke[d].add(n)
    toi_duoc, hang_doi = set(), ["fls_itl"]
    while hang_doi:
        cur = hang_doi.pop()
        if cur in toi_duoc:
            continue
        toi_duoc.add(cur)
        hang_doi.extend(ke.get(cur, ()))
    mo_coi = set(canh) - toi_duoc
    assert mo_coi <= ERD_ISLANDS, (
        f"bang khong noi voi fls_itl va chua khai island: {sorted(mo_coi - ERD_ISLANDS)}")


def test_g_erd_3_moi_island_phai_co_ly_do_bang_chu():
    for n in ERD_ISLANDS:
        assert TABLES[n].island_reason.strip(), f"{n} khai island nhung khong co ly do"
```

- [x] **Step 2: Chạy để thấy nó đỏ**

Run: `pytest tests/db/test_erd_gates.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'fls.db.erd_policy'`

- [x] **Step 3: Viết policy**

```python
# fls/db/erd_policy.py
"""Chinh sach cong ERD: doc BA nao la doi chieu, bang nao duoc phep khong noi FK."""

from __future__ import annotations

import pathlib

BA_ERD_DOC = pathlib.Path(
    __file__).resolve().parents[2] / "docs" / "05_DATA_DICTIONARY_ERD.md"

# Bang KHONG noi FK voi fls_itl. Moi ten o day PHAI co island_reason trong schema.
ERD_ISLANDS: frozenset[str] = frozenset({
    "fls_mapping_master",   # tra theo gia tri hd; hd co the UNMAPPED nen khong FK duoc
    "fls_source",           # manifest pipeline, khong gan dong nao
})
```

- [x] **Step 4: Đồng bộ ERD của BA — chỗ drift được đóng**

Thay khối `erDiagram` trong `02_BA/05_DATA_DICTIONARY_ERD.md` bằng nội dung `ERD-CONTRACT.mmd`, đặt `docs/05_DATA_DICTIONARY_ERD.md` là bản đồng bộ trong repo `FLS` *(symlink hoặc bước copy trong CI)*. Sửa luôn hai chỗ nói trái nhau:

- Bỏ câu *"`ITL_LEDGE` là **view kết hợp** RAW + bút toán, không phải bảng"* → thay bằng *"`fls_itl` là **một bảng ba lớp**; `raw_frozen=true` là ranh giới bất biến (`INV-I03`); bút toán ở `fls_adjustment` append-only"*.
- Bỏ `fls_id_counter` khỏi §6 và ghi lý do *(`GAP-PLAN-02`)*.

Bump `05_DATA_DICTIONARY_ERD` lên **v0.7** kèm changelog nêu rõ: ERD từ nay **sinh ra từ code**, sửa tay là bị cổng G-ERD-1 bắt.

- [x] **Step 5: Chạy cả 4 cổng**

Run: `pytest tests/db -v && lint-imports`
Expected: all passed · `Contracts: 2 kept, 0 broken`

- [x] **Step 6: Commit**

```bash
git add fls/db/erd_policy.py tests/db/test_erd_gates.py docs/05_DATA_DICTIONARY_ERD.md
git commit -m "feat(db): G-ERD-2 day du entity hai chieu + G-ERD-3 bang phai co ket noi"
```

---

### Task 7: Trigger cưỡng chế `INV-I03` + `INV-I04a` trên PG thật

**Files:**
- Create: `fls/db/triggers.py`, `fls/db/pg_migrate.py`, `docker-compose.yml`
- Test: `tests/db/test_invariants_pg.py`

**Interfaces:**
- Consumes: `TABLES`, `CREATE_ORDER`, `SEQUENCES` (Task 4); `render_ddl` (Task 2)
- Produces: `TRIGGER_DDL: tuple[str, ...]` · `statements() -> list[str]`

- [x] **Step 1: Viết test đỏ (đánh dấu `pg`)**

```python
# tests/db/test_invariants_pg.py
import os

import psycopg
import pytest

pytestmark = pytest.mark.pg

DSN = os.environ.get("PG_DSN", "postgresql://fls:fls@localhost:5433/fls")


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _chen_mot_dong(conn, raw_frozen: bool) -> int:
    with conn.cursor() as cur:
        cur.execute("INSERT INTO fls_le (le_code, le_name) VALUES ('SGO1','SGO1') "
                    "ON CONFLICT DO NOTHING")
        cur.execute("""
            INSERT INTO fls_itl (content_key, source_system, source_sheet, source_row,
                                 run_id, contract_version, canon_version, mapping_version,
                                 raw_frozen, canon)
            VALUES (%s,'P100','Bank',1,'r1','v1.0','v1.0','v1.0',%s,'[]'::jsonb)
            RETURNING itl_id""", (f"k-{raw_frozen}-{os.urandom(4).hex()}", raw_frozen))
        return cur.fetchone()[0]


def test_inv_i03_raw_frozen_thi_cam_update(conn):
    iid = _chen_mot_dong(conn, raw_frozen=True)
    with pytest.raises(psycopg.errors.RaiseException):
        with conn.cursor() as cur:
            cur.execute("UPDATE fls_itl SET memo='sua' WHERE itl_id=%s", (iid,))


def test_inv_i03_raw_frozen_thi_cam_delete(conn):
    iid = _chen_mot_dong(conn, raw_frozen=True)
    with pytest.raises(psycopg.errors.RaiseException):
        with conn.cursor() as cur:
            cur.execute("DELETE FROM fls_itl WHERE itl_id=%s", (iid,))


def test_inv_i04a_itl_id_khong_bao_gio_doi(conn):
    iid = _chen_mot_dong(conn, raw_frozen=False)
    with pytest.raises(psycopg.errors.RaiseException):
        with conn.cursor() as cur:
            cur.execute("UPDATE fls_itl SET itl_id=%s WHERE itl_id=%s", (iid + 9999, iid))


def test_itl_id_tang_don_khong_trung(conn):
    a = _chen_mot_dong(conn, raw_frozen=False)
    b = _chen_mot_dong(conn, raw_frozen=False)
    assert b > a, "SEQUENCE phai tang don — day la cho fps_id_counter tung sinh id trung"


def test_content_key_trung_thi_bi_chan(conn):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO fls_le (le_code, le_name) VALUES ('SGO1','SGO1') "
                    "ON CONFLICT DO NOTHING")
        sql = """INSERT INTO fls_itl (content_key, source_system, source_sheet, source_row,
                     run_id, contract_version, canon_version, mapping_version, canon)
                 VALUES ('trung','P100','Bank',1,'r1','v1.0','v1.0','v1.0','[]'::jsonb)"""
        cur.execute(sql)
        with pytest.raises(psycopg.errors.UniqueViolation):
            cur.execute(sql)
```

- [x] **Step 2: Dựng PG rồi chạy để thấy nó đỏ**

```yaml
# docker-compose.yml
services:
  pg:
    image: postgres:16
    environment:
      POSTGRES_USER: fls
      POSTGRES_PASSWORD: fls
      POSTGRES_DB: fls
    ports: ["5433:5432"]
```

Run: `docker compose up -d && pytest tests/db/test_invariants_pg.py -v -m pg`
Expected: FAIL — `relation "fls_itl" does not exist`

- [x] **Step 3: Viết trigger + migration runner**

```python
# fls/db/triggers.py
"""Cuong che bat bien o tang DB. Doc: 04_DB_IMPLEMENTATION §5."""

from __future__ import annotations

TRIGGER_DDL: tuple[str, ...] = (
    # INV-I03: raw_frozen la diem khong quay lui
    """
CREATE OR REPLACE FUNCTION fls_chan_sua_dong_dong_bang() RETURNS trigger AS $$
BEGIN
  IF OLD.raw_frozen THEN
    RAISE EXCEPTION 'INV-I03: itl_id % da raw_frozen, sua chi bang but toan moi', OLD.itl_id;
  END IF;
  RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END $$ LANGUAGE plpgsql;""",
    """
DROP TRIGGER IF EXISTS trg_fls_itl_inv_i03 ON fls_itl;
CREATE TRIGGER trg_fls_itl_inv_i03 BEFORE UPDATE OR DELETE ON fls_itl
FOR EACH ROW EXECUTE FUNCTION fls_chan_sua_dong_dong_bang();""",
    # INV-I04a: danh tinh dong bang
    """
CREATE OR REPLACE FUNCTION fls_chan_doi_itl_id() RETURNS trigger AS $$
BEGIN
  IF NEW.itl_id <> OLD.itl_id THEN
    RAISE EXCEPTION 'INV-I04a: itl_id dong bang, khong duoc doi (% -> %)',
      OLD.itl_id, NEW.itl_id;
  END IF;
  RETURN NEW;
END $$ LANGUAGE plpgsql;""",
    """
DROP TRIGGER IF EXISTS trg_fls_itl_inv_i04a ON fls_itl;
CREATE TRIGGER trg_fls_itl_inv_i04a BEFORE UPDATE ON fls_itl
FOR EACH ROW EXECUTE FUNCTION fls_chan_doi_itl_id();""",
)
```

```python
# fls/db/pg_migrate.py
"""Ap DDL Postgres. Idempotent.

  export PG_DSN='postgresql://fls:fls@localhost:5433/fls'
  python -m fls.db.pg_migrate --dry-run   # offline, khong can DB
  python -m fls.db.pg_migrate             # ap that
"""

from __future__ import annotations

import argparse
import os
import sys

from fls.db.render import render_ddl
from fls.db.schema import CREATE_ORDER, SEQUENCES, TABLES
from fls.db.triggers import TRIGGER_DDL


def statements() -> list[str]:
    """Sequence -> bang/view theo CREATE_ORDER -> trigger."""
    out = [s + ";" for s in SEQUENCES.values()]
    out += [render_ddl(TABLES[n]) for n in CREATE_ORDER]
    out += [s.strip() for s in TRIGGER_DDL]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    stmts = statements()
    if args.dry_run:
        print("\n\n".join(stmts))
        return 0
    dsn = os.environ.get("PG_DSN")
    if not dsn:
        print("thieu PG_DSN", file=sys.stderr)
        return 2
    import psycopg
    with psycopg.connect(dsn, autocommit=True) as conn, conn.cursor() as cur:
        for s in stmts:
            cur.execute(s)
    print(f"da ap {len(stmts)} cau DDL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Thêm `fls.db` vào ngoại lệ import-linter contract 1 *(chỉ `fls/repo/` và `fls/db/` được chạm `psycopg`)*.

- [x] **Step 4: Áp rồi chạy để thấy nó xanh**

Run: `python -m fls.db.pg_migrate --dry-run | head -20 && PG_DSN='postgresql://fls:fls@localhost:5433/fls' python -m fls.db.pg_migrate && pytest tests/db -v -m pg`
Expected: 5 passed

- [x] **Step 5: Commit**

```bash
git add fls/db/triggers.py fls/db/pg_migrate.py docker-compose.yml tests/db/test_invariants_pg.py .importlinter
git commit -m "feat(db): trigger INV-I03/I04a + pg_migrate, test tren PG that"
```

---

### Task 8: Khoá hợp đồng 14 trường (`INV-I07`)

**Files:**
- Create: `fls/contract/__init__.py`, `fls/contract/itl_contract.py`
- Test: `tests/contract/test_itl_contract_v1_lock.py`

**Interfaces:**
- Consumes: `TABLES` (Task 4)
- Produces: `ITL_CONTRACT_V1: tuple[tuple[str, str, str], ...]` — `(ten_truong, kieu, cot_excel)`

- [x] **Step 1: Viết test đỏ**

```python
# tests/contract/test_itl_contract_v1_lock.py
from fls.contract.itl_contract import ITL_CONTRACT_V1
from fls.db.schema import TABLES


def test_dung_14_truong():
    assert len(ITL_CONTRACT_V1) == 14


def test_le_la_cot_P_khong_phai_BL():
    """QD-owner-0820: BL trong 6.379 dong, ruong dan ve 0% thang 8/2026."""
    truong = {t[0]: t[2] for t in ITL_CONTRACT_V1}
    assert truong["le"] == "P"
    assert "BL" not in truong.values()


def test_moi_truong_hop_dong_ton_tai_trong_fls_itl():
    cot = {c.name: c for c in TABLES["fls_itl"].columns}
    for ten, kieu, _ in ITL_CONTRACT_V1:
        assert ten in cot, f"hop dong doi {ten} nhung fls_itl khong co"
        assert cot[ten].type.startswith(kieu), f"{ten}: hop dong {kieu}, schema {cot[ten].type}"


def test_doc_theo_TEN_khong_theo_vi_tri():
    """QD-ITL-42: doc theo TEN. Cot Excel chi de doi chieu reader that."""
    assert len({t[0] for t in ITL_CONTRACT_V1}) == 14, "ten truong phai duy nhat"
```

- [x] **Step 2: Chạy để thấy nó đỏ**

Run: `pytest tests/contract -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'fls.contract'`

- [x] **Step 3: Khai báo hợp đồng dạng DATA**

```python
# fls/contract/itl_contract.py
"""ITL-CONTRACT v1.0 — DONG BANG 2026-08-24 (QD-ITL-42).

14 truong, doc THEO TEN. Cot Excel chi de doi chieu reader dang chay.
le = cot P (QD-owner-0820), KHONG phai BL.
Doi file nay la CR loai 3, kem test tuong thich (02_REPO_CONVENTIONS §4.5).
"""

from __future__ import annotations

ITL_CONTRACT_V1: tuple[tuple[str, str, str], ...] = (
    ("doc_date", "date", "A"),
    ("doc_no", "text", "B"),
    ("memo", "text", "C"),
    ("curr", "text", "D"),
    ("ps_no", "numeric", "E"),
    ("ps_co", "numeric", "F"),
    ("acct", "text", "G"),
    ("le", "text", "P"),
    ("itl_id", "bigint", "R"),
    ("hd", "text", "V"),
    ("pay_type", "text", "Z"),
    ("cdt1", "text", "AD"),
    ("svc_start", "date", "AH"),
    ("svc_end", "date", "AL"),
)
```

- [x] **Step 4: Chạy trọn bộ — cả 4 cổng**

Run: `pytest -v && lint-imports && python -m fls.db.erd_export --write && git diff --exit-code ERD-CONTRACT.json`
Expected: all passed · `Contracts: 2 kept, 0 broken` · `git diff` không có thay đổi *(ERD đã đồng bộ)*

- [x] **Step 5: Commit**

```bash
git add fls/contract tests/contract
git commit -m "feat(contract): khoa ITL-CONTRACT v1.0 14 truong theo TEN (INV-I07)"
```

---

## Cổng ra của P0

Chạy được và xanh hết:

```bash
pytest -v                                  # unit + PG (mark pg)
lint-imports                               # ranh gioi module
python -m fls.db.pg_migrate --dry-run      # in tron DDL, offline
python -m fls.db.erd_export --write && git diff --exit-code ERD-CONTRACT.json
```

| Cổng | Nội dung |
|---|---|
| **G-ERD-1** | ERD sinh từ code == ERD đã commit |
| **G-ERD-2** | mọi bảng/view có trên ERD của BA **và** ngược lại |
| **G-ERD-3** | mọi bảng nối được `fls_itl`, hoặc khai `ERD_ISLANDS` kèm lý do |
| **`INV-I07`** | 14 trường hợp đồng khoá, `le` = `P` |
| Bất biến DB | `INV-I03` · `INV-I04a` · `content_key UNIQUE` có test trên PG thật |
| Kỷ luật | **0 dòng luật nghiệp vụ** trong P0; `import-linter` xanh |

## Việc P0 sinh ra cho doc

| Doc | Sửa gì |
|---|---|
| `04_DB_IMPLEMENTATION` → v1.1 | bỏ `fls_id_counter` khỏi §5/§6, ghi lý do FPS đã khai tử pattern (`GAP-PLAN-02`) |
| `05_DATA_DICTIONARY_ERD` → v0.7 | ERD thay bằng bản sinh; bỏ câu *"`ITL_LEDGE` là view"*; ghi ERD từ nay do code sinh (`GAP-PLAN-03`) |
| `11_INVARIANTS` | ghi `INV-I03`/`INV-I04a` đã có cưỡng chế + test, kèm tên test |

## Self-review

**Phủ spec:** `04_DB` §2 lớp C → Task 3 · §3 lớp A → Task 3 + Task 8 · §4 lớp A' → Task 3 · §5 bất biến → Task 7 *(I03/I04a/I04b có test; I10 FK có trong schema; I11/I12/I13/I14 là kiểu cột + NOT NULL, test ở Task 3)* · §6 bảng phụ → Task 4 · §6b DDL mới → Task 4 · §7 kỷ luật migration → Task 7. **Chưa phủ:** `INV-I16` cưỡng chế ở tầng code/DQ *(spec nói rõ là không phải DDL)* → thuộc P1; `GAP-DB-01` thành phần `content_key` → P1 khi có dữ liệu thật để test.

**Quét placeholder:** không có TBD/TODO; mọi step có lệnh chạy và kết quả mong đợi; mọi step code có code thật.

**Nhất quán kiểu:** `Column`/`Table` khai ở Task 2 dùng nguyên ở Task 3/4; `render_ddl` Task 2 → Task 5/7; `render_erd_json`/`render_erd_mermaid` Task 5 → Task 6; `TABLES`/`CREATE_ORDER`/`SEQUENCES` Task 3/4 → Task 5/6/7/8. `ERD_ISLANDS` Task 6 khớp `island_reason` khai ở Task 4.
