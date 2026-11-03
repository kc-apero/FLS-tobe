# FLS P1 — `ITL-CANON` 36 cột + lớp sổ mỏng · Implementation Plan

> ✅ **ĐÃ CHẠY XONG 2026-08-26** — 5 commit, **107 test xanh** *(86 offline + 21 trên PG 16 container)*, `lint-imports` **4 kept 0 broken**, `pg_verify` khớp, ERD đồng bộ.
>
> ⭐ **Cổng chèn lùi ngày đã thấy đỏ theo cách mạnh nhất**: làm đúng thao tác AS-IS *(đánh số lại `itl_id` theo ngày)* trên PG thật thì **DB từ chối** — `INV-I04a: itl_id dong bang, khong duoc doi (37 -> 136)`. Lỗi AS-IS nay là **bất khả thi ở tầng DB**, không chỉ là "không làm".
> ⭐ **Cổng `content_key` cũng đã thấy đỏ**: nhét `source_row` vào khoá *(cái ai cũng dễ "cho tiện" làm)* → `test_content_key_KHONG_dung_source_row` đỏ ngay.
>
> **Hai chỗ siết hơn plan** *(ghi lại để không hiểu là tuỳ tiện)*:
> 1. `parse_ngay` **không đoán** khi định dạng mơ hồ — `03/01/2026` *(cả hai phần ≤ 12)* thì **NỔ**, buộc gọi rõ `thu_tu='dmy'|'mdy'`. Lý do: 93% dòng nguồn từng bị **hoán ngày↔tháng**, ~181 tỷ sai kỳ; đoán là cách tái lập đúng cái lỗi đó.
> 2. `content_key` có test khoá **không chứa `source_row`** — đưa vị trí dòng vào khoá là tái lập lỗi AS-IS ở một chỗ khác.
>
> **`import-linter` 2 → 4 contract**: mũi tên một chiều về `canon`/`contract` của `01_TECH_DESIGN` §4 nay là **test**, không còn là lời khuyên.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Có khuôn `ITL-CANON` **theo vị trí** và lớp sổ dựng được dòng `fls_itl` từ nó, với cổng quan trọng nhất: **chèn một dòng lùi ngày không làm đổi `itl_id` của bất kỳ dòng nào**.

**Architecture:** `canon` giữ dữ liệu **theo vị trí** (không theo tên — khuôn có 4 cột trùng tên hệt nhau). `ledger` là hàm thuần: canon + ngữ cảnh run → payload để `repo` ghi. Luật `Final` của sổ AS-IS được **tái hiện nguyên văn** vào cột parity, đồng thời **đánh dấu tường minh** ở cột `*_thyt` + `work_status` — đó là cách vừa khớp sổ 100% vừa không nói dối.

**Tech Stack:** Python 3.12 · psycopg v3 · pytest · PostgreSQL 16

**Spec:** `02_BA/05_DATA_DICTIONARY_ERD.md` v0.7 §DD-I01 *(36 cột)* · §DD-I06 *(công thức 4 cột `Classifying→Manual→MID→Final`)* · `11_INVARIANTS` v0.6 · `03_IMPLEMENTATION_PLAN` v1.3 §5.3 · §5.4 *(DoD)*

## Global Constraints

- Kế thừa toàn bộ ràng buộc P0. **4 cổng ERD + `pg_verify` + `import-linter`** phải xanh cuối pha.
- Đổi schema ⇒ **thêm file `000N_*.sql`**; ⛔ không sửa `0001_baseline.sql`.
- `fls/canon/` ⛔ **không import `fls/adapters/`** *(`01_TECH_DESIGN` §4)*; `canon`/`ledger` ⛔ không import `psycopg`.
- ⛔ **Cấm mặc định im lặng** (`INV-I16`). Máy được phép **tái hiện** giá trị mặc định của sổ cũ vào cột parity, nhưng **bắt buộc** kèm `*_thyt = NULL` + `work_status='UNMAPPED'`.
- File ≤ 300 dòng · hàm ≤ 40 dòng.

### ⚠ Hai hệ toạ độ cùng dùng chữ cái A–AL — ghim trước khi code

