# -*- coding: utf-8 -*-
"""Luat DOC cua man GAN LENH CHI — `SCR-F01`.

⭐⭐⭐ `QĐ-ITL-148` · `2026-09-21` · chang `B2` cua `Plan-Test-Dev-Man-Ghep.md`.
Dac ta: `BA-07 §4h` · `BA-06 §4.5` · `§4.6`.

⛔⛔ **Bon luat o day deu CHUA TUNG duoc viet o dau**, va ba trong bon da co
   tien su sai:

    ⓐ `tach_nguon`  — moi tai lieu cua du an trich `source_sheet` **thieu
       tien to `R | `**, ma kho co no o **`8.387/8.387`** dong.
    ⓑ `chieu_tien`  — du an **da lay dau tu `pay_type`** mot lan, thay vi
       tu cot `No`/`Co`.
    ⓒ `ngay_tu_seri` — goc `1900`/`1904` lech **4 nam 1 ngay**, va ⛔ khong
       o nao tren man noi cho biet da chon goc nao.
    ⓓ `CHIP`       — ban dung co **ba** chip, thieu chip cho **DICH CUOI**
       ⇒ `768` dong ⛔ khong gan duoc bi tron vao viec hang ngay (`INV-I20`).
"""
from __future__ import annotations

import datetime as dt
import re
from decimal import Decimal, InvalidOperation
from typing import Any

from fls.adapters.pm_join import canon_ref
from fls.canon.tien_te import TAP_TRANG_TIEN_TE, ma_tien_te  # noqa: F401 — xem ⓔ
from fls.repo.anh_pm import anh_pm_hieu_luc
from fls.repo.lenh_cho import (RO_KHONG, RO_MAY, RO_NGUOI, _dk_ten,
                               doc_mot_dong_lenh)
from fls.repo.pham_vi import PhamVi

# ── ⓐ tach `source_sheet` ───────────────────────────────────────────────

#: Tien to tang sheet nguon. Do `21/09`: **8.387/8.387** dong mang no.
#: ⛔ Moi tai lieu cua du an dang trich gia tri NAY THIEU tien to.
TIEN_TO_TANG = "R | "

#: `<tk>_<bank> <curr>_<le>` — do: dung khuon o **8.387/8.387** dong, **49** nguon.
_KHUON_NGUON = re.compile(r"^([^_]+)_([^_ ]+) ([A-Z]{3})_([^_]+)$")


def tach_nguon(source_sheet: str) -> dict[str, str]:
    """`R | PO2_OCBC USD_SGO2` ⇒ `{tk, bank, curr, le}`.

    ⛔ Chuoi la thi **NO**, ⛔ khong doan — `INV-I16`.
    """
    s = str(source_sheet or "")
    if s.startswith(TIEN_TO_TANG):
        s = s[len(TIEN_TO_TANG):]
    m = _KHUON_NGUON.match(s.strip())
    if not m:
        raise ValueError(
            f"⛔ `source_sheet` ⛔ khong dung khuon `<tk>_<bank> <curr>_<le>`: "
            f"{source_sheet!r}")
    return {"tk": m.group(1), "bank": m.group(2),
            "curr": m.group(3), "le": m.group(4)}


def che_tai_khoan(tk: str) -> str:
    """Rut con **4 so cuoi** — ⭐ CHI KHI no toan chu so.

    ⛔ `6` tai khoan la **THE**, ⛔ khong phai so: `PO1`·`PO2`·`PO3`·`PO5`·
       `PO6`·`PO9`. Cat mu quang cho ra `••PO2` — vua vo nghia vua ⛔ khong
       che duoc gi.
    """
    t = str(tk or "")
    if not t.isdigit():
        return t
    return "••" + t[-4:]


# ── ⓑ chieu No/Co ───────────────────────────────────────────────────────

def chieu_tien(ps_no: Any, ps_co: Any) -> str:
    """`'no'` = tien VAO · `'co'` = tien RA.

    ⭐ Do `21/09` tren `fls_itl`: **3.691/8.387** dong mang **ca hai** o,
      nhung **`0`** dong co ca hai khac `0` ⇒ *"ben nao ≠ 0 thi do la chieu"*.

    ⛔⛔ ⛔ KHONG suy tu loai thanh toan — du an da di duong ay mot lan va
       ra dau sai.
    """
    co_no = ps_no is not None and ps_no != 0
    co_co = ps_co is not None and ps_co != 0
    if co_no and co_co:
        raise ValueError(
            f"⛔ ca hai o deu khac 0 (`{ps_no}` / `{ps_co}`) — do duoc `0` dong "
            "nhu vay tren kho that. Day la du lieu HONG, va may ⛔ khong duoc "
            "chon giup mot ben (`INV-I16`).")
    if co_no:
        return "no"
    if co_co:
        return "co"
    raise ValueError("⛔ ca hai o deu rong hoac bang 0 ⇒ ⛔ khong co chieu")


# ── ⓒ se-ri Excel → ngay ───────────────────────────────────────────────

#: ⭐ Goc `1900` — **DO duoc**, ⛔ khong chon: doi chieu voi ngay cua dong tien
#: **da noi** (`fls_itl.doc_date`, mot nguon DOC LAP) cho lech trung vi **3**
#: ngay; goc `1904` cho **1.462** ngay va dai `2029…2030`.
NEN_SE_RI = dt.datetime(1899, 12, 30)


