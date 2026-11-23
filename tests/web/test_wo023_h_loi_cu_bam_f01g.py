# -*- coding: utf-8 -*-
"""`WO-023` `(h)` · `BA-06` **v4.21**/**v4.22** `§4.5 ⓦ` ④ ⑤ — lỗi của một cú
bấm `F01G` nói với **người**, ⛔ rơi ra console *(`TL-049` · `KQ-050 F-2`)*.

⛔⛔ Lỗi gốc *(mã khi nhận `7e67a09`, đọc lại sau `(i)` @ `bc5e0bc`)*:
  ⓐ `gan` — `await FLS.ghi('/queue/<itl>/match', …)` ⛔ `try`; `nut()` gắn
     `click` thẳng ⇒ cửa ghi trả `422` ⇒ `Uncaught (in promise) LoiCua`, màn
     **⛔ một chữ**; nút `Gán` ⛔ khoá khi chờ ⇒ bấm hai lần là **hai** `POST`.
  ⓑ `mo_lenh` gọi từ phím `j`/`k`/`↓` · chuột hàng · ô tìm ⛔ `catch` ⇒ lỗi lượt
     mới nhất ⇒ `Uncaught` *(vùng ứng viên **đã** nói)*.
  ⓒ vùng ứng viên **lỗi** ⛔ có nút `Thử lại`.
  ⓔ lượt **ô tìm** mới nhất lỗi ⇒ `_tai_toan_so` chỉ `throw` ⇒ khung `Đang hỏi
     sổ…` **treo** *(`ST.dang_tai_uv` vẫn `true`)*, ⛔ câu lỗi.

⭐ Bẫy lỗi chưa bắt: kịch bản bật `globalThis._BAT_TU_CHOI = []` ⇒ khung
`khung_node.py` ghi mọi lời hứa bị từ chối ⛔ ai bắt *(trình duyệt in
`Uncaught (in promise)`)*; bài đếm, mong **0**. ⛔ Bật ⇒ `node` sập như cũ.

⭐ Thân lỗi `422` **từ cửa thật** kho TEST *(`POST /queue/<M4 USD>/match
{pm_line_ids:[L VND]}` ⇒ cửa ghi từ chối khác tiền tệ — ⛔ ghi)*; `fetch` giả
trả **nguyên văn** thân ấy cho **`goi_cua.js` thật** dựng `LoiCua` *(⛔ bài tự
dựng `LoiCua` cho ca `422`)*.
"""
from __future__ import annotations

import json

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.ca_wo023 import dung_ca_wo023
from tests.web.ca_wo032 import goi_ok
from tests.web.khung_giu import CUA_GIU, nap
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import V, _goi, _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01
from tests.web.test_wo023_i_chon_ung_vien_theo_itl import VO, _GO

pytestmark = [pytest.mark.pg, can_node]

#: ⭐ `fetch` giả cho cú **GHI**: `FLS.ghi` đi qua `FLS.goi` **thật** *(dựng URL,
#: đọc thân, dựng `LoiCua` đúng như trình duyệt)*. `_GHI_TRA` = `{status,
#: than}` nguyên văn cửa thật; `_GHI_TREO = true` ⇒ lượt ghi **treo** mãi.
_GHI = """
  globalThis._BAT_TU_CHOI = [];
  globalThis._GHI_TRA = null; globalThis._GHI_TREO = false;
  globalThis.fetch = function (url, tuy) {
    if (_GHI_TREO) return new Promise(() => {});
    const t = _GHI_TRA;
    return Promise.resolve({status: t.status, ok: t.status < 400,
                            json: async () => t.than});
  };
  FLS.ghi = function (duong, than) {
    _GOI.push(['ghi', duong, than]);
    return FLS.goi(duong, {phuong_thuc: 'POST', than: than});
  };
  const man = () => document.querySelector('#ghep-goc').textContent;
  const nut_gan = () => document.querySelectorAll('.act button')[0];
"""


