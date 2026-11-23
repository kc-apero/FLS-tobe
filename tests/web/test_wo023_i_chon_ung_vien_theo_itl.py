# -*- coding: utf-8 -*-
"""`WO-023` `(i)` · `BA-06` **v4.22** `§4.5 ⓦ` ⑥ — lựa chọn ứng viên `F01G`
gắn theo **`itl_id`**, ⛔ theo chỉ số mảng *(`KQ-050 F-3`, PO nâng **`NANG`**)*.

⛔⛔ Lỗi gốc *(mã khi nhận `7e67a09`)*: `ST.ung_vien_chon` là **chỉ số** vào
`ST.ung_vien`. Lựa chọn chỉ bị xoá ở **đầu** một lượt *(`mo_lenh` · hẹn giờ ô
tìm)*, ⛔ ở **cuối** — khi danh sách mới **thay** `ST.ung_vien`. Trong khoảng
ấy danh sách cũ **vẫn trên màn**, bấm được; người bấm hàng `k` của danh sách
**cũ**, lượt mới về, chỉ số `k` trỏ một dòng tiền **khác** ⇒ màn tô sẵn dòng
ấy và `Gán` / `Enter` gửi `/queue/<itl người ⛔ chọn>/match`. `KQ-050` ① đo cửa
ghi **nhận** cặp trong dung sai ⇒ dòng người ⛔ chọn vào sổ **chỉ-thêm**.

⭐ Bốn ca của `AC-13` *(ⓐ…ⓓ)*, mỗi ca một bài, mỗi bài ghi **chiều ĐỎ** đã chạy
trên mã khi nhận *(`git stash` mã `fls/web/tep/man_f01_ghep.js` — `BG` dán)*:

  ⓐ ô tìm — `itl_id` đã chọn **⛔** có trong danh sách mới ⇒ **0** hàng tô,
     `Gán` khoá, `Enter` **0** `POST`        *(đỏ cũ: `Enter` gửi `M2`)*
  ⓑ ô tìm — `itl_id` đã chọn **có**, ở vị trí khác ⇒ tô đúng hàng, `Enter` /
     `Gán` đúng **một** `POST` itl ấy     *(đỏ cũ: chỉ số ra ngoài ⇒ 0 `POST`)*
  ⓒ ca lệch — đã bấm `Gán` một lần *(`xac_nhan`)* rồi danh sách bị thay ⇒ nhãn
     về `Gán`, **một** cú bấm ⇒ **0** `POST`  *(đỏ cũ: một cú là ghi)*
  ⓓ `mo_lenh` mở lại **cùng** lệnh *(xoá ô tìm)* — như ⓐ
                                            *(đỏ cũ: `Gán` gửi `M1`)*

⭐ Luật của tệp *(như `test_wo045_luot_moi_nhat_cua_that.py`)*: thân cửa lấy từ
**cửa HTTP thật** kho TEST *(`ca_wo023.py`)*, nguyên văn vào `_TRA`; độ trễ **có
kiểm soát** *(`khung_giu.py` — bài quyết thứ tự về)*; bấm đi đúng đường người
bấm *(`_bam` — nút `disabled` ⛔ nhận)*, phím đi qua trình nghe `document` thật.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.ca_wo023 import dung_ca_wo023
from tests.web.ca_wo032 import goi_ok
from tests.web.khung_giu import CUA_GIU, nap
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = [pytest.mark.pg, can_node]

#: ⭐ Vỏ `F01` + `#man-ghep.on` — trình nghe phím của `F01G` tự chặn khi màn
#: ghép ⛔ bật *(`_noi_ban_phim`)*; ⛔ có thẻ này thì `Enter` qua `document` là
#: một phím **⛔ ai nghe** và ca `Enter` xanh **giả**.
VO = VO_F01 + """
{ const g = d.document.createElement('section'); g.id = 'man-ghep';
  g.className = 'screen on'; d.body.appendChild(g); }
