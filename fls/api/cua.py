"""Cua HTTP — **mong**: doc yeu cau, tra loi, ⛔ khong mot luat nghiep vu nao.

★ Dung thu vien chuan (`http.server`), ⛔ khong khung web. Ly do: kho nay co
**ba** goi phu thuoc va cua doc `P4` chi can dinh tuyen + JSON. Doi lai: ⛔ khong
co ASGI, ⛔ khong co tai lieu tu sinh. Neu ve sau can chung thi thay `cua.py`,
⛔ dung nhoi vao no.

⛔⛔ **Ba dieu file nay tu choi, va chung la thiet ke chu khong phai su cham tre:**

  ⓐ **Khong co chia khoa thi khong mo cua.** `FLS_JWT_SECRET` trong ⇒ may **tu
    choi chay**. ⛔ Khong co che do "cho qua tam thoi".
  ⓑ **Ket noi phai bi PostgreSQL chan ghi.** Truoc khi nhan yeu cau dau tien,
    may kiem `default_transaction_read_only = on`; khong phai thi **tu choi
    chay**. Mot cua doc chi-doc-vi-quy-uoc la mot cua se ghi vao mot ngay nao
    do — meo nay da bat that mot bai test dang `CREATE TABLE` len so that.
  ⓒ **Khong lay `run_id` "ca kho" tu nguoi goi.** Xem `xu_ly.pham_vi_cua_yeu_cau`.
  ⓓ ⭐ **HAI duong noi kho, va duong nao dung cho tuyen nao la do BANG TUYEN
    quyet, ⛔ khong do ham xu ly quyet.** Duong DOC bi PostgreSQL chan ghi;
    duong GHI thi khong. Mot tuyen khai `ghi=False` ⇒ ham cua no **khong bao gio
    nhin thay** ket noi ghi duoc. Nho vay `P5` mo cua ghi ma ⛔ khong lam yeu
    dieu ⓑ cua `P4` mot chut nao.

★ `fls/api` ⛔ khong duoc import `fls.db` (co rang buoc `import-linter`): ket noi
duoc **truyen vao** tu ngoai (`tools/chay_cua.py`). Nho vay cua doc khong co
duong nao tu mo ket noi ghi duoc, ke ca khi ai do go nham.
"""
from __future__ import annotations

import json
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, ContextManager

from fls.api import bao, bang_tuyen
from fls.api.the import Nguoi, TheKhongHopLe, khoa, kiem, tu_dau_de
from fls.api.xu_ly import (HAM, LoiCua, YeuCau,
                           pham_vi_cua_yeu_cau)

# Kieu cua ham mo ket noi: mot `with` cho ra doi tuong ket noi DB.
MoKetNoi = Callable[[], ContextManager[Any]]

# ⭐ `P6`: ham phuc vu TEP TINH. `duong` → `(kieu_noi_dung, than)`, hay `None`.
# ⛔⛔ Cung khuon "ket noi duoc truyen vao": tang cua ⛔ khong biet `fls.web` ton
# tai, no chi goi cai duoc dua cho. Nho vay ⓐ rang buoc `import-linter` giu
# duoc mui ten mot chieu, va ⓑ mac dinh `None` ⇒ cua `P4`/`P5` chay **y het**
# nhu truoc, ⛔ khong mot byte khac.
PhucVuTep = Callable[[str], "tuple[str, bytes] | None"]

# ⛔ Dia chi may DUOC phep kiem nhiem phuc vu tep. Ban TRANG.
LOOPBACK: frozenset[str] = frozenset({"127.0.0.1", "::1", "localhost"})


def _trong_vung_cua(duong: str) -> bool:
    """⛔ `True` neu duong thuoc vung cua API — tep tinh ⛔ khong duoc cham vao.

    ⚠ Phai chan ca `/api/fls/v1` **tran** lan `/api/fls/v1/...`: neu chi chan
    dang co gach cheo thi mot tep khai o dung `/api/fls/v1` se **gia lam mot
    cau tra loi that**, va no se ⛔ khong co `meta`/`error` — man hinh doc no
    thanh du lieu.
    """
    t = bang_tuyen.TIEN_TO
    return duong == t or duong.startswith(t + "/")


# Than yeu cau toi da. 64 KB du cho moi phep ghi that (mot gia tri + ly do).
THAN_TOI_DA = 64 * 1024


