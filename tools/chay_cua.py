"""Chay cua doc `P4`. Day la CHO DUY NHAT noi cua voi kho.

    PG_DSN=... FLS_JWT_SECRET=... python tools/chay_cua.py [--cong 8088]
    python tools/chay_cua.py --the-tam 3600      # phat mot the de thu

⭐ Vi sao viec noi day nam o `tools/` chu khong trong `fls/api/`: rang buoc
`import-linter` so 7 cam `fls.api` biet `fls.db`. Nho vay tang cua ⛔ khong co
duong nao tu mo mot ket noi — no chi dung cai duoc dua cho. Va cai duoc dua cho
o day la `noi_chi_doc()`: PostgreSQL **chan ghi o tang kho**.

⛔ Cua tu choi chay neu: thieu `FLS_JWT_SECRET` · ket noi con ghi duoc · bang
tuyen vi pham. Ba cai tu choi nay la thiet ke, ⛔ khong phai su cham tre.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import contextlib
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fls.api import cua                                          # noqa: E402
from fls.api.the import dong_the, khoa                           # noqa: E402
from fls.db.kho import dsn_that, noi_chi_doc                     # noqa: E402


def _mo_ket_noi(dsn: str):
    """Ham mo ket noi CHI DOC. ⛔ Moi phep ghi bi PostgreSQL tu choi."""
    @contextlib.contextmanager
    def mo():
        conn = noi_chi_doc(dsn)
        try:
            yield conn
        finally:
            conn.close()
    return mo


def _mo_ghi(dsn: str):
    """Ham mo ket noi GHI duoc. ⛔ Chi dung khi co `--cho-ghi` tuong minh.

    ⚠ Day la ham duy nhat trong ca he mo mot ket noi ghi duoc cho cua HTTP. No
    ⛔ khong bat duoc dung nhieu hon mot cho, va no ⛔ khong duoc mac dinh bat.
    """
    import psycopg

    @contextlib.contextmanager
    def mo():
        conn = psycopg.connect(dsn, autocommit=True)
        try:
            yield conn
        finally:
            conn.close()
    return mo


def _danh_muc_js(dsn: str) -> bytes:
    """Sinh `danh_muc.js` — anh chup danh muc luc khoi dong.

    ⛔ Doc bang ket noi **CHI DOC** (`QĐ-ITL-34`: may chi DOC).
    """
    import json

    conn = noi_chi_doc(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT hd_code FROM fls_mapping_master"
                        " ORDER BY hd_code")
            ma = [r[0] for r in cur.fetchall()]
            # ⚠⚠ Ba danh sach duoi **SUY TU DU LIEU DANG DUNG**, ⛔ khong phai
            #    danh muc. Khac han `ma` phia tren — cai do co ban khai that.
            #    ⛔ Chung ⛔ khong dua ra duoc gia tri chua ai dung, va chung
            #    **dua luon ca loi go cua nguoi truoc**. Man PHAI noi ro.
            suy = {}
            for truong in ("pay_type", "cdt1", "id_payee"):
                cur.execute(
                    "SELECT {0} FROM fls_itl WHERE coalesce({0},'') <> ''"
                    " GROUP BY {0} ORDER BY count(*) DESC".format(truong))
                suy[truong] = [r[0] for r in cur.fetchall()]

            # ══ ⭐⭐ TU VUNG CHUNG cua `le` va `le_payer` (`US-032`) ════════
            #
            # ⛔⛔ **Vi sao cho nay can mot danh sach.** `US-032` doi man bao do
            # khi `LE` lech `Pháp nhân thanh toán`. Ban thiet ke viet luat la
            # `le != le_payer`. Do that: luat ay bao tren **1.304 dong (13%)**
            # — mot bang bao ke toan gap **mot tren tam dong**, tuc la ta vua
            # tai tao dung cai *"kho nhin"* vua cat.
            #
            # ⭐ Va ly do: **hai cot ⛔ khong noi cung mot tu vung.** `le` co 23
            # gia tri, `le_payer` co 16, trung nhau **44%**. `le` con chua
            # `Cash Treasury`, `CN`, `HGO1` — nhung thu **⛔ khong bao gio**
            # xuat hien o `le_payer`. **1.225 / 1.304** bao la kieu ay: so
            # **tao voi cam**, ⛔ khong phai lech phap nhan.
            #
            # ⇒ Chi bao khi **ca hai** gia tri thuoc tu vung CHUNG. Do lai:
            # **79 dong (0,8%)** — va moi cap con lai la hai **ma phap nhan
            # that, khac nhau** (`SGO2 != VVOS`). Do moi la *"it, hiem, that"*.
            #
            # ⚠ Day la phep do **CO SO SANH DUOC KHONG**, ⛔ khong phai phep do
            # **DUNG SAI** ⇒ no ⛔ khong pham `INV-I18`: no ⛔ khong dung du
            # lieu de cuong che mot gia tri, no dung du lieu de biet hai o co
            # cung **don vi do** hay khong.
            cur.execute(
                "SELECT btrim(le) FROM fls_itl WHERE coalesce(le,'') <> ''"
                " INTERSECT"
                " SELECT btrim(le_payer) FROM fls_itl"
                " WHERE coalesce(le_payer,'') <> '' ORDER BY 1")
            le_chung = [r[0] for r in cur.fetchall()]
    finally:
        conn.close()
    return ("// ⛔ SINH LUC KHOI DONG tu `fls_mapping_master` — ⛔ khong go tay.\n"
            "// ⚠ Day la ANH CHUP: Master doi thi phai khoi dong lai cua.\n"
            "window.FLS_DM_HD = "
            + json.dumps(ma, ensure_ascii=False) + ";\n"
            "window.FLS_DM_SUY = "
            + json.dumps(suy, ensure_ascii=False) + ";\n"
            "window.FLS_LE_CHUNG = "
            + json.dumps(le_chung, ensure_ascii=False) + ";\n"
            "window.FLS_DM_LUC = "
            + json.dumps(datetime.now().strftime("%Y-%m-%d %H:%M"))
            + ";\n").encode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cong", type=int, default=8088)
    ap.add_argument("--dia-chi", default="127.0.0.1",
                    help="⛔ mac dinh chi nghe may nay")
    ap.add_argument("--the-tam", type=int, metavar="GIAY",
                    help="in mot the song GIAY giay roi thoat (de thu bang curl)")
    ap.add_argument("--actor", default="thu@apero.vn")
    ap.add_argument("--in-bang-tuyen", action="store_true")
    ap.add_argument("--cho-ghi", action="store_true",
                    help="⛔ MO NHOM GHI (P5). Mac dinh TAT: cua chay o che do "
                         "chi doc, moi duong ghi tra 405. Bat la mo duong sua "
                         "so THAT — phai go tuong minh.")
    ap.add_argument("--cho-web", action="store_true",
                    help="⭐ P6: phuc vu MAN HINH (`fls/web/tep/`) tren CUNG "
                         "cong voi cua. Mac dinh TAT. ⛔ Cua se TU CHOI chay "
                         "neu `--dia-chi` ⛔ khong phai loopback.")
    ap.add_argument("--the-song", type=int, default=8 * 3600, metavar="GIAY",
                    help="han cua the cap cho man hinh (mac dinh mot ngay lam "
                         "viec). ⛔ Khong co che do 'khong han'.")
    a = ap.parse_args()

    if a.in_bang_tuyen:
        print(cua._in_bang_tuyen())
        return 0

    if a.the_tam:
        print(dong_the({"sub": a.actor, "exp": int(time.time()) + a.the_tam,
                        "vai": ["ke_toan"]}, khoa()))
        return 0

    # ⭐ `P6`: noi tang man hinh vao. ⛔ Viec noi nam O DAY chu ⛔ khong trong
    # `fls/api/` — cung ly do voi ket noi kho: rang buoc `import-linter` cam
    # `fls.api` biet `fls.web`, nen tang cua ⛔ khong co duong nao tu tim thay
    # mot tep tinh de phuc vu.
    phuc_vu = None
    if a.cho_web:
        from fls.api.cot_so import than_js
        from fls.web.phuc_vu import lam_nguoi_phuc_vu

        # ⛔⛔ Cai the do CHO CHAY dong, ⛔ khong do trinh duyet xin. `actor` vi
        # the la *"ai khoi dong may nay"* — mot cau tra loi that tren mot may
        # mot nguoi ngoi. ⚠ Xem `GAP-WEB-01`: khi FLS chay cho nhieu hon mot
        # may thi cho nay phai thanh mot duong dang nhap that.
        phuc_vu = lam_nguoi_phuc_vu({
            "the": dong_the({"sub": a.actor,
                             "exp": int(time.time()) + a.the_song,
                             "vai": ["ke_toan"]}, khoa()),
            "actor": a.actor,
            "cho_ghi": bool(a.cho_ghi),
            "pham_vi": "lan nap that",
            "the_het_luc": int(time.time()) + a.the_song,
        }, than_sinh={
            # ⭐ Bang cot cua luoi `F02`. ⛔ Viec noi nam O DAY vi
            # `import-linter` luat thu 8 cam `fls.web` voi xuong `fls.canon` /
            # `fls.oracle` — ma ten cot lai o dung hai cho ay. ⇒ Than duoc
            # **dua vao**, cung khuon "ket noi duoc truyen vao" cua `P4`.
            # ⛔ `than_js()` NO neu bang cot vi pham, va no NO **truoc** khi
            # may mo cong — mot luoi thieu tieu de trong y het mot luoi chua
            # tai xong.
            "cot.js": than_js(),
            # ⭐ DANH MUC ma hop dong — 73 ma, va do that thi **0** ma `hd`
            #   trong so nam ngoai no ⇒ no **co tham quyen**, ⛔ chu ⛔ khong
            #   phai mot danh sach goi y.
            # ⚠ **Anh chup luc khoi dong.** Master doi thi man cu cho toi lan
            #   khoi dong sau — man hinh PHAI noi ra dieu ay, ⛔ khong duoc de
            #   ke toan tuong minh dang nhin danh muc song.
            "danh_muc.js": _danh_muc_js(dsn_that()),
        })

    dsn = dsn_that()
    may = cua.dung_may(_mo_ket_noi(dsn), cong=a.cong, dia_chi=a.dia_chi,
                       mo_ghi=_mo_ghi(dsn) if a.cho_ghi else None,
                       phuc_vu_tep=phuc_vu)
    print(f"cua FLS: http://{a.dia_chi}:{a.cong}/api/fls/v1/  "
          f"({'DOC + GHI' if a.cho_ghi else 'CHI DOC'} · the bat buoc · "
          f"pham vi = lan nap that)")
    if a.cho_web:
        print(f"⭐ man hinh: http://{a.dia_chi}:{a.cong}/   "
              f"(the cap cho `{a.actor}`, song {a.the_song // 3600} gio)")
        print("  xem BON trang thai ma ⛔ khong phai tat may chu:")
        for ten in ("tai", "rong", "loi", "mat_ket_noi"):
            print(f"    http://{a.dia_chi}:{a.cong}/?gia_lap={ten}")
    if not a.cho_ghi:
        print("  (nhom ghi TAT — them `--cho-ghi` de mo, va no sua so THAT)")
    for t in cua.bang_tuyen.BANG_TUYEN:
        co = "" if not t.ghi else ("  [GHI]" if a.cho_ghi else "  [GHI · TAT]")
        print(f"  {t.phuong_thuc:4} {t.duong}{co}")
    try:
        may.serve_forever()
    except KeyboardInterrupt:
        print("\ndung")
    finally:
        may.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
