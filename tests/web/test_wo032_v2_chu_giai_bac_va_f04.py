# -*- coding: utf-8 -*-
"""`WO-032` **vòng 2** — `(j)` chú giải bậc ở `F01G` *(`BA-06` v4.15 §4.5 ⓒ ①)* ·
`(k)` `F04` `_ve_thu_tu` rỗng vẽ được.

⛔⛔ `(j)` — lỗi gốc *(`BG-034` yếu #7, `TL-033 ⓑ`)*: quyết ① nói nghĩa bậc ở
*"chú giải ＋ `title`"* từ 21/09, nhưng chú giải **⛔ bao giờ được dựng** *(grep
`tlegend`/`chu_giai` ở `fls/web/` + `tests/web/` **0**; bản dựng đã duyệt
`Artifacts/fls-gan-lenh-chi_10.html:739` **có**)* ⇒ **cả năm** ký hiệu
`①②③④≠` chỉ đọc được bằng di chuột — trái quyết ② *("⛔ tooltip ⛔ được là lối
**duy nhất**")*. Chữ chú giải **sinh từ `BAC`** — ⛔ gõ tay: thêm bậc mà quên
chú giải là nói thiếu **im lặng**.

⛔ Luật của tệp *(`BA-07` §4h ⓵ — luật bài thử)*: thân vẽ màn lấy từ **cửa HTTP
thật** trên **kho TEST** *(ca `tests/web/ca_wo032.py`)*. Ca **rỗng** đi đường
khung trả `data: null` cho đường ⛔ có thân — đúng hình `?gia_lap=rong` của vỏ,
⛔ một khoá do bài đặt.
"""
from __future__ import annotations

import json
import os
import re

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.web import phuc_vu as pv
from tests.web.ca_wo032 import dung_ca, goi_ok
from tests.web.khung_node import TEP_F04, VO_F04, _chay, can_node
from tests.web.test_vong_f02_pg import _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = pytest.mark.pg

D_NGUOI = "/queue/lenh-cho?ro=nguoi&limit=500"
D_MAY = "/queue/lenh-cho?ro=may&tu_chung=0&limit=500"
D_DA_GAN = "/queue/lenh-da-gan?limit=500"


@pytest.fixture(scope="module")
def ca_tra():
    """`(ca, {đường MÀN gọi: thân 'data' cửa thật})` — đúng chuỗi `F01G` gọi."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca(c)
    L = ca["lenh"]
    duong = [D_NGUOI, D_MAY, D_DA_GAN,
             f"/queue/lenh/{L['A']}/itl-candidates",
             f"/queue/lenh/{L['A']}/so?q={ca['h']}"]
    with _may() as m:
        tra = {d: goi_ok(m, d)["data"] for d in duong}
    return ca, tra


def _nap(tra: dict) -> str:
    return ("const TRA = %s;\n"
            "for (const k of Object.keys(TRA)) _TRA[k] = {data: TRA[k]};\n"
            % json.dumps(tra, ensure_ascii=False, default=str))


#: Đọc chú giải: số phần tử `.tlegend`, chữ **nhìn thấy** *(`textContent`)*,
#: và **mọi** mục của `BAC` lúc vẽ.
_DOC = """
  const cg = document.querySelectorAll('.tlegend');
  return {n: cg.length, chu: cg.length ? cg[0].textContent : null,
          title: cg.length ? cg[0].getAttribute('title') : null,
          bac: Object.keys(F01G.BAC).map(k => [k, F01G.BAC[k].k, F01G.BAC[k].l]),
          uv: F01G.ST.ung_vien.length, toan_so: F01G.ST.toan_so};
"""

_MAY_DE_XUAT = """
  await F01G.mo_man();
  await F01G.mo_lenh(%(ma)s);
""" + _DOC

_TOAN_SO = """
  await F01G.mo_man();
  await F01G.mo_lenh(%(ma)s);
  F01G.ST.tim = %(q)s;
  await F01G.tai_toan_so(%(ma)s);
  F01G.ST.toan_so = true;
  F01G.ve();
