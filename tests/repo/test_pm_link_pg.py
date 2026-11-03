"""Cong bang noi `fls_pm_link` — hinh `B` DAU DUOC, va tien khong sai mot dong.

⛔⛔ Bai quan trong nhat o day chay tren **HIEN VAT DA DO** (`pm_join.json`:
3.703 dong lenh × 9.992 dong bank, checksum ghim), ⛔ khong tren dau vao tu bia.
Ly do: cong chung **#8** — *"101 phep thu tu bia deu xanh, mot cu chay that lam
do 6 lo"*. Dau vao tu bia thi sach, va sach thi khong chung minh duoc gi.

★ Truoc 27/08, **27 dong hinh `B`** (mot lan chuyen tra N dong lenh) phai vao
hang cho **kem ly do co ten** vi mot cot `pm_line_id` giu duoc mot moi noi.
Bai `test_hinh_B_DAU_DUOC_vao_bang_noi` la chung cu chung do het.
"""
from __future__ import annotations

import json
import uuid
from decimal import Decimal as D
from pathlib import Path

import psycopg
import pytest

from fls.adapters.pm_join import DongBank, DongPM, canon_ref
from fls.db.kho import dsn_test
from fls.ledger.build import NgucCanh
from fls.repo.chay_nap import chen_moi_noi, kiem_tong_moi_noi

pytestmark = pytest.mark.pg

HIEN_VAT = Path(__file__).resolve().parents[1] / "fixture" / "pm_join.json"
DSN = dsn_test()


@pytest.fixture(scope="module")
def that() -> dict:
    d = json.loads(HIEN_VAT.read_text(encoding="utf-8"))
    return {
        "bank": [DongBank(x["dong"], canon_ref(x["ref_tho"]), D(x["tien"]), x["cur"])
                 for x in d["bank"]],
        "pm": [DongPM(x["dong"], x["slip"], x["line"],
                      D(x["tien"]) if x["tien"] else None, x["cur"], x["status"],
                      canon_ref(x["ref_tho"]), x["hd"] or None, x["cdt1"] or None)
               for x in d["pm"]],
    }


def _noi_tu_hien_vat(that: dict):
    """Chay `ghep_pm` bang duong `xep_ca_lat` tren hien vat, tra dict moi noi."""
    from fls.adapters.pm_join import moi_noi, xep_ca_lat
    nhom, _tk = xep_ca_lat(that["bank"], that["pm"])
    noi: dict[int, list[tuple[str, D, str]]] = {}
    for n in nhom:
        if n.ghep_duoc:
            for dong, line, tien in moi_noi(n):
                noi.setdefault(dong, []).append((line, tien, n.hinh))
    return noi


# ------------------------------------------------------------------ hinh B
def test_hinh_B_DAU_DUOC_vao_bang_noi(that):
    """★★ 27 dong hinh `B` nay CO moi noi, va mot dong mang NHIEU moi noi."""
    noi = _noi_tu_hien_vat(that)
    b = {d: ms for d, ms in noi.items() if ms and ms[0][2] == "B"}
    assert len(b) == 29, f"hinh B phai la 29 dong, do duoc {len(b)}"
    nhieu = [d for d, ms in b.items() if len(ms) > 1]
    assert nhieu, "hinh B phai co dong mang NHIEU moi noi — neu khong thi no la A"


def test_TONG_moi_noi_bang_tien_dong_bank_tren_CA_HIEN_VAT(that):
    """⛔ Cong Σ tren toan bo hien vat: ⛔ khong bia ra, ⛔ khong lam mat dong nao."""
    noi = _noi_tu_hien_vat(that)
    tien = {b.dong_sheet: b.tien for b in that["bank"]}
    assert kiem_tong_moi_noi(noi, tien) == []


def test_DONG_SO_va_MOI_NOI_la_HAI_con_so_khac_nhau(that):
    """★★ Hai con so, ⛔ dung goi lan nhau — chinh toi da goi lan mot lan 27/08.

        DONG SO ghep duoc : 2.701  (A 2.272 · B   29 · C 400)  -> ty le ghep
        MOI NOI           : 2.745  (A 2.272 · B   73 · C 400)  -> so dong bang noi

    Lech **44** nam tron o hinh `B`: **29 dong so mang 73 moi noi** (binh quan
    2,5 dong lenh moi dong so; co mot dong chia cho **10** dong lenh).

    ⇒ *"Ty le ghep 27,03%"* la 2.701/9.992 tinh theo **DONG SO** — con dung.
    ⇒ *"2.650 moi noi trong kho"* la so cu, khi hinh `B` **chua dau duoc**.

    ★ Con so truoc khi owner chot dung sai 1.000 VND (27/08): DONG SO **2.677**
    (A 2.256 · B 27 · C 394) · MOI NOI **2.719** · ty le **26,79%**. Dung sai
    cuu **+24 dong**.
    """
    noi = _noi_tu_hien_vat(that)
    dong_theo_hinh: dict[str, int] = {}
    link_theo_hinh: dict[str, int] = {}
    for ms in noi.values():
        h = ms[0][2]
        dong_theo_hinh[h] = dong_theo_hinh.get(h, 0) + 1
        link_theo_hinh[h] = link_theo_hinh.get(h, 0) + len(ms)

    assert dong_theo_hinh == {"A": 2272, "B": 29, "C": 400}
    assert sum(dong_theo_hinh.values()) == 2701
    assert link_theo_hinh == {"A": 2272, "B": 73, "C": 400}
    assert sum(link_theo_hinh.values()) == 2745
    assert sum(link_theo_hinh.values()) - sum(dong_theo_hinh.values()) == 44


