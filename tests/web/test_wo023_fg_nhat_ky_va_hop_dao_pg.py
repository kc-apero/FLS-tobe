# -*- coding: utf-8 -*-
"""`WO-023` `(f)` + `(g)` · `BA-06` **v4.12** *(dòng "F02 · nhật ký" ⓐ…ⓔ · dòng
"F02 · hoàn tác" ⓐ…ⓒ)* · `BA-07` **v3.6** *(`la_ban_dao` · `but_toan[].nguon`)*.

⛔⛔ Lỗi gốc *(`KQ-025` `F-3` · `F-4`, mã khi nhận `7e67a09`)*:
  `(f)` ⑦ in bản đảo giá trị **người** `X → (trống) · người sửa` — **y hệt** cú
        người xoá ô *(`/adjust value=null`)*.
  `(g)` hộp `Đảo` hứa *"giá trị lùi về bút toán trước đó…"* cho **mọi** bút
        toán — kể cả gợi ý **máy**, nơi đảo **⛔ đổi Final** *(`QĐ-ITL-149`)*.

⭐ Thân **cửa HTTP thật** trên kho TEST *(`dung_ca_wo023` — ghép/bỏ ghép thật,
`/adjust` thật, `/reverse` thật)* ⇒ màn `F02` ⑦ / hộp `Đảo`. Nút `Đảo` dựng
bằng `innerHTML` *(DOM giả ⛔ phân tích HTML ⇒ ⛔ bấm được)* ⇒ bài đọc
`data-dao` + `data-nguon` của **từng nút** trong HTML ⑥ rồi gọi `F02._dao` với
**đúng** ba tham số trình nghe `onclick` sẽ gọi; Chrome *(`BG`)* bấm nút thật.
"""
from __future__ import annotations

import json
import re

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.ca_wo023 import dung_ca_wo023
from tests.web.khung_node import _VE, _chay, can_node
from tests.web.test_vong_f02_pg import V, _goi, _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import NHAN_NGUOI, RUT, _bang_nhat_ky
from tests.web.test_wo023_ab_hop_modal_va_hop_cho_cua import VO_F02S

pytestmark = [pytest.mark.pg]

DAO = "đảo — giá trị này hết hiệu lực"
XOA = "xoá ô"


def _ok(m, duong, **kw):
    st, r = _goi(m, V + duong, **kw)
    assert st == 200, (duong, st, r)
    return r["data"]


def _adj(m, itl, field, value):
    return _ok(m, f"/ledger/{itl}/adjust", pt="POST",
               than={"field": field, "value": value, "force": True,
                     "reason": "WO-023 (f)(g)"})


def _dao(m, adj):
    return _ok(m, f"/adjustments/{adj}/reverse", pt="POST",
               than={"reason": "WO-023 (f)(g) dao"})


def _bt(m, itl):
    return _ok(m, f"/ledger/{itl}")["but_toan"]


@pytest.fixture(scope="module")
def ca():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_wo023(c)
    i, L = ca["i"], ca["lenh"]
    with _may() as m:
        # ⓐ M3 · invoice: người gõ X rồi Đảo
        a = _adj(m, i["M3"], "invoice", "INV-X")["adj_id"]
        _dao(m, a)
        # ⓑ M3 · cdt1: gõ C-1 rồi gõ ô rỗng (xoá ô)
        _adj(m, i["M3"], "cdt1", "C-1")
        _adj(m, i["M3"], "cdt1", None)
        # ⓓ M3 · id_payee: gõ A rồi B, đảo A ⇒ Final vẫn B
        pa = _adj(m, i["M3"], "id_payee", "PAY-A")["adj_id"]
        _adj(m, i["M3"], "id_payee", "PAY-B")
        _dao(m, pa)
        # ⓒ M2: ghép rồi bỏ ghép ⇒ "rút gợi ý"
        _ok(m, f"/queue/{i['M2']}/match", pt="POST", than={"pm_line_ids": [L]})
        _ok(m, f"/queue/{i['M2']}/unmatch", pt="POST", than={})
        ca["nk"] = {k: _ok(m, f"/journal?itl_id={i[k]}")["rows"] for k in ("M2", "M3")}
        # (g) M2 lần hai: ghép lại ⇒ gợi ý máy hd/cdt1; người gõ cdt1 ĐÈ lên
        #   *(M1 lệch 2.000 với lệnh nào cũng ngoài dung sai ⇒ cửa 422)*
        _ok(m, f"/queue/{i['M2']}/match", pt="POST", than={"pm_line_ids": [L]})
        _adj(m, i["M2"], "cdt1", "C-NGUOI-G")
        ca["nk"]["G"] = _ok(m, f"/journal?itl_id={i['M2']}")["rows"]
        ca["led"] = {k: _ok(m, f"/ledger/{i[k]}") for k in ("M2", "M3")}
        ca["pay"] = _ok(m, f"/ledger/{i['M3']}/fields/id_payee")
    return ca


