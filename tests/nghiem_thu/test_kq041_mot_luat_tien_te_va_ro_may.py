# -*- coding: utf-8 -*-
"""`KQ-041` *(kiểm gộp `BG-039` + `BG-040` — `WO-037` vòng 1 + 2)* · hai phép
đo **độc lập** mà bài của Dev ⛔ có, và một chỗ *"một luật so tiền tệ"* chưa là
một luật. ⭐ **Viết lại 05/10 ở `KQ-046`** *(`fls-test`, theo `TL-043`)* — xem
khối *"Viết lại"* cuối docstring.

⭐ Cách tìm *(`fls-test`, 05/10)*: `BG-040` yếu #4 tự khai — bài `AC-14` mang
**một bản SQL `btrim`** làm phía "mong" của `tong_cung_tien_te`, nên mã và bài
**cùng trôi một chiều** thì xanh. Phía mong độc lập duy nhất có sẵn là **chính
`man_ghep.ma_tien_te`** *(hàm Python mà rổ `xep_ro` + bậc `ma` + `lech` dùng)*.

ⓐ **Canh** *(xanh)*: tám chuỗi "ca thường" *(space · tab · CR · LF · chữ
   thường)* ⇒ dòng tiền mang mã ấy vào bậc `tien` của lệnh cùng mã.
ⓑ **`F-2`**: `str.strip()` của Python gỡ **nhiều hơn** bốn ký tự SQL cũ —
   `\\x0b` `\\x0c` `\\x85` `\\xa0` *(NBSP)* `\\u2003` `\\u3000`… ⇒ một dòng
   tiền `curr = '\\xa0VND'` ⛔ mã khớp: rổ *(Python)* coi là VND, ba bậc tiền
   *(SQL)* ⛔ bao giờ hiện nó, `tong_cung_tien_te` ⛔ đếm nó. `BA-07` v3.11:
   **một** tập `TAP_TRANG_TIEN_TE` cho Python / SQL / JS ⇒ `WO-042 (c)`.
ⓒ **Canh** *(xanh, sổ THẬT chỉ đọc)*: oracle độc lập của rổ `WO-037`.
ⓓ **`F-3`** *(`NANG`)*: đổi chip khi danh sách `②b` đang tải ⇒ hai lượt đổ
   vào **một** mảng *(8088: `Đã gán` **2955** = 2.219 ＋ 736; bấm lại chip
   đang chọn ⇒ **1.472** = 736 × 2)* ⇒ `WO-042 (a)`, `BA-06` `§4.5 ⓥ`.

⭐⭐ **Viết lại `KQ-046`** *(`TL-043` Q1–Q3 — gác cũ **⛔ thể** qua dưới mã đúng
spec; lo gốc giữ nguyên, dấu `xfail` bỏ)*:
  · `F2` — gác cũ so `ma_tien_te` với **một câu SQL gõ trong chính bài**
    *(`_SQL_VE_SO`, `btrim(…, E' \\t\\r\\n')`)* ⇒ mã đổi gì bài cũng ⛔ thấy.
    Nay đi qua **hàm thật** `lenh_cho.ung_vien_itl` *(có ở cả `77737f7` lẫn
    `db0adae`)* trên **kho TEST**: mỗi chuỗi biên là `curr` của một dòng tiền
    ⛔ mã, cùng số tiền với một lệnh mang mã sạch ⇒ dòng ấy ở bậc `tien`
    **⟺** `ma_tien_te(x) == ma_tien_te(lệnh)`; và `tong_cung_tien_te` = số
    dòng chưa nối mà **Python** coi là `VND` *(oracle)*. ⚠ ⛔ nhập
    `fls.canon.tien_te` — trên `77737f7` bài phải đỏ vì **lệch**, ⛔ vì
    `ImportError`.
  · `F3` đổi chip — gác cũ `goi >= 3` đòi lượt **bị thay** xin tiếp cửa thứ
    hai; `BA-06` v4.19 `ⓥ` ①: lượt bị thay **được dừng ngay**. Nay gác
    *"đo được"* đếm **theo đường**: cả đường `lenh-cho` *(Chưa gán)* lẫn
    `lenh-da-gan` đều có ≥ 1 `GET`. Cửa giả **giữ** từng phản hồi tới khi bài
    thả *(⛔ đồng hồ 40 ms)* — hai thứ tự: lượt cũ về **sau** / về **trước**.
  · `F3` bấm lại chip — gác cũ `goi >= 4` = **hai** lượt × hai cửa, đúng
    điều `ⓥ` ② cấm. Nay số `GET` **=** số `GET` của **một** lượt `Chưa gán`
    đo bằng **mỏ neo** cùng khuôn *(⛔ gõ số 2 cứng)*; số hàng = số hàng của
    một lượt.
  Chứng ĐỎ đúng lý do trên `77737f7` + xanh trên `db0adae`: `KQ-046`.
"""
from __future__ import annotations

