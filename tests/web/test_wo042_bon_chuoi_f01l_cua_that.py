# -*- coding: utf-8 -*-
"""`WO-042 (b)` · `AC-6` — bốn chuỗi `F01L` *(`BA-06` **v4.18** `§4.5 ⓤ` bảng
ⓐ…ⓓ)* vẽ từ thân **`/lenh-cho/ro` CỬA THẬT** trên **kho TEST**.

⛔⛔ Lỗi gốc *(`KQ-041 F-1`, sổ thật chỉ đọc, hàm thật `ds_tu_chung`)*: rổ `may`
**184** = tự chứng **64** ＋ cửa ghi ⛔ nhận theo lô **120**. Ba chỗ của `F01L`
hứa *"lệch tiền"* / *"khớp đúng một dòng — người chỉ DUYỆT"* cho cả rổ —
*"lệch tiền"* đúng **78 / 120**, *"chỉ DUYỆT"* sai **120 / 184** — và câu ghi
chú v4.17 gọi `chum_lech_tien` là *"nhiều dòng tiền cùng mã"*.

⛔ Luật của tệp *(`BA-07` §4h ⓵ — luật bài thử)*: thân lấy từ **cửa HTTP thật**
*(ca `tests/web/ca_wo042.dung_ca_wo042` — có **cả** `t > 0` lẫn `c > 0`, thứ ca
`WO-037` v2 ⛔ có: `tu_chung = 0` ⇒ `note ok` ⓑ ⛔ bao giờ vẽ)*, đưa
**nguyên văn** vào `_TRA`.

Chữ **mong** chép **nguyên văn** từ spec *(⛔ đọc từ JS — bài sẽ tự so với
chính nó)*; riêng `LY_DO_LO` còn so **thêm** với hằng màn xuất ra để bắt hai
bản gõ lệch nhau.
"""
from __future__ import annotations

import json
import os
import re

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.ca_wo032 import goi_ok
from tests.web.ca_wo042 import dung_ca_wo042
from tests.web.khung_node import _chay, can_node
from tests.web.test_luat_ky_hieu_man_hinh import CAM
from tests.web.test_vong_f02_pg import _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = pytest.mark.pg

RO = "/queue/lenh-cho/ro"
NGUON = os.path.join(os.path.dirname(__file__), "..", "..", "fls", "web", "tep",
                     "man_f01_lenh.js")

#: ⭐ Chữ **nguyên văn** `BA-06` v4.18 `§4.5 ⓤ` *(dòng 702 — mở đầu một dấu cách)*
LY_DO_LO = (" khớp số chứng từ cùng tiền tệ nhưng cửa ghi chưa nhận theo lô — "
            "lệch tiền, nhiều dòng tiền cùng mã, một dòng tiền mang mã của nhiều "
            "dòng lệnh mà tổng các dòng lệnh khác tiền bank, có dòng lệnh cùng "
            "chùm chưa được duyệt, hoặc vướng một cổng khác của cửa ghi.")
#: ⓐ băng · ghi chú `note warn` *(＋ liên kết `Xem <c> dòng`)*
GHI_CHU_A = "Còn {c} dòng" + LY_DO_LO + " Phải mở từng dòng. " + "Xem {c} dòng"
#: ⓑ dưới bảng rổ · `note ok`
NOTE_OK_B = ("Trong rổ “máy trả lời được” có {t} dòng tự chứng — khớp cả số "
             "chứng từ, số tiền và tiền tệ; cửa ghi nhận chúng theo lô. Còn {c} "
             "dòng" + LY_DO_LO + " Phải mở từng dòng.")
#: ⓒ thanh lọc khi đang xem rổ `may` ⛔ tự chứng
NHAN_C = "đang xem rổ: máy trả lời được · chỉ CHƯA NHẬN THEO LÔ"
#: ⓓ bảng rổ · hàng `may` · *Nghĩa là gì*
RO_MAY_D = ("Số chứng từ khớp ít nhất một dòng tiền cùng tiền tệ — máy đề xuất "
            "được dòng tiền. Dòng tự chứng được duyệt theo lô; các dòng còn lại "
            "phải mở từng dòng.")

#: chữ CŨ *(biên bản)* — quét nguồn ngoài chú thích phải ra **0**
CU = ["chỉ LỆCH TIỀN", "người chỉ DUYỆT", "khớp đúng một dòng tiền trong sổ",
      "lại khớp số chứng từ nhưng"]


@pytest.fixture(scope="module")
def than_ro():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        dung_ca_wo042(c)
    with _may() as m:
        return goi_ok(m, RO)["data"]


