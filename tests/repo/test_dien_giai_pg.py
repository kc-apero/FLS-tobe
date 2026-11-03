# -*- coding: utf-8 -*-
"""DIEN GIAI sao ke — no ⛔ KHONG phai thu can NAP, no DA O TRONG KHO.

⭐⭐⭐ `QĐ-ITL-145` · `2026-09-18`. Owner tra loi *"mo"* cho `GAP-NAP-04`
*(mo pham vi nap them cot dien giai)*. ⛔⛔ **Nhung phep do TRUOC KHI LAM cho
thay ⛔ khong co gi de mo — no da mo tu `17/09` va du lieu da nam san trong
kho.**

── BA DIEU DO DUOC `18/09` ────────────────────────────────────────────

    ⓐ `QĐ-ITL-128` *(17/09)* DA cho doc `Description`, ca `6/6` truong.
       `sao_ke.TRUONG_DOC_DUOC == SAU_TRUONG` — ban khai **da co** no.

    ⓑ `fls_itl.memo` van **`0 / 8.387`**, va `canon[2]` la `None`.
       ⇒ Quyet dinh **da doi**, duong ghi **o lai** — dung lop loi
         *"tien de doi o cho khac, phat bieu cu o lai"*, lan nay NGUOC
         chieu: **quyen da mo, ma phan thuc thi dung yen**.

    ⓒ ⭐ Nhung `fls_chup_dong` — **nhip chup moi gio** — DANG giu no:
         anh `152380` · **8.592** dong · **8.589** dong co `Description`.

── ⇒ CACH XU: ⛔ KHONG nap lai, ⛔ KHONG sua so ─────────────────────────

⛔ **Nap lai ⛔ khong giai quyet gi:** `content_key` ⛔ khong chua dien giai,
   nen mot luot nap lai se **bo qua vi trung** va `memo` van rong.
⛔ **`UPDATE fls_itl.memo` thi pham `INV-I08`** — so la sach **chi-them**.

⭐ Dien giai **noi duoc** vao dong so bang `(source_key, dong_so)`:

       noi duoc      8.361 / 8.387  = 99,7%
       co dien giai  8.358 / 8.387  = 99,7%
       ⭐ tien te KHOP 8.358         ⇒ noi **dung dong**, ⛔ khong lech hang

⇒ Mot **khung xem** la du. ⛔ Khong ghi mot o nao, ⛔ khong bat bien nao bi
  dung toi, va no **tu moi theo nhip chup**.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.db.schema import TABLES

pytestmark = pytest.mark.pg


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def test_ban_khai_CO_khung_xem_dien_giai():
    """⛔ Ban khai la nguon su that cua schema — khung xem phai co o do."""
    assert "fls_dien_giai" in TABLES, (
        "⛔ thieu khung xem `fls_dien_giai`. Dien giai sao ke **da nam trong "
        "kho** (`fls_chup_dong`, nhip moi gio) nhung ⛔ khong duong nao noi no "
        "voi mot dong so — nen no vo hinh voi ca man hinh lan luat ghep.")


def test_kho_THAT_co_khung_xem(conn):
    r = conn.execute("select table_name from information_schema.views"
                     " where table_name='fls_dien_giai'").fetchone()
    assert r is not None, "⛔ kho thieu khung xem `fls_dien_giai`"


def test_khung_xem_tra_dung_BA_cot(conn):
    """`itl_id` · `dien_giai` · `chup_id` — ⭐ cot thu ba la TUOI cua cau chu.

    ⛔ Thieu `chup_id` thi man hinh ⛔ khong noi duoc *"cau nay doc luc nao"*,
       va mot cau chu ⛔ khong co tuoi thi ⛔ khong ai biet no con dung khong.
    """
    cot = [r[0] for r in conn.execute(
        "select column_name from information_schema.columns"
        " where table_name='fls_dien_giai' order by ordinal_position")]
    assert cot == ["itl_id", "dien_giai", "chup_id"], cot


def test_KHONG_mot_duong_nao_GHI_vao_fls_itl_memo():
    """⭐⭐ `INV-I08`: dien giai den bang phep NOI, ⛔ khong bang phep GHI.

    ⛔⛔ **Bai nay quet MA NGUON, ⛔ khong dem tren kho — va do la co y.**
    Ban dau toi viet `select count(memo) from fls_itl` == 0; no **do sai thu**:
    kho TEST duoc cac bai khac chen `memo` mot cach hop le, nen phep dem ay
    bat oan. ⇒ Dieu can ghim ⛔ khong phai *"kho co gia tri khong"* ma
    *"co duong GHI nao tro vao `fls_itl.memo` khong"*.

    ⛔ `UPDATE fls_itl ... memo` la duong de nhat de "cho nhanh xong", va no
      pha `INV-I08`: so la sach **chi-them**.
    """
    import pathlib, re
    goc = pathlib.Path(__file__).resolve().parents[2] / "fls"
    xau: list[str] = []
    for f in goc.rglob("*.py"):
        t = f.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"UPDATE\s+fls_itl[^;]*", t, re.I | re.S):
            if re.search(r"memo", m.group(0), re.I):
                xau.append(f"{f.name}: {m.group(0)[:70]}")
    assert not xau, (
        "⛔ co duong GHI vao `fls_itl.memo` — dien giai phai den bang khung "
        "xem `fls_dien_giai` (`INV-I08`): " + " · ".join(xau))


def test_moi_dong_khung_xem_deu_CO_CHU__khong_tra_o_rong(conn):
    """⛔ Mot khung xem tra ve o rong thi no dang noi *'giao dich nay khong co
    noi dung'* — trong khi su that la *'chua doc duoc'*. Hai cau KHAC NHAU.
    """
    n = conn.execute("select count(*) from fls_dien_giai"
                     " where btrim(coalesce(dien_giai,'')) = ''").fetchone()[0]
    assert n == 0, f"⛔ {n} dong tra ve chuoi rong — phai VANG khoi khung xem"


def test_mot_dong_so_chi_co_MOT_dien_giai(conn):
    """⛔⛔ `fls_chup_dong` co **29 anh chup**; noi ⛔ khong chon anh thi mot
    dong so se co **N** dien giai va moi phep dem tren no phong len N lan —
    dung cai bay da can hai lan trong mot ngay `18/09`.
    """
    n = conn.execute("""select count(*) from (
        select itl_id from fls_dien_giai group by itl_id having count(*) > 1) z
    """).fetchone()[0]
    assert n == 0, f"⛔ {n} dong so co NHIEU dien giai — phep noi ⛔ chua chon anh"
