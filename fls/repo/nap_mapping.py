# -*- coding: utf-8 -*-
"""Ghi `Mapping Master` vao kho — DANH MUC, ⛔ khong phai so.

⛔⛔ **Vi sao cho nay duoc `UPDATE` ma `fls/repo/ghi_tay.py` thi khong.**
`INV-I08` (*"chi THEM, ⛔ khong SUA"*) la luat cua **SO**: mot but toan, mot moi
noi, mot su kien — chung la **su viec da xay ra**, va sua chung la viet lai lich
su. `fls_mapping_master` ⛔ khong phai so: no la **ban sao mot DANH MUC** dang
song o Google Sheets. Danh muc thi co **trang thai hien tai**, va cai dung phai
lam la **soi guong** trang thai do.

⇒ Phep nap la **thay the toan bo** *(xoa het roi chen lai, trong MOT giao dich)*,
  ⛔ khong phai `UPSERT` tung dong. Ly do: `UPSERT` ⛔ khong bao gio bo duoc mot
  ma **da bi xoa khoi sheet** — no se song mai trong kho va tiep tuc tra ve mot
  quyet dinh phan bo ma ke toan ⛔ khong con thay o sheet. Do la loai lech im
  lang nhat.

⚠ **Va phai khai ra cai gia cua no:** thay the toan bo nghia la kho ⛔ khong giu
  lich su cua danh muc — hoi *"thang truoc ma nay can phan bo khong"* thi kho
  ⛔ khong tra loi duoc. Ta CHAP NHAN dieu do o buoc nay vi sheet that cung
  ⛔ khong giu lich su ay (`VLOOKUP` doc gia tri hien tai). Muon so phan bo dong
  bang theo ky thi phai mo mot quyet dinh moi — ⛔ khong sua le o day.

⛔ Cho nay ⛔ KHONG ghi `fls_adjustment`/`fls_journal`: nap mot danh muc
  ⛔ khong phai thao tac cua nguoi tren mot dong so. Vet cua no la
  `fls_source` *(`src_type='Mapping'`)* — mot manifest, dung cho man `F06`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from fls.adapters.mapping_master import TRUONG, DongMM

KHOA_NGUON = "Mapping Master"          # `fls_source.source_key`
LOAI_NGUON = "Mapping"                 # `fls_source.src_type`


@dataclass(frozen=True)
class KetQuaNap:
    da_xoa: int
    da_chen: int
    bi_loai: int


def nap_mapping_master(conn, dong: Sequence[DongMM], *, bi_loai: int = 0,
                       ) -> KetQuaNap:
    """Thay the toan bo `fls_mapping_master` bang `dong`, trong MOT giao dich.

    ⛔ NO khi `dong` RONG. Ly do: mot luot doc that bai *(mang chap, quyen bi
    thu, tab doi ten)* cung tra ve mot danh sach rong — va neu ta cu the ma xoa
    thi **mot su co doc bien thanh mot lan xoa sach danh muc**, roi moi phep suy
    phan bo lang le tra `#N/A`. Rong ⇒ ⛔ khong dong den kho.
    """
    if not dong:
        raise ValueError(
            "⛔ danh sach RONG — ⛔ khong nap. Mot luot doc that bai cung tra ve "
            "rong, nen nap rong = xoa sach danh muc vi mot su co mang. Neu "
            "sheet THAT su rong thi do la mot su kien phai bao cho nguoi, "
            "⛔ khong phai mot lan nap")

    cot = ", ".join(TRUONG)
    o = ", ".join(["%s"] * len(TRUONG))
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM fls_mapping_master")
            da_xoa = int(cur.fetchone()[0])
            # ⛔ `DELETE` o day la CO Y va da duoc khai o dau file: day la danh
            # muc soi guong, ⛔ khong phai so.
            cur.execute("DELETE FROM fls_mapping_master")
            cur.executemany(
                f"INSERT INTO fls_mapping_master ({cot}) VALUES ({o})",
                [tuple(getattr(d, t) for t in TRUONG) for d in dong])
            # Vet: manifest nguon cho man `F06`.
            cur.execute(
                "INSERT INTO fls_source (source_key, src_type, last_seen_at,"
                " txn_count) VALUES (%s,%s,now(),%s)"
                " ON CONFLICT (source_key) DO UPDATE SET"
                " last_seen_at = now(), txn_count = EXCLUDED.txn_count,"
                " src_type = EXCLUDED.src_type",
                (KHOA_NGUON, LOAI_NGUON, len(dong)))
    return KetQuaNap(da_xoa=da_xoa, da_chen=len(dong), bi_loai=bi_loai)


def tra_mapping(conn, hd: str | None) -> dict[str, str | None] | None:
    """Tra mot dong theo `hd`. `None` = ⛔ khong tra duoc *(sheet cho `#N/A`)*.

    ⚠ So khoa **KHONG phan biet hoa thuong**, dung nhu `VLOOKUP` cua Sheets —
    xem hai bay ngu nghia o `fls/ledger/allocate.py`. So phan biet hoa thuong o
    day thi may se cho `#N/A` o nhung dong ma sheet that tra duoc gia tri.
    """
    if hd is None or not str(hd).strip():
        return None
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT {', '.join(TRUONG)} FROM fls_mapping_master"
            " WHERE lower(btrim(hd_code)) = lower(btrim(%s))", (str(hd),))
        r = cur.fetchone()
    return None if r is None else dict(zip(TRUONG, r))
