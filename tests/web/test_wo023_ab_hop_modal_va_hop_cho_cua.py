# -*- coding: utf-8 -*-
"""`WO-023` `(a)` + `(b)` · `BA-06` **v4.11** `ⓕ1` · `ⓕ2` — hộp đang mở là
**MODAL** với bàn phím; hộp đang **chờ cửa** ⛔ đóng giữa chừng *(`KQ-021`
`F-1` · `F-2`)*.

⛔⛔ Lỗi gốc *(mã khi nhận `7e67a09`)*:
  ⓐ `F-1` — trình nghe phím của màn *(`man_f01_ghep.js::_noi_ban_phim` ·
     `man_f02.js::_noi_ban_phim`)* ⛔ hỏi hộp đang mở ⇒ `Esc` đóng hộp **và**
     lệnh; `j` đổi lệnh **sau lưng** hộp; `Ctrl+Z` hoàn tác ô lưới sau lưng hộp.
  ⓑ `F-2` — luật ⓒ của `hop_thoai.js` cho `Esc` / bấm ra ngoài đóng hộp **cả
     khi** hàng nút đang khoá chờ cửa ⇒ cửa lỗi ⇒ câu lỗi viết vào hộp **đã
     đóng**, màn im.

⭐ Bài nạp `hop_thoai.js` **THẬT** và **⛔ chép** trình nghe nào của nó *(khác
`KQ-021` — bài ấy chép trình nghe `Esc` vì mã khi nhận chỉ gắn nó khi `HT`
**tự dựng** `#scrim`)*: mã mới gắn trình nghe ở lần `HT.mo` **đầu tiên** dù
`#scrim` có sẵn hay ⛔. Mỗi bài phím chạy **hai** thứ tự đăng ký:
  `man_truoc` — màn nối bàn phím **trước**, hộp mở lần đầu **sau** *(như
               trình duyệt: mở màn rồi mới bấm hộp)*;
  `hop_truoc` — một hộp mở + đóng **trước** khi màn nối bàn phím.
DOM giả ⛔ có pha `capture` *(`dom_gia.js::ban` gọi trình nghe theo thứ tự
đăng ký)* ⇒ hai thứ tự ở đây **là** hai thứ tự thật mà phép chặn phải chịu.
"""
from __future__ import annotations

import json

import pytest

from fls.repo import man_ghep as mg
from tests.web.khung_node import TEP as TEP_F02, VO_F02, _VE_GO, _chay, can_node

pytestmark = [can_node]

TEP_F01 = ["thanh_phan.js", "goi_cua.js", "trang_thai.js", "hop_thoai.js",
           "man_f01_lenh.js", "man_f01.js", "man_f01_ghep.js"]

#: Vỏ: `#scrim` dựng sẵn ba ô *(DOM giả ⛔ phân tích `innerHTML` — `HT._khung`
#: thấy `#scrim` thì dùng luôn)* ＋ `#man-ghep.on` *(trình nghe phím `F01G` tự
#: chặn khi màn ghép ⛔ bật)*.
_SCRIM = """
const scrim = d.document.createElement('div'); scrim.id = 'scrim';
for (const id of ['dlg-t', 'dlg-b', 'dlg-f']) {
  const e = d.document.createElement('div'); e.id = id; scrim.appendChild(e);
}
d.body.appendChild(scrim);
"""
VO_F01 = """
const man = d.document.createElement('section'); man.id = 'man-f01';
man.className = 'screen';
const tf = d.document.createElement('div'); tf.id = 'than-f01';
man.appendChild(tf); d.body.appendChild(man);
const man2 = d.document.createElement('section'); man2.id = 'man-ghep';
man2.className = 'screen on';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
man2.appendChild(goc); d.body.appendChild(man2);
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
d.body.appendChild(tim);
""" + _SCRIM
VO_F02S = VO_F02 + _SCRIM

THU_TU = ["man_truoc", "hop_truoc"]