| Chữ | Trong `ITL-CANON` *(đầu vào, 38 vị trí / 36 trường)* | Trong `ITL Ledge` *(đầu ra, 64 cột)* |
|:--:|---|---|
| `S` | `Budget Code (HDCode)` | `Classifying` của khối 1 |
| `V` | `Status_Final` | **`Final` khối 1** = `hd` |
| `AH` | `MID I DoubleCheck LE` *(1 trong 4 cột trùng tên)* | **`Final` khối 4** = `svc_start` |
| `AL` | `No` | **`Final` khối 5** = `svc_end` |

⛔ **Trộn hai hệ này là lỗi lặng, không nổ.** Nên trong code: canon dùng **chỉ số vị trí** `0..37` và hằng `CANON_*`; Ledge dùng hằng `LEDGE_*`. ⛔ Không hàm nào nhận tham số tên là `col` chung chung.

---

## File Structure

| File | Trách nhiệm |
|---|---|
| `fls/canon/__init__.py` | rỗng |
| `fls/canon/spec.py` | `CanonCol` · `CANON_COLS` **38 vị trí** · tra vị trí↔chữ cái. Không logic |
| `fls/canon/row.py` | `CanonRow` — bọc **tuple 38 phần tử**, truy cập theo vị trí. ⛔ không dict theo tên |
| `fls/canon/validate.py` | `validate()` — phân biệt **thiếu** *(→`UNMAPPED`)* với **sai kiểu** *(→loại, lý do CÓ TÊN)* |
| `fls/ledger/__init__.py` | rỗng |
| `fls/ledger/final_rule.py` | luật `Final` 4 cột của sổ AS-IS, dạng **hàm thuần** + tách parity/`_thyt` |
| `fls/ledger/build.py` | canon + ngữ cảnh run → payload `fls_itl`; `content_key` |
| `fls/repo/__init__.py` · `fls/repo/itl_repo.py` | ghi `fls_itl` — **chỗ duy nhất** chạm DB |
| `tests/canon/*` · `tests/ledger/*` · `tests/repo/test_itl_repo_pg.py` | |

---

### Task 1: `fls/canon/spec.py` — 38 vị trí, 36 trường

**Files:** Create `fls/canon/spec.py`, `fls/canon/__init__.py`; Test `tests/canon/test_spec.py`

**Interfaces:**
- Produces `CanonCol(pos: int, letter: str, name: str, group: str, source: str)`
- Produces `CANON_COLS: tuple[CanonCol, ...]` *(38 phần tử, `pos` 0…37)* · `CANON_36: tuple[CanonCol, ...]` · `pos_of(letter) -> int` · `letter_of(pos) -> str`

- [x] **Step 1: Viết test đỏ**