import random
import re
import uuid
from collections import Counter
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import DongPM, canon_ref
from fls.api import xu_ly
from fls.db.kho import dsn_test, dsn_that, noi_chi_doc
from fls.ledger.build import NgucCanh
from fls.repo import lenh_cho as lc
from fls.repo.anh_pm import anh_pm_hieu_luc
from fls.repo.chay_nap import chen_dong_pm
from fls.repo.kho_sach import HINH_RUN_THAT
# ⚠ `man_ghep.ma_tien_te` — tên có ở **cả hai** commit *(`db0adae`: trỏ về
#   `fls.canon.tien_te`, cùng đối tượng hàm)*. ⛔ nhập `fls.canon.tien_te`.
from fls.repo.man_ghep import ma_tien_te
from tests.web.ca_wo037 import _tien
from tests.web.khung_node import _chay, can_node

pytestmark = pytest.mark.pg

# ⚠ Ký tự trắng viết bằng `chr(<điểm mã>)`, ⛔ ký tự thật trong nguồn
#   *(bản 05/10 mang `U+3000` + `U+2003` **vô hình** ngay trong dòng này)*.
#: ca thường — ⓐ *(bỏ `""` và `" "`: mã rỗng ⛔ là một tiền tệ của lệnh)*
CA_THUONG = ["VND", " vnd ", "\tUSD", "usd\r\n", "\nSgd\t", "  HKD  ", "eur",
             "Vnd"]
#: ký tự `str.strip()` gỡ mà `btrim(…, E' \t\r\n')` cũ ⛔ gỡ — ⓑ *(6 chuỗi
#: `KQ-041`, giữ nguyên)*
CA_BIEN = [chr(0xA0) + "VND", "VND" + chr(0x0B), chr(0x0C) + "USD",
           "SGD" + chr(0x3000), chr(0x2003) + "HKD", "VND" + chr(0x85)]
#: hai ca canh hai chiều của tập *(`BA-07` v3.11)*: `U+FEFF` **trong** tập
#: v3.11 *(trên `77737f7` Python cũ ⛔ gỡ ⇒ oracle cũ cũng ⛔ — nhất quán)* ·
#: `U+200B` **ngoài** tập ⇒ phải **giữ** *(⛔ lọt vào bậc `tien`)*
CA_CANH_TAP = [chr(0xFEFF) + "VND", chr(0x200B) + "VND"]


def _te_lenh(x: str) -> str:
    """Mã **sạch** của lệnh đi cặp với chuỗi `x` *(chỉ chữ cái ASCII)*."""
    return re.sub(r"[^A-Za-z]", "", x).upper()