#: Mở + đóng một hộp ⇒ `hop_thoai.js` gắn trình nghe **trước** màn.
_HOP_TRUOC = "HT.mo('khởi', '', [['OK', null]]); HT.dong();\n"

CONG_CU = """
  globalThis._ngu = ms => new Promise(r => setTimeout(r, ms));
  globalThis._dem = re => _GOI.filter(g => re.test(g[1])).length;
  globalThis._hop = function () {
    const s = document.getElementById('scrim');
    return {mo: s.classList.contains('on'),
            b: document.getElementById('dlg-b').textContent,
            nut: document.getElementById('dlg-f').children.map(x => [x.textContent, !!x.disabled])};
  };
  globalThis._bam_man = function (chu) {
    const ra = [];
    (function di(e) {
      if (e.tagName === 'BUTTON' && e.textContent.trim() === chu) ra.push(e);
      e.children.forEach(di);
    })(document.getElementById('ghep-goc'));
    if (ra.length !== 1) throw new Error('⛔ không đo được: ' + ra.length + ' nút ' + chu);
    (ra[0]._nghe.click || []).forEach(f => f());
  };
  globalThis._bam_hop = chu => document.getElementById('dlg-f').children
    .filter(b => b.textContent === chu)[0].onclick();
  globalThis._phim = (k, tuy) => _ban('keydown', Object.assign({key: k,
    preventDefault() {}, stopPropagation() {}}, tuy || {}));
"""


def _lenh(ma: str, itl: list[int]) -> dict:
    k = mg.khuon_the_lenh({"pm_line_id": ma, "itl_da_gan": itl})
    gd = [{"itl_id": i, "bac": "tien", "doc_no": "FT-%d" % i, "amount": "5000000.00",
           "curr": "VND", "doc_date": "2026-09-01", "dien_giai": "GD-%d" % i,
           "da_gan": True} for i in itl]
    return {"ma_lenh": ma, "noi_dung": "chi " + ma, "so_tien": "5000000.00",
            "curr": "VND", "loai_phieu": "PM", "itl_da_gan": list(itl),
            "nhom_du_truong": [], "gd_ds": gd, "gd": gd[0] if gd else None,
            "trang_thai": k["trang_thai"], "trang_thai_nhan": k["trang_thai_nhan"],
            "trang_thai_mau": k["trang_thai_mau"]}


CHUM2 = {"itl_id": 4242, "can_hoi": True, "so_dong": 2, "dong_lenh": [
    {"pm_line_id": "PWB-1", "amount": "3000000.00", "curr": "VND"},
    {"pm_line_id": "PWB-2", "amount": "2000000.00", "curr": "VND"}]}
DONG3 = [_lenh("PWB-1", [4242]), _lenh("PWB-2", [4242]), _lenh("PWB-3", [5000])]


def _ghep(thu_tu: str, kich_ban: str, *, dong=DONG3, tra=None) -> dict:
    tra = dict(tra or {"/queue/4242/chum": CHUM2})
    t = ["_TRA[%s] = %s;" % (json.dumps(k), json.dumps(
        v if isinstance(v, dict) and "no" in v else {"data": v}, ensure_ascii=False))
         for k, v in tra.items()]
    for d in dong:
        t.append("_TRA[%s] = {data: {ung_vien: [{itl_id: 7, bac: 'tien', "
                 "amount: '1.00', curr: 'VND'}]}};"
                 % json.dumps("/queue/lenh/%s/itl-candidates" % d["ma_lenh"]))
    dau = _HOP_TRUOC if thu_tu == "hop_truoc" else ""
    return _chay(CONG_CU + "\n".join(t) + dau + """
      await F01G.mo_man();
      F01G.ST.dong = %s;
      await F01G.mo_lenh('PWB-1');
    """ % json.dumps(dong, ensure_ascii=False) + kich_ban, tep=TEP_F01, vo=VO_F01)


# ══ (a) `ⓕ1` — hộp MODAL với bàn phím ════════════════════════════════════