def ngay_tu_seri(s: Any) -> dt.datetime:
    """Se-ri Excel ⇒ `datetime` (**giu ca gio**).

    ⛔ Kho co **3.772/3.772** o `Timestamp` la se-ri, **`0`** dong co dau ngay.
    ⛔ Chuoi ⛔ khong phai so thi **NO** — *"⛔ chua doc duoc"* ⛔ khong duoc
       bien thanh mot ngay nao do.
    """
    try:
        v = float(str(s).strip())
    except (TypeError, ValueError):
        raise ValueError(f"⛔ `{s!r}` ⛔ khong phai se-ri Excel") from None
    return NEN_SE_RI + dt.timedelta(days=v)


# ── ⓓ bon chip loc + ba duong ra ───────────────────────────────────────

#: ⭐⭐ **BON** chip, ⛔ khong ba. Ban dung `21/09` co ba, va `Chua gan` cua no
#: la *"moi dong ⛔ khong phai da gan"* ⇒ gop ca **768** dong DICH CUOI vao
#: viec hang ngay ⇒ danh sach mac dinh `1.553` thay vi **738** (`G-a` truot).
CHIP: dict[str, frozenset[str]] = {
    "chua_gan":       frozenset({RO_NGUOI, RO_MAY}),   # 535 + 203 + 47 = 738
    "khong_gan_duoc": frozenset({RO_KHONG}),           # 768 — DICH CUOI
    "da_gan":         frozenset(),                     # doc tu moi noi
    "tat_ca":         frozenset({RO_NGUOI, RO_MAY, RO_KHONG}),
}

CHIP_MAC_DINH = "chua_gan"

#: ⭐ `INV-I20` — mot dong roi hang cho bang **BA** duong.
#: ⚰ Nut `Xong` (`QĐ-ITL-71`) **KHAI TU** `21/09` (`QĐ-ITL-148 ④`): ly do goc
#: *"cho danh dau viec dang lam do"* da duoc thiet ke moi giai bang cach khac
#: — gan xong **tu nhay** sang lenh chua gan ke tiep.
DUONG_RA = ("ghep_duoc", "khong_gan_duoc", "loi_nguon")


def chip_cua_dong(d: dict[str, Any]) -> str:
    """Mot dong lenh chua noi thuoc chip nao."""
    return "khong_gan_duoc" if d.get("ro") == RO_KHONG else "chua_gan"


def thuoc_chip(d: dict[str, Any], chip: str) -> bool:
    if chip not in CHIP:
        raise ValueError(f"⛔ chip la: {chip!r}")
    return d.get("ro") in CHIP[chip]


# ── ⓔ khuon `ung_vien[]` — **10** truong ───────────────────────────────

#: ⭐ Thu tu la thu tu **DOC**, ⛔ khong phai thu tu cot tren man: mot dong ung
#: vien tra loi ba cau theo thu tu *"day la khoan gi → bao nhieu, vao hay ra →
#: vi sao no o trong danh sach"* (`BA-06 §4.5`).
TRUONG_UNG_VIEN = ("itl_id", "doc_date", "doc_no", "dien_giai", "amount",
                   "chieu", "curr", "nguon", "bac", "lech")


# ⭐ `ma_tien_te` — mã tiền tệ để **SO** *(`trim` + chữ hoa)*. Một chỗ cho
#   **mọi** phép so tiền tệ của khuôn `⓵` *(`lech` · bậc toàn sổ)*: so có `trim`
#   ở chỗ này mà ⛔ ở chỗ kia là hai luật — `WO-032` Rủi ro 2. Cùng phép với
#   `F01G.khop_dung_tien` / `F01L._tinh` phía màn.
# ⚠ `WO-042 (c)` *(`BA-07` v3.11)*: định nghĩa **dời xuống** `fls.canon.tien_te`
#   cùng tập `TAP_TRANG_TIEN_TE` *(30 ký tự)* — `fls.adapters.pm_join` cũng so
#   tiền tệ mà ⛔ được nhập `fls.repo` *(hợp đồng nhập 6)*. Tên ở đây giữ cho
#   mọi chỗ gọi cũ *(`mg.ma_tien_te`, bài thử)* — **cùng một đối tượng hàm**,
#   ⛔ bản thứ hai *(`str.strip()` trần gỡ **29**, thiếu `U+FEFF`)*.
#   ⇒ nhập ở đầu tệp *(`from fls.canon.tien_te import …`)*.