class _May(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, dia_chi, xu_ly, mo_doc: MoKetNoi,
                 mo_ghi: MoKetNoi | None, k: bytes,
                 phuc_vu_tep: PhucVuTep | None = None):
        super().__init__(dia_chi, xu_ly)
        self.mo_doc = mo_doc
        # `None` ⇒ may chay o che do CHI DOC: moi tuyen ghi tra 405. Khai tuong
        # minh, ⛔ khong am tham cho ghi bang ket noi doc (se loi kho, kho hieu).
        self.mo_ghi = mo_ghi
        self.khoa = k
        # `None` ⇒ ⛔ KHONG phuc vu tep tinh nao. Mac dinh, va do la mac dinh
        # dung: mot cua doc so tien that ⛔ khong nen kiem nhiem may chu web
        # tru khi ai do go tuong minh.
        self.phuc_vu_tep = phuc_vu_tep


class _Tay(BaseHTTPRequestHandler):
    # ⛔ Khong khoe ten/phien ban may chu.
    server_version = "fls"
    sys_version = ""
    protocol_version = "HTTP/1.1"

    # ── cac phuong thuc ─────────────────────────────────────────────────
    def do_GET(self) -> None:          # noqa: N802
        self._di("GET")

    def do_POST(self) -> None:         # noqa: N802
        self._di("POST")

    def do_PUT(self) -> None:          # noqa: N802
        self._di("PUT")

    def do_DELETE(self) -> None:       # noqa: N802
        self._di("DELETE")

    def do_PATCH(self) -> None:        # noqa: N802
        self._di("PATCH")

    # ── loi ────────────────────────────────────────────────────────────
    def log_message(self, dinh_dang: str, *doi_so) -> None:
        """Ghi gon ra stderr. ⛔ Khong ghi de `Authorization`.

        ⛔⛔ **Khong ghi duoc nhat ky thi ⛔ KHONG duoc keo cua chet theo.**
        Ngay `03/09` may dang chay bi mat dau ra *(phien nen ket thuc, dau kia
        cua ong dan dong lai)*: moi yeu cau vao la `log_message` **no
        `BrokenPipeError`** truoc khi kip tra loi ⇒ cong **van MO** nen nhin
        nhu dang song, ma ⛔ khong tra loi gi ca. Owner bao *"toi khong mo
        duoc"*, va `netstat` van bao `LISTENING`.

        ⇒ Do la lop hong te nhat: **im lang va trong nhu binh thuong**. Mot cai
        cua ⛔ khong ghi duoc nhat ky van phai **tra loi**; mat nhat ky la mat
        mot lop kiem soat, con mat cau tra loi la mat ca cai cua.

        ⚠ Va ⛔ khong nuot **moi** loi: chi nuot loi cua **duong ghi nhat ky**
        (`OSError`/`ValueError` khi dau ra da dong). Mot loi khac lot vao day
        van phai noi.
        """
        try:
            sys.stderr.write("fls-api %s\n" % (dinh_dang % doi_so))
        except (BrokenPipeError, ValueError, OSError):
            # ⛔ ⛔ Khong thu ghi lai, ⛔ khong doi sang `stdout` — dau ra kia co
            # the cung da dong, va mot vong thu-lai o day se lam chet dung cai
            # thu no dang cuu.
            pass

    def _tra(self, http: int, than: bytes) -> None:
        self.send_response(http)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(than)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        if self.close_connection:
            self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(than)

    # ── ⭐ `P6` · tep tinh ──────────────────────────────────────────────
    def _tra_tep(self, kieu: str, than: bytes) -> None:
        self.send_response(200)
        self.send_header("Content-Type", kieu)
        self.send_header("Content-Length", str(len(than)))
        # ⛔ `no-store` ke ca cho tep tinh: sau mot lan trien khai, mot man
        # hinh cu nam trong bo nho dem trinh duyet se goi cua MOI bang ma CU —
        # va no se trong nhu dang chay dung.
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        # ⛔⛔ ⛔ Khong tep ngoai nao. Man hinh nay ⛔ khong co thu vien
        # (`QĐ-ITL-66`) va ⛔ khong nhung font tu mang ⇒ `'self'` la du, va no
        # chan luon moi duong ma mot doan ma la co the goi ra ngoai. `style`
        # phai cho `unsafe-inline` vi ban ve dung thuoc tinh `style=` tai cho.
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; font-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; "
            "base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
        if self.close_connection:
            self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(than)

    def _loi(self, ma: str, pham_vi: str = "-", chi_tiet: str = "",
             **them) -> None:
        # ⛔⛔ Tu choi mot yeu cau CO THAN ma chua doc than thi ket noi
        # keep-alive con du byte ⇒ yeu cau SAU bi doc lech (bo test bat duoc:
        # log in ra mot "dong yeu cau" chinh la than cua yeu cau truoc).
        # Chua o MOT CHO nay, de moi duong tu choi — ke ca duong them ve sau —
        # deu duoc chua.
        if not getattr(self, "_than_da_doc", False):
            try:
                if int(self.headers.get("Content-Length") or 0) > 0:
                    self.close_connection = True
            except ValueError:
                self.close_connection = True
        http, than = bao.dong_goi_loi(ma, bao.meta(pham_vi), chi_tiet, **them)
        self._tra(http, than)

    # ── than yeu cau ───────────────────────────────────────────────────
    def _doc_than(self) -> dict:
        """Doc + kiem than JSON. ⛔ Mac dinh la TU CHOI, khong phai "coi nhu rong".

        ⛔ `Content-Length` khong doc duoc, qua to, khong phai JSON, hay khong
        phai mot doi tuong ⇒ **400**. Mot phep ghi doan y nguoi goi la mot phep
        ghi ⛔ khong truy duoc ve sau.
        """
        # ⛔ Tu choi mot than ma **khong doc het** thi ket noi keep-alive con
        # du byte cua yeu cau cu ⇒ yeu cau SAU bi doc lech. Nen moi duong tu
        # choi o day deu **dong ket noi**. (Bo test in ra "Exception occurred
        # during processing of request" — khong bai nao do, nhung mot client
        # THAT se nhan mot loi vo nghia.)
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self.close_connection = True
            raise LoiCua("FLS-BAD-REQUEST",
                         "Content-Length khong doc duoc") from None
        if n <= 0:
            self.close_connection = True
            raise LoiCua("FLS-BAD-REQUEST", "phep ghi phai co than JSON")
        if n > THAN_TOI_DA:
            # ⛔ ⛔ KHONG doc het roi moi tu choi — doc het la lam dung cai viec
            # ma gioi han nay dung ra de tranh.
            self.close_connection = True
            raise LoiCua("FLS-TOO-LARGE",
                         f"than {n} byte > {THAN_TOI_DA} — qua to cho mot phep ghi")
        ct = (self.headers.get("Content-Type") or "").split(";")[0].strip()
        if ct != "application/json":
            self.close_connection = True
            raise LoiCua("FLS-BAD-REQUEST",
                         f"Content-Type={ct!r}, phai la application/json")
        try:
            tho = self.rfile.read(n)
            self._than_da_doc = True
            d = json.loads(tho)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise LoiCua("FLS-BAD-REQUEST", f"than khong phai JSON: {e}") from e
        if not isinstance(d, dict):
            raise LoiCua("FLS-BAD-REQUEST", "than phai la mot doi tuong JSON")
        # ⛔⛔ `actor` ⛔ KHONG duoc den tu than yeu cau — no den TU THE. Neu ai
        # gui `actor` thi NO, chu ⛔ khong am tham bo qua: mot cai nut gui
        # `actor` roi thay no bi bo qua la mot ky vong sai da hinh thanh.
        if "actor" in d:
            raise LoiCua("FLS-BAD-REQUEST",
                         "⛔ `actor` khong duoc gui trong than — no lay TU THE "
                         "(`AUD-1`: nhat ky ma nguoi goi tu khai thi vo nghia)")
        return d

    # ── duong di chinh ─────────────────────────────────────────────────
    def _di(self, phuong_thuc: str) -> None:
        self._than_da_doc = False
        p = urllib.parse.urlparse(self.path)
        duong = p.path.rstrip("/") or p.path
        q = {k: v[0] for k, v in urllib.parse.parse_qs(p.query).items()}

        # ⓪ ⭐ `P6` · TEP TINH — **truoc** phep kiem the, va **chi** ngoai vung
        #    cua. Mot trinh duyet ⛔ khong the gan dau de `Authorization` vao
        #    lan tai trang dau tien, nen vo man hinh phai ra duoc truoc the.
        #
        # ⛔⛔ Ba hang rao giu cho phep ngoai le nay ⛔ khong lam yeu cua:
        #   ⓐ **⛔ khong bao gio cham vung cua** — `_trong_vung_cua` chan tuyet
        #     doi, nen `404` vs `405` cua tang cua van ⛔ khong lo mot duong nao.
        #   ⓑ **chi `GET`** — moi phep ghi van di het duong the.
        #   ⓒ **tat mac dinh**, va `dung_may` ⛔ TU CHOI bat no khi may nghe ra
        #     ngoai loopback (xem `dung_may`).
        pv_tep = self.server.phuc_vu_tep
        if (pv_tep is not None and phuong_thuc == "GET"
                and not _trong_vung_cua(duong)):
            co = pv_tep(duong)
            if co is None:
                return self._loi("FLS-NOT-FOUND")
            return self._tra_tep(*co)

        # ⓐ the TRUOC dinh tuyen — nguoi khong co the ⛔ khong duoc biet duong
        #    nao ton tai (404 vs 405 la mot ban do he thong).
        try:
            nguoi: Nguoi = kiem(tu_dau_de(self.headers.get("Authorization")),
                                self.server.khoa)
        except TheKhongHopLe as e:
            self.log_message("401 %s %s (%s)", phuong_thuc, duong, e.chi_tiet)
            return self._loi("FLS-UNAUTHORIZED")

        tim = bang_tuyen.tim(phuong_thuc, duong)
        if tim is None:
            if bang_tuyen.duong_ton_tai(duong):
                # Duong co, phuong thuc khong. `P4` chi doc nen moi PUT/DELETE
                # deu ve day — va do la cau tra loi dung, khong phai 501.
                return self._loi("FLS-METHOD")
            return self._loi("FLS-NOT-FOUND")
        tuyen, tham = tim

        try:
            pv = pham_vi_cua_yeu_cau(q)
        except ValueError as e:
            return self._loi("FLS-BAD-REQUEST", chi_tiet=str(e))

        # ⭐ Ket noi do BANG TUYEN chon, ⛔ khong do ham xu ly chon.
        if tuyen.ghi:
            if self.server.mo_ghi is None:
                return self._loi("FLS-METHOD", pv.mo_ta(),
                                 "cua nay dang chay o che do CHI DOC")
            mo = self.server.mo_ghi
        else:
            mo = self.server.mo_doc

        try:
            than = self._doc_than() if tuyen.ghi else {}
        except LoiCua as e:
            return self._loi(e.ma, pv.mo_ta(), e.chi_tiet)

        try:
            with mo() as conn:
                data, trang_thai = HAM[tuyen.ham](YeuCau(
                    conn=conn, pv=pv, q=q, tham=tham, actor=nguoi.actor,
                    than=than))
        except LoiCua as e:
            return self._loi(e.ma, pv.mo_ta(), e.chi_tiet, **e.them)
        except Exception as e:                                   # noqa: BLE001
            # ⛔ Loi trong may ⛔ khong duoc ra ngoai: mot vet ngan xep la mot
            # ban do duong dan + phien ban thu vien. Ghi vao log, tra ma tron.
            self.log_message("500 %s %s: %r", phuong_thuc, duong, e)
            return self._loi("FLS-INTERNAL", pv.mo_ta())

        m = bao.meta(pv.mo_ta(), data_status=trang_thai,
                     run_id=pv.run_id)
        self.log_message("200 %s %s actor=%s", phuong_thuc, duong, nguoi.actor)
        self._tra(200, bao.dong_goi(data, m))