@pytest.fixture(scope="module")
def ca_tap():
    """Kho TEST: một lần nạp mới; mỗi chuỗi `x` ⇒ một dòng tiền `curr = x` ⛔
    mã khớp + một lệnh ⛔ số chứng từ, tiền tệ `_te_lenh(x)`, **cùng** số tiền.
    ⚠ Ghi **kho TEST** *(⛔ kho thật — `assert current_database()`)*."""
    ds = CA_THUONG + CA_BIEN + CA_CANH_TAP
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        h = uuid.uuid4().hex[:8].upper()
        run = "NAP-2000-01-01-T41" + h[:6]
        c.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                  " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        goc = random.randint(10_000, 89_999) * 1000
        nguon = "R | 123456789_VPB VND_K41" + h
        ca = []
        for k, x in enumerate(ds):
            tien = goc + 7 * k + 3
            itl = _tien(c, run, nguon, k + 1, f"{tien}.00", x, f"FT41Z{h}{k:02d}")
            ca.append({"x": x, "te": _te_lenh(x), "tien": tien, "itl": itl,
                       "lenh": f"PK41{h[:5]}{k:02d}-1"})
        chen_dong_pm(c, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
            DongPM(3 + k, a["lenh"].split("-")[0], a["lenh"], D(f"{a['tien']}.00"),
                   a["te"], "Approve", None, "HD-K41", "C-K41", ref_tho=None)
            for k, a in enumerate(ca)])
        da = dict(c.execute("SELECT itl_id, curr FROM fls_itl WHERE run_id = %s",
                            (run,)).fetchall())
        assert [da[a["itl"]] for a in ca] == ds, "⛔ kho đổi curr lúc nạp — ca vô nghĩa"
    return {"run": run, "ca": ca}