@pytest.fixture(scope="module")
def ca_tra():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_wo023(c)
    L, doc, i = ca["lenh"], ca["doc"], ca["i"]
    D = {
        "g_nguoi": "/queue/lenh-cho?ro=nguoi&limit=500",
        "g_may": "/queue/lenh-cho?ro=may&tu_chung=0&limit=500",
        "uv": f"/queue/lenh/{L}/itl-candidates",
        "so_M4": f"/queue/lenh/{L}/so?q={doc['M4']}",
        "so_M2": f"/queue/lenh/{L}/so?q={doc['M2']}",
    }
    with _may() as m:
        TRA = {d: goi_ok(m, d) for d in D.values()}
        # ⭐ thân lỗi THẬT của cửa ghi — khác tiền tệ ⇒ từ chối, ⛔ ghi
        st, than = _goi(m, f"{V}/queue/{i['M4']}/match", pt="POST",
                        than={"pm_line_ids": [L]})
    assert st == 422 and than.get("error"), ("⛔ không đo được: cửa ghi ⛔ trả "
                                             "422 cho cặp khác tiền tệ", st, than)
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        n = c.execute("SELECT count(*) FROM fls_pm_link WHERE itl_id = %s",
                      (i["M4"],)).fetchone()[0]
    assert n == 0, "⛔ cú 422 đã ghi mối nối?"
    return ca, D, TRA, {"status": st, "than": than}


def _js(tra: dict, kb: str) -> dict:
    return _chay(CUA_GIU + nap(tra) + _GO + _GHI + kb, tep=TEP_F01, vo=VO)


_MO = """
  await F01G.mo_man(); await _cho();
  const co_L = F01G.ST.dong.some(d => d.ma_lenh === %(L)r);
  [...document.querySelectorAll('#ghep-goc .mrow')]
    .filter(r => r.textContent.indexOf(%(L)r) >= 0).forEach(r => _bam(r));
  await _cho();
"""


def _mo(ca):
    return _MO % {"L": ca["lenh"]}


# ══ ⓐ `gan` — dòng lỗi + khoá nút ═══════════════════════════════════════════

def test_AC10_GAN_cua_tra_422_THAT__dong_loi_trong_khoi_hanh_dong__0_Uncaught(ca_tra):
    """Mở `L` *(chuột — hàng lệnh)*, gõ `doc(M4)` ⇒ `[M4]` *(USD — ca lệch ⇒
    hai cú `Gán`)*; cửa ghi trả **thân thật** `422`.

    Mong *(`ⓦ` ⑤ ⓐ)*: `#ghep-goc` chứa `Gán chưa xảy ra — Cửa lỗi: <e.cau>`
    ＋ `e.lam_gi`; **0** lỗi chưa bắt; nút `Gán` mở lại *(cửa đã trả lời)*.
    ⛔ Chiều ĐỎ *(mã khi nhận)*: `_BAT_TU_CHOI` = `['FLS-DQ-FAILED']`, màn ⛔ chữ."""
    ca, D, TRA, LOI = ca_tra
    ma = LOI["than"]["error"]["code"]
    r = _js(TRA, _mo(ca) + f"""
      _GHI_TRA = {json.dumps(LOI, ensure_ascii=False)};
      await go({ca['doc']['M4']!r});
      _bam(document.querySelectorAll('.cands .cand')[0]); await _cho();
      for (let k = 0; k < 2 && !_ghi().length; k++) {{ _bam(nut_gan()); await _cho(); }}
      await new Promise(r => setTimeout(r, 30)); await _cho();
      const c = FLS.CAU[{ma!r}];
      return {{co_L, ghi: _ghi().length, man: man(), cau: c.cau, lam_gi: c.lam_gi,
               bat: _BAT_TU_CHOI, khoa: !!nut_gan().disabled}};
    """)
    assert r["co_L"], r
    assert r["ghi"] == 1, ("⛔ không đo được: cú Gán ⛔ gửi", r)
    # ⭐ mong
    assert r["bat"] == [], f"⛔ lỗi chưa bắt (Uncaught in promise): {r['bat']}"
    assert "Gán chưa xảy ra — Cửa lỗi: " + r["cau"] in r["man"], r["man"][-400:]
    assert r["lam_gi"] and r["lam_gi"] in r["man"], r["man"][-400:]
    assert r["khoa"] is False, "⛔ nút Gán vẫn khoá sau khi cửa đã trả lời"


