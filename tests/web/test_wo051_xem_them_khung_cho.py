# -*- coding: utf-8 -*-
"""`WO-051` `(c)` · `BA-06` v4.22 `§4.5 ⓦ` ⑦ — `F01` `Xem thêm` có **khung
chờ** và lỗi **⛔ xoá lưới** *(`AC-6` · `AC-7`)*.

⛔⛔ Lỗi gốc *(`KQ-050 F-1` · `fls-ba` đọc `man_f01.js:214-232` @ `c903eb3`)*:
  ⓐ bấm `Xem thêm` ⇒ nút **khoá** mà **⛔ một chữ** — trang 2 `VND` sổ thật
     **104,33 s** ⇒ một nút xám gần hai phút;
  ⓑ lượt lỗi ⇒ `TT.loi(o, …)` thay **cả** khung ⇒ **50** hàng người đang đọc
     biến mất; nút `Thử lại` của nó tải lại **từ trang đầu**.

⭐ Luật của tệp *(như `test_wo045_luot_moi_nhat_cua_that.py`)*:
  · thân cửa lấy từ **cửa HTTP thật** trên **kho TEST** — một lần nạp riêng
    **120** dòng `VND` *(⇒ **ba** trang `limit=50`: để thấy nút **về** `Xem
    thêm` sau lượt hai, ⛔ chỉ chip `hết danh sách`)*; cửa hỏi kèm
    `?run_id=<lần nạp>` rồi thân đặt dưới **đúng** đường màn gọi *(màn ⛔ gửi
    `run_id` — khuôn `_pham_vi_ca` của `WO-023` `(j)`)*;
  · cửa giả **giữ** lượt có `cursor=` tới khi kịch bản thả / ném — thứ tự do
    **bài** quyết;
  · bấm đi đúng đường người bấm *(`_bam`: nút `disabled` ⛔ nhận cú bấm)*.

⭐ Mỗi bài ghi **chiều ĐỎ** đã chạy trên mã khi nhận *(`9af99c4`)* — `BG-064`.
"""
from __future__ import annotations

import random
import uuid

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.ca_wo032 import goi_ok
from tests.web.ca_wo037 import _tien
from tests.web.khung_giu import CUA_GIU, ma_uri, nap
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = [pytest.mark.pg, can_node]

#: số dòng `VND` của ca — **> 100** ⇒ ba trang `limit=50`
SO_VND = 120
CHU_TAI = "Đang tải thêm…"


@pytest.fixture(scope="module")
def ca():
    """`(D, TRA)` — `D` tên ⇒ đường màn gọi; `TRA` đường ⇒ phong bì cửa thật."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        h = uuid.uuid4().hex[:8].upper()
        run = "NAP-2000-01-01-W51F" + h[:6]
        c.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                  " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        nguon = "R | 123456789_VPB VND_W51" + h
        for j in range(SO_VND):
            _tien(c, run, nguon, 10 + j,
                  f"{random.randint(1_000, 8_999) * 1000 + j}.00", "VND",
                  f"FT51{j:03d}{h}")
    rid = "run_id=" + run
    D = {"tom": "/queue/summary", "lo": "/queue/tu-chung",
         "p1": "/queue?curr=VND&limit=50"}
    TRA = {}
    with _may() as m:
        for k in ("tom", "lo", "p1"):
            TRA[D[k]] = goi_ok(m, D[k] + ("&" if "?" in D[k] else "?") + rid)
        for k, truoc in (("p2", "p1"), ("p3", "p2")):
            nx = TRA[D[truoc]]["data"]["next_cursor"]
            assert nx, f"⛔ không đo được: {truoc} ⛔ có trang kế"
            D[k] = "/queue?curr=VND&cursor=" + ma_uri(nx) + "&limit=50"
            TRA[D[k]] = goi_ok(m, D[k] + "&" + rid)
    n = [len(TRA[D[k]]["data"]["rows"]) for k in ("p1", "p2", "p3")]
    assert n == [50, 50, SO_VND - 100], ("⛔ không đo được: ca ⛔ ba trang", n)
    assert TRA[D["p2"]]["data"]["next_cursor"] and \
        not TRA[D["p3"]]["data"]["next_cursor"], "⛔ con trỏ trang cuối"
    return D, TRA


def _itl(env: dict) -> list:
    return [x["itl_id"] for x in env["data"]["rows"]]


def _js(tra: dict, kich_ban: str) -> dict:
    return _chay(CUA_GIU + nap(tra) + kich_ban, tep=TEP_F01, vo=VO_F01)


_DUNG = """
  const o = document.querySelector('#than-f01');
  F01.ST.curr = 'VND'; F01.ST.den_pct = '';
  F01.ve(o); await _cho();
  const hang = () => o.querySelectorAll('tbody tr').length;
  const nut_chan = () => o.querySelectorAll('button')
    .filter(b => b.className === 'b tiny'
            && ['Xem thêm', 'Đang tải thêm…', 'Thử lại'].includes(b.textContent))
    .map(b => [b.textContent, !!b.disabled]);
  const loi = () => o.querySelectorAll('.banner')
    .map(x => [x.className, x.textContent]);
  _GIU.push('cursor=');