def test_hinh_A_va_C_moi_dong_dung_MOT_moi_noi(that):
    """Neu `A`/`C` mang >1 moi noi thi phan hinh da sai, ⛔ khong phai bang noi sai."""
    noi = _noi_tu_hien_vat(that)
    for dong, ms in noi.items():
        if ms[0][2] in ("A", "C"):
            assert len(ms) == 1, f"dong {dong} hinh {ms[0][2]} co {len(ms)} moi noi"


# ------------------------------------------------------------------ cong Σ
def test_cong_TONG_bat_duoc_tien_BIA_RA():
    noi = {5: [("L1", D("60"), "B"), ("L2", D("50"), "B")]}
    lech = kiem_tong_moi_noi(noi, {5: D("100")})
    assert lech and "Σ moi noi 110" in lech[0]


def test_cong_TONG_bat_duoc_tien_BI_MAT():
    noi = {5: [("L1", D("40"), "B"), ("L2", D("50"), "B")]}
    lech = kiem_tong_moi_noi(noi, {5: D("100")})
    assert lech and "lech -10" in lech[0]


def test_cong_TONG_bat_duoc_moi_noi_KHONG_CO_dong_bank():
    lech = kiem_tong_moi_noi({99: [("L1", D("10"), "A")]}, {})
    assert lech and "KHONG co dong bank" in lech[0]


def test_cong_TONG_kiem_ca_hinh_A_khong_chi_hinh_B():
    """Mot cong chi kiem truong hop kho la cong khong biet minh con song."""
    lech = kiem_tong_moi_noi({5: [("L1", D("99"), "A")]}, {5: D("100")})
    assert lech, "hinh A lech Σ cung phai bi bat"


# ------------------------------------------------------------------ ghi kho
@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _nc(run: str) -> NgucCanh:
    return NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "Transaction Mapping L1")


def _mot_dong_so(conn, run: str) -> int:
    """Chen mot dong so toi thieu de co `itl_id` that ma treo moi noi vao."""
    with conn.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                    " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')"
                    " ON CONFLICT DO NOTHING", (run,))
        cur.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon)"
            " VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb)"
            " RETURNING itl_id", (uuid.uuid4().hex, run))
        return cur.fetchone()[0]


def test_chen_moi_noi_ghi_duoc_N_moi_noi_cho_MOT_dong_so(conn):
    run = "T-" + uuid.uuid4().hex[:8]
    itl_id = _mot_dong_so(conn, run)
    n = chen_moi_noi(conn, _nc(run), [
        (itl_id, "PM1-1", D("60.00"), "B"),
        (itl_id, "PM1-2", D("40.00"), "B"),
    ])
    assert n == 2
    r = conn.execute("select sum(amount), count(*) from fls_pm_link where itl_id=%s",
                     (itl_id,)).fetchone()
    assert r == (D("100.00"), 2)


def test_chen_lai_KHONG_nhan_doi_moi_noi(conn):
    """⛔ Khoa `(itl_id, pm_line_id)` + ON CONFLICT DO NOTHING: chay lai khong nhan ban.

    Khoa hai cot nay chi khai duoc sau khi dong `GAP-DB-P0-03` (27/08).
    """
    run = "T-" + uuid.uuid4().hex[:8]
    itl_id = _mot_dong_so(conn, run)
    m = [(itl_id, "PM1-1", D("100.00"), "A")]
    chen_moi_noi(conn, _nc(run), m)
    chen_moi_noi(conn, _nc(run), m)
    assert conn.execute("select count(*) from fls_pm_link where itl_id=%s",
                        (itl_id,)).fetchone()[0] == 1


def test_bang_noi_TU_CHOI_moi_noi_tro_toi_dong_so_KHONG_TON_TAI(conn):
    """FK ve `fls_itl` — moi noi treo lo lung la moi noi mat dau vet (`INV-I05`)."""
    run = "T-" + uuid.uuid4().hex[:8]
    with conn.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                    " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')"
                    " ON CONFLICT DO NOTHING", (run,))
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        chen_moi_noi(conn, _nc(run), [(-999, "PM1-1", D("1.00"), "A")])