```python
# tests/canon/test_spec.py
from fls.canon.spec import CANON_36, CANON_COLS, letter_of, pos_of


def test_38_vi_tri_va_36_truong():
    """Nhin thi 38 vi tri (A..AL) nhung chi 36 truong — Z, AA trong.
    Dem sai la lech mapping toan bo khuon (DD-I01 khuyet tat 3)."""
    assert len(CANON_COLS) == 38
    assert len(CANON_36) == 36
    trong = [c.letter for c in CANON_COLS if not c.name]
    assert trong == ["Z", "AA"]


def test_vi_tri_lien_tuc_tu_0():
    assert [c.pos for c in CANON_COLS] == list(range(38))


def test_chu_cai_dung_khuon_bang_tinh():
    assert letter_of(0) == "A" and letter_of(25) == "Z"
    assert letter_of(26) == "AA" and letter_of(37) == "AL"
    assert pos_of("A") == 0 and pos_of("V") == 21 and pos_of("AL") == 37


def test_bon_cot_AH_AK_trung_ten_van_phan_biet_duoc_theo_vi_tri():
    """Khuyet tat 1: 4 cot ten y het nhau => KHONG the tham chieu theo ten."""
    trung = [c for c in CANON_COLS if c.name == "MID I DoubleCheck LE"]
    assert len(trung) == 4
    assert [c.letter for c in trung] == ["AH", "AI", "AJ", "AK"]
    assert len({c.pos for c in trung}) == 4


def test_W_X_va_AB_AC_trung_ten_nhung_khac_nguon():
    """Khuyet tat 2: cung ten, khac nguon (PE vs PI). Tron nham = sai ky P&L."""
    ten = "Thời điểm bắt đầu sử dụng dịch vụ"
    same = [c for c in CANON_COLS if c.name == ten]
    assert [c.letter for c in same] == ["W", "AB"]
    assert {c.source for c in same} == {"[Importrange]PE_Unpivot",
                                        "[Importrange]PI_Unpivot"}


def test_bay_cot_BASE_dung_thu_tu():
    assert [c.name for c in CANON_COLS[:7]] == [
        "Ngày chứng từ", "Số chứng từ", "Diễn giải", "Đơn vị tiền tệ",
        "PS Nợ", "PS Có", "Tài khoản"]


def test_lineage_PM_song_sot():
    """INV-I05 + QD-ITL-20/CR#1: AS-IS vut ID PMLine o chang 8."""
    ten = {c.name for c in CANON_COLS}
    assert {"ID PMLine", "ID PMSlip", "Pháp nhân thanh toán"} <= ten


def test_nhom_dem_dung_DD_I01():
    """7 BASE + 15 (H-V) + 3 (W-Y) + 5 (AB-AF) + 6 (AG-AL) = 36."""
    from collections import Counter
    c = Counter(x.group for x in CANON_36)
    assert sum(c.values()) == 36
    assert c["BASE"] == 7
```

- [x] **Step 2: Chạy để thấy nó đỏ** — `pytest tests/canon -q` → `ModuleNotFoundError`
- [x] **Step 3: Viết `spec.py`** — 38 `CanonCol` chép **nguyên văn** bảng `DD-I01`
- [x] **Step 4: Xanh** — 8 passed
- [x] **Step 5: Commit** — `feat(canon): ITL-CANON 38 vi tri / 36 truong theo VI TRI`

---

### Task 2: `fls/canon/row.py` — dòng canon theo vị trí

**Files:** Create `fls/canon/row.py`; Test `tests/canon/test_row.py`

**Interfaces:** `CanonRow.from_list(vals) -> CanonRow` · `.at(pos)` · `.by_letter(letter)` · `.as_jsonb_list() -> list` · `.__len__() == 38`

- [x] **Step 1: Viết test đỏ**

```python
# tests/canon/test_row.py
import pytest

from fls.canon.row import CanonRow


def _38(**kw):
    v = [None] * 38
    for k, x in kw.items():
        v[int(k[1:])] = x
    return v


def test_dung_38_phan_tu():
    r = CanonRow.from_list(_38(p0="2026-01-31"))
    assert len(r) == 38 and r.at(0) == "2026-01-31"


def test_sai_do_dai_thi_NO_khong_tu_dem_hay_cat():
    """Tu pad/cat la cach mat cot trong im lang."""
    with pytest.raises(ValueError, match="38"):
        CanonRow.from_list([None] * 37)
    with pytest.raises(ValueError, match="38"):
        CanonRow.from_list([None] * 39)


def test_truy_cap_theo_chu_cai():
    r = CanonRow.from_list(_38(p21="Da thanh toan"))
    assert r.by_letter("V") == "Da thanh toan"


def test_bon_gia_tri_AH_AK_khong_de_len_nhau():
    r = CanonRow.from_list(_38(p33="a", p34="b", p35="c", p36="d"))
    assert [r.by_letter(x) for x in ("AH", "AI", "AJ", "AK")] == ["a", "b", "c", "d"]


def test_as_jsonb_list_giu_nguyen_38_o_ke_ca_o_trong():
    r = CanonRow.from_list(_38(p0="x"))
    js = r.as_jsonb_list()
    assert len(js) == 38 and js[25] is None and js[26] is None
```

- [x] **Step 2: Đỏ** · **Step 3: Viết** · **Step 4: Xanh** · **Step 5: Commit**

---

### Task 3: `fls/canon/validate.py` — thiếu ≠ sai kiểu