@pytest.mark.parametrize("thu_tu", THU_TU)
def test_AC1_ESC_tren_hop__CHI_dong_hop__lenh_van_mo(thu_tu):
    """Hộp ② *(`Bỏ gán sẽ gỡ CẢ 2 lệnh chi`)* mở; `Esc` ⇒ hộp đóng, `ST.mo`
    **giữ** `PWB-1`, **0** `/unmatch`. ⛔ Chiều ĐỎ *(mã khi nhận)*: `man_truoc`
    ⇒ `ST.mo` `null` *(Esc bóc hai lớp)*; `hop_truoc` ⇒ hộp **⛔** đóng *(trình
    nghe của hộp ⛔ gắn khi `#scrim` có sẵn)*."""
    r = _ghep(thu_tu, """
      _bam_man('Bỏ gán'); await _ngu(30);
      const h1 = _hop();
      _phim('Escape'); await _ngu(30);
      return {h1, h2: _hop(), mo: F01G.ST.mo, unmatch: _dem(/\\/unmatch$/)};
    """)
    assert r["h1"]["mo"], "⛔ không đo được: hộp ⛔ mở"
    assert r["h2"]["mo"] is False, "⛔ Esc ⛔ đóng hộp"
    assert r["mo"] == "PWB-1", f"⛔ Esc bóc HAI lớp: ST.mo = {r['mo']!r}"
    assert r["unmatch"] == 0


@pytest.mark.parametrize("thu_tu", THU_TU)
@pytest.mark.parametrize("phim", ["j", "k", "ArrowDown", "ArrowUp", "Enter", "ArrowLeft", "/"])
def test_AC1_phim_man_khi_hop_MO__nam_im(thu_tu, phim):
    """Hộp ② mở; phím của màn ⇒ `ST.mo` **giữ**, hộp **vẫn** mở, **0** ghi.
    ⛔ Chiều ĐỎ *(mã khi nhận)*: `j`/`↓` ⇒ `PWB-2` sau lưng hộp; `ArrowLeft` ⇒
    `null`."""
    r = _ghep(thu_tu, """
      _bam_man('Bỏ gán'); await _ngu(30);
      const h1 = _hop();
      _phim(%s); await _ngu(30);
      return {h1, h2: _hop(), mo: F01G.ST.mo, ghi: _GOI.filter(g => g[0] === 'ghi').length};
    """ % json.dumps(phim))
    assert r["h1"]["mo"], "⛔ không đo được: hộp ⛔ mở"
    assert r["mo"] == "PWB-1", f"⛔ phím {phim!r} đổi màn sau lưng hộp: {r['mo']!r}"
    assert r["h2"]["mo"] is True, f"⛔ phím {phim!r} đóng hộp"
    assert r["ghi"] == 0


@pytest.mark.parametrize("thu_tu", THU_TU)
def test_AC1_MAU_SO_hop_DA_dong__phim_man_van_song(thu_tu):
    """⭐ Mẫu số *(`Đ3`)*: chặn **cả khi ⛔ có hộp** ⇒ bài này ĐỎ. Hộp mở rồi
    `Thôi` ⇒ `j` đổi lệnh, `Esc` đóng lệnh."""
    r = _ghep(thu_tu, """
      _bam_man('Bỏ gán'); await _ngu(30);
      await _bam_hop('Thôi'); await _ngu(10);
      const h = _hop();
      _phim('j'); await _ngu(30);
      const sau_j = F01G.ST.mo;
      _phim('Escape'); await _ngu(10);
      return {h, sau_j, sau_esc: F01G.ST.mo};
    """)
    assert r["h"]["mo"] is False, r
    assert r["sau_j"] == "PWB-2", r
    assert r["sau_esc"] is None, r


# ── F02 — `Ctrl+Z` sau lưng hộp ─────────────────────────────────────────