def lech_ung_vien(amount: Any, curr: Any, amount_lenh: Any,
                  curr_lenh: Any) -> Decimal | None:
    """`lech` của khuôn `⓵` — ⭐ **MỘT** hàm cho cả **bốn** cửa trả khuôn ấy.

    ⭐⭐ `BA-07` **v3.7** §4h ⓵ *(`KQ-031` `F-2`)*: `|amount ứng viên − amount
      dòng lệnh|` — **trị tuyệt đối**, có số ở **MỌI** bậc *(kể cả `ma`)*;
      khớp tuyệt đối ⇒ `0`, ⛔ `None`. **`None` ⇔ ⛔ so được**: tiền tệ khác
      nhau *(so sau `trim` + chữ hoa)*, hoặc một bên thiếu `amount`/`curr`.

    ⛔⛔ **Vì sao một hàm, ⛔ bốn bản.** Trước `WO-032` mỗi cửa tự quyết:
       `itl-candidates` lấy `lech_tuyet_doi` của SQL bậc tiền nhưng ép `None`
       cho **mọi** bậc `ma` *(`lenh_cho.py:420` — sổ thật **338 / 448** ứng
       viên bậc `ma` lệch thật mà in `—`)*; `/so` *(`man_ghep.py:306`)* và
       `the.gd` / `the.gd_ds` *(`xu_ly.py:683` / `:717`)* ép `None` ở **mọi**
       dòng. Bốn chỗ, ba luật — đúng thứ hợp đồng gọi là *"bản sự thật thứ
       hai"*.

    ⛔⛔ **Khác tiền tệ ⛔ bao giờ trừ nhau** *(`QĐ-ITL-62` — *"NGOẠI TỆ KHÔNG CÓ
       DUNG SAI"*; `BA-06 §4.3` BIA)*: `100.000 VND` ↔ `100.000,00 USD` mà ra
       `0` là nói *"khớp"* cho một cặp cửa ghi **từ chối** *(`KhacTienTe`)*.
    """
    cu, cl = ma_tien_te(curr), ma_tien_te(curr_lenh)
    if not cu or not cl or cu != cl:
        return None
    a, b = _so(amount), _so(amount_lenh)
    if a is None or b is None:
        return None
    return abs(a - b)


def khuon_ung_vien(r: dict[str, Any], *, lenh: dict[str, Any]) -> dict[str, Any]:
    """Hang THO tu `lenh_cho.ung_vien_itl` ⇒ khuon hop dong `BA-07 §4h ⓵`.

    ⭐ `lenh` *(bắt buộc, `{amount, curr}` của **dòng lệnh của chính cửa/thẻ**)*
      — để `lech` tính bằng **một** hàm `lech_ung_vien` ở mọi cửa *(`WO-032`)*.
      ⛔ Một tham số tuỳ ý ở đây là mở lại đường *"quên truyền ⇒ `None` im
      lặng"* — đúng lỗi `F-2` của `KQ-031`. Cột `lech_tuyet_doi` của SQL
      **chỉ** còn dùng để **xếp** *(`lenh_cho.ung_vien_itl`)*, ⛔ để in.

    ⛔⛔ **Truoc khuon nay, `BA-07` khai `ung_vien[]` co `0` truong** — nen
       nguoi dung ban dung ⛔ khong co gi de nhan ngoai mot chuoi da ghep san
       *(`"18/09 · OCBC · ••4001 · SGO2 · CT#88213"`)* va phai **cat chuoi
       hien thi** de lay lai cau truc.

    ⭐ `nguon` la **OBJECT**: mot chuoi da ghep thi tang duoi ⛔ **khong the**
      bo bot cot khi man hep — ma luat hy sinh cot *(`Nguon` → `So CT` →
      ⛔ khong bao gio `Dien giai`)* doi dung dieu do.
    """
    # ⛔⛔⛔ **MOT dong hong ⛔ KHONG duoc lam sap ca danh sach.** `tach_nguon`
    #    NEM khi `source_sheet` sai khuon — dung o tang doc *(`INV-I16`: may
    #    ⛔ khong doan)*. ⛔ Nhung khuon nay chay tren **tung dong cua mot
    #    danh sach**, va mot ngoai le o day tra `500` cho **ca trang** ⇒ ke
    #    toan mat **50 ung vien** vi **mot**.
    # ⭐ `nguon=None` ＋ `loi_nguon` — mot trang thai **da co ten** o `DUONG_RA`,
    #   ⛔ khong phai mot cho va. Va no giu lai `dien_giai`/`amount`, tuc
    #   nguoi ta van doc duoc **bang chung** du ⛔ khong biet no tu tai khoan
    #   nao.
    loi_nguon = None
    try:
        tk_bank = tach_nguon(r["source_sheet"])
    except ValueError as e:
        tk_bank, loi_nguon = None, str(e)
    dg = r.get("dien_giai")
    ra: dict[str, Any] = {
        # ⛔ `itl_id` **phai** tra (cua GHI can no) nhung man ⛔ **khong in**
        #    (`UI-F8`). Ranh gioi la *"cua tra ≠ man in"* — `QĐ-ITL-142`.
        "itl_id": r["itl_id"],
        "doc_date": r.get("doc_date"),
        "doc_no": r.get("doc_no"),
        "dien_giai": dg,
        "amount": r.get("tien"),
        "chieu": chieu_tien(r.get("ps_no"), r.get("ps_co")),
        "curr": r.get("curr"),
        "nguon": None if tk_bank is None else {
            "tk": che_tai_khoan(tk_bank["tk"]), "bank": tk_bank["bank"],
            "curr": tk_bank["curr"], "le": tk_bank["le"]},
        "bac": r.get("bac"),
        # ⭐ `WO-022`→`WO-032`: ⛔ còn đọc `lech_tuyet_doi` của SQL — xem
        #   `lech_ung_vien`.
        "lech": lech_ung_vien(r.get("tien"), r.get("curr"),
                              lenh.get("amount"), lenh.get("curr")),
    }
    if loi_nguon is not None:
        ra["loi_nguon"] = loi_nguon
    if dg is None:
        # ⛔⛔ `null` mang HAI nghia, va gop chung la dung thu `INV-I16` cam.
        #    Do `21/09`: **3** dong noi duoc ma ⛔ khong chu · **26** dong
        #    ⛔ khong noi duoc. *"Giao dich nay ⛔ khong co noi dung"* va
        #    *"FLS ⛔ chua doc duoc"* la HAI cau khac nhau.
        ra["dien_giai_vi_sao"] = "rong" if r.get("noi_duoc") else "chua_noi_duoc"
    return ra