"""


@pytest.fixture(scope="module")
def ca_tra():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_wo023(c)
    L, doc = ca["lenh"], ca["doc"]
    D = {
        "g_nguoi": "/queue/lenh-cho?ro=nguoi&limit=500",
        "g_may": "/queue/lenh-cho?ro=may&tu_chung=0&limit=500",
        "uv": f"/queue/lenh/{L}/itl-candidates",
        "so_h": f"/queue/lenh/{L}/so?q={ca['h']}",
    }
    for k in doc:
        D["so_" + k] = f"/queue/lenh/{L}/so?q={doc[k]}"
    with _may() as m:
        TRA = {d: goi_ok(m, d) for d in D.values()}
    return ca, D, TRA


def _ids(env: dict) -> list:
    return [u["itl_id"] for u in (env["data"] or {}).get("ung_vien") or []]


def _js(tra: dict, kich_ban: str) -> dict:
    return _chay(CUA_GIU + nap(tra) + _GO + kich_ban, tep=TEP_F01, vo=VO)


_GO = """
  const go = async (q) => {
    _ban('input', {target: {id: 'ghep-tim', value: q}});
    await new Promise(r => setTimeout(r, F01G.TRE_TIM + 80)); await _cho();
  };
  const enter = async () => {
    _ban('keydown', {key: 'Enter', preventDefault() {}}); await _cho();
  };
  const nhin = () => {
    const hang = document.querySelectorAll('.cands .cand');
    const g = document.querySelectorAll('.act button')[0];
    return {uv: F01G.ST.ung_vien.map(u => u.itl_id),
            chon: F01G.ST.ung_vien_chon,
            to: hang.map((h, i) => h.className.indexOf('chon') >= 0 ? i : -1)
                    .filter(i => i >= 0),
            gan_khoa: !!(g && g.disabled), gan_chu: g ? g.textContent : null,
            xac_nhan: F01G.ST.xac_nhan, mo: F01G.ST.mo};
  };
"""

_MO = """
  await F01G.mo_man(); await _cho();
  const co_L = F01G.ST.dong.some(d => d.ma_lenh === %(L)r);
  await F01G.mo_lenh(%(L)r); await _cho();