""" + _DOC


def _kiem_du(r: dict):
    """Đúng **một** chú giải; mọi mục `BAC` có **cả** ký hiệu lẫn nghĩa trong
    chữ nhìn thấy *(⛔ chỉ `title`)*."""
    assert r["n"] == 1, f"⛔ mong ĐÚNG 1 chú giải, gặp {r['n']}"
    assert r["uv"] > 0, "⛔ không đo được: 0 ứng viên"
    thieu = [b for b in r["bac"] if b[1] not in r["chu"] or b[2] not in r["chu"]]
    assert not thieu, f"⛔ chú giải thiếu {thieu} — chữ: {r['chu']!r}"
    assert len(r["bac"]) >= 5, r["bac"]


@can_node
def test_AC13_chu_giai_MAY_DE_XUAT_dung_mot_va_du_moi_bac_tu_BAC(ca_tra):
    """Chế độ *Máy đề xuất* *(cửa `itl-candidates` thật của lệnh `A`)*.

    ⛔ Chiều ĐỎ *(mã `363a441`)*: **0** `.tlegend` ⇒ ĐỎ."""
    ca, tra = ca_tra
    r = _chay(_nap(tra) + _MAY_DE_XUAT % {"ma": json.dumps(ca["lenh"]["A"])},
              tep=TEP_F01, vo=VO_F01)
    assert r["toan_so"] is False, r
    print(f"WO-032 v2 AC-13 · máy đề xuất: {r['uv']} ứng viên · chú giải "
          f"{r['n']} · {r['chu']!r}")
    _kiem_du(r)


@can_node
def test_AC13_chu_giai_TOAN_SO_dung_mot_co_KHAC_TIEN_TE_bang_CHU(ca_tra):
    """Chế độ *Toàn sổ* *(cửa `/so` thật — có dòng USD cạnh lệnh VND, bậc
    `khac_tien_te`)* ⇒ chú giải hiện **chữ** `≠ khác tiền tệ` *(`AC-5` đính
    chính)*. ⛔ Chiều ĐỎ *(mã `363a441`)*: **0** `.tlegend` ⇒ ĐỎ."""
    ca, tra = ca_tra
    r = _chay(_nap(tra) + _TOAN_SO % {"ma": json.dumps(ca["lenh"]["A"]),
                                      "q": json.dumps(ca["h"])},
              tep=TEP_F01, vo=VO_F01)
    assert r["toan_so"] is True, r
    print(f"WO-032 v2 AC-13 · toàn sổ: {r['uv']} dòng · {r['chu']!r}")
    _kiem_du(r)
    assert "≠" in r["chu"] and "khác tiền tệ" in r["chu"], r["chu"]


@can_node
def test_AC13_them_BAC_GIA_thi_chu_giai_CO_bac_ay(ca_tra):
    """Chữ chú giải **sinh từ `BAC`**: thêm một bậc giả vào `BAC` rồi vẽ lại ⇒
    chú giải có mục ấy. ⛔ Chiều ĐỎ: chú giải gõ tay năm mục ⇒ thiếu `⑨` ⇒ ĐỎ."""
    ca, tra = ca_tra
    r = _chay(_nap(tra) + """
      await F01G.mo_man();
      await F01G.mo_lenh(%s);
      F01G.BAC.gia_cua_bai = {k: '⑨', l: 'bậc giả của bài thử', m: ''};
      F01G.ve();
    """ % json.dumps(ca["lenh"]["A"]) + _DOC, tep=TEP_F01, vo=VO_F01)
    _kiem_du(r)
    assert "⑨" in r["chu"] and "bậc giả của bài thử" in r["chu"], r["chu"]


@can_node
def test_AC13_danh_sach_RONG_thi_KHONG_chu_giai(ca_tra):
    """`BA-06` v4.15 §4.5 ⓒ ①: *"⛔ hiện khi danh sách rỗng"* — ⛔ có ký hiệu
    nào để giải. Hai cửa ứng viên trả `data: null` *(hình `?gia_lap=rong`)* ⇒
    `ST.ung_vien = []` ⇒ **0** chú giải. ⛔ Chiều ĐỎ: vẽ chú giải vô điều kiện
    ⇒ `1` ⇒ ĐỎ."""
    ca, tra = ca_tra
    rong = {k: v for k, v in tra.items() if "/queue/lenh/" not in k}
    r = _chay(_nap(rong) + _MAY_DE_XUAT % {"ma": json.dumps(ca["lenh"]["A"])},
              tep=TEP_F01, vo=VO_F01)
    assert r["uv"] == 0, r
    assert r["n"] == 0, r


def test_AC13_CSS_tlegend_chi_dung_token_co_san():
    """Một lớp `.tlegend` *(ngoại lệ có tên của `TL-033 ⓑ`)*: mọi `var(--…)`
    trong khối ấy **đã khai** ở `tokens.css`; ⛔ mã màu / cỡ `px` gõ tay.
    ⛔ Chiều ĐỎ: `font-size:10.5px` gõ tay *(như bản dựng)* ⇒ ĐỎ."""
    css = open(os.path.join(pv.THU_MUC, "hinh.css"), encoding="utf-8").read()
    tok = open(os.path.join(pv.THU_MUC, "tokens.css"), encoding="utf-8").read()
    khoi = re.findall(r"\.tlegend[^{]*\{([^}]*)\}", css)
    assert khoi, "⛔ không đo được: `hinh.css` ⛔ có khối `.tlegend`"
    for k in khoi:
        assert not re.search(r"#[0-9a-fA-F]{3,8}\b|\d+(\.\d+)?px", k), k
        for v in re.findall(r"var\((--[\w-]+)\)", k):
            assert re.search(re.escape(v) + r"\s*:", tok), f"token {v} ⛔ khai"


# ══ (k) · F04 `_ve_thu_tu` rỗng ═══════════════════════════════════════════
@can_node
def test_AC14_F04_ve_thu_tu_than_NULL_cau_rong_KHONG_TypeError():
    """`_ve_thu_tu` đi **đường thật** `TT.chay` với cửa `/chup/<cid>/thu-tu` trả
    `data: null` *(khung trả `null` cho đường ⛔ có thân — hình `?gia_lap=rong`)*
    ⇒ `#nap-thu-tu` câu rỗng *"Chưa đo được nguồn nào"*, **0** ngoại lệ.

    ⛔ Chiều ĐỎ *(mã `363a441`)*: `la_rong: d => !d.nguon` ⇒ `TypeError` ⇒ ĐỎ."""
    r = _chay("""
      let loi = null;
      try { await F04._ve_thu_tu(7); } catch (e) { loi = String(e); }
      return {loi: loi, chu: document.getElementById('nap-thu-tu').textContent,
              goi: _GOI.map(g => g[1])};
    """, tep=TEP_F04, vo=VO_F04)
    assert "/chup/7/thu-tu" in r["goi"], r
    assert r["loi"] is None, r
    assert "Chưa đo được nguồn nào" in r["chu"], r