def _do_ung_vien(ca: list[dict]) -> list[tuple]:
    """Gọi **hàm thật** `ung_vien_itl` cho từng lệnh; trả `(x, có ở bậc tien,
    mong)` — mong = `ma_tien_te(x) == ma_tien_te(lệnh)` *(oracle Python)*."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        pv = xu_ly.pham_vi_cua_yeu_cau({})
        ra = []
        for a in ca:
            r = lc.ung_vien_itl(c, pv, a["lenh"], n=200)
            assert r is not None, f"⛔ không đo được: lệnh {a['lenh']} ⛔ ở ảnh hiệu lực"
            x = [u for u in r["ung_vien"] if u["itl_id"] == a["itl"]]
            co = bool(x) and x[0]["bac"] == "tien"
            ra.append((a["x"], co, ma_tien_te(a["x"]) == ma_tien_te(a["te"]),
                       r["tong_cung_tien_te"], a["te"]))
    return ra


def test_CANH_ca_thuong_dong_tien_vao_BAC_TIEN_qua_ham_that(ca_tap):
    ca = [a for a in ca_tap["ca"] if a["x"] in CA_THUONG]
    ra = _do_ung_vien(ca)
    print(f"KQ-046 ⓐ ca thường · {[(repr(x), co) for x, co, *_ in ra]}")
    assert len(ra) == 8 and all(m for _, _, m, *_ in ra), "⛔ mẫu ca thường hỏng"
    assert [r for r in ra if r[1] != r[2]] == []


def test_F2_ca_bien_HAM_THAT_ung_vien_itl_BANG_ma_tien_te(ca_tap):
    """`F-2` *(lo gốc `KQ-041`)*: dòng tiền mang mã dính ký tự trắng biên ⇒
    bậc tiền *(SQL thật của `lenh_cho`)* và `ma_tien_te` *(Python)* phải là
    **một** luật — cả ở danh sách lẫn ở `tong_cung_tien_te`."""
    ca = [a for a in ca_tap["ca"] if a["x"] in CA_BIEN + CA_CANH_TAP]
    ra = _do_ung_vien(ca)
    lech = [(repr(x), co, mong) for x, co, mong, *_ in ra if co != mong]
    so_bien_mong = sum(1 for x, _, m, *_ in ra if x in CA_BIEN and m)
    print(f"KQ-046 ⓑ F-2 · ca biên mong-có {so_bien_mong}/{len(CA_BIEN)} · "
          f"{[(repr(x), co, m) for x, co, m, *_ in ra]}")
    assert so_bien_mong == len(CA_BIEN), "⛔ không đo được: oracle ⛔ coi ca biên là mã sạch"
    assert not lech, f"⛔ bậc tiền (SQL) ≠ ma_tien_te (Python): {lech}"

    # vế `tong_cung_tien_te` — oracle Python trên **mọi** dòng chưa nối trong
    # phạm vi *(⛔ một bản SQL)*
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        te = [r[0] for r in c.execute(
            "SELECT i.curr FROM fls_itl i WHERE i.run_id ~ %s AND NOT EXISTS"
            " (SELECT 1 FROM fls_moi_noi m WHERE m.itl_id = i.itl_id)",
            (HINH_RUN_THAT.pattern,)).fetchall()]
    dem = {}
    for x, _co, _m, tong, te_l in ra:
        dem.setdefault(te_l, set()).add(tong)
    for te_l, tong in dem.items():
        mong = sum(1 for t in te if ma_tien_te(t) == te_l)
        print(f"KQ-046 ⓑ F-2 · tong_cung_tien_te {te_l}: cửa {sorted(tong)} · oracle {mong}")
        assert mong > 0, f"⛔ tập rỗng (Đ3) {te_l}"
        assert tong == {mong}, (te_l, sorted(tong), mong)


# ═══ ⓒ oracle độc lập của rổ — sổ THẬT chỉ đọc ═════════════════════════════
def _het_trang(c, pv, ro):
    rows, cur = [], None
    for _ in range(100):
        q = {"limit": "500", "ro": ro, **({"cursor": cur} if cur else {})}
        out, _ = xu_ly.lenh_cho(xu_ly.YeuCau(conn=c, pv=pv, q=q, tham={}))
        rows += out["rows"]
        cur = out["next_cursor"]
        if not cur:
            return rows
    raise AssertionError("⛔ không đo được: cửa lenh-cho ⛔ hết trang sau 100 lượt")


def test_CANH_ORACLE_ro_WO037_so_that_khop_tung_pm_line_id():
    with noi_chi_doc(dsn_that()) as c:
        assert c.execute("SHOW default_transaction_read_only").fetchone()[0] == "on"
        pv = xu_ly.pham_vi_cua_yeu_cau({})
        run = anh_pm_hieu_luc(c, pv)
        assert run, "⛔ không đo được: sổ thật ⛔ có ảnh PM hiệu lực"
        dk, ts = pv.dieu_kien("i.run_id")
        lenh = c.execute(
            "SELECT l.pm_line_id, l.ref_tho,"
            " upper(btrim(coalesce(l.curr,''), E' \\t\\r\\n'))"
            " FROM fls_pm_line l WHERE l.run_id = %s AND NOT EXISTS"
            " (SELECT 1 FROM fls_moi_noi m WHERE m.pm_line_id = l.pm_line_id)",
            (run,)).fetchall()
        so = c.execute(
            "SELECT i.doc_no, upper(btrim(coalesce(i.curr,''), E' \\t\\r\\n'))"
            " FROM fls_itl i WHERE " + dk + " AND i.doc_no IS NOT NULL AND NOT EXISTS"
            " (SELECT 1 FROM fls_moi_noi m WHERE m.itl_id = i.itl_id)", ts).fetchall()
        dem = lc.dem_theo_ro(c, pv)
        nguoi = _het_trang(c, pv, "nguoi")
        may = _het_trang(c, pv, "may")
        assert anh_pm_hieu_luc(c, pv) == run, "⛔ không đo được: ảnh PM trôi giữa đo"

    te_theo_ma: dict[str, set[str]] = {}
    for doc_no, cu in so:
        k = canon_ref(doc_no)
        if k:
            te_theo_ma.setdefault(k, set()).add(cu)
    o_ro, khac_te = {}, set()
    for pm, ref, cl in lenh:
        k = canon_ref(ref)
        if not k:
            o_ro[pm] = "nguoi"
        elif k not in te_theo_ma:
            o_ro[pm] = "khong"
        elif cl and cl in te_theo_ma[k]:
            o_ro[pm] = "may"
        else:
            o_ro[pm] = "nguoi"
            khac_te.add(pm)
    oc = Counter(o_ro.values())
    the_vs = {x["pm_line_id"] for x in nguoi if "vi_sao" in (x.get("the") or {})}
    gd_khac = [x["pm_line_id"] for x in may
               if ma_tien_te(((x.get("the") or {}).get("gd") or {}).get("curr"))
               != ma_tien_te(x.get("curr"))]
    print(f"KQ-041 oracle · ảnh {run} · lệnh chờ {len(lenh)} · oracle {dict(oc)} · "
          f"khác tệ {len(khac_te)} · cửa {dem} · the.vi_sao {len(the_vs)} · "
          f"may gd khác tệ {len(gd_khac)}/{len(may)}")
    assert len(lenh) > 0 and len(may) > 0 and len(khac_te) > 0, "⛔ tập rỗng (Đ3)"
    assert len(lenh) == dem["tong"], (len(lenh), dem)
    for ro in ("may", "nguoi", "khong"):
        assert oc[ro] == dem[ro], (ro, oc[ro], dem[ro])
    assert len(khac_te) == dem["nguoi_khac_tien_te"], (len(khac_te), dem)
    assert the_vs == khac_te, (sorted(the_vs - khac_te)[:5], sorted(khac_te - the_vs)[:5])
    assert {x["pm_line_id"] for x in may} == {p for p, r in o_ro.items() if r == "may"}
    assert not gd_khac, gd_khac[:5]


# ═══ ⓓ `F-3` — đổi chip KHI danh sách đang tải ⇒ hai lượt tải đổ vào MỘT mảng ═══
#: ⭐ Đo 05/10 trên **8088 sổ thật chỉ đọc**, Chrome chuột thật *(`KQ-041`)*:
#:   chip `Đã gán` in **`2955 dòng`** = **2.219** ＋ **736**; bấm lại chip đang
#:   chọn `Chưa gán` khi đang tải ⇒ **1.472** = 736 × 2.
#: ⭐ Viết lại `KQ-046`: cửa giả **GIỮ** từng phản hồi tới khi bài thả
#:   *(`_tha` / `_tha_het`)* — thứ tự về do **bài** quyết, ⛔ đồng hồ.
_VO_GHEP = """
const man = d.document.createElement('section'); man.id = 'man-ghep';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
d.body.appendChild(man); d.body.appendChild(goc); d.body.appendChild(tim);
"""
_TEP_GHEP = ["thanh_phan.js", "goi_cua.js", "man_f01_ghep.js"]
#: mỗi đường trả **một** hàng mang tên đường + trạng thái rổ ấy; phản hồi
#: nằm trong `_HANG` tới khi bài thả
_CUA_GIU = """
globalThis._HANG = [];
FLS.doc = function (duong) {
  _GOI.push(['doc', duong]);
  const da = duong.indexOf('lenh-da-gan') >= 0;
  const ma = (da ? 'DA-' : 'CHO-') + duong.replace(/[^a-z_=0-9]/gi, '');
  return new Promise(r => _HANG.push({duong, tra: () => r({data: {rows: [
    {pm_line_id: ma, the: {ma_lenh: ma, trang_thai: da ? 'da_gan' : 'chua_gan'}}],
    next_cursor: null}, meta: {}})}));
};
globalThis._nhip = () => new Promise(r => setTimeout(r, 0));
globalThis._tha = async (khop) => {
  await _nhip();
  const i = _HANG.findIndex(h => khop(h.duong));
  if (i < 0) throw new Error('⛔ không đo được: ⛔ có phản hồi nào đang giữ khớp');
  _HANG.splice(i, 1)[0].tra(); await _nhip(); await _nhip();
};
globalThis._tha_het = async () => {
  for (let k = 0; k < 60; k++) {
    await _nhip(); await _nhip();
    if (!_HANG.length) return;
    _HANG.shift().tra();
  }
  throw new Error('⛔ không đo được: hàng giữ ⛔ cạn sau 60 lượt');
};
"""
_KET = """
  const S = F01G.ST; const d = S.dong;
  const theo = (re) => _GOI.filter(g => g[0] === 'doc' && re.test(g[1])).length;
  return {chip: S.chip, n: d.length, khac: new Set(d.map(x => x.ma_lenh)).size,
          tt: d.map(x => x.trang_thai), dang_tai: S.dang_tai, loi: S.loi,
          goi: _GOI.filter(g => g[0] === 'doc').length,
          goi_cho: theo(/lenh-cho\\?/), goi_da: theo(/lenh-da-gan/),
          giua: (typeof _GIUA === 'undefined') ? null : _GIUA};"""


def _chay_giu(kich_ban: str) -> dict:
    return _chay(_CUA_GIU + kich_ban + _KET, tep=_TEP_GHEP, vo=_VO_GHEP)


def _mot_luot_chua_gan() -> dict:
    """Mỏ neo: **một** lượt `Chưa gán` đơn, tải xong ⇒ số `GET` + số hàng
    của một lượt *(hôm nay: hai đường của chip)*."""
    return _chay_giu("const a = F01G.doi_chip('chua_gan'); await _tha_het(); await a;")


@can_node
def test_CANH_doi_chip_SAU_khi_tai_xong_danh_sach_dung_mot_ro():
    """Mỏ neo xanh: đợi tải xong rồi đổi chip ⇒ chỉ hàng `da_gan`."""
    r = _chay_giu("let a = F01G.doi_chip('chua_gan'); await _tha_het(); await a;"
                  " a = F01G.doi_chip('da_gan'); await _tha_het(); await a;")
    assert r["goi_cho"] >= 1 and r["goi_da"] >= 1, f"⛔ không đo được: {r}"
    assert r["chip"] == "da_gan" and r["tt"] == ["da_gan"], r


@can_node
@pytest.mark.parametrize("thu_tu", ["cu_ve_SAU", "cu_ve_TRUOC"])
def test_F3_doi_chip_KHI_DANG_TAI_danh_sach_KHONG_tron_ro_cu(thu_tu):
    """`F-3` ⓐ *(`WO-042` `AC-1`)*: bấm `Chưa gán` rồi `Đã gán` khi lượt đầu
    còn bay. Hai thứ tự về: lượt cũ về **sau** lượt mới / về **trước**."""
    tha_dau = ("await _tha(d => d.indexOf('lenh-da-gan') >= 0);"
               if thu_tu == "cu_ve_SAU" else
               "await _tha(d => d.indexOf('lenh-cho?') >= 0);")
    r = _chay_giu(
        "const a = F01G.doi_chip('chua_gan'); await _nhip();"
        " const b = F01G.doi_chip('da_gan'); await _nhip();"
        + tha_dau
        + " globalThis._GIUA = {dang_tai: F01G.ST.dang_tai, n: F01G.ST.dong.length};"
        " await _tha_het(); await a; await b;")
    print(f"KQ-046 F-3 đổi chip ({thu_tu}) · {r}")
    # gác "đo được" — đếm THEO ĐƯỜNG (`BA-06` v4.19 `ⓥ` ①): cả hai chip đã bay
    assert r["goi_cho"] >= 1 and r["goi_da"] >= 1, f"⛔ không đo được: {r}"
    assert r["chip"] == "da_gan", r
    assert r["tt"] == ["da_gan"], f"⛔ chip 'Đã gán' mang hàng rổ khác: {r}"
    assert r["dang_tai"] is False and r["loi"] is None, r


@can_node
def test_F3_bam_lai_chip_DANG_CHON_khi_dang_tai_KHONG_nhan_doi():
    """`F-3` ⓑ *(`WO-042` `AC-2`, `ⓥ` ②)*: bấm lại chip đang chọn khi lượt
    của nó còn bay ⇒ **0** `GET` thêm, mỗi lệnh **một** lần."""
    neo = _mot_luot_chua_gan()
    assert neo["goi"] >= 1 and neo["n"] >= 1, f"⛔ không đo được (mỏ neo): {neo}"
    assert neo["tt"] == ["chua_gan"] * neo["n"], neo
    r = _chay_giu("const a = F01G.doi_chip('chua_gan'); await _nhip();"
                  " const b = F01G.doi_chip('chua_gan');"
                  " await _tha_het(); await a; await b;")
    print(f"KQ-046 F-3 bấm lại · mỏ neo một lượt {neo['goi']} GET / {neo['n']} hàng · đo {r}")
    assert r["n"] == r["khac"] == neo["n"], f"⛔ mỗi lệnh hiện hai lần: {r} · neo {neo}"
    assert r["goi"] == neo["goi"], f"⛔ mở lượt thứ hai: {r['goi']} GET ≠ một lượt {neo['goi']}"