"""


def _mo(ca: dict) -> str:
    return _MO % {"L": ca["lenh"]}


def _tu_chung_ca(ca, D, TRA):
    """⭐ Tự chứng ca *(`Đ3`)* — mỗi số chứng từ tìm ra **đúng** dòng của nó;
    `M4` ⛔ nằm trong `itl-candidates`; `M1` là hàng đầu *(bậc `ma`)*."""
    i = ca["i"]
    for k in i:
        assert _ids(TRA[D["so_" + k]]) == [i[k]], ("⛔ không đo được: /so?q="
                                                    + k, _ids(TRA[D["so_" + k]]))
    uv = _ids(TRA[D["uv"]])
    assert uv and uv[0] == i["M1"], ("⛔ không đo được: hàng đầu ⛔ phải M1", uv[:4])
    assert i["M4"] not in uv, "⛔ không đo được: M4 lọt vào itl-candidates"
    assert {i["M2"], i["M3"]} <= set(uv), ("⛔ không đo được: M2/M3 ⛔ là ứng "
                                           "viên", uv[:6])
    return uv


def test_AC13a_o_tim_itl_da_chon_KHONG_con__bo_chon__ENTER_va_GAN_khong_POST(ca_tra):
    """Mở `L`; gõ `doc(M3)` ⇒ `[M3]`; gõ `doc(M2)` — lượt **giữ**; trong lúc
    chờ bấm hàng **đầu** *(`M3`)*; thả ⇒ `[M2]`. Rồi `Enter` + bấm `Gán` hai
    lần.

    Mong *(`ⓦ` ⑥ hàng "⛔ có")*: **0** hàng tô, `ung_vien_chon` `null`, `Gán`
    khoá, **0** `POST`. ⛔ Chiều ĐỎ *(mã khi nhận)*: chỉ số `0` giữ ⇒ `M2`
    *(khớp **đúng** tiền)* được tô, `Enter` gửi `/queue/<M2>/match` — một phím
    là ghi dòng người ⛔ chọn."""
    ca, D, TRA = ca_tra
    _tu_chung_ca(ca, D, TRA)
    i, doc = ca["i"], ca["doc"]
    r = _js(TRA, _mo(ca) + f"""
      await go({doc['M3']!r});
      const q1 = nhin();
      _GIU.push('/so?');
      await go({doc['M2']!r});
      _bam(document.querySelectorAll('.cands .cand')[0]); await _cho();
      const da_chon = nhin();
      await _tha('q={doc['M2']}');
      const sau = nhin();
      await enter();
      const sau_enter = _ghi().length;
      for (let k = 0; k < 2; k++) {{
        _bam(document.querySelectorAll('.act button')[0]); await _cho();
      }}
      return {{co_L, q1, da_chon, sau, sau_enter, ghi: _ghi()}};
    """)
    assert r["co_L"], ("⛔ không đo được: lệnh L ⛔ ở chip Chưa gán", r)
    assert r["q1"]["uv"] == [i["M3"]], ("⛔ không đo được: q1 ⛔ lên màn", r["q1"])
    assert r["da_chon"]["to"] == [0] and r["da_chon"]["chon"] == 0, (
        "⛔ không đo được: cú bấm hàng ⛔ chọn", r["da_chon"])
    assert r["sau"]["uv"] == [i["M2"]], r["sau"]
    # ⭐ mong
    assert r["sau_enter"] == 0, (f"⛔ MỘT phím Enter đã GHI dòng người ⛔ chọn: "
                                 f"{r['ghi']} (đã bấm M3={i['M3']}, M2={i['M2']})")
    assert r["ghi"] == [], f"⛔ GHI dòng người ⛔ chọn: {r['ghi']} (đã bấm M3={i['M3']})"
    assert r["sau"]["to"] == [], ("⛔ màn tô sẵn dòng người ⛔ chọn", r["sau"])
    assert r["sau"]["chon"] is None, r["sau"]
    assert r["sau"]["gan_khoa"], ("⛔ nút Gán ⛔ khoá khi ⛔ chọn gì", r["sau"])


def test_AC13b_o_tim_itl_da_chon_CON__giu_dung_hang_moi__ENTER_mot_POST_dung_itl(ca_tra):
    """Mở `L`; gõ `h` ⇒ cả bốn dòng; bấm hàng mang `M2` *(vị trí `k ≠ 0`)*;
    gõ `doc(M2)` — **giữ**; thả ⇒ `[M2]` *(vị trí `0`)*. `Enter`.

    Mong *(`ⓦ` ⑥ hàng "có")*: tô hàng `0` *(mang `M2`)*, `Enter` ⇒ đúng **một**
    `POST /queue/<M2>/match {pm_line_ids:[L]}`. ⭐ Mẫu số của ca ⓐ: `Enter` qua
    trình nghe **thật** ghi được *(⛔ có ca này thì "0 `POST`" của ⓐ có thể chỉ
    là phím ⛔ ai nghe)*. ⛔ Chiều ĐỎ *(mã khi nhận)*: chỉ số `k` ra ngoài
    danh sách một hàng ⇒ ⛔ hàng tô, **0** `POST`. Và *"luôn bỏ chọn"* cũng ĐỎ
    ở đây."""
    ca, D, TRA = ca_tra
    _tu_chung_ca(ca, D, TRA)
    i, doc, L = ca["i"], ca["doc"], ca["lenh"]
    q_h = _ids(TRA[D["so_h"]])
    k = q_h.index(i["M2"]) if i["M2"] in q_h else -1
    assert k > 0, ("⛔ không đo được: M2 phải ở vị trí ≠ 0 của /so?q=h", q_h)
    r = _js(TRA, _mo(ca) + f"""
      await go({ca['h']!r});
      const q1 = nhin();
      _GIU.push('/so?');
      await go({doc['M2']!r});
      _bam(document.querySelectorAll('.cands .cand')[{k}]); await _cho();
      const da_chon = nhin();
      await _tha('q={doc['M2']}');
      const sau = nhin();
      await enter();
      return {{co_L, q1, da_chon, sau, ghi: _ghi()}};
    """)
    assert r["co_L"], r
    assert r["q1"]["uv"] == q_h, ("⛔ không đo được: q1 ⛔ lên màn", r["q1"])
    assert r["da_chon"]["to"] == [k], ("⛔ không đo được: cú bấm ⛔ chọn", r["da_chon"])
    assert r["sau"]["uv"] == [i["M2"]], r["sau"]
    # ⭐ mong
    assert r["sau"]["to"] == [0], ("⛔ ⛔ tô hàng mang itl đã chọn", r["sau"])
    assert r["sau"]["chon"] == 0 and not r["sau"]["gan_khoa"], r["sau"]
    assert r["ghi"] == [[f"/queue/{i['M2']}/match", {"pm_line_ids": [L]}]], r["ghi"]


def test_AC13c_ca_lech_da_bam_GAN_mot_lan_roi_danh_sach_thay__xac_nhan_ve_false(ca_tra):
    """Mở `L`; gõ `doc(M3)` ⇒ `[M3]` *(lệch +500)*; gõ `h` — **giữ**; trong lúc
    chờ bấm hàng `M3` rồi `Gán` **một** lần *(bước một của ca lệch —
    `xac_nhan`)*; thả ⇒ bốn dòng, `M3` ở vị trí khác. Bấm `Gán` **một** lần.

    Mong *(`ⓦ` ⑥ hàng `xac_nhan`)*: lựa chọn **giữ** trên hàng mang `M3`,
    `xac_nhan` `false`, nhãn nút ⛔ còn *"Xác nhận…"*; **một** cú bấm ⇒ **0**
    `POST` *(bước một lần nữa)*. ⛔ Chiều ĐỎ *(mã khi nhận)*: `xac_nhan` sống qua
    lượt + chỉ số `0` ⇒ nhãn *"Xác nhận gán <M1>…"*, một cú là ghi."""
    ca, D, TRA = ca_tra
    _tu_chung_ca(ca, D, TRA)
    i, doc = ca["i"], ca["doc"]
    q_h = _ids(TRA[D["so_h"]])
    j = q_h.index(i["M3"]) if i["M3"] in q_h else -1
    assert j > 0, ("⛔ không đo được: M3 phải ở vị trí ≠ 0 của /so?q=h", q_h)
    r = _js(TRA, _mo(ca) + f"""
      await go({doc['M3']!r});
      _GIU.push('/so?');
      await go({ca['h']!r});
      _bam(document.querySelectorAll('.cands .cand')[0]); await _cho();
      _bam(document.querySelectorAll('.act button')[0]); await _cho();
      const buoc1 = nhin();
      await _tha('q={ca['h']}');
      const sau = nhin();
      _bam(document.querySelectorAll('.act button')[0]); await _cho();
      return {{co_L, buoc1, sau, ghi: _ghi(), sau_bam: nhin()}};
    """)
    assert r["co_L"], r
    assert r["buoc1"]["xac_nhan"] is True, (
        "⛔ không đo được: bước một ca lệch ⛔ bật", r["buoc1"])
    assert "Xác nhận" in (r["buoc1"]["gan_chu"] or ""), r["buoc1"]
    assert r["sau"]["uv"] == q_h, r["sau"]
    # ⭐ mong
    assert r["ghi"] == [], f"⛔ một cú bấm sau khi danh sách đổi đã GHI: {r['ghi']}"
    assert r["sau"]["xac_nhan"] is False, r["sau"]
    assert "Xác nhận" not in (r["sau"]["gan_chu"] or ""), r["sau"]
    assert r["sau"]["to"] == [j], ("⛔ lựa chọn ⛔ giữ trên hàng mang M3", r["sau"])


def test_AC13d_mo_lenh_mo_lai_CUNG_lenh_itl_da_chon_KHONG_con__0_POST(ca_tra):
    """Mở `L`; gõ `doc(M4)` ⇒ `[M4]` *(USD — ⛔ ứng viên)*; xoá ô tìm ⇒
    `mo_lenh(L)` **cùng** lệnh — `itl-candidates` **giữ** *(danh sách `[M4]`
    còn trên màn — mở lại cùng lệnh ⛔ xoá)*; bấm hàng `M4`; thả. `Enter` +
    `Gán` hai lần.

    Mong: **0** hàng tô, `Gán` khoá, **0** `POST`. ⛔ Chiều ĐỎ *(mã khi nhận)*:
    chỉ số `0` ⇒ `M1` *(hàng đầu `itl-candidates`)* tô sẵn, hai cú `Gán` gửi
    `/queue/<M1>/match`."""
    ca, D, TRA = ca_tra
    uv = _tu_chung_ca(ca, D, TRA)
    i, doc = ca["i"], ca["doc"]
    r = _js(TRA, _mo(ca) + f"""
      await go({doc['M4']!r});
      const q1 = nhin();
      _GIU.push('/itl-candidates');
      await go('');
      const dang = nhin();
      _bam(document.querySelectorAll('.cands .cand')[0]); await _cho();
      const da_chon = nhin();
      await _tha('/itl-candidates');
      const sau = nhin();
      await enter();
      for (let k = 0; k < 2; k++) {{
        _bam(document.querySelectorAll('.act button')[0]); await _cho();
      }}
      return {{co_L, q1, dang, da_chon, sau, ghi: _ghi(),
               goi: _doc('/itl-candidates').length}};
    """)
    assert r["co_L"], r
    assert r["q1"]["uv"] == [i["M4"]], ("⛔ không đo được: q1", r["q1"])
    assert r["dang"]["uv"] == [i["M4"]], ("⛔ không đo được: danh sách cũ "
                                          "⛔ còn trên màn khi lượt bay", r["dang"])
    assert r["goi"] == 2, ("⛔ không đo được: xoá ô tìm ⛔ mở lại lệnh", r["goi"])
    assert r["da_chon"]["to"] == [0], r["da_chon"]
    assert r["sau"]["uv"] == uv, r["sau"]
    # ⭐ mong
    assert r["ghi"] == [], f"⛔ GHI dòng người ⛔ chọn: {r['ghi']} (đã bấm M4)"
    assert r["sau"]["to"] == [] and r["sau"]["chon"] is None, r["sau"]
    assert r["sau"]["gan_khoa"], r["sau"]


def test_AC13_doi_sang_lenh_KHAC_van_bo_chon(ca_tra):
    """⭐ Mẫu số dòng cuối bảng `ⓦ` ⑥ *("đổi sang lệnh khác · đổi chip ⇒ `null`
    như nay")*: chọn `M1` dưới `L`, đổi chip rồi quay lại ⇒ ⛔ còn chọn — kể cả
    khi `itl_id` ấy lại có trong danh sách mới *(cùng `itl-candidates`)*.
    ⛔ Chiều ĐỎ: một bản *"giữ itl_id qua mọi lượt"* ngây thơ giữ cả khi đổi
    lệnh."""
    ca, D, TRA = ca_tra
    _tu_chung_ca(ca, D, TRA)
    r = _js(TRA, _mo(ca) + f"""
      _bam(document.querySelectorAll('.cands .cand')[0]); await _cho();
      const da_chon = nhin();
      F01G.ST.mo = null;
      await F01G.mo_lenh({ca['lenh']!r}); await _cho();
      return {{co_L, da_chon, sau: nhin()}};
    """)
    assert r["da_chon"]["to"] == [0], r
    assert r["sau"]["to"] == [] and r["sau"]["chon"] is None, r["sau"]