"""


def test_AC6_XEM_THEM_dang_tai_nut_KHOA_chu_DANG_TAI_THEM_hang_GIU(ca):
    """Cửa giả **treo** lượt `cursor`: bấm ⇒ nút `disabled` **và** chữ `Đang
    tải thêm…`; lưới **giữ** 50 hàng; bấm thêm ⇒ **0** `GET` thêm. Thả ⇒ 100
    hàng, nút **về** `Xem thêm` *(còn trang 3)*.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: chữ ⛔ đổi ⇒ `chu` = `Xem thêm`."""
    D, TRA = ca
    r = _js(TRA, _DUNG + """
      const b = _nut(o, 'Xem thêm')[0];
      const bam1 = _bam(b); await _cho();
      const r = {bam1, chu: b.textContent, khoa: b.disabled, hang_cho: hang(),
                 nut_cho: nut_chan()};
      r.bam2 = _bam(b); r.bam3 = _bam(_nut(o, 'Xem thêm')[0]); await _cho();
      r.cursor_cho = _doc('cursor=');
      await _tha('cursor=');
      r.hang_sau = hang(); r.nut_sau = nut_chan(); r.loi = loi();
      r.itl = F01.ST.dong.map(x => x.itl_id); r.tro = F01.ST.con_tro;
      return r;""")
    assert r["bam1"], "⛔ không đo được: nút Xem thêm ⛔ bấm được"
    assert r["chu"] == CHU_TAI and r["khoa"] is True, (r["chu"], r["khoa"])
    assert r["hang_cho"] == 50, f"⛔ lưới ⛔ giữ hàng khi chờ: {r['hang_cho']}"
    assert r["nut_cho"] == [[CHU_TAI, True]], r["nut_cho"]
    assert not r["bam2"] and not r["bam3"], "⛔ bấm được khi đang tải"
    assert r["cursor_cho"] == [D["p2"]], f"⛔ mở lượt thứ hai: {r['cursor_cho']}"
    mong = _itl(TRA[D["p1"]]) + _itl(TRA[D["p2"]])
    assert r["itl"] == mong and r["hang_sau"] == 100, (len(r["itl"]), r["hang_sau"])
    assert r["nut_sau"] == [["Xem thêm", False]], r["nut_sau"]
    assert r["tro"] == TRA[D["p2"]]["data"]["next_cursor"]
    assert r["loi"] == [], r["loi"]


@pytest.mark.parametrize("ma,cau", [
    ("FLS-INTERNAL", "Máy gặp lỗi bên trong."),
    ("FLS-MAT-KET-NOI", "Không nối được tới máy chủ FLS."),
])
def test_AC7_XEM_THEM_loi_hang_GIU_cau_loi_va_THU_LAI_dung_con_tro(ca, ma, cau):
    """Lượt `cursor` lỗi ⇒ lưới **còn 50** hàng; dưới lưới **một** dòng
    `⛔ Cửa lỗi: <e.cau>` *(lớp `banner crit` — khuôn `ⓦ` ④)* ＋ **một** nút
    `Thử lại` lớp `b tiny`; bấm *(hai lần)* ⇒ **một** `GET` mang **đúng**
    `cursor` vừa lỗi; xanh ⇒ 100 hàng, câu lỗi mất, nút về `Xem thêm`.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: `TT.loi` thay cả khung ⇒ **0** hàng; nút
    `Thử lại` của nó lật **từ đầu** *(`GET` ⛔ `cursor`)*."""
    D, TRA = ca
    r = _js(TRA, _DUNG + f"""
      _bam(_nut(o, 'Xem thêm')[0]); await _cho();
      await _no('cursor=', new FLS.LoiCua({ma!r}, 0, 'x'));
      const r = {{hang_loi: hang(), loi: loi(), nut_loi: nut_chan(),
                  thu: _nut(o, 'Thử lại').map(b => b.className)}};
      const t = _nut(o, 'Thử lại')[0];
      const truoc = _doc('/queue?').length;
      r.bam1 = _bam(t); await _cho(); r.bam2 = _bam(t); await _cho();
      r.luot = _doc('/queue?').slice(truoc);
      r.loi_khi_tai = loi(); r.nut_khi_tai = nut_chan(); r.hang_khi_tai = hang();
      /* ⚠ ⛔ lượt `cursor=` nào đang chờ ⇒ `Thử lại` ⛔ lật đúng con trỏ —
         trả ngay để bài **assert** nói điều ấy *(⛔ để `_tha` ném "⛔ không đo
         được")* */
      if (!_tim('cursor=')) return r;
      await _tha('cursor=');
      r.hang_sau = hang(); r.loi_sau = loi(); r.nut_sau = nut_chan();
      r.itl = F01.ST.dong.map(x => x.itl_id);
      return r;""")
    assert r["hang_loi"] == 50, f"⛔ lỗi xoá lưới: còn {r['hang_loi']} hàng"
    assert r["loi"] == [["banner crit", "⛔ Cửa lỗi: " + cau]], r["loi"]
    assert r["thu"] == ["b tiny"], f"⛔ nút Thử lại: {r['thu']}"
    assert r["nut_loi"] == [["Thử lại", False]], r["nut_loi"]
    assert r["bam1"] and not r["bam2"], (r["bam1"], r["bam2"])
    assert r["luot"] == [D["p2"]], f"⛔ Thử lại ⛔ đúng con trỏ / >1 lượt: {r['luot']}"
    assert r["hang_khi_tai"] == 50 and r["loi_khi_tai"] == [], r
    assert r["nut_khi_tai"] == [[CHU_TAI, True]], r["nut_khi_tai"]
    mong = _itl(TRA[D["p1"]]) + _itl(TRA[D["p2"]])
    assert r["itl"] == mong and r["hang_sau"] == 100, (len(r["itl"]), r["hang_sau"])
    assert r["loi_sau"] == [] and r["nut_sau"] == [["Xem thêm", False]], r


def test_AC7_THU_LAI_lai_loi_MOT_dong_loi_khong_chong(ca):
    """Bấm `Thử lại`, lượt **lại** lỗi ⇒ vẫn **một** dòng lỗi + **một** nút
    `Thử lại`, lưới vẫn 50 *(⛔ hai câu lỗi chồng nhau)*; lượt thứ ba xanh ⇒
    lật tiếp tới hết *(trang 3 ⇒ chip `hết danh sách`, ⛔ nút)*."""
    D, TRA = ca
    r = _js(TRA, _DUNG + """
      _bam(_nut(o, 'Xem thêm')[0]); await _cho();
      await _no('cursor=', new FLS.LoiCua('FLS-INTERNAL', 0, 'x'));
      const r = {hang1: hang()};
      _bam(_nut(o, 'Thử lại')[0]); await _cho();
      if (!_tim('cursor=')) return r;
      await _no('cursor=', new FLS.LoiCua('FLS-INTERNAL', 0, 'x'));
      Object.assign(r, {loi2: loi(), nut2: nut_chan(), hang2: hang()});
      _bam(_nut(o, 'Thử lại')[0]); await _cho(); await _tha('cursor=');
      _bam(_nut(o, 'Xem thêm')[0]); await _cho(); await _tha('cursor=');
      r.hang = hang(); r.nut = nut_chan(); r.loi = loi();
      r.het = o.textContent.indexOf('hết danh sách') >= 0;
      r.cursor = _doc('cursor=');
      return r;""")
    assert r["hang1"] == 50, f"⛔ lỗi xoá lưới: còn {r['hang1']} hàng"
    assert "loi2" in r, "⛔ Thử lại ⛔ mở lượt cursor= (lật từ đầu?)"
    assert len(r["loi2"]) == 1 and r["nut2"] == [["Thử lại", False]], r
    assert r["hang2"] == 50, r["hang2"]
    assert r["hang"] == SO_VND and r["nut"] == [] and r["het"], r
    assert r["cursor"] == [D["p2"], D["p2"], D["p2"], D["p3"]], r["cursor"]


def test_AC7_doi_tien_te_khi_XEM_THEM_dang_tai_loi_cu_KHONG_hien(ca):
    """Luật lượt `WO-045` ⛔ đổi: lượt `Xem thêm` **cũ** lỗi về **sau** khi lưới
    đã dựng lại *(`ve()` — đổi lọc)* ⇒ ⛔ câu lỗi, ⛔ nút `Thử lại` trên lưới
    mới."""
    D, TRA = ca
    r = _js(TRA, _DUNG + """
      _bam(_nut(o, 'Xem thêm')[0]); await _cho();
      F01.ve(o); await _cho();
      await _no('cursor=', new FLS.LoiCua('FLS-INTERNAL', 0, 'x'));
      return {loi: loi(), nut: nut_chan(), hang: hang()};""")
    assert r["loi"] == [] and r["nut"] == [["Xem thêm", False]], r
    assert r["hang"] == 50, r["hang"]