# ── ⓕ chum moi noi ─────────────────────────────────────────────────────

_SQL_CHUM = """
SELECT m.pm_line_id, m.amount, p.curr, p.tho ->> 'Tên tài khoản' AS nguoi_nhan
  FROM fls_moi_noi m
  LEFT JOIN fls_pm_line p
    ON p.pm_line_id = m.pm_line_id AND p.run_id = %(run_pm)s
 WHERE m.itl_id = %(itl_id)s
 ORDER BY m.pm_line_id
"""


def chum_cua_dong_tien(conn, pv: PhamVi, itl_id: int) -> list[dict[str, Any]]:
    """Cac dong lenh mot cu `Bo gan` se go — ⭐ **KEM TEN**, ⛔ khong mot con so.

    ⛔ Cua `unmatch` (`QĐ-ITL-69`) bo **TOAN BO** moi noi cua dong tien va
       ⛔ khong nhan `pm_line_ids`. Owner chot `21/09`: **giu cua, MAN noi ra
       thiet hai**.

    ⛔⛔ Mot con so *"se go 3 moi noi"* ⛔ khong du — nguoi dung can biet **dong
       nao**, vi ho chi dinh dong toi **mot** trong so do.
    """
    run_pm = anh_pm_hieu_luc(conn, pv)
    with conn.cursor() as cur:
        cur.execute(_SQL_CHUM, {"run_pm": run_pm, "itl_id": itl_id})
        ten = [c.name for c in cur.description]
        return [dict(zip(ten, r)) for r in cur.fetchall()]


# ── ⓖ tra cuu TOAN SO ──────────────────────────────────────────────────

_SQL_SO = """
SELECT i.itl_id, i.doc_date, i.doc_no, i.curr, i.source_sheet,
       i.ps_no, i.ps_co,
       COALESCE(i.ps_no, 0) + COALESCE(i.ps_co, 0) AS tien,
       dg.dien_giai,
       (EXISTS (SELECT 1 FROM fls_source s2
                  JOIN fls_chup_dong d2 ON d2.source_id = s2.source_id
                                       AND d2.dong_so = i.source_row
                 WHERE s2.source_key = i.source_sheet)) AS noi_duoc
  FROM fls_itl i
  LEFT JOIN fls_dien_giai dg ON dg.itl_id = i.itl_id
 WHERE {dk}
   AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m WHERE m.itl_id = i.itl_id)
   {loc_q}
 ORDER BY i.doc_date DESC NULLS LAST, i.itl_id DESC
 LIMIT %(n)s
"""

SO_MAC_DINH, SO_TOI_DA = 50, 200


def so_theo_lenh(conn, pv: PhamVi, pm_line_id: str, *,
                 q: str | None = None, n: int = SO_MAC_DINH) -> dict[str, Any]:
    """TOAN SO nhin tu MOT dong lenh — bac **tinh lai** theo lenh dang mo.

    ⭐⭐ **Che do nay la LOI THOAT NGO CUT.** Voi lenh may ⛔ khong tim duoc
      ung vien nao *(**768** dong)*, day la duong duy nhat de nguoi lam tiep —
      nen no ⛔ **khong** phai mot bo loc noi rong, no la **mot cau hoi khac**:
      danh sach ung vien tra loi *"may nghi nhung dong nao hop"*, con day tra
      loi *"so co nhung dong nao"*.

    ⛔⛔ **Bac `ma` tinh o PYTHON bang `canon_ref`.** Mot cau `regexp` trong SQL
       la **ban thu hai** cua phep chuan hoa va no ⛔ khong tuong duong — **da
       do**: `560` vs **`475`**, lech **17,9%**.
    """
    lenh = doc_mot_dong_lenh(conn, pv, pm_line_id)
    if lenh is None:
        return {}
    n = min(max(int(n), 1), SO_TOI_DA)
    dk, ts = _dk_ten(pv, "i.run_id")
    ts = dict(ts, n=n)
    loc_q = ""
    if q and str(q).strip():
        loc_q = ("AND (dg.dien_giai ILIKE %(q)s OR i.doc_no ILIKE %(q)s)")
        ts["q"] = f"%{str(q).strip()}%"

    with conn.cursor() as cur:
        cur.execute(_SQL_SO.format(dk=dk, loc_q=loc_q), ts)
        ten = [c.name for c in cur.description]
        tho = [dict(zip(ten, r)) for r in cur.fetchall()]

    ma_lenh = canon_ref(lenh.get("ref_tho"))
    tien, cur_lenh = lenh.get("amount"), ma_tien_te(lenh.get("curr"))
    ra = []
    for r in tho:
        cung_te = ma_tien_te(r.get("curr")) == cur_lenh
        if ma_lenh and canon_ref(r.get("doc_no")) == ma_lenh:
            bac = "ma"
        elif r.get("tien") == tien and cung_te:
            bac = "tien"
        elif cung_te:
            bac = "cung_tien_te"
        else:
            # ⭐⭐ `BA-07` v3.7 §4h ⓹ *(`WO-032` (d))*: cửa này là **toàn sổ**,
            #   ⛔ lọc tiền tệ ⇒ nhánh `else` cũ dán *"cùng tiền tệ"* lên
            #   **mọi** dòng khác tiền tệ lệnh — sổ thật 02/10 *(`fls-ba`, chỉ
            #   `SELECT`)*: với một lệnh VND **3.926 / 6.165** dòng chưa nối
            #   mang nhãn sai. ⛔ Lọc bỏ chúng: toàn sổ trả lời *"sổ có những
            #   dòng nào"* — người phải **thấy** tiền đã đi bằng ngoại tệ, chỉ
            #   ⛔ được gọi nó là *"cùng tiền tệ"*.
            bac = "khac_tien_te"
        ra.append(khuon_ung_vien(dict(r, bac=bac), lenh=lenh))
    ra.sort(key=lambda x: BAC_XEP.index(x["bac"]))
    return {"dong_lenh": lenh, "ung_vien": ra, "toan_so": True}