**Files:** Create `fls/canon/validate.py`; Test `tests/canon/test_validate.py`

**Interfaces:** `validate(row) -> KetQua(loai: list[str], cho: list[str])` — `loai` ⇒ vào `fls_reject` *(lý do CÓ TÊN)*; `cho` ⇒ `work_status='UNMAPPED'`. Cộng `parse_ngay(v) -> date | None` và `parse_so(v)`.

- [x] **Step 1: Viết test đỏ**

```python
# tests/canon/test_validate.py
from datetime import date

from fls.canon.row import CanonRow
from fls.canon.validate import parse_ngay, parse_so, validate


def _row(**kw):
    v = [None] * 38
    v[0] = kw.get("ngay", date(2026, 1, 31))
    v[3] = kw.get("curr", "VND")
    v[4] = kw.get("no", 0)
    v[5] = kw.get("co", 1000)
    v[6] = kw.get("acct", "1121")
    return CanonRow.from_list(v)


def test_ngay_dang_chuoi_duoc_parse():
    """~5.369 dong nguon co ngay dang CHUOI (itl-ledge-text-dates-unmapped)."""
    assert parse_ngay("2026-01-31") == date(2026, 1, 31)
    assert parse_ngay("31/01/2026") == date(2026, 1, 31)
    assert parse_ngay(date(2026, 1, 31)) == date(2026, 1, 31)


def test_ngay_khong_doc_duoc_thi_bao_TEN_ly_do_khong_tra_None_am_tham():
    r = _row(ngay="ba muoi mot")
    kq = validate(r)
    assert any("Ngày chứng từ" in x and "không đọc được" in x for x in kq.loai)


def test_thieu_ngay_la_LOAI_khong_phai_cho():
    """Khong co ngay thi khong biet ky — khong the treo o hang cho."""
    kq = validate(_row(ngay=None))
    assert kq.loai and not any("Ngày chứng từ" in c for c in kq.cho)


def test_no_va_co_cung_rong_la_LOAI():
    kq = validate(_row(no=None, co=None))
    assert any("PS Nợ" in x or "PS Có" in x for x in kq.loai)


def test_thieu_tai_khoan_la_CHO_khong_phai_loai():
    """Thieu thong tin phan loai => hang cho UNMAPPED, khong nem dong tien di."""
    kq = validate(_row(acct=None))
    assert not kq.loai and kq.cho


def test_moi_ly_do_loai_deu_co_ten_khong_duoc_rong():
    """ACC-4: ly do CO TEN."""
    for r in (_row(ngay=None), _row(no=None, co=None), _row(ngay="rac")):
        for x in validate(r).loai:
            assert x.strip() and len(x) > 8, x


def test_parse_so_chap_dinh_dang_ke_toan():
    assert parse_so("1.234.567") == 1234567
    assert parse_so("1,234,567.89") == 1234567.89
    assert parse_so("") is None and parse_so(None) is None


def test_parse_so_rac_thi_NO_khong_tra_0():
    """Tra 0 la cach lam bien mat tien trong im lang."""
    import pytest
    with pytest.raises(ValueError):
        parse_so("mot ty")
```

- [x] **Step 2: Đỏ** · **Step 3: Viết** · **Step 4: Xanh** · **Step 5: Commit**

---

### Task 4: `fls/ledger/final_rule.py` — 5 câu `if`, và chỗ nói thật

**Files:** Create `fls/ledger/final_rule.py`, `fls/ledger/__init__.py`; Test `tests/ledger/test_final_rule.py`

**Interfaces:**
- `MAC_DINH_CUNG = "OGA | GAC - Other"`
- `KHONG_TRA_LOI = "Need to manual input"`
- `CO_INPUT_HERE = "Input here"`
- `tinh_final(classifying, manual) -> KetQuaFinal(parity: str | None, thyt: str | None, may_tu_bia: bool)`
- `NAM_KHOI: tuple[tuple[str, str], ...]` — `(ten_truong, ten_truong_thyt)` cho 5 khối

★ Luật AS-IS *(`DD-I06`, đọc từ công thức thật)*:

```
MID   = if(T="" và S<>"Need to manual input", S,
           if(T="Input here", "OGA | GAC - Other", T))     ← MẶC ĐỊNH CỨNG
Final = if(or(S="Need to manual input", len(S)=0), MID, S)
```

⭐ **`Final` chỉ có thể khác `Classifying` khi `Classifying` rỗng hoặc thất bại** — hằng đúng của công thức, không phải phát hiện. Đo tỷ lệ `Classifying ≠ Final` là đo một điều tất yếu.

⭐ **Chỗ nói thật:** khi giá trị đến từ `MAC_DINH_CUNG`, `parity` **vẫn mang** nó *(để khớp sổ 100% từng ô — `QĐ-ITL-35`)* nhưng `thyt = None` và `may_tu_bia = True` *(→ `work_status='UNMAPPED'`)*. ⚠ `AUD-12`: `thyt` **chỉ** biến giá trị **máy tự bịa** thành `None`; ⛔ **không bao giờ** chạm giá trị người gõ.

- [x] **Step 1: Viết test đỏ**

```python
# tests/ledger/test_final_rule.py
from fls.ledger.final_rule import (
    CO_INPUT_HERE,
    KHONG_TRA_LOI,
    MAC_DINH_CUNG,
    NAM_KHOI,
    tinh_final,
)


def test_dung_nam_khoi():
    assert len(NAM_KHOI) == 5
    assert [a for a, _ in NAM_KHOI] == [
        "hd", "pay_type", "cdt1", "svc_start", "svc_end"]
    assert all(b == a + "_thyt" for a, b in NAM_KHOI)


def test_may_tra_loi_duoc_thi_dung_ket_qua_may():
    kq = tinh_final("NB | Lưu chuyển nội bộ", "")
    assert kq.parity == "NB | Lưu chuyển nội bộ"
    assert kq.thyt == "NB | Lưu chuyển nội bộ"
    assert kq.may_tu_bia is False


def test_may_khong_tra_loi_va_nguoi_da_go_thi_dung_cua_nguoi():
    kq = tinh_final(KHONG_TRA_LOI, "SHQ2 | Headquarters2")
    assert kq.parity == "SHQ2 | Headquarters2"
    assert kq.thyt == "SHQ2 | Headquarters2", "AUD-12: KHONG duoc cham gia tri nguoi go"
    assert kq.may_tu_bia is False


def test_o_van_con_co_Input_here_thi_parity_mang_mac_dinh_NHUNG_thyt_la_None():
    """★ Cho nay la ca thiet ke: vua khop so 100%, vua khong noi doi."""
    kq = tinh_final(KHONG_TRA_LOI, CO_INPUT_HERE)
    assert kq.parity == MAC_DINH_CUNG, "phai khop so cu tung o (QD-ITL-35)"
    assert kq.thyt is None, "may tu bia => KHONG vao parity that"
    assert kq.may_tu_bia is True


def test_classifying_rong_va_khong_ai_go_thi_may_tu_bia():
    kq = tinh_final("", CO_INPUT_HERE)
    assert kq.parity == MAC_DINH_CUNG and kq.thyt is None and kq.may_tu_bia


def test_ca_hai_rong_thi_khong_bia_ra_gi_ca():
    """INV-I16: khong suy duoc thi de trong TUONG MINH, khong gan mac dinh."""
    kq = tinh_final("", "")
    assert kq.parity is None and kq.thyt is None
    assert kq.may_tu_bia is False


def test_final_khong_bao_gio_khac_classifying_khi_classifying_co_gia_tri():
    """Hang dung cua cong thuc (DD-I06)."""
    for s in ("A", "B | C", "202410"):
        for t in ("", "gi cung duoc", CO_INPUT_HERE):
            assert tinh_final(s, t).parity == s
```

- [x] **Step 2: Đỏ** · **Step 3: Viết** · **Step 4: Xanh** · **Step 5: Commit**

---

### Task 5: `fls/ledger/build.py` — 6 chép · 1 join · content_key

**Files:** Create `fls/ledger/build.py`; Test `tests/ledger/test_build.py`

