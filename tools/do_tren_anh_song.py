# -*- coding: utf-8 -*-
"""ĐO LẠI HD2 (11 gói) trên ảnh CŨ hoặc ảnh MỚI đóng băng từ nguồn sống *(ISP 3.1.2 · `WO-345`)*.

⭐ Vì sao có tệp này. Chủ 23/11: *"lấy nguồn sống làm chuẩn"* ⇒ đóng băng LẠI mọi ảnh cổng HD1/HD2 đọc, giữ ảnh CŨ
làm BIÊN BẢN *(Đ2 — ⛔ xoá lịch sử)*. Ảnh mới nằm CẠNH ảnh cũ, tên `<ảnh>_<ngày>.json` *(vd `gl_406_20261123.json`)*;
ảnh nào đóng băng lại ra checksum BẰNG ảnh cũ thì ⛔ có tệp mới *(≡ — ⛔ nhân đôi repo)*.

Công cụ này ⛔ viết lại cổng nào: nó chạy CHÍNH đường sản phẩm `tools/do_hd2.chay_goi(gói, dsn, fx="kho")` *(như bài
I2 `tests/tich_hop/test_hd2_xuyen_suot.py`)* với một thay đổi DUY NHẤT — mọi lần MỞ tệp `tests/fixture/**/X.json` được
chuyển sang `X<hậu tố>.json` NẾU tệp ấy có. Chuyển ở tầng `open` *(⛔ vá từng hằng đường)* vì nhiều gói ghép đường từ
thư mục *(`do_hd2_c3d._DA` · `do_hd2_c5c.DA/DV`)* — vá hằng thì sót. Mọi tệp bị chuyển được GHI LẠI và in ra *(Đ4: biết
gói đã đọc ảnh nào)*.

Kho: một kho TEST RIÊNG `fls_wo345_<cu|moi>` dựng lại từ 0 *(`dung_lai_kho_test` — ⛔ kho thật)*, nạp config
y như `_nap_config` của I2 *(IX.FX · IX.PER/ALR/PL · IX.ORG · IX.VEN — đọc từ ảnh qua cùng cơ chế chuyển hướng)*, ký
MỌI tháng tỷ giá bằng `ky_fx` *(actor TEST — ⛔ chữ ký thật; O6/O8 là chủ)*.

    python tools/do_tren_anh_song.py --anh cu                       # 11 gói trên ảnh cũ ⇒ in + JSON
    python tools/do_tren_anh_song.py --anh moi --hau-to _20261123   # 11 gói trên ảnh mới
    python tools/do_tren_anh_song.py --anh moi --hau-to _20261123 --ra /tmp/hd2_moi.json

Exit 0 ⇔ chạy hết 11 gói *(⛔ nghĩa là ĐẠT — `dat` từng gói in riêng)*; 1 ⇔ có gói ⛔ đo được *(ĐỎ có tên)*.
"""
from __future__ import annotations

import argparse
import builtins
import contextlib
import io
import json
import os
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))
FX_DIR = GOC / "tests" / "fixture"
GOI = ("WP-C2", "WP-C3a", "WP-C3b", "WP-C3c", "WP-C3d", "WP-C4a", "WP-C4b", "WP-C4c", "WP-C5a", "WP-C5b", "WP-C5c")
ACTOR = "wo345.do.lai@vi-du.invalid"       # actor TEST — ⛔ chữ ký thật


@contextlib.contextmanager
def chuyen_huong(hau_to: str, da_chuyen: dict[str, str]):
    """Trong khối: mở `tests/fixture/**/X.json` ⇒ `X<hau_to>.json` nếu có. `hau_to` rỗng ⇒ ⛔ chuyển gì."""
    goc_open, goc_io = builtins.open, io.open

    def _doi(f):
        if not hau_to or not isinstance(f, (str, os.PathLike)):
            return f
        p = Path(os.fspath(f))
        try:
            p.resolve().relative_to(FX_DIR)
        except ValueError:
            return f
        if p.suffix != ".json" or p.stem.endswith(hau_to):
            return f
        moi = p.with_name(p.stem + hau_to + ".json")
        if moi.exists():
            da_chuyen[str(p.resolve().relative_to(FX_DIR))] = str(moi.resolve().relative_to(FX_DIR))
            return type(f)(moi) if isinstance(f, Path) else str(moi)
        return f

    def mo(f, *a, **k):
        return goc_open(_doi(f), *a, **k)

    def mo_io(f, *a, **k):
        return goc_io(_doi(f), *a, **k)

    builtins.open, io.open = mo, mo_io
    try:
        yield
    finally:
        builtins.open, io.open = goc_open, goc_io