#: Thu tu bac — ⭐ ten giu **y nguyen** hai chieu (`BA-07 §4g ⓹`).
#: ⚠ `khac_tien_te` *(v3.7)* **chỉ** sinh ở cửa `/so` — thiếu nó ở đây là
#:   `.index` ném ⇒ `500` cho **cả trang** toàn sổ *(`WO-032` Rủi ro 1)*.
BAC_XEP = ("ma", "tien", "gan_tien", "cung_tien_te", "khac_tien_te")


def can_hoi_truoc_khi_bo_gan(conn, pv: PhamVi, itl_id: int) -> bool:
    """⭐⭐ CHI hoi khi dong tien mang **chum** — do duoc **25/2.222 = 1,1%**.

    ⛔⛔ **⛔ KHONG hoi o ca hai ca *"cho chac"*:** mot hop thoai bat **2.222**
       lan de dung **25** lan la cach nhanh nhat **day nguoi ta bam `OK`
       ⛔ khong doc** — va khi ay no ⛔ khong con can duoc gi o dung `25` lan
       can can.
    """
    return len(chum_cua_dong_tien(conn, pv, itl_id)) > 1


# ── ⓘ khuon THE LENH CHI — **11** truong (`UI-F7`, `QĐ-ITL-147`) ────────

#: ⛔⛔ **Vi sao khuon nay phai o TANG DOC, ⛔ khong o man hinh.**
#:
#: Cua `/queue/lenh-cho` tra `pm_line_id`·`amount`·`curr`·`cdt1`… ＋ mot tui
#: `tho` khoa theo **TEN COT CUA SHEET** *(`"Tên tài khoản"`, `"Pháp nhân
#: thanh toán"`, …)*. Do `22/09`: the lenh chi can **6** truong ma ⛔ **khong
#: cua nao** goi ten — ca 6 chi nam trong `tho`.
#:
#: ⇒ Neu man hinh tu moc `tho["Tên tài khoản"]` thi **JS doc thang ten cot cua
#:   Google Sheets**. Ten cot ay **da doi** *(`itl-xlsx-export`, `PD220`)*, va
#:   khi no doi lan nua thi cho hong la mot **o trong im lang** tren man — ⛔
#:   khong mot bai thu nao do duoc, vi bai thu se go y het ten ay.
#:
#: ⭐ Mot ban khai, mot cho sua, mot cho do.
KHOA_THO: dict[str, tuple[str, ...]] = {
    "nguoi_nhan":  ("Tên tài khoản",),
    "phap_nhan":   ("Pháp nhân thanh toán",),
    "ngan_hang":   ("Ngân hàng",),
    "tai_khoan":   ("Số tài khoản",),
    # ⭐ Hai nguon noi dung: o bank la cai ke toan **doc tren sao ke**, con
    #   `Nội dung PI` la cai **he thong tu sinh**. Do `22/09` tren lan nap
    #   that: bank **3.772/3.772** · PI **3.272/3.772** ⇒ bank di TRUOC.
    "noi_dung":    ("Nội dung giao dịch nhập khi lập lệnh ở bank",
                    "ID PILine - Nội dung PI", "Ghi chú (nếu có)"),
    "loai_phieu":  ("Loại giao dịch (Payment Type)",),
}

#: ⭐ Nhan NGAN cho `loai_phieu`. ⛔ Ban tho dai toi **28** ky tu (*"Tạm ứng
#: bình thường (Advance)"*) va no nam tren **dong dau** cua the, canh ma lenh
#: — mot nhan dai o do day **noi dung** *(cai duy nhat ke toan doc)* ra khoi
#: tam mat. Do `22/09` tren lan nap that: dung **4** gia tri.
#: ⚠ Gia tri la NGHIA ⇒ ⛔ khong cat bang regex: mot ban tho moi se ra mot
#:   nhan la, va luc ay man phai hien **nguyen van** chu ⛔ khong im lang.
NHAN_LOAI: dict[str, str] = {
    "Thanh toán (Regular)": "Regular",
    "Tạm ứng bình thường (Advance)": "Advance",
    "Tạm ứng gấp (Urgent)": "Urgent",
    "Thu tiền": "Thu tiền",
}