**Interfaces:**
- `NgucCanh(run_id, contract_version, canon_version, mapping_version, source_system, source_sheet)`
- `content_key(source_system, source_sheet, doc_date, ps_no, ps_co, doc_no, seq_trung) -> str`
- `dung_dong(row, source_row, nc, khoi: dict[str, tuple[str, str]], seq_trung=0) -> dict`

★ `content_key` theo `INV-I04b` — khoá **đối sánh**, ⛔ không phải danh tính.

- [x] **Step 1: Viết test đỏ**

```python
# tests/ledger/test_build.py
from datetime import date

import pytest

from fls.canon.row import CanonRow
from fls.ledger.build import NgucCanh, content_key, dung_dong

NC = NgucCanh(run_id="r1", contract_version="v1.0", canon_version="v1.0",
              mapping_version="v1.0", source_system="P100", source_sheet="Bank")


def _row():
    v = [None] * 38
    v[0], v[1], v[2], v[3] = date(2026, 1, 31), "CT-1", "chuyen tien", "VND"
    v[4], v[5], v[6] = 0, 1000, "1121"
    return CanonRow.from_list(v)


def test_sau_phep_chep_BASE_giu_nguyen_van():
    d = dung_dong(_row(), 7, NC)
    assert d["doc_date"] == date(2026, 1, 31)
    assert (d["doc_no"], d["memo"], d["curr"]) == ("CT-1", "chuyen tien", "VND")
    assert (d["ps_no"], d["ps_co"], d["acct"]) == (0, 1000, "1121")


def test_lineage_va_ba_version_khong_bao_gio_NULL():
    d = dung_dong(_row(), 7, NC)
    for k in ("source_system", "source_sheet", "source_row", "run_id",
              "contract_version", "canon_version", "mapping_version"):
        assert d[k] not in (None, ""), k
    assert d["source_row"] == 7


def test_khong_tu_gan_itl_id():
    """INV-I04a: itl_id do SEQUENCE cua DB cap, lop so KHONG duoc tu danh so."""
    assert "itl_id" not in dung_dong(_row(), 1, NC)


def test_canon_luu_du_38_o():
    assert len(dung_dong(_row(), 1, NC)["canon"]) == 38


def test_content_key_tat_dinh_va_doi_khi_thanh_phan_doi():
    a = content_key("P100", "Bank", date(2026, 1, 31), 0, 1000, "CT-1", 0)
    assert a == content_key("P100", "Bank", date(2026, 1, 31), 0, 1000, "CT-1", 0)
    assert a != content_key("P100", "Bank", date(2026, 1, 31), 0, 1000, "CT-1", 1)
    assert a != content_key("Cash", "Bank", date(2026, 1, 31), 0, 1000, "CT-1", 0)


def test_hai_dong_trung_noi_dung_phai_khac_khoa_nho_seq_trung():
    """281 dong trung + 103 dong khong co so chung tu => khoa noi dung MOT MINH
    khong du lam danh tinh (DD-I05)."""
    d0 = dung_dong(_row(), 1, NC, seq_trung=0)
    d1 = dung_dong(_row(), 2, NC, seq_trung=1)
    assert d0["content_key"] != d1["content_key"]


def test_work_status_UNMAPPED_khi_may_tu_bia():
    from fls.ledger.final_rule import CO_INPUT_HERE, KHONG_TRA_LOI, MAC_DINH_CUNG
    khoi = {"hd": (KHONG_TRA_LOI, CO_INPUT_HERE)}
    d = dung_dong(_row(), 1, NC, khoi=khoi)
    assert d["hd"] == MAC_DINH_CUNG and d["hd_thyt"] is None
    assert d["work_status"] == "UNMAPPED"


def test_work_status_ok_khi_khong_co_gi_bia():
    d = dung_dong(_row(), 1, NC, khoi={"hd": ("NB | Noi bo", "")})
    assert d["hd"] == "NB | Noi bo" and d["hd_thyt"] == "NB | Noi bo"
    assert d["work_status"] == "ok"


def test_khoi_ten_la_khong_thuoc_5_khoi_thi_NO():
    with pytest.raises(ValueError, match="khong thuoc 5 khoi"):
        dung_dong(_row(), 1, NC, khoi={"khong_co_that": ("a", "b")})
```