def _ve_nk(ca, k: str) -> list[list[str]]:
    itl = ca["i"]["M2" if k == "G" else k]
    led = ca["led"].get("M2" if k == "G" else k) or {"itl_id": itl, "but_toan": []}
    ra = _chay(("""
      _TRA['/ledger/%d'] = {data: %s};
      _TRA['/journal'] = {data: {rows: %s}};
    """ % (itl, json.dumps(led, ensure_ascii=False, default=str),
           json.dumps(ca["nk"][k], ensure_ascii=False, default=str))) + _VE + """
      await F02.mo_drawer(%d);
      await new Promise(r => setTimeout(r, 0));
      return document.querySelector('#so-panel').textContent;
    """ % itl, tep=None, vo=VO_F02S)
    return _bang_nhat_ky(ra), ra


# ══ (f) nhật ký ⑦ ═══════════════════════════════════════════════════════

def test_AC8e_than_GET_journal__MOI_dong_co_la_ban_dao_BOOL(ca):
    rows = [r for k in ca["nk"] for r in ca["nk"][k]]
    assert len(rows) >= 10, ("⛔ không đo được: ít dòng nhật ký", len(rows))
    assert all(type(r.get("la_ban_dao")) is bool for r in rows), \
        [r for r in rows if type(r.get("la_ban_dao")) is not bool][:3]
    assert {r["la_ban_dao"] for r in rows} == {True, False}, "⛔ mẫu số: cần cả hai giá trị"


@can_node
def test_AC8_man_F02_7_DAO_nguoi__XOA_O__RUT_GOI_Y__theo_LOP(ca):
    """ⓐ `INV-X` đảo ⇒ hàng *"đảo — giá trị này hết hiệu lực"*, **0** hàng
    `(trống)` của `invoice`; ⓑ `cdt1` gõ rỗng ⇒ *"xoá ô"*; ⓓ đảo `PAY-A` ⇒
    *"đảo — …"* và cửa `fields/id_payee` vẫn `PAY-B`. ⛔ Chiều ĐỎ *(mã khi
    nhận)*: cửa ⛔ trả `la_ban_dao` ⇒ hàng đảo in ô trống như cú xoá."""
    hang, _ = _ve_nk(ca, "M3")
    o = {(h[1], h[3]) for h in hang}
    assert ("invoice", "INV-X") in o and ("invoice", DAO) in o, hang
    assert ("cdt1", "C-1") in o and ("cdt1", XOA) in o, hang
    assert ("id_payee", DAO) in o, hang
    assert not [h for h in hang if h[1] == "invoice" and h[3] == ""], hang
    assert not [h for h in hang if h[3] == ""], ("⛔ còn hàng ô trống", hang)
    assert [h[5] for h in hang if h[3] in (DAO, XOA)] and \
        {h[5] for h in hang if h[3] in (DAO, XOA)} == {NHAN_NGUOI}, hang
    assert ca["pay"]["gia_tri"] == "PAY-B", ca["pay"]