#: ⭐⭐ `UI-F9` — **mot su that, MOT cho hien**. Muoi khoa `tho` nay **da nam
#: tren the** roi, nen khoi *"Xem du truong"* ⛔ **khong** duoc lap lai chung:
#: mot con so hien hai lan la mot con so se **lech** vao ngay ai do sua mot
#: trong hai cho.
THO_DA_LEN_THE: frozenset[str] = frozenset({
    "Tổng số tiền thanh toán (Transaction Amount)",   # = `so_tien`
    "Đơn vị tiền tệ (Currency)",                      # = `curr`
    "Loại giao dịch (Payment Type)",                  # = `loai_phieu`
    "Nội dung giao dịch nhập khi lập lệnh ở bank",    # = `noi_dung`
    "Pháp nhân thanh toán", "Ngân hàng",
    "Tên tài khoản", "Số tài khoản",
    "Reference number",                               # = `so_chung_tu`
    "Chủ dự toán (CDT1)",                             # = `cdt`
})

#: ⭐ Nhom cho khoi *"Xem du truong"* — thu tu la thu tu **DOC**.
#: ⚠ Khoa `tho` ⛔ chua khai o day **van hien ra**, o nhom `Khác`. Mot cot MOI
#:   cua sheet ⛔ khong duoc bien mat chi vi ⛔ chua ai khai no.
#: ⭐ Do `22/09`: sheet co **27** khoa · **10** da len the · **17** khoa o day
#:   ⇒ nhom `Khác` hom nay **rong**, va no ton tai cho **ngay mai**.
NHOM_DU_TRUONG: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Lập lệnh", ("Timestamp", "Chi nhánh", "Ghi chú (nếu có)")),
    ("Chứng từ", ("Status_Final", "Status_Log", "Check trùng ID PMLine")),
    ("Đường dẫn phiếu", ("ID PMSlip", "ID PMLine", "ID PISlip", "ID PILine",
                         "ID PILine - Nội dung PI", "ID PESlip", "ID PELine",
                         "ID PELine - Nội dung PE (Advance)",
                         "ID PELine - Nội dung PE (Urgent)")),
    ("Ngân sách", ("Budget Code (HDCode)", "Chủ dự toán *")),
)

#: ⭐ Khoa `tho` cho **so se ri Excel**, ⛔ khong phai chu. Ban TRANG: mot khoa
#: ⛔ chua khai o day se len man **nguyen so** *(`46091.42265217593`)*.
KHOA_NGAY_SE_RI: frozenset[str] = frozenset({"Timestamp"})

#: ⛔ `UI-F7` — **11**. Cung mot con so voi `TRUONG_THE` ben `man_f01_ghep.js`;
#: bai `tests/repo/test_b1_the_lenh_chi.py` canh cho hai ban ⛔ khong lech.
TRUONG_THE = ("ma_lenh", "trang_thai", "loai_phieu", "noi_dung", "so_tien",
              "nguoi_nhan", "so_chung_tu", "phap_nhan", "ngan_hang",
              "tai_khoan", "cdt")


def _lay_tho(tho: dict[str, Any] | None, khoa: tuple[str, ...]) -> Any:
    """Thu tung khoa, tra cai dau tien **co chu**. ⛔ `''` ⇒ VANG."""
    for k in khoa:
        v = (tho or {}).get(k)
        if v is not None and str(v).strip() != "":
            return v
    return None