- [x] **Step 2: Đỏ** · **Step 3: Viết** · **Step 4: Xanh** · **Step 5: Commit**

---

### Task 6: `fls/repo/itl_repo.py` + ⭐ CỔNG CHÈN LÙI NGÀY

**Files:** Create `fls/repo/__init__.py`, `fls/repo/itl_repo.py`; Test `tests/repo/test_itl_repo_pg.py`

**Interfaces:** `chen(conn, payloads: list[dict]) -> list[int]` *(trả `itl_id` theo thứ tự)* · `chen_mot(conn, payload) -> int`

★ **Đây là cổng quan trọng nhất của cả P1.** AS-IS sinh `itl_id` bằng `="ITL#"&ROW()` trên bảng đã SORT theo ngày ⇒ chèn một dòng lùi ngày **đánh số lại toàn bộ phía dưới**, và đó là gốc của **1.356 dòng `FALSE`** ở vùng AUDIT.

- [x] **Step 1: Viết test đỏ**

```python
# tests/repo/test_itl_repo_pg.py
import os
from datetime import date

import psycopg
import pytest

from fls.canon.row import CanonRow
from fls.ledger.build import NgucCanh, dung_dong
from fls.repo.itl_repo import chen, chen_mot

pytestmark = pytest.mark.pg

DSN = os.environ.get("PG_DSN", "postgresql://fls:fls@localhost:5433/fls")
NC = NgucCanh("r1", "v1.0", "v1.0", "v1.0", "P100", "Bank")


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        with c.cursor() as cur:
            cur.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                        " mapping_version) VALUES ('r1','v1.0','v1.0','v1.0')"
                        " ON CONFLICT DO NOTHING")
        yield c


def _p(ngay: date, no: str, seq: int = 0):
    v = [None] * 38
    v[0], v[1], v[3], v[4], v[5], v[6] = ngay, no, "VND", 0, 1000, "1121"
    return dung_dong(CanonRow.from_list(v), seq + 1, NC, seq_trung=seq)


def test_CHEN_LUI_NGAY_KHONG_LAM_DOI_ID_CUA_DONG_NAO(conn):
    """★★ Cong quan trong nhat P1. AS-IS dung ="ITL#"&ROW() tren bang SORT theo
    ngay => chen lui ngay danh so lai toan bo phia duoi (1.356 dong FALSE)."""
    import uuid
    lo = uuid.uuid4().hex[:8]
    ids = chen(conn, [_p(date(2026, 3, 1), f"{lo}-a"),
                      _p(date(2026, 3, 2), f"{lo}-b"),
                      _p(date(2026, 3, 3), f"{lo}-c")])
    assert len(set(ids)) == 3

    lui = chen_mot(conn, _p(date(2026, 1, 1), f"{lo}-lui"))

    with conn.cursor() as cur:
        cur.execute("SELECT itl_id FROM fls_itl WHERE doc_no = ANY(%s) ORDER BY doc_no",
                    ([f"{lo}-a", f"{lo}-b", f"{lo}-c"],))
        sau = [r[0] for r in cur.fetchall()]
    assert sau == sorted(ids), "chen lui ngay DA LAM DOI id — dung loi AS-IS"
    assert lui > max(ids), "id cap theo thu tu VAO SO, khong theo ngay"


def test_content_key_trung_bi_chan_o_DB(conn):
    import uuid
    p = _p(date(2026, 2, 2), uuid.uuid4().hex[:8])
    chen_mot(conn, p)
    with pytest.raises(psycopg.errors.UniqueViolation):
        chen_mot(conn, dict(p))


def test_repo_khong_phat_UPDATE_hay_DELETE_len_fls_itl():
    """INV-I08: ghi la THEM. Quet ma nguon, khong doan."""
    import pathlib
    src = pathlib.Path("fls/repo/itl_repo.py").read_text(encoding="utf-8").upper()
    assert "UPDATE FLS_ITL" not in src
    assert "DELETE FROM FLS_ITL" not in src


def test_chen_lo_rong_khong_no_va_khong_ghi_gi(conn):
    assert chen(conn, []) == []
```