def kiem_truoc_khi_mo(conn) -> None:
    """⛔ NO neu ket noi con ghi duoc. Goi mot lan luc dung may."""
    from fls.repo.doc_bao_cao import la_chi_doc

    if not la_chi_doc(conn):
        raise RuntimeError(
            "⛔ ket noi cua cua doc con GHI duoc. Truyen vao mot ham mo ket noi "
            "co `SET default_transaction_read_only = on` (xem "
            "`fls.db.kho.noi_chi_doc`). Mot cua doc chi-doc-vi-quy-uoc la mot "
            "cua se ghi vao mot ngay nao do.")


def kiem_duong_ghi(conn) -> None:
    """⛔ NO neu duong GHI lai la mot ket noi chi-doc — loi kho se rat kho hieu."""
    from fls.repo.doc_bao_cao import la_chi_doc

    if la_chi_doc(conn):
        raise RuntimeError(
            "⛔ duong GHI dang la ket noi CHI DOC. Truyen hai ham mo ket noi "
            "KHAC NHAU: `mo_doc` (chi doc) va `mo_ghi` (ghi duoc).")


def kiem_phuc_vu_tep(dia_chi: str) -> None:
    """⛔ NO neu ai do vua bat man hinh tren mot may nghe RA NGOAI.

    ⛔⛔ **Vi sao day la mot cai NO chu ⛔ khong phai mot canh bao.** Vo man hinh
    ra duoc **truoc the** *(trinh duyet ⛔ khong gan duoc dau de o lan tai dau)*,
    va `phien.js` **cho mot cai the**. Tren `127.0.0.1` dieu do co nghia la
    *"ai dang ngoi truoc may nay"* — mot cau tra loi that. Mo ra mang thi no
    thanh *"bat ky ai cham toi cong nay"*, va luc do cai the la mot cai the
    **phat khong cho nguoi la**.

    ⇒ Chua co dang nhap thi ⛔ khong duoc mo ra mang. Day la **`GAP-WEB-01`**:
      *khi nao FLS chay cho nhieu hon mot may, phai co duong dang nhap that*.
    """
    if dia_chi not in LOOPBACK:
        raise RuntimeError(
            f"⛔ dia chi {dia_chi!r} ⛔ khong phai loopback, nen ⛔ khong duoc "
            f"phuc vu man hinh: vo man hinh ra duoc TRUOC the, va `phien.js` "
            f"cho mot cai the. Tren mang do la phat the cho nguoi la. "
            f"⇒ Bo `--cho-web`, hay chay tren 127.0.0.1 (`GAP-WEB-01`).")