_VE = """
  const TRA = %(than)s;
  _TRA['/queue/lenh-cho/ro'] = {data: TRA};
  const cho = async () => { for (let i = 0; i < 30; i++) await Promise.resolve(); };
  const o = document.createElement('div'); document.body.appendChild(o);
  await F01L.ve_viec(o);
  const ghi = o.querySelectorAll('.note').filter(x => x.className.includes('warn'));
  const r = document.createElement('div'); document.body.appendChild(r);
  await F01L.ve_ro(r);
  const ok = r.querySelectorAll('.note').filter(x => x.className.includes('ok'));
  const tr = r.querySelectorAll('tr').filter(x => x.textContent.includes('máy trả lời được'));
  // ⓒ đi đúng đường người bấm: liên kết `Xem <c> dòng` ⇒ `_loc('may', false)`
  const vo = document.querySelector('#than-f01');
  F01L.ve(vo); await cho();
  const lk = vo.querySelector('#f01l-lech');
  if (lk) { lk.onclick({preventDefault() {}}); await cho(); }
  const lbl = vo.querySelectorAll('.lbl').map(x => x.textContent)
                .filter(x => x.startsWith('đang xem rổ'));
  return {ghi_a: ghi.map(x => x.textContent),
          ok_b: ok.map(x => x.textContent),
          nhan_c: lbl,
          ro_may_d: tr.length ? tr[0].children[2].textContent : null,
          st: {ro: F01L.ST.ro, tu_chung: F01L.ST.tu_chung},
          ly_do_lo: F01L.LY_DO_LO,
          goi: _GOI.map(g => g[1])};
"""


def _ve(than: dict) -> dict:
    return _chay(_VE % {"than": json.dumps(than, ensure_ascii=False)},
                 tep=TEP_F01, vo=VO_F01)


def _cam(*s: str) -> list[str]:
    return sorted({ch for x in s for ch in (x or "") if ch in CAM})


@can_node
def test_AC6_bon_chuoi_F01L_DUNG_chu_v4_18_so_tu_CUA(than_ro):
    d = than_ro
    t, c = d["tu_chung"], d["may"] - d["tu_chung"]
    print(f"WO-042 AC-6 · /ro {d} ⇒ t {t} · c {c}")
    assert t > 0 and c > 0, ("⛔ không đo được: ca thiếu t hoặc c", d)
    r = _ve(d)
    so = lambda n: f"{n:,}".replace(",", ".")          # noqa: E731 — TP.so vi-VN
    assert r["ghi_a"] == [GHI_CHU_A.format(c=so(c))], r["ghi_a"]
    assert r["ok_b"] == [NOTE_OK_B.format(t=so(t), c=so(c))], r["ok_b"]
    assert r["st"] == {"ro": "may", "tu_chung": False}, r["st"]
    assert r["nhan_c"] == [NHAN_C], r["nhan_c"]
    assert r["ro_may_d"] == RO_MAY_D, r["ro_may_d"]
    assert not _cam(*r["ghi_a"], *r["ok_b"], *r["nhan_c"], r["ro_may_d"]), r


@can_node
def test_AC6_LY_DO_LO_GIONG_HET_o_a_va_b_va_bang_hang_man(than_ro):
    """Câu `LY_DO_LO` xuất hiện **giống hệt** ở ⓐ và ⓑ, và **=** hằng màn
    xuất *(một hằng — ⛔ hai bản gõ)*. ⛔ Chiều ĐỎ: sửa một ký tự ở một chỗ
    ⇒ đỏ."""
    r = _ve(than_ro)
    assert r["ly_do_lo"] == LY_DO_LO, "⛔ hằng màn ≠ chữ v4.18"
    assert LY_DO_LO in r["ghi_a"][0] and LY_DO_LO in r["ok_b"][0], r


def _bo_chu_thich_js(src: str) -> str:
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", src, flags=re.S)


def test_AC6_QUET_nguon_KHONG_con_chu_cu_ngoai_chu_thich():
    src = open(NGUON, encoding="utf-8").read()
    ma = _bo_chu_thich_js(src)
    assert "chỉ CHƯA NHẬN THEO LÔ" in ma, "⛔ không đo được: chữ mới ⛔ có trong mã"
    con = {x: ma.count(x) for x in CU}
    assert not any(con.values()), con
    # tự chứng: chữ cũ đặt ngoài chú thích thì bị bắt
    assert "chỉ LỆCH TIỀN" in _bo_chu_thich_js("x = ' · chỉ LỆCH TIỀN'; /* a */")
    # `LY_DO_LO` gõ **một** lần trong mã *(⛔ hai bản)*
    assert ma.count("cổng khác của cửa ghi") == 1, ma.count("cổng khác của cửa ghi")