- [x] **Step 2: Đỏ** · **Step 3: Viết** — `INSERT … RETURNING itl_id`, tham số hoá, ⛔ không nối chuỗi SQL
- [x] **Step 4: Xanh** — 4 passed
- [x] **Step 5: Commit**

---

### Task 7: Cổng cuối pha + đồng bộ doc

- [x] **Step 1: Cập nhật `.importlinter`** — thêm `fls.canon`, `fls.ledger` vào `source_modules` của contract 1 *(cấm chạm `psycopg`)*; thêm contract 3: `fls.canon` ⛔ không import `fls.adapters`/`fls.ledger`/`fls.repo`
- [x] **Step 2: Chạy trọn 5 cổng**

```bash
pytest -q && lint-imports
PG_DSN=… python -m fls.db.pg_migrate            # ap + tu verify
python -m fls.db.erd_export --write && git diff --exit-code ERD-CONTRACT.json
```

- [x] **Step 3: Đồng bộ doc** — `BA-05` ghi `ITL-CANON` đã có code + tên test; `DEV-03` §2 P1 → ✅ và §5.3/§5.4 đánh dấu xong; `ORC-06` bump
- [x] **Step 4: Commit + push**

---

## Cổng ra của P1

| Cổng | Nội dung |
|---|---|
| ⭐ **Chèn lùi ngày** | `test_CHEN_LUI_NGAY_KHONG_LAM_DOI_ID_CUA_DONG_NAO` |
| `content_key` | `UNIQUE` chặn ở DB; đổi thành phần ⇒ đổi khoá |
| **38 vị trí / 36 trường** | 4 cột `AH–AK` trùng tên vẫn phân biệt được |
| **Thiếu ≠ sai kiểu** | thiếu → hàng chờ; sai kiểu → loại **kèm lý do CÓ TÊN** |
| ⭐ **Nói thật** | máy tự bịa ⇒ `parity` khớp sổ **nhưng** `*_thyt = NULL` + `UNMAPPED` |
| 4 cổng ERD + `pg_verify` + `import-linter` | xanh |
| **Đã thấy đỏ** | ít nhất một cổng của pha bị cố tình làm đỏ, có commit chứng minh |

## Ngoài phạm vi P1 — nói rõ để không ai tưởng thiếu

| Việc | Vì sao chưa |
|---|---|
| **Nguồn của `Manual input`** trong 5 khối | Đó là **ô người gõ** sống trong `ITL Ledge`. P1 làm **luật** dạng hàm thuần; **dây nối** vào ô thật thuộc P2 *(oracle đọc sổ gốc)* và P5 *(app thu ô gõ)* |
| Adapter A–F | P2 · P3 |
| `seq_trung` tính tự động cho dòng trùng trong cùng lô | cần dữ liệu thật để chốt quy tắc thứ tự — `GAP-DB-01`; P1 nhận `seq_trung` như **tham số tường minh**, ⛔ không tự đoán |

## Self-review

**Phủ spec:** `DD-I01` 36 cột → Task 1–2 · ba khuyết tật đặt tên → Task 1 *(4 test riêng)* · `INV-I11` ngày → Task 3 · `ACC-4` lý do có tên → Task 3 · `DD-I06` công thức `Final` → Task 4 · `QĐ-ITL-35` cột song song → Task 4–5 · `AUD-12` không chạm giá trị người gõ → Task 4 · `INV-I04a` id đóng băng → Task 6 · `INV-I04b` `content_key` → Task 5–6 · `INV-I05`/`I12` lineage → Task 5 · `INV-I08` append-only → Task 6.

**Quét placeholder:** không có TBD; mọi step có lệnh và kết quả mong đợi; mọi step code có code thật.

**Nhất quán kiểu:** `CanonRow` (Task 2) dùng ở Task 3/5/6 · `tinh_final`/`NAM_KHOI` (Task 4) dùng ở Task 5 · `NgucCanh`/`dung_dong` (Task 5) dùng ở Task 6 · `pos_of`/`letter_of` (Task 1) dùng ở Task 2.