def _f02(thu_tu: str, mo_hop: bool) -> dict:
    dau = _HOP_TRUOC if thu_tu == "hop_truoc" else ""
    hop = ("HT.mo('Hộp thử', '<div class=\"note\">x</div>', [['Đóng', null]]);"
           if mo_hop else "")
    return _chay(CONG_CU + dau + _VE_GO + """
      const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
      const i = h.findIndex(c => c.textContent.startsWith('Chủ dự toán'));
      const o = than.rows[0].cells[i];
      F02.ST.o = o;
      _ban('paste', {clipboardData:{getData:()=> 'CDT-X'},
                     preventDefault(){}, stopPropagation(){}});
      const truoc = {chu: o.textContent, lich: F02.ST.lich.length};
      %s
      _phim('z', {ctrlKey: true});
      return {truoc, sau: {chu: o.textContent, lich: F02.ST.lich.length},
              hop: _hop().mo};
    """ % hop, tep=TEP_F02, vo=VO_F02S)


@pytest.mark.parametrize("thu_tu", THU_TU)
def test_AC1_F02_CTRL_Z_khi_hop_MO__ST_lich_khong_doi(thu_tu):
    """⛔ Chiều ĐỎ *(mã khi nhận)*: `Ctrl+Z` hoàn tác ô `CDT-X` sau lưng hộp."""
    r = _f02(thu_tu, True)
    assert r["truoc"] == {"chu": "CDT-X", "lich": 1}, ("⛔ không đo được", r)
    assert r["hop"] is True, r
    assert r["sau"] == r["truoc"], f"⛔ Ctrl+Z chạy sau lưng hộp: {r}"


@pytest.mark.parametrize("thu_tu", THU_TU)
def test_AC1_F02_MAU_SO_khong_hop__CTRL_Z_hoan_tac(thu_tu):
    r = _f02(thu_tu, False)
    assert r["truoc"] == {"chu": "CDT-X", "lich": 1}, r
    assert r["sau"]["lich"] == 0 and r["sau"]["chu"] == "chưa gán", r


# ══ (b) `ⓕ2` — hộp đang chờ cửa ⛔ đóng ═══════════════════════════════════

_TREO = """
  let tha_loi, tha_ok;
  const ghi0 = FLS.ghi;
  FLS.ghi = function (duong, than) {
    if (/unmatch$/.test(duong)) {
      _GOI.push(['ghi', duong, than]);
      return new Promise((ok, no) => {
        tha_loi = () => no(new FLS.LoiCua('FLS-MAT-KET-NOI', 0, 'Failed to fetch'));
        tha_ok = () => ok({data: {itl_id: 4242, da_bo: [], but_toan_dao: [], bo_qua: []}, meta: {}});
      });
    }
    return ghi0(duong, than);
  };
"""

CAU_CHO = "Đang ghi vào sổ — chờ máy trả lời."


@pytest.mark.parametrize("thu_tu", THU_TU)
def test_AC2_GO_CA_N_dang_cho__ESC_va_bam_nen_bi_nuot__loi_hien_TRONG_hop(thu_tu):
    """Bấm `Gỡ cả 2`, cửa **treo**: `Esc` ⇒ `#scrim.on` **vẫn**; bấm nền ⇒
    **vẫn**; `#dlg-b` chứa dòng chờ; cửa lỗi ⇒ lỗi trong hộp **đang mở**, nút
    mở lại, dòng chờ **mất**. ⛔ Chiều ĐỎ *(mã khi nhận)*: `Esc` đóng hộp
    *(`man_truoc` — trình nghe hộp ⛔ gắn: thì `hop_truoc` cũng ⛔ có dòng chờ)*."""
    r = _ghep(thu_tu, _TREO + """
      _bam_man('Bỏ gán'); await _ngu(30);
      const p = _bam_hop('Gỡ cả 2'); await _ngu(20);
      const cho = _hop();
      _phim('Escape'); await _ngu(10);
      const sau_esc = _hop().mo;
      const s = document.getElementById('scrim');
      (s._nghe.click || []).forEach(f => f({target: s}));
      const sau_nen = _hop().mo;
      tha_loi(); await p; await _ngu(30);
      return {cho, sau_esc, sau_nen, xong: _hop(), mo: F01G.ST.mo,
              unmatch: _dem(/\\/unmatch$/)};
    """)
    assert r["unmatch"] == 1, ("⛔ không đo được: ⛔ gọi cửa", r)
    assert r["cho"]["mo"] and CAU_CHO in r["cho"]["b"], ("⛔ ⛔ có dòng chờ", r["cho"])
    assert all(d for _, d in r["cho"]["nut"]), ("⛔ hàng nút ⛔ khoá khi chờ", r["cho"])
    assert r["sau_esc"] is True, "⛔ Esc đóng hộp đang chờ cửa"
    assert r["sau_nen"] is True, "⛔ bấm nền đóng hộp đang chờ cửa"
    assert r["xong"]["mo"] is True, r["xong"]
    assert "Không nối được tới máy chủ FLS." in r["xong"]["b"], r["xong"]
    assert CAU_CHO not in r["xong"]["b"], ("⛔ dòng chờ còn sau khi cửa đã trả", r["xong"])
    assert not any(d for _, d in r["xong"]["nut"]), ("⛔ nút ⛔ mở lại", r["xong"])
    assert r["mo"] == "PWB-1", r