def khuon_the_lenh(r: dict[str, Any]) -> dict[str, Any]:
    """Hang tho tu `/queue/lenh-cho` ⇒ the lenh chi **11 truong**.

    ⭐⭐ **`None` la mot CAU TRA LOI**, ⛔ khong phai mot cho de bo qua. Man ve
      `— khong co` cho moi truong vang (`INV-I16`), nen o day **⛔ khong duoc**
      thay `None` bang `''` hay bo han khoa di: ca hai deu bien *"lenh nay ⛔
      khong co so chung tu"* thanh *"FLS ⛔ khong biet"*.
      ⭐ Do `22/09` tren lan nap that: `so_chung_tu` vang **535/3.772** =
      **14,2%** ⇒ duong **thuong gap**, ⛔ khong phai ca hiem.

    ⚠ `tai_khoan` di qua `che_tai_khoan` — **cung mot luat** voi `nguon.tk` cua
      ung vien. ⛔ Hai cho che khac nhau la hai muc rieng tu khac nhau.
    ⭐ `nguoi_nhan` hien **NGUYEN** — owner chot `21/09` (`QĐ-ITL-148 ②`): ten
      nguoi nhan la **noi dung cua khoan chi**, ⛔ khong phai ho so nhan su.
      Luat che chi ap cho **ban xuat ra ngoai kho**.
    """
    tho = r.get("tho") or {}
    loai = _lay_tho(tho, KHOA_THO["loai_phieu"])
    tk = _lay_tho(tho, KHOA_THO["tai_khoan"])
    # ⭐⭐ **DANH SACH**, ⛔ khong mot so — do `22/09` tren kho that:
    #   **23/2.219 = 1,0%** lenh chi gan **nhieu hon mot** dong tien. Mot
    #   khoa so it se **im lang bo mat** moi noi thu hai, dung o cho nguoi ta
    #   bam `Bo gan`.
    # ⭐ `1,0%` gan dung `1,1%` ca co chum: **cung mot su that** *(tien va
    #   lenh la quan he nhieu ↔ nhieu)* nhin tu hai phia.
    da_gan = sorted(r.get("itl_da_gan") or [])
    return {
        "ma_lenh": r.get("pm_line_id"),
        # ⭐ `trang_thai` la trang thai **CUA VIEC** *(da noi duoc tien chua)*,
        #   ⛔ khong phai `status` cua sheet *(`Approve`/`Reject`/`Close`)*.
        #   Hai truc khac nhau; gop chung la cach chac nhat de mot dong
        #   `Reject` **da gan** trong y het mot dong ⛔ chua ai dong vao.
        "trang_thai": "da_gan" if da_gan else "chua_gan",
        "trang_thai_nhan": "Đã gán" if da_gan else "Chưa gán",
        "trang_thai_mau": "ok" if da_gan else "",
        "loai_phieu": NHAN_LOAI.get(str(loai), loai),
        "noi_dung": _lay_tho(tho, KHOA_THO["noi_dung"]),
        "so_tien": r.get("amount"),
        "curr": r.get("curr"),
        "nguoi_nhan": _lay_tho(tho, KHOA_THO["nguoi_nhan"]),
        "so_chung_tu": (r.get("ref_tho") or None),
        "phap_nhan": _lay_tho(tho, KHOA_THO["phap_nhan"]),
        "ngan_hang": _lay_tho(tho, KHOA_THO["ngan_hang"]),
        "tai_khoan": che_tai_khoan(tk) if tk is not None else None,
        "cdt": r.get("cdt1"),
        # ⭐ `ngay` — cot **dau** cua BANG SO *(ban dung: `18/09`)*.
        # ⚠ No **⛔ KHONG** dem vao ngan sach `UI-F7 = 11`: tran ay la cua
        #   **THE** o man lam viec, con bang so la mot component khac
        #   *(`C9`)*. Ban dung cho bang **12** cot, va owner da duyet ban ay.
        "ngay": _ngay_ngan(tho),
        # ⭐ `[]` la mot **CAU TRA LOI** *(⛔ chua gan gi)*; thieu khoa la
        #   *"FLS ⛔ khong biet"*. Hai cau khac nhau — `INV-I16`.
        "itl_da_gan": da_gan,
        "nhom_du_truong": du_truong(tho),
    }