def test_AC10_GAN_khi_cua_TREO__nut_khoa__bam_them_0_POST(ca_tra):
    """`[M2]` *(đúng tiền — một cú là ghi)*; cửa ghi **treo**. Bấm `Gán` rồi
    bấm thêm hai lần + `Enter`.

    Mong: đúng **một** `POST`; nút `Gán` `disabled` trong lúc chờ. ⛔ Chiều ĐỎ
    *(mã khi nhận)*: mỗi cú bấm một `POST` *(3)*."""
    ca, D, TRA, LOI = ca_tra
    r = _js(TRA, _mo(ca) + f"""
      _GHI_TREO = true;
      await go({ca['doc']['M2']!r});
      _bam(document.querySelectorAll('.cands .cand')[0]); await _cho();
      _bam(nut_gan()); await _cho();
      const khoa = !!nut_gan().disabled;
      _bam(nut_gan()); await _cho();
      _bam(nut_gan()); await _cho();
      _ban('keydown', {{key: 'Enter', preventDefault() {{}}}}); await _cho();
      return {{co_L, ghi: _ghi(), khoa, bat: _BAT_TU_CHOI}};
    """)
    assert r["co_L"], r
    assert len(r["ghi"]) >= 1, ("⛔ không đo được: cú Gán đầu ⛔ gửi", r)
    # ⭐ mong
    assert len(r["ghi"]) == 1, f"⛔ bấm khi cửa đang chờ ⇒ {len(r['ghi'])} POST"
    assert r["khoa"] is True, "⛔ nút Gán ⛔ khoá khi cửa ghi đang chờ"


# ══ ⓑ `mo_lenh` từ phím / chuột / ô tìm ⛔ `Uncaught` ════════════════════════

def test_AC11_phim_J_mo_lenh_KE_cua_LOI__vung_ung_vien_noi__0_Uncaught(ca_tra):
    """Mở `L` *(chuột — `ST.tro` = hàng `L`)*; `itl-candidates` lệnh **kế**
    *(giữ)*; phím `j` qua trình nghe `document` **thật**; cửa lỗi
    `FLS-INTERNAL`.

    Mong *(`ⓦ` ⑤ ⓑ)*: `ST.mo` = lệnh kế, vùng ứng viên `⛔ Cửa lỗi: Máy gặp lỗi
    bên trong.`, **0** lỗi chưa bắt. ⛔ Chiều ĐỎ *(mã khi nhận)*: `_BAT_TU_CHOI`
    = `['FLS-INTERNAL']`. ⭐ Mẫu số *"`mo_lenh` vẫn ném cho `bo_gan`"*:
    `test_wo008_v2_nam_ca_bo_gan.py::test_AC12_…` *(xanh — chạy cùng bộ)*."""
    ca, D, TRA, LOI = ca_tra
    r = _js(TRA, _mo(ca) + """
      const L = F01G.ST.mo;
      /* `L` là lệnh mới nhất ⇒ có thể đứng **cuối** danh sách ⇒ ⛔ có lệnh
         kế cho `j`; khi ấy dùng `k` *(cùng nhánh `doi_lenh`)*. */
      const xuong = !!F01G.ST.dong[F01G.ST.tro + 1];
      const ke = F01G.ST.dong[F01G.ST.tro + (xuong ? 1 : -1)];
      if (!ke) return {loi: 'không có lệnh kề'};
      _GIU.push('/lenh/' + ke.ma_lenh + '/itl-candidates');
      _ban('keydown', {key: xuong ? 'j' : 'k', preventDefault() {}}); await _cho();
      await _no('/lenh/' + ke.ma_lenh + '/itl-candidates',
                new FLS.LoiCua('FLS-INTERNAL', 500, 'wo023'));
      await new Promise(r => setTimeout(r, 30)); await _cho();
      return {co_L, L, ke: ke.ma_lenh, mo: F01G.ST.mo,
              cands: document.querySelector('.cands').textContent,
              bat: _BAT_TU_CHOI, thu_lai: _nut(document, 'Thử lại').length};
    """)
    assert r.get("co_L") and r.get("L") == ca["lenh"], r
    assert r["mo"] == r["ke"], ("⛔ không đo được: phím j ⛔ đổi lệnh", r)
    # ⭐ mong
    assert r["bat"] == [], f"⛔ lỗi chưa bắt: {r['bat']}"
    assert "⛔ Cửa lỗi: Máy gặp lỗi bên trong." in r["cands"], r["cands"][-300:]