def _nap_config(dsn: str) -> list[int]:
    """Đúng `_nap_config` của bài I2 + ký mọi tháng IX.FX *(actor TEST)*. Trả danh sách tháng đã ký."""
    import psycopg

    from fls.repo import cau_hinh_repo as chc
    from tools import do_hd2 as h
    from tools import do_hd2_c3c, do_hd2_c5c
    with psycopg.connect(dsn, autocommit=True) as c:
        chc.nap_ix_fx(c, str(h.IX_FX), actor=ACTOR, thang_dau=h.THANG_DAU_FX, nguon="WO-345 · ix_fx")
        do_hd2_c5c.nap_nen_kho(c, actor=ACTOR)
        chc.nap_ix_org(c, str(do_hd2_c3c.CDT_CORRECT), str(do_hd2_c3c.MM), actor=ACTOR)
        chc.nap_ix_ven(c, str(FX_DIR / "cau_hinh" / "ix_ven.json"),
                       duong_cdt1=str(FX_DIR / "cau_hinh" / "cdt_correct.json"), actor=ACTOR)
        thang = [d.yyyymm for d in chc.doc_fx(c).ky]
        for t in thang:
            chc.ky_fx(c, t, actor=ACTOR)
    return thang


def do(anh: str, hau_to: str) -> dict:
    from fls.db.kho import doi_ten_kho, dsn_test, dung_lai_kho_test
    from tools import do_hd2 as h
    dsn = doi_ten_kho(dsn_test(), f"fls_wo345_{anh}")
    dung_lai_kho_test(dsn)
    da_chuyen: dict[str, str] = {}
    khoi: dict[str, dict] = {}
    with chuyen_huong(hau_to if anh == "moi" else "", da_chuyen):
        thang = _nap_config(dsn)
        for g in GOI:
            try:
                k, _dat, _tq, _doc = h.chay_goi(g, dsn, fx="kho")
            except Exception as e:  # noqa: BLE001 — Đ5: gói ⛔ đo được ⇒ khối ĐỎ có tên, ⛔ nổ cả lượt
                k = {"bang": f"HD2.{g}", "goi": g, "dat": False,
                     "ly_do": [f"⛔ đo được: {type(e).__name__}: {' '.join(str(e).split())[:400]}"], "loi_chay": True}
            khoi[g] = k
    return {"anh": anh, "hau_to": hau_to, "kho": dsn.rsplit("/", 1)[-1], "thang_fx_ky": len(thang),
            "da_chuyen": dict(sorted(da_chuyen.items())), "khoi": khoi}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="do_tren_anh_song.py")
    p.add_argument("--anh", choices=("cu", "moi"), required=True)
    p.add_argument("--hau-to", default="_20261123")
    p.add_argument("--ra", default=None, help="ghi JSON kết quả (⛔ ghi hd2_cong.json — việc của do_hd2 --ghi)")
    a = p.parse_args(argv)
    kq = do(a.anh, a.hau_to)
    print(f"══ HD2 × 11 gói trên ảnh {a.anh.upper()} · kho {kq['kho']} · {kq['thang_fx_ky']} tháng FX ký (TEST)")
    print(f"   ảnh chuyển hướng: {len(kq['da_chuyen'])}" + "".join(f"\n     {k} → {v}" for k, v in kq["da_chuyen"].items()))
    loi = 0
    for g, k in kq["khoi"].items():
        loi += bool(k.get("loi_chay"))
        so = {x: k.get(x) for x in ("tong_o", "khop", "lech_co_chu_dich", "lech_ngoai_ten") if x in k}
        print(f"   {g:7s} dat={k.get('dat')!s:5s} {so}" + ("" if k.get("dat") else f"  ly_do={str(k.get('ly_do'))[:300]}"))
    if a.ra:
        Path(a.ra).write_text(json.dumps(kq, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