def du_truong(tho: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Khoi *"Xem du truong"* — ⭐ phuc vu **niem tin vao du lieu**.

    ⛔⛔ **⛔ KHONG o nao bi bo vi vang.** Mot khoa da khai ma hang tho ⛔ khong
       co van ra mot o `None`, va man ve no thanh `— khong co`. Bo di la bien
       *"dong nay ⛔ khong co Chi nhánh"* thanh *"FLS ⛔ khong biet"* — dung o
       cai khoi sinh ra de **yen tam ve du lieu** (`INV-I16`).
       ⭐ Do `22/09`: `Chi nhánh` chi **11,7%** hang tho co ⇒ **88,3%** so lan
       mo khoi nay, o ay la mot o VANG. No phai **doc duoc**.

    ⛔ Nhom chi bien mat khi **⛔ KHONG khoa nao** cua no co trong hang tho —
      do la ca *"ca nhanh nay ⛔ khong ap dung"*, khac han mot o vang.
    """
    con = dict(tho or {})
    for k in THO_DA_LEN_THE:
        con.pop(k, None)
    # ⛔⛔⛔ **`46091.42265217593` ⛔ KHONG duoc len man mot nguoi.**
    #
    # `BA-06 §4.5 ⓕ` khai *"da het timestamp se ri"*, va khai ay **sai**: no do
    # tren BAN DUNG *(nguoi thiet ke go tay `18/09/2026 09:14`)*, ⛔ khong do
    # tren kho. Do lai `22/09` **tren cua that**: `Timestamp` ra dung
    # **3.772/3.772** dong duoi dang so se ri.
    #
    # ⭐ Doi o day — tang DOC — chu ⛔ khong o JS: phep doi se ri ⇒ ngay da co
    #   mot ban (`ngay_tu_seri`, neo `1899-12-30`, da do doi chieu voi ngay
    #   giao dich that). Viet ban thu hai bang JS la mo lai dung cau hoi
    #   *"nen la ngay nao"* — cau ma du an nay **da tra loi bang phep do**.
    for k in KHOA_NGAY_SE_RI:
        if k in con and con[k] is not None:
            try:
                con[k] = ngay_tu_seri(con[k]).strftime("%d/%m/%Y %H:%M")
            except (ValueError, TypeError, OverflowError):
                pass   # ⛔ ⛔ khong doi duoc thi giu NGUYEN, ⛔ khong xoa
    ra: list[dict[str, Any]] = []
    for ten, khoa in NHOM_DU_TRUONG:
        if not any(k in con for k in khoa):
            continue
        ra.append({"ten": ten, "o": [[k, con.pop(k, None)] for k in khoa]})
    if con:
        # ⭐ Loi thoat cho cot MOI cua sheet — ⛔ khong de no bien mat.
        ra.append({"ten": "Khác", "o": [[k, con[k]] for k in sorted(con)]})
    return ra


# ── ⓙ khoa BANG CHUNG — to cai gi trong dien giai ───────────────────────

#: ⭐ Tu RAC — tu phap ly／chung chung. To chung len thi mau **thoi mang
#: nghia**: mot nen mau o cot Dien giai co nghia *"day dung la khoan cua
#: ban"*, va neu no sang o **moi** dong thi no ⛔ khong con noi gi.
#: ⚠ So sanh bang **chu thuong** ⇒ moi muc o day phai la chu thuong.
#: ⭐ Lay nguyen tu ban dung `fls-gan-lenh-chi_10.html` — ⛔ khong tu bia lai.
TU_RAC: frozenset[str] = frozenset("""
thanh toan toán công ty tnhh cong cty chi phi phí joint stock company corp
corporation inc incorporated ltd limited pte plc llc gmbh group holding
holdings services service trading trade quoc te quốc tế viet nam việt và and
the for bank
""".split())

#: ⛔ Chuoi ngan hon nguong nay se to **rai rac khap** moi dien giai.
DAI_TOI_THIEU = 3

#: ⭐ Dau tach ten ben nhan. ⛔ ⛔ Khong tach bang mot dau cach: ten that mang
#: ca `,` `.` `_` `-` `/` `(` `)` — `"SENSORTOWER, INC."` ma tach bang dau
#: cach se ra khoa `SENSORTOWER,` **kem dau phay**, va no ⛔ khong khop gi.
_TACH_TEN = re.compile(r"[\s,._\-/()]+")


def khoa_bang_chung(lenh: dict[str, Any], uv: dict[str, Any]) -> list[str]:
    """Cac chuoi dang to trong dien giai — ⭐ **dai truoc, ngan sau**.

    Hop dong `§6` doi **ba** nguon, moi nguon mot dieu kien rieng:
      ⓐ `so_chung_tu` — **CHI khi trung dung** so cua lenh chi;
      ⓑ `so_tien` — **CHI khi khop tuyet doi** *(ca so LAN don vi tien)*;
      ⓒ ten ben nhan — sau khi **loc tu rac**.

    ⛔⛔ **Thu tu dai-truoc ⛔ khong phai cho dep.** To `1026946429` roi to
       tiep `102` nam **ben trong** no se ra `<mark>` **long nhau** va HTML
       vo. ⇒ Tang tren quet **mot luot** bang mot regex hop nhat, va thu tu
       nay bao dam **mieng dai thang**.

    ⭐⭐ Dieu kien `ⓑ` doi **ca don vi tien**: cung con so ma khac tien te ma
      van to len la noi rang chung khop — cach nhanh nhat de mot ke toan gan
      nham ca tien te *(`5.264` dong `USD` va `2.683` dong `VND` nam chung
      mot cuon so)*.
    """
    ra: list[str] = []

    ct = lenh.get("so_chung_tu")
    if ct is not None and str(ct).strip() and str(uv.get("doc_no") or "") == str(ct):
        ra.append(str(ct))

    tien = lenh.get("so_tien")
    if (tien is not None
            and str(uv.get("curr")) == str(lenh.get("curr"))
            and _so(uv.get("amount")) is not None
            and _so(uv.get("amount")) == _so(tien)):
        ra.append(str(tien))

    for tu in _TACH_TEN.split(str(lenh.get("nguoi_nhan") or "")):
        if len(tu) >= DAI_TOI_THIEU and tu.lower() not in TU_RAC:
            ra.append(tu)

    thay: set[str] = set()
    sach: list[str] = []
    for k in ra:
        t = k.lower()
        if len(k) < DAI_TOI_THIEU or t in thay:
            continue
        thay.add(t)
        sach.append(k)
    return sorted(sach, key=len, reverse=True)


def _so(x: Any) -> Decimal | None:
    """⛔ Mot phep doi so that bai ⛔ khong duoc lam sap ca man: cot `curr`
    tung mang gia tri `20` *(mot o bi lech cot)*, va kho van phai doc duoc."""
    try:
        return Decimal(str(x))
    except (InvalidOperation, TypeError, ValueError):
        return None


def _ngay_ngan(tho: dict[str, Any] | None) -> str | None:
    """`Timestamp` se-ri ⇒ `dd/mm`. ⛔ ⛔ Khong doc duoc ⇒ `None`, ⛔ khong doan.

    ⭐ Cung phep doi voi `du_truong` *(neo `1899-12-30`, da do doi chieu voi
      ngay giao dich that)* — ⛔ khong mot phep thu hai.
    """
    for k in KHOA_NGAY_SE_RI:
        v = (tho or {}).get(k)
        if v is None:
            continue
        try:
            return ngay_tu_seri(v).strftime("%d/%m")
        except (ValueError, TypeError, OverflowError):
            return None
    return None