def test_AC11_bam_CHUOT_lai_CUNG_lenh_cua_LOI__man_noi__0_Uncaught(ca_tra):
    """Mở `L`; bấm **lại** hàng `L` *(chuột — `mo_lenh` cùng lệnh, danh sách
    cũ **giữ** khi lượt bay)*; `itl-candidates` lỗi.

    Mong: lỗi lượt mới nhất **hiện** *(`⛔ Cửa lỗi:` + `Thử lại`)* — ⛔ để danh
    sách cũ đứng im như thể lượt đã thành; **0** lỗi chưa bắt. ⛔ Chiều ĐỎ
    *(mã khi nhận)*: `Uncaught`, màn ⛔ chữ *(danh sách cũ còn)*."""
    ca, D, TRA, LOI = ca_tra
    r = _js(TRA, _mo(ca) + f"""
      const truoc = F01G.ST.ung_vien.length;
      _GIU.push('/itl-candidates');
      /* view ② — rail `.rrow` *(view ① là `.mrow`)* */
      const hang = [...document.querySelectorAll('#ghep-goc .rrow')]
        .filter(r => r.textContent.indexOf({ca['lenh']!r}) >= 0);
      if (hang.length !== 1) return {{loi: 'hàng rail L: ' + hang.length}};
      _bam(hang[0]); await _cho();
      await _no('/itl-candidates', new FLS.LoiCua('FLS-MAT-KET-NOI', 0, 'wo023'));
      await new Promise(r => setTimeout(r, 30)); await _cho();
      return {{truoc, cands: document.querySelector('.cands').textContent,
               bat: _BAT_TU_CHOI, thu_lai: _nut(document, 'Thử lại').length,
               gan_khoa: !!nut_gan().disabled}};
    """)
    assert r["truoc"] > 0, ("⛔ không đo được: danh sách đầu rỗng", r)
    assert r["bat"] == [], f"⛔ lỗi chưa bắt: {r['bat']}"
    assert "⛔ Cửa lỗi: Không nối được tới máy chủ FLS." in r["cands"], r["cands"][-300:]
    assert r["thu_lai"] == 1, r
    assert r["gan_khoa"] is True, "⛔ danh sách đã thôi hiện mà Gán còn bấm được"


# ══ ⓒ nút `Thử lại` ════════════════════════════════════════════════════════

def test_AC12_THU_LAI_o_tim_RONG__mot_luot_itl_candidates__danh_sach_ve(ca_tra):
    """Đổi chip rồi mở `L` *(lệnh **khác** ⇒ danh sách xoá)*; `itl-candidates`
    lỗi `FLS-INTERNAL` ⇒ **một** nút `Thử lại` lớp `b tiny` ngay dưới câu lỗi;
    bấm ⇒ **một** lượt `itl-candidates`; về ⇒ danh sách = thân cửa, ⛔ còn câu
    lỗi. ⛔ Chiều ĐỎ *(mã khi nhận)*: ⛔ nút."""
    ca, D, TRA, LOI = ca_tra
    r = _js(TRA, f"""
      await F01G.mo_man(); await _cho();
      _GIU.push('/itl-candidates');
      const p = F01G.mo_lenh({ca['lenh']!r}).catch(e => 'ném'); await _cho();
      await _no('/itl-candidates', new FLS.LoiCua('FLS-INTERNAL', 500, 'wo023'));
      await p;
      const nut = _nut(document, 'Thử lại');
      const lop = nut.length ? nut[0].className : null;
      /* DOM giả ⛔ có `previousSibling` — đọc anh em qua `parentNode.children` */
      const anh = nut.length ? nut[0].parentNode.children : [];
      const k_nut = anh.indexOf(nut[0]);
      const sau_cau = k_nut > 0 ? anh[k_nut - 1].textContent : null;
      const goi0 = _doc('/itl-candidates').length;
      _GIU.length = 0;
      if (nut.length) _bam(nut[0]);
      await new Promise(r => setTimeout(r, 30)); await _cho();
      return {{n: nut.length, lop, sau_cau, goi: _doc('/itl-candidates').length - goi0,
               uv: F01G.ST.ung_vien.map(u => u.itl_id), loi: F01G.ST.loi_uv,
               cands: document.querySelector('.cands').textContent,
               bat: _BAT_TU_CHOI}};
    """)
    want = [u["itl_id"] for u in TRA[D["uv"]]["data"]["ung_vien"]]
    assert r["n"] == 1, ("⛔ ⛔ có nút Thử lại dưới câu lỗi", r)
    assert r["lop"] == "b tiny", r
    assert r["sau_cau"] and "⛔ Cửa lỗi:" in r["sau_cau"], r
    assert r["goi"] == 1, r
    assert r["uv"] == want and r["loi"] is None, r
    assert "Cửa lỗi" not in r["cands"], r["cands"][-200:]
    assert r["bat"] == [], r["bat"]