def dung_may(mo_doc: MoKetNoi, cong: int = 8088,
             dia_chi: str = "127.0.0.1",
             mo_ghi: MoKetNoi | None = None,
             phuc_vu_tep: PhucVuTep | None = None) -> _May:
    """Dung may (chua chay). ⛔ NO neu thieu khoa hay ket noi sai loai.

    `mo_ghi=None` ⇒ che do **CHI DOC**: moi tuyen ghi tra `405`. Khai tuong minh,
    ⛔ khong am tham cho ghi bang duong doc.

    ⛔ Mac dinh chi nghe `127.0.0.1`: cua nay chua qua ra soat an ninh nao va
    dang doc so tien that. Muon mo ra mang thi phai go tuong minh.
    """
    # ⛔⛔ Phep tu choi RE NHAT va DUT KHOAT NHAT dung dau tien. Ban dau toi dat
    # no sau phep mo ket noi — va bai
    # `test_dung_may_TU_CHOI_khi_vua_mo_man_hinh_vua_nghe_ra_mang` **do** vi
    # may di mo mot ket noi vao SO THAT roi moi phat hien no se tu choi. Mot
    # cai NO ma phai cham vao so truoc la mot cai NO dat hon can thiet.
    if phuc_vu_tep is not None:
        kiem_phuc_vu_tep(dia_chi)    # ⛔ NO neu may nghe ra ngoai loopback
    k = khoa()                       # ⛔ NO neu thieu FLS_JWT_SECRET
    with mo_doc() as conn:
        kiem_truoc_khi_mo(conn)      # ⛔ NO neu duong DOC con ghi duoc
    if mo_ghi is not None:
        with mo_ghi() as conn:
            kiem_duong_ghi(conn)     # ⛔ NO neu duong GHI lai chi doc
    loi = bang_tuyen.kiem_bang_tuyen()
    if loi:
        raise RuntimeError("⛔ bang tuyen vi pham:\n  - " + "\n  - ".join(loi))
    return _May((dia_chi, cong), _Tay, mo_doc, mo_ghi, k, phuc_vu_tep)


def _in_bang_tuyen() -> str:
    return json.dumps(
        [{"phuong_thuc": t.phuong_thuc, "duong": t.duong, "ghi": t.ghi,
          "bang": list(t.bang), "mo_ta": t.mo_ta} for t in bang_tuyen.BANG_TUYEN],
        ensure_ascii=False, indent=2)