@can_node
def test_AC8c_ghep_bo_ghep__RUT_GOI_Y_khong_doi(ca):
    hang, _ = _ve_nk(ca, "M2")
    rut = [h for h in hang if h[3] == RUT]
    assert len(rut) >= 2, ("⛔ mẫu số: ≥ 2 hàng rút gợi ý", hang)
    assert not [h for h in hang if h[3] in (DAO, XOA)], hang


# ══ (g) hộp Đảo theo lớp ════════════════════════════════════════════════

def _nut_dao(html: str) -> list[tuple[int, str]]:
    return [(int(a), n) for a, n in re.findall(
        r'data-dao="(\d+)" data-nguon="([^"]*)"', html)]


def test_AC9_than_GET_ledger__MOI_but_toan_co_nguon__hai_ma(ca):
    bt = ca["led"]["M2"]["but_toan"]
    assert len(bt) >= 2 and all("nguon" in b for b in bt), bt
    assert {b["nguon"] for b in bt} >= {"may_goi_y", "sua_tay"}, bt


@can_node
def test_AC9_hop_DAO_theo_LOP_cua_CHINH_but_toan__may_duoi_nguoi(ca):
    """Dòng `M2` *(ghép lần hai)*: ô `cdt1` có gợi ý **máy** *(dưới)* + giá trị **người** *(trên)*.
    Đảo bút toán máy ⇒ *"không đổi Final"*, ⛔ *"lùi về"*; đảo bút toán người ⇒
    *"hết hiệu lực"* + *"lùi về"*. ⛔ Chiều ĐỎ: lấy `nguon` theo **ô** *(bút toán
    trên cùng `cdt1` = người)* ⇒ hộp của bút toán máy nói *"lùi về"*."""
    itl = ca["i"]["M2"]
    bt = ca["led"]["M2"]["but_toan"]
    da_dao = {b["reversal_of"] for b in bt if b["reversal_of"]}
    may = [b for b in bt if b["field"] == "cdt1" and b["nguon"] == "may_goi_y"
           and not b["reversal_of"] and b["adj_id"] not in da_dao]
    nguoi = [b for b in bt if b["field"] == "cdt1" and b["nguon"] == "sua_tay"
             and not b["reversal_of"]]
    assert may and nguoi and may[0]["adj_id"] < nguoi[0]["adj_id"], ("⛔ không đo được", bt)
    _, panel = _ve_nk(ca, "G")
    nut = dict(_nut_dao(panel))
    assert nut.get(may[0]["adj_id"]) == "may_goi_y", nut
    assert nut.get(nguoi[0]["adj_id"]) == "sua_tay", nut
    r = _chay(("""
      _TRA['/ledger/%d'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
    """ % (itl, json.dumps(ca["led"]["M2"], ensure_ascii=False, default=str))) + _VE + """
      const hop = () => ({t: document.getElementById('dlg-t').textContent,
                          b: document.getElementById('dlg-b').textContent});
      F02._dao(%d, %d, %s); const may = hop(); HT.dong();
      F02._dao(%d, %d, %s); const nguoi = hop(); HT.dong();
      F02._dao(77, %d, 'xyz'); const la = hop(); HT.dong();
      return {may, nguoi, la};
    """ % (may[0]["adj_id"], itl, json.dumps(nut[may[0]["adj_id"]]),
           nguoi[0]["adj_id"], itl, json.dumps(nut[nguoi[0]["adj_id"]]), itl),
        tep=None, vo=VO_F02S)
    assert r["may"]["t"] == f"Rút gợi ý máy #{may[0]['adj_id']}", r["may"]
    assert "không đổi Final" in r["may"]["b"] and "lùi về" not in r["may"]["b"], r["may"]
    assert r["nguoi"]["t"] == f"Đảo bút toán #{nguoi[0]['adj_id']}", r["nguoi"]
    assert "hết hiệu lực" in r["nguoi"]["b"] and "lùi về" in r["nguoi"]["b"], r["nguoi"]
    assert "chưa biết" in r["la"]["b"] and "xyz" in r["la"]["b"], r["la"]
    for k in ("may", "nguoi", "la"):
        assert "Đảo <b>không xoá</b> gì cả" in r[k]["b"], r[k]