def test_AC12_THU_LAI_o_tim_CO_CHU__mot_luot_so_q_chu_giu(ca_tra):
    """Mở `L`; gõ `doc(M2)`; `/so` lỗi ⇒ câu lỗi + `Thử lại`; bấm ⇒ **một**
    lượt `/so?q=<doc M2>` *(⛔ `itl-candidates`)*, chữ **giữ**; về ⇒ `[M2]`.
    ⛔ Chiều ĐỎ: nút gọi `mo_lenh` khi ô tìm có chữ ⇒ ca này ĐỎ."""
    ca, D, TRA, LOI = ca_tra
    q = ca["doc"]["M2"]
    r = _js(TRA, _mo(ca) + f"""
      _GIU.push('/so?');
      await go({q!r});
      await _no('/so?', new FLS.LoiCua('FLS-INTERNAL', 500, 'wo023'));
      await new Promise(r => setTimeout(r, 30)); await _cho();
      const cands_loi = document.querySelector('.cands').textContent;
      const nut = _nut(document, 'Thử lại');
      const so0 = _doc('/so?').length, uv0 = _doc('/itl-candidates').length;
      _GIU.length = 0;
      if (nut.length) _bam(nut[0]);
      await new Promise(r => setTimeout(r, 30)); await _cho();
      return {{n: nut.length, cands_loi, so: _doc('/so?').slice(so0),
               uv: _doc('/itl-candidates').length - uv0, tim: F01G.ST.tim,
               ds: F01G.ST.ung_vien.map(u => u.itl_id), bat: _BAT_TU_CHOI}};
    """)
    assert "⛔ Cửa lỗi: Máy gặp lỗi bên trong." in r["cands_loi"], r
    assert r["n"] == 1, r
    assert r["so"] == [D["so_M2"]] and r["uv"] == 0, r
    assert r["tim"] == q and r["ds"] == [ca["i"]["M2"]], r
    assert r["bat"] == [], r["bat"]


# ══ ⓔ `KQ-050 F-2` — khung chờ ⛔ treo khi lượt ô tìm lỗi ══════════════════

def test_AC14_tim_LOI_khi_lenh_moi_dang_tai__khung_ha__cau_loi__thu_lai(ca_tra):
    """Đổi chip *(ST.mo = null)* rồi `mo_lenh(L)` với `itl-candidates` **giữ**
    ⇒ khung `Đang hỏi sổ…`; gõ `doc(M2)` ⇒ lượt chữ là lượt mới nhất; `/so`
    lỗi; thả lượt lệnh *(đã bị thay)*.

    Mong: `ST.dang_tai_uv` `false`, `⛔ Cửa lỗi:` + `Thử lại` *(bấm ⇒ **một**
    `/so?q=<chữ>`)*, **0** lỗi chưa bắt. ⛔ Chiều ĐỎ *(mã khi nhận)*: khung
    treo, `_BAT_TU_CHOI` ⛔ rỗng."""
    ca, D, TRA, LOI = ca_tra
    q = ca["doc"]["M2"]
    r = _js(TRA, f"""
      await F01G.mo_man(); await _cho();
      _GIU.push('/itl-candidates'); _GIU.push('/so?');
      const p = F01G.mo_lenh({ca['lenh']!r}).catch(e => 'ném: ' + e.message); await _cho();
      const khung = document.querySelector('.cands').textContent;
      await go({q!r});
      await _no('/so?', new FLS.LoiCua('FLS-INTERNAL', 500, 'wo023'));
      await _tha('/itl-candidates');
      await new Promise(r => setTimeout(r, 30)); await _cho();
      const sau = {{dang: F01G.ST.dang_tai_uv,
                    cands: document.querySelector('.cands').textContent}};
      const nut = _nut(document, 'Thử lại');
      const so0 = _doc('/so?').length;
      _GIU.length = 0;
      if (nut.length) _bam(nut[0]);
      await new Promise(r => setTimeout(r, 30)); await _cho();
      return {{khung, sau, n: nut.length, so: _doc('/so?').slice(so0),
               ra: await p, bat: _BAT_TU_CHOI}};
    """)
    assert "Đang hỏi sổ…" in r["khung"], ("⛔ không đo được: khung tải ⛔ bật", r)
    # ⭐ mong
    assert r["bat"] == [], f"⛔ lỗi chưa bắt: {r['bat']}"
    assert r["sau"]["dang"] is False, r["sau"]
    assert "Đang hỏi sổ…" not in r["sau"]["cands"], r["sau"]
    assert "⛔ Cửa lỗi: Máy gặp lỗi bên trong." in r["sau"]["cands"], r["sau"]
    assert r["n"] == 1 and r["so"] == [D["so_M2"]], r