@pytest.mark.parametrize("thu_tu", THU_TU)
def test_AC2_MAU_SO_hop_CHUA_bam_nut__ESC_dong(thu_tu):
    """⭐ Mẫu số: luật ⓒ **giữ** khi chưa có lượt ghi nào đang bay — nuốt `Esc`
    cả khi ⛔ chờ ⇒ ĐỎ. Và cửa trả `200` ⇒ hộp đóng như nay."""
    r = _ghep(thu_tu, _TREO + """
      _bam_man('Bỏ gán'); await _ngu(30);
      const h1 = _hop();
      _phim('Escape'); await _ngu(10);
      const sau_esc = _hop().mo;
      _bam_man('Bỏ gán'); await _ngu(30);
      const p = _bam_hop('Gỡ cả 2'); await _ngu(20);
      tha_ok(); await p; await _ngu(30);
      return {h1, sau_esc, sau_ok: _hop().mo};
    """)
    assert r["h1"]["mo"] is True and CAU_CHO not in r["h1"]["b"], r
    assert r["sau_esc"] is False, "⛔ Esc ⛔ đóng hộp CHƯA bấm nút"
    assert r["sau_ok"] is False, "⛔ cửa 200 mà hộp ⛔ đóng"


# ── `F01` ⑥ `_bo_ghep` — cùng khuôn ──────────────────────────────────────

def test_AC2_F01_bo_ghep_dang_cho__ESC_bi_nuot__loi_trong_hop():
    """`F01` ⑥ `Bỏ ghép · dòng N` *(hàm nút `async`)* — `ⓕ2` áp **mọi** hộp
    `HT.mo`. Gọi thẳng `HT.mo` với một hàm nút treo *(cùng khuôn ghi bên trong
    hàm nút của `_bo_ghep`)*: `Esc` ⇒ hộp **vẫn** mở + dòng chờ; lỗi ⇒ trong
    hộp. ⛔ Chiều ĐỎ *(mã khi nhận)*: hộp đóng."""
    r = _ghep("man_truoc", """
      let tha;
      HT.mo('Bỏ ghép · dòng 1', '<div class="note">x</div>',
        [['Thôi', null],
         ['Bỏ ghép', async function () {
            try { await new Promise((ok, no) => { tha = () => no(new FLS.LoiCua('FLS-INTERNAL', 500)); }); }
            catch (e) { HT.loi_trong_hop(e); return false; }
          }, {danger: true}]]);
      const p = _bam_hop('Bỏ ghép'); await _ngu(10);
      _phim('Escape'); await _ngu(10);
      const cho = _hop();
      tha(); await p; await _ngu(10);
      return {cho, xong: _hop()};
    """)
    assert r["cho"]["mo"] is True and CAU_CHO in r["cho"]["b"], r["cho"]
    assert r["xong"]["mo"] is True and "Máy gặp lỗi bên trong." in r["xong"]["b"], r["xong"]
