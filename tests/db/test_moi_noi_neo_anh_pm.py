# -*- coding: utf-8 -*-
"""`fls_pm_link` phai NEO duoc vao ANH LENH CHI da dung luc ghep.

⛔⛔ **Vi sao bai nay ton tai — do duoc, ⛔ khong phai mot lo ngai.**

`fls_pm_line` co khoa chinh **ghep doi** `(run_id, pm_line_id)`: moi cu chup
giu mot ban cua cung mot dong lenh. Do `2026-09-18` tren kho that:

    22 anh PM  ·  3.772 dong lenh THAT  ·  82.984 dong luu   =>  22,0 ban sao
    moi noi that 2.262  ->  noi bang `pm_line_id` DON: 49.764  (phong 22,0 lan)

⇒ Mot cau SQL noi hai bang bang khoa DON van **chay trot lot** va tra ve mot
con so **trong hop ly**. Bay nay da can HAI lan trong MOT ngay *(3.486 thay
vi 166 · 49.764 thay vi 2.262)*, ca hai deu ⛔ khong co canh bao nao.

⛔ Va cot `run_id` san co ⛔ **KHONG** dung duoc lam ve thu hai cua khoa: no
mang **HAI nghia** tuy duong ghi —

    `chay_nap.chen_moi_noi`  ghi `nc.run_id`  = lan NAP
    `ghi_tay` (ghep tay)     ghi `run_pm`     = anh LENH CHI

Do tren kho that: ca **2.262** dong deu la lan NAP *(`la_anh_pm=false`,
`la_run_so=true`)* — vi ⛔ chua ai ghep tay lan nao *(`hinh='T'` = 0)*.

⇒ Can mot cot **RIENG** `run_pm`, va bai nay ghim ba dieu ay.

⚠ **Bai nay ⛔ KHONG doi mot `FOREIGN KEY` that.** Backfill `run_pm` cho
2.262 dong cu phai **suy** anh PM hieu luc ngay `10/09`, va mot phep suy
⛔ khong duoc bien thanh rang buoc cung tren du lieu lich su *(`INV-I16`)*.
Bai ghim **cot** + **kieu** + **nghia**; rang buoc de lan sau, khi moi dong
deu do duong ghi moi sinh ra.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.db.schema import TABLES

pytestmark = pytest.mark.pg


def test_ban_khai_CO_cot_run_pm_tren_fls_pm_link():
    """⛔ Ban khai phai co `run_pm` — day la nguon su that cua schema."""
    bang = TABLES["fls_pm_link"]
    ten = {c.name for c in bang.columns}
    assert "run_pm" in ten, (
        "⛔ `fls_pm_link` thieu cot `run_pm`. ⛔ Khong co no thi mot moi noi "
        "⛔ khong noi duoc no dung ANH LENH CHI nao, va moi phep noi sang "
        "`fls_pm_line` phong len dung bang SO ANH PM (do 18/09: 22,0 lan).")


def test_run_pm_KHAC_run_id_va_ca_hai_deu_tro_ve_fls_run():
    """⭐ Hai cot, hai cau hoi khac nhau — ⛔ khong duoc gop lam mot."""
    bang = TABLES["fls_pm_link"]
    cot = {c.name: c for c in bang.columns}
    assert cot["run_id"].fk == "fls_run.run_id"
    assert cot["run_pm"].fk == "fls_run.run_id"
    assert cot["run_pm"] is not cot["run_id"]
    # ⛔ `run_pm` PHAI nullable: 2.262 dong cu ⛔ khong suy nguoc duoc mot
    #    cach chac chan, va `NOT NULL` se buoc toi bia ra mot gia tri.
    assert cot["run_pm"].null is True, (
        "⛔ `run_pm` phai cho `NULL`: dong cu ⛔ khong biet anh PM nao, va "
        "`NULL` o day co nghia THAT — *'moi noi sinh truoc khi cot nay ra doi'*. "
        "Mot `DEFAULT` hay `NOT NULL` se bien *'⛔ khong biet'* thanh mot lo "
        "doan (`INV-I16`).")


@pytest.mark.parametrize("cot", ["run_id", "run_pm"])
def test_kho_THAT_co_du_hai_cot(cot: str):
    """⛔ Ban khai va kho phai noi cung mot chuyen."""
    with psycopg.connect(dsn_test(), autocommit=True) as conn:
        r = conn.execute(
            "select data_type, is_nullable from information_schema.columns "
            "where table_name='fls_pm_link' and column_name=%s", (cot,)).fetchone()
    assert r is not None, f"⛔ kho thieu cot `fls_pm_link.{cot}`"
    assert r[0] == "text"


def test_moi_noi_co_run_pm_thi_run_pm_ay_PHAI_la_mot_anh_PM():
    """⭐⭐ Phep do THAT, ⛔ khong phai rang buoc: dong nao DA khai `run_pm`
    thi `run_pm` ay phai co dong trong `fls_pm_line`.

    ⛔ Dong `NULL` duoc bo qua **co y** — do la 2.262 dong lich su.
    """
    with psycopg.connect(dsn_test(), autocommit=True) as conn:
        lac = conn.execute(
            "select count(*) from fls_pm_link l where l.run_pm is not null "
            "and not exists (select 1 from fls_pm_line p where p.run_id = l.run_pm)"
        ).fetchone()[0]
    assert lac == 0, (
        f"⛔ {lac} moi noi khai `run_pm` tro vao mot lan nap ⛔ KHONG phai anh "
        f"lenh chi. Do la dung cai lech ma cot nay sinh ra de chan.")
